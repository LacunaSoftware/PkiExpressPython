import base64
import binascii

from pkiexpress.digest_algorithm import DigestAlgorithm


class DigestAlgorithmAndValue(object):

    def __init__(self, model):

        algorithm = model.get('algorithm', None)
        if algorithm is None:
            raise Exception('The algorithm was not set')

        value = model.get('value', None)
        if value is None:
            raise Exception('The value was not set')

        self.__algorithm = DigestAlgorithm.get_instance_by_api_model(algorithm)
        try:
            raw = base64.standard_b64decode(str(value))
        except (TypeError, binascii.Error):
            raise Exception('The provided certificate is not Base64-encoded')
        self.__value = raw

    @property
    def algorithm(self):
        return self.__algorithm

    @algorithm.setter
    def algorithm(self, value):
        self.__algorithm = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, v):
        self.__value = v

    @property
    def hex_value(self):
        return binascii.hexlify(self.__value)

    @hex_value.setter
    def hex_value(self, value):
        self.__value = binascii.unhexlify(value)

    def to_model(self):
        return {
            'algorithm': self.__algorithm.api_model,
            'value': self.__value
        }


__all__ = ['DigestAlgorithmAndValue']
