from typing import TypeVar

from django_id_areadata.models import Province, Area, Regency, District, SubDistrict
from django_id_areadata.csv_utils import read_csv

# Create a type variable matching your model definition
AreaType = TypeVar("AreaType", bound=Area)

class AreaData:
    __type__: AreaType
    __data__: list[AreaType]

    def __init__(self, area_type: AreaType) -> None:
        if not area_type or area_type not in [Province, Regency, District, SubDistrict]:
            raise ValueError(f"Invalid area type: {area_type}")

        self.__type__ = area_type
        self.__data__ = read_csv(area_type)

    def get_all(self) -> list[AreaType]:
        return self.__data__

    def filter_by_parent_id(self, parent_id: str) -> list[AreaType]:
        try:
            return [
                data
                for data in self.__data__
                if data.parent_id and data.parent_id == parent_id
            ]
        except KeyError:
            raise ValueError("Province not found")


class ProvinceData(AreaData):
    def __init__(self):
        super().__init__(Province)


class RegencyData(AreaData):
    def __init__(self):
        super().__init__(Regency)


class DistrictData(AreaData):
    def __init__(self):
        super().__init__(District)


class SubDistrictData(AreaData):
    def __init__(self):
        super().__init__(SubDistrict)
