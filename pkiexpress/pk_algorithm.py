from .oids import Oids
from .signature_algorithm import RSASignatureAlgorithm


class PKAlgorithms(object):
    RSA = 'RSA'


class PKAlgorithm(object):
    RSA = None

    def __init__(self, name, oid):
        self.__name = name
        self.__oid = oid

    def __eq__(self, instance):
        if instance is None:
            return False

        if self == instance:
            return True

        return self.__oid == instance.oid

    @staticmethod
    def _algorithms():
        return [PKAlgorithm.RSA]

    @staticmethod
    def get_instance_by_name(name):
        filtered_list = list(filter(lambda p: p.name == name,
                                    PKAlgorithm._algorithms()))
        alg = filtered_list[0] if len(filtered_list) > 0 else None

        if alg is None:
            raise Exception('Unrecognized private key algorithm name: %s' %
                            name)

        return alg

    @staticmethod
    def get_instance_by_oid(oid):
        filtered_list = list(filter(lambda p: p.oid == oid,
                                    PKAlgorithm._algorithms()))
        alg = filtered_list[0] if len(filtered_list) > 0 else None

        if alg is None:
            raise Exception('Unrecognized private key algorithm oid: %s' % oid)

        return alg

    @staticmethod
    def get_instance_api_model(algorithm):
        if algorithm is Algorithms.RSA:
            return PKAlgorithm.RSA
        else:
            raise Exception('Unsupported private key algorithm: %s' % algorithm)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def oid(self):
        return self.__oid

    @oid.setter
    def oid(self, value):
        self.__oid = value


class RSAPKAlgorithm(PKAlgorithm):

    def __init__(self):
        name = Algorithms.RSA
        oid = Oids.RSA
        super(RSAPKAlgorithm, self).__init__(name, oid)

    @staticmethod
    def get_signature_algorithm(digest_algorithm):
        return RSASignatureAlgorithm(digest_algorithm)


PKAlgorithm.RSA = RSAPKAlgorithm()

__all__ = [
    'PKAlgorithms',
    'PKAlgorithm',
    'RSAPKAlgorithm'
]
