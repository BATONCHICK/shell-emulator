import argparse
import os
from datetime import datetime

from vfs import VirtualFileSystem


def parse_arguments():
    """Разбирает аргументы командной строки эмулятора."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--vfs")
    parser.add_argument("--script")
    return parser.parse_args()


def get_prompt(vfs):
    """Формирует приглашение командной строки."""
    path = vfs.current_path() if vfs else "/"
    return f"VFS:{path}$ "


def require_vfs(vfs):
    """Проверяет, что виртуальная файловая система загружена."""
    if vfs is not None:
        return True

    print("Ошибка: VFS не загружена")
    return False


def command_ls(arguments, vfs):
    """Выполняет команду ls."""
    if not require_vfs(vfs):
        return "error"

    if len(arguments) > 1:
        print("Ошибка: ls принимает не более одного пути")
        return "error"

    path = arguments[0] if arguments else "."

    try:
        print("  ".join(vfs.list_path(path)))
    except ValueError as error:
        print("Ошибка ls:", error)
        return "error"

    return "ok"


def command_cd(arguments, vfs):
    """Выполняет команду cd."""
    if not require_vfs(vfs):
        return "error"

    if len(arguments) > 1:
        print("Ошибка: cd принимает не более одного пути")
        return "error"

    path = arguments[0] if arguments else "/"

    try:
        vfs.change_directory(path)
    except ValueError as error:
        print("Ошибка cd:", error)
        return "error"

    return "ok"


def parse_find_arguments(arguments):
    """Разбирает аргументы команды find."""
    if len(arguments) == 1:
        return ".", arguments[0]

    if len(arguments) == 2:
        return arguments[0], arguments[1]

    if (
        len(arguments) == 3
        and arguments[1] == "-name"
    ):
        return arguments[0], arguments[2]

    raise ValueError(
        "использование: find NAME или "
        "find PATH [-name] NAME"
    )


def command_find(arguments, vfs):
    """Выполняет команду find."""
    if not require_vfs(vfs):
        return "error"

    try:
        path, name = parse_find_arguments(arguments)
        results = vfs.find(name, path)
    except ValueError as error:
        print("Ошибка find:", error)
        return "error"

    for result in results:
        print(result)

    return "ok"


def command_date(arguments):
    """Выполняет команду date."""
    if arguments:
        print("Ошибка: date не принимает аргументы")
        return "error"

    print(
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )
    return "ok"


def execute_command(command, vfs):
    """Выполняет одну команду эмулятора."""
    command = os.path.expandvars(command)
    parts = command.split()

    if not parts:
        return "ok"

    command_name = parts[0]
    arguments = parts[1:]

    if command_name == "exit":
        return "exit"

    if command_name == "ls":
        return command_ls(arguments, vfs)

    if command_name == "cd":
        return command_cd(arguments, vfs)

    if command_name == "find":
        return command_find(arguments, vfs)

    if command_name == "date":
        return command_date(arguments)

    print("Неизвестная команда", command_name)
    return "error"


def run_script(path, vfs):
    """Выполняет команды из стартового скрипта."""
    try:
        with open(
            path,
            "r",
            encoding="utf-8",
        ) as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                print(
                    f"{get_prompt(vfs)}{line}"
                )
                result = execute_command(
                    line,
                    vfs,
                )

                if result != "ok":
                    return result

    except OSError as error:
        print(
            "Ошибка стартового скрипта:",
            error,
        )
        return "error"

    return "ok"


def run_shell(vfs):
    """Запускает эмулятор в интерактивном режиме."""
    while True:
        command = input(
            get_prompt(vfs)
        )
        result = execute_command(
            command,
            vfs,
        )

        if result == "exit":
            break


def load_vfs(path):
    """Загружает VFS и выводит информацию о ней."""
    try:
        vfs = VirtualFileSystem.from_directory(
            path
        )
    except (OSError, ValueError) as error:
        print("Ошибка VFS:", error)
        return None

    directories, files = vfs.stats()

    print(
        f"VFS загружена: каталогов {directories}, "
        f"файлов {files}"
    )

    return vfs


def main():
    """Запускает эмулятор."""
    args = parse_arguments()

    print("VFS:", args.vfs)
    print("Script:", args.script)

    vfs = load_vfs(
        args.vfs
    ) if args.vfs else None

    if args.vfs and vfs is None:
        return 1

    if args.script:
        result = run_script(
            args.script,
            vfs,
        )

        if result == "exit":
            return 0

    run_shell(vfs)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())