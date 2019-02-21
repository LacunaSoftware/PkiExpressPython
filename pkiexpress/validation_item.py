from .validation_results import ValidationResults


class ValidationItem(object):

    def __init__(self, model):
        self.__type = model.get('type', None)
        self.__message = model.get('message', None)
        self.__detail = model.get('detail', None)
        self.__inner_validation_results = None
        inner_validation_results = model.get('innerValidationResults', None)
        if inner_validation_results is not None:
            self.__inner_validation_results = \
                ValidationResults(inner_validation_results)

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        self.__type = value

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        self.__message = value

    @property
    def detail(self):
        return self.__detail

    @detail.setter
    def detail(self, value):
        self.__detail = value

    @property
    def inner_validation_results(self):
        return self.__inner_validation_results

    @inner_validation_results.setter
    def inner_validation_results(self, value):
        self.__inner_validation_results = value


__all__ = ['ValidationItem']
