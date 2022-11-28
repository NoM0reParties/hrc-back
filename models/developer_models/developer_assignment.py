from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref

from models.base_model import EntityMeta


class DeveloperAssignment(EntityMeta):
    __tablename__ = "dev_assignments"

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now())
    feature_team_order_id = Column(Integer, ForeignKey("feature_team_orders.id"))
    feature_team_order = relationship("FeatureTeamOrder", backref=backref("dev_assignment"))
    developer_id = Column(Integer, ForeignKey("developers.id"))
    developer = relationship("Developer", back_populates="dev_assignments")

    def normalize(self):
        return {
            "id": self.id,
        }
