import os

def run_shell():
    while True:
        command = input("VFS:/$ ")
        command = os.path.expandvars(command)
        parts = command.split()

        if not parts:
            continue

        command_name = parts[0]
        arguments = parts[1:]

        if command_name == "exit":
            break
        elif command_name == "cd":
            print(command_name, arguments)
        elif command_name == "ls":
            print(command_name, arguments)
        else:
            print("Неизвестная команда", command_name)


run_shell()