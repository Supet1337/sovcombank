

class SessionsContainer:
    def __init__(self):
        self.__sessions: dict[str, dict] = {}

    def check_session(self, token: str) -> str | None:
        """
        Checking if session's token valid and if yes return email that is linked to session
        :param token: session's hashed token
        :return: email if there's session or none if there's no session
        """
        session = self.__sessions.get(token)
        if session is None:
            return None  # Если сессии нет возвращаем ничего
        else:
            return self.__sessions.get("email")

    def add_session(self, token: str, email: str, client_ip: str, is_admin: bool = False) -> None:
        self.__sessions[token] = {"email": email, "client_ip": client_ip, "is_admin": is_admin}
