

class SessionsContainer:
    def __init__(self):
        self.__sessions: dict[str, dict] = {}

    def check_session(self, token: str) -> dict | None:
        """
        Checking if session's token valid and if yes return email that is linked to session
        :param token: session's hashed token
        :return: email if there's session or none if there's no session
        """
        return self.__sessions.get(token)

    def add_session(self, token: str, email: str, client_ip: str, is_admin: bool = False) -> None:
        self.__sessions[token] = {"email": email, "client_ip": client_ip, "is_admin": is_admin}

    def delete_session(self, token: str | None):
        if token is None: return
        self.__sessions.pop(token, None)
