from typing import Iterable

from .models import PositionSkillStat, CommonSkillStat


class SkillTableData:
    def __init__(self, year: int, common_data, position_data):
        self.year: int = year
        self.common_data: Iterable[CommonSkillStat] = common_data
        self.position_data: Iterable[PositionSkillStat] = position_data
