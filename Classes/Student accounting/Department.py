import typing
from Year import Year


class Department:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.subjects = []

    @staticmethod
    def _validate_year_list(year_list: typing.List[Year]):
        if not all(isinstance(year, Year) for year in year_list):
            raise TypeError("year_list must be a list of Year objects")