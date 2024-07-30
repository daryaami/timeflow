class TokenRefreshError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(f"TokenRefreshError {status_code}: {message}")

class CredentialsNotFoundError(Exception):
    pass

class RefreshTokenMissing(Exception):
    pass

class InvalidGrantError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(f"InvalidGrantError: {message}")

class RequestError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(f"RequestError: {message}")