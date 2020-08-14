class TrustServiceSessionResult():
    def __init__(self, model):
        self.__session = model.get("session", None)

    def get_session(self):
        return self.__session

    def set_session(self, session):
        self.__session = session

    session = property(get_session, set_session)


__all__ = [
    'TrustServiceSessionResult'
]