class TrustServiceSessionResult():
    def __init__(self, model):
        self.__session = model.get("session", None)
        self.__custom_state = model.get("customState", None)

    def get_session(self):
        return self.__session

    def set_session(self, session):
        self.__session = session

    def get_custom_state(self):
        return self.__custom_state

    def set_custom_state(self, customState):
        self.__custom_state = customState

    session = property(get_session, set_session)
    custom_state = property(get_custom_state, set_custom_state)

__all__ = [
    'TrustServiceSessionResult'
]