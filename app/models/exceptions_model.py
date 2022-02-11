class InvalidEmail(Exception):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.code = 422

    @staticmethod
    def email_err_description(email):
        return {'error': f'{email} is not a valid email'}

class InvalidPhone(Exception):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.description = {'error': 'Phone in an invalid format. Must be in (xx)xxxxx-xxxx'}
        self.code = 400