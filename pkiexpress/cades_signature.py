from .cades_signer_info import CadesSignerInfo


class CadesSignature(object):

    def __init__(self, model):
        self.__encapsulated_content_type = \
            model.get('encapsulatedContentType', None)
        self.__has_encapsulated_content = \
            model.get('hasEncapsulatedContent', None)

        self.__signers = []
        signers = model.get('signers', None)
        if signers is not None:
            self.__signers = [CadesSignerInfo(s) for s in signers]

    @property
    def encapsulated_content_type(self):
        return self.__encapsulated_content_type

    @encapsulated_content_type.setter
    def encapsulated_content_type(self, value):
        self.__encapsulated_content_type = value

    @property
    def has_encapsulated_content(self):
        return self.__has_encapsulated_content

    @has_encapsulated_content.setter
    def has_encapsulated_content(self, value):
        self.__has_encapsulated_content = value

    @property
    def signers(self):
        return self.__signers

    @signers.setter
    def signers(self, value):
        self.__signers = value


__all__ = ['CadesSignature']
