from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True, order=True)
class Area:
    id: str
    name: str
    parent_id: str | None = None


class Province(Area):
    pass


class Regency(Area):
    pass


class District(Area):
    pass


class SubDistrict(Area):
    pass
