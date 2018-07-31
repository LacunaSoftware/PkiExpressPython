from distutils.version import StrictVersion


class VersionManager(object):

    def __init__(self):
        self.__min_version = StrictVersion('0.0')

    def require_version(self, min_version_candidate):
        candidate = StrictVersion(min_version_candidate)
        if candidate > self.__min_version:
            self.__min_version = candidate

    def require_min_version_flag(self):
        return self.__min_version > StrictVersion('1.3')

    @property
    def min_version(self):
        return self.__min_version


__all__ = ['VersionManager']
