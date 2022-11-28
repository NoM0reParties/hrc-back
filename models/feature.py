from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.base_model import EntityMeta


class Feature(EntityMeta):
    __tablename__ = "features"

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, info={"verbose_name": 'Название', })
    sprint_id = Column(Integer, ForeignKey("sprints.id"))
    sprint = relationship("Sprint", back_populates="features")
    dev_team_orders = relationship("FeatureTeamOrder", back_populates="feature")

    def normalize(self):
        return {
            "id": self.id,
            "name": self.name,
            "sprint_id": self.sprint_id,
        }
