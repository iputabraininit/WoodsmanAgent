class CommandPayload:
    def __init__(self, command:str, arguments=[]):
        self._command = command
        self._arguments = arguments

    def get_command(self):
        return self._command

    def get_arguments(self):
        return self._arguments