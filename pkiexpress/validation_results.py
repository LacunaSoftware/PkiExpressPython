from .validation_item import ValidationItem


class ValidationResults(object):

    def __init__(self, model):
        self.__errors = []
        self.__warnings = []
        self.__passed_checks = []

        if model is not None:
            errors = model.get('errors', None)
            warnings = model.get('warnings', None)
            passed_checks = model.get('passedChecks', None)

            if errors is not None and len(errors) > 0:
                self.__errors = ValidationResults.__convert_items(errors)

            if warnings is not None and len(warnings) > 0:
                self.__warnings = ValidationResults.__convert_items(errors)

            if passed_checks is not None and len(passed_checks) > 0:
                self.__passed_checks = \
                    ValidationResults.__convert_items(passed_checks)

    def __str__(self, indentation_level=0):
        item_indent = '\t' * indentation_level
        text = ''

        text += self.get_summary(indentation_level)
        if self.has_errors:
            text += '\n' + item_indent + 'Errors:\n'
            text += ValidationResults.__join_items(self.__errors,
                                                   indentation_level)
        if self.has_warnings:
            text += '\n' + item_indent + 'Warnings:\n'
            text += ValidationResults.__join_items(self.__warnings,
                                                   indentation_level)
        if self.__passed_checks is not None and len(self.__passed_checks) > 0:
            text += '\n' + item_indent + 'Passed Checks:\n'
            text += ValidationResults.__join_items(self.__passed_checks,
                                                   indentation_level)

        return text

    @property
    def is_valid(self):
        return not self.has_errors

    @property
    def checks_performed(self):
        return len(self.__errors) + \
               len(self.__warnings) + \
               len(self.__passed_checks)

    @property
    def has_errors(self):
        return self.__errors is not None and len(self.__errors) > 0

    @property
    def has_warnings(self):
        return self.__warnings is not None and len(self.__warnings) > 0

    def get_summary(self, indentation_level=0):
        item_indent = '\t' * indentation_level
        text = item_indent + 'Validation results: '

        if self.checks_performed == 0:
            text += 'no checks performed'
        else:
            text += str(self.checks_performed) + ' checks performed'
            if self.has_errors:
                text += ', ' + str(len(self.__errors)) + ' errors'
            if self.has_warnings:
                text += ', ' + str(len(self.__warnings)) + ' warnings'
            if self.__passed_checks is not None and \
                    len(self.__passed_checks) > 0:
                if not self.has_errors and not self.has_warnings:
                    text += ', all passed'
                else:
                    text += ', ' + str(len(self.__passed_checks)) + ' passed'

        return text

    @staticmethod
    def __convert_items(items):
        return [ValidationItem(i) for i in items]

    @staticmethod
    def __join_items(items, indentation_level=0):
        text = ''
        is_first = True
        item_ident = '\t' * indentation_level

        for item in items:
            if is_first:
                is_first = False
            else:
                text += '\n'
            text += item_ident + '- '
            text += item.__str__(indentation_level)

        return text


__all__ = ['ValidationResults']
