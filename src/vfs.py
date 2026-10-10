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