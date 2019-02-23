from .pdf_mark_page_options import PdfMarkPageOptions
from .color import Color


class PdfMark(object):

    def __init__(self):
        self.__container = None
        self.__border_width = 0.0
        self.__border_color = Color.BLACK
        self.__background_color = Color.TRANSPARENT
        self.__elements = []
        self.__page_option = PdfMarkPageOptions.ALL_PAGES
        self.__page_option_number = None

    @property
    def container(self):
        return self.__container

    @container.setter
    def container(self, value):
        self.__container = value

    @property
    def border_width(self):
        return self.__border_width

    @border_width.setter
    def border_width(self, value):
        self.__border_width = value

    @property
    def border_color(self):
        return self.__border_color

    @border_color.setter
    def border_color(self, value):
        self.__border_color = value

    @property
    def background_color(self):
        return self.__background_color

    @background_color.setter
    def background_color(self, value):
        self.__background_color = value

    @property
    def elements(self):
        return self.__elements

    @elements.setter
    def elements(self, value):
        self.__elements = value

    @property
    def page_option(self):
        return self.__page_option

    @page_option.setter
    def page_option(self, value):
        self.__page_option = value

    @property
    def page_option_number(self):
        return self.__page_option_number

    @page_option_number.setter
    def page_option_number(self, value):
        self.__page_option_number = value


__all__ = ['PdfMark']
