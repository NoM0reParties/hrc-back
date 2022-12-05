from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

from models.base_model import EntityMeta


class Sprint(EntityMeta):
    __tablename__ = "sprints"

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, info={"verbose_name": 'Название', })
    beginning_date = Column(Date, info={"verbose_name": 'Дата начала спринта', })
    ending_date = Column(Date, info={"verbose_name": 'Дата окончания', })
    # owner USERID
    gap = Column(Integer, info={"verbose_name": 'Буффер в процентах', })
    features = relationship("Feature", back_populates="sprint", cascade='all, delete')

    def normalize(self):
        return {
            "id": self.id,
            "name": self.name,
            "beginning_date": self.beginning_date,
            "ending_date": self.ending_date,
            "gap": self.gap,
        }
