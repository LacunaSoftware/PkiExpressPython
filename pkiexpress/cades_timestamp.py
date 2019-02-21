from .cades_signature import CadesSignature


class CadesTimestamp(CadesSignature):

    def __init__(self, model):
        super(CadesTimestamp, self).__init__(model)
        self.__gen_time = model.get('genTime', None)
        self.__serial_number = model.get('serialNumber', None)
        self.__message_imprint = model.get('messageImprint', None)

    @property
    def gen_time(self):
        return self.__gen_time

    @gen_time.setter
    def gen_time(self, value):
        self.__gen_time = value

    @property
    def serial_number(self):
        return self.__serial_number

    @serial_number.setter
    def serial_number(self, value):
        self.__serial_number = value

    @property
    def message_imprint(self):
        return self.__message_imprint

    @message_imprint.setter
    def message_imprint(self, value):
        self.__message_imprint = value


__all__ = ['CadesTimestamp']
