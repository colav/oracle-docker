class CommandExecutor:
    def __init__(self):
        self.commands = []

    def add(self, command):
        self.commands.append(command)

    def run(self):
        for command in self.commands:
            command.execute()
