from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from models.base_model import EntityMeta


class FeatureTeamOrder(EntityMeta):
    __tablename__ = "feature_team_orders"

    id = Column(Integer, primary_key=True)
    updated = Column(DateTime, server_default=func.now(), onupdate=func.current_timestamp())
    dev_team_id = Column(Integer, ForeignKey("dev_teams.id"), nullable=False)
    dev_team = relationship("DeveloperTeam", back_populates="dev_team_orders")
    feature_id = Column(Integer, ForeignKey("features.id"), nullable=False)
    feature = relationship("Feature", back_populates="dev_team_orders")
    assigned = Column(Boolean)
    hours = Column(Integer)
    auto_assignment = Column(Boolean)
    gap = Column(Integer)

    def normalize(self):
        return {
            "id": self.id,
            "updated": self.updated,
            "dev_team_id": self.dev_team_id,
            "feature_id": self.feature_id,
            "assigned": self.assigned,
            "hours": self.hours,
            "auto_assignment": self.auto_assignment,
            "gap": self.gap,
        }
