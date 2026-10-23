from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class VFSNode:
    """Описывает файл или каталог виртуальной файловой системы."""

    name: str
    is_directory: bool
    content: bytes = b""
    children: dict = field(default_factory=dict)


class VirtualFileSystem:
    """Хранит копию файловой системы полностью в памяти."""

    def __init__(self, root):
        self.root = root
        self.cwd = []

    @classmethod
    def from_directory(cls, path):
        """Создаёт VFS из физической директории."""
        source = Path(path)

        if not source.exists():
            raise ValueError(
                f"Путь VFS не существует: {path}"
            )

        if not source.is_dir():
            raise ValueError(
                f"Путь VFS не является директорией: {path}"
            )

        root = cls._load_directory(source, "/")
        return cls(root)

    @classmethod
    def _load_directory(cls, directory, name):
        """Рекурсивно загружает каталог в память."""
        node = VFSNode(
            name=name,
            is_directory=True,
        )

        items = sorted(
            directory.iterdir(),
            key=lambda item: item.name,
        )

        for child in items:
            if child.is_symlink():
                continue

            if child.is_dir():
                node.children[child.name] = cls._load_directory(
                    child,
                    child.name,
                )
            else:
                node.children[child.name] = VFSNode(
                    name=child.name,
                    is_directory=False,
                    content=child.read_bytes(),
                )

        return node

    def stats(self):
        """Возвращает число каталогов и файлов в VFS."""
        directories = 0
        files = 0

        def count(node):
            nonlocal directories, files

            for child in node.children.values():
                if child.is_directory:
                    directories += 1
                    count(child)
                else:
                    files += 1

        count(self.root)
        return directories, files

    def current_path(self):
        """Возвращает текущий путь внутри VFS."""
        if not self.cwd:
            return "/"

        return "/" + "/".join(self.cwd)

    def _normalize_path(self, path):
        """Преобразует путь в список его компонентов."""
        parts = [] if path.startswith("/") else list(self.cwd)

        for part in path.split("/"):
            if not part or part == ".":
                continue

            if part == "..":
                if parts:
                    parts.pop()
                continue

            parts.append(part)

        return parts

    def _get_node(self, parts):
        """Возвращает узел VFS по компонентам пути."""
        node = self.root

        for part in parts:
            if not node.is_directory:
                raise ValueError(
                    "часть пути не является каталогом"
                )

            if part not in node.children:
                raise ValueError("путь не найден")

            node = node.children[part]

        return node

    def resolve(self, path="."):
        """Возвращает узел по абсолютному или относительному пути."""
        parts = self._normalize_path(path)
        return self._get_node(parts)

    def resolve_directory(self, path="."):
        """Возвращает каталог по указанному пути."""
        node = self.resolve(path)

        if not node.is_directory:
            raise ValueError(
                "указанный путь не является каталогом"
            )

        return node

    def change_directory(self, path):
        """Изменяет текущий каталог VFS."""
        self.resolve_directory(path)
        self.cwd = self._normalize_path(path)

    def list_path(self, path="."):
        """Возвращает содержимое каталога или имя файла."""
        node = self.resolve(path)

        if not node.is_directory:
            return [node.name]

        return sorted(node.children)

    def find(self, name, path="."):
        """Ищет объекты по имени внутри VFS."""
        parts = self._normalize_path(path)
        node = self._get_node(parts)
        results = []
        self._find_recursive(
            node,
            parts,
            name,
            results,
        )
        return results

    def _find_recursive(self, node, parts, name, results):
        """Рекурсивно ищет имя в дереве VFS."""
        if node.name == name:
            results.append(
                self._format_path(parts)
            )

        if not node.is_directory:
            return

        for child_name, child in node.children.items():
            self._find_recursive(
                child,
                parts + [child_name],
                name,
                results,
            )

    @staticmethod
    def _format_path(parts):
        """Преобразует компоненты пути в строку."""
        if not parts:
            return "/"

        return "/" + "/".join(parts)