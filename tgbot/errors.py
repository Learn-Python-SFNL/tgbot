class AppError(Exception):
    def __init__(self, reason: str, message: str) -> None:
        super().__init__(f' {reason}')
        self.reason = reason
        self.message = message


class IncorrectCmdError(AppError):
    def __init__(self, cmd: str, text: str, message: str) -> None:
        super().__init__(f'Incorrect command: [{cmd}] {text}', message)
        self.cmd = cmd
        self.text = text


class IncorrectAddCmdError(IncorrectCmdError):
    def __init__(self, text: str) -> None:
        super().__init__('/add', text, 'Неправильная команда, пример `/add Цветок - Фикус`')
