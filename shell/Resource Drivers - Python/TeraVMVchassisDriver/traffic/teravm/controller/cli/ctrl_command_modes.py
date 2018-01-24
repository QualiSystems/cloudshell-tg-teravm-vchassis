from collections import OrderedDict

from cloudshell.cli.command_mode import CommandMode


class DefaultCommandMode(CommandMode):
    PROMPT = r':~\$'
    ENTER_COMMAND = ''
    EXIT_COMMAND = ''

    def __init__(self):
        super(DefaultCommandMode, self).__init__(DefaultCommandMode.PROMPT,
                                                 DefaultCommandMode.ENTER_COMMAND,
                                                 DefaultCommandMode.EXIT_COMMAND)


class CliCommandMode(CommandMode):
    PROMPT = r'cli>'
    ENTER_COMMAND = 'cli'
    EXIT_COMMAND = '\x03'  # Ctrl-C code

    def __init__(self):
        super(CliCommandMode, self).__init__(
            CliCommandMode.PROMPT,
            CliCommandMode.ENTER_COMMAND,
            CliCommandMode.EXIT_COMMAND,
            enter_error_map=self.enter_error_map())

    def enter_error_map(self):
        return OrderedDict((('command not found', 'TeraVM CLI is not installed'),))


CommandMode.RELATIONS_DICT = {
    DefaultCommandMode: {
        CliCommandMode: {}
    }
}