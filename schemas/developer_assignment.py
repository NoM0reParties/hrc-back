from pydantic import BaseModel


class DeveloperAssignmentCreateDTO(BaseModel):
    developer_id: int
    feature_team_order_id: int
