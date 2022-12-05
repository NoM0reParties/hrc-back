from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from models.base_model import EntityMeta


class DeveloperTeam(EntityMeta):
    __tablename__ = "dev_teams"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), info={"verbose_name": "Название команды", })
    developers = relationship("Developer", back_populates="dev_team")
    dev_team_orders = relationship("FeatureTeamOrder", back_populates="dev_team", cascade='all, delete')

    def normalize(self):
        return {
            "id": self.id.__str__(),
            "name": self.name.__str__(),
        }
