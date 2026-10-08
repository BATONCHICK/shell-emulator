import argparse
import os


def parse_arguments():
    """Разбирает аргументы командной строки эмулятора"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--vfs")
    parser.add_argument("--script")
    return parser.parse_args()


def execute_command(command):
    """Выполняет одну команду эмулятора"""
    command = os.path.expandvars(command)
    parts = command.split()

    if not parts:
        return "ok"

    command_name = parts[0]
    arguments = parts[1:]

    if command_name == "exit":
        return "exit"

    if command_name == "cd":
        print(command_name, arguments)
        return "ok"

    if command_name == "ls":
        print(command_name, arguments)
        return "ok"

    print("Неизвестная команда", command_name)
    return "error"


def run_script(path):
    """Выполняет команды из стартового скрипта"""
    try:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                print(f"VFS:/$ {line}")
                result = execute_command(line)

                if result != "ok":
                    return result

    except OSError as error:
        print("Ошибка стартового скрипта:", error)
        return "error"

    return "ok"


def run_shell():
    """Запускает эмулятор в интерактивном режиме"""
    while True:
        command = input("VFS:/$ ")
        result = execute_command(command)

        if result == "exit":
            break


def main():
    """Запускает эмулятор"""
    args = parse_arguments()

    print("VFS:", args.vfs)
    print("Script:", args.script)

    if args.script:
        result = run_script(args.script)

        if result == "exit":
            return

    run_shell()


if __name__ == "__main__":
    main()