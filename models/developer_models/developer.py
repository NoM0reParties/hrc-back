from typing import Dict

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.base_model import EntityMeta


class Developer(EntityMeta):
    __tablename__ = "developers"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(64), nullable=False, info={"verbose_name": 'Имя', })
    last_name = Column(String(64), nullable=False, info={"verbose_name": 'Фамилия', })
    dev_team_id = Column(Integer, ForeignKey("dev_teams.id"))
    dev_team = relationship("DeveloperTeam", back_populates="developers")
    involvement = Column(Integer, info={"verbose_name": 'Задействованность на проекте', })
    dev_assignments = relationship("DeveloperAssignment", back_populates="developer")

    def normalize(self) -> Dict[str, str]:
        return {
            "id": self.id.__str__(),
            "name": f"{self.first_name.__str__()}, {self.last_name.__str__()}",
            "dev_team_id": self.dev_team_id,
            "involvement": self.involvement,
        }
