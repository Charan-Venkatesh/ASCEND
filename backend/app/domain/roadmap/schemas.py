from uuid import UUID

from pydantic import BaseModel


class GenerateRoadmapRequest(BaseModel):
    current_role: str = "IT Operations Engineer"
    target_role: str = "Enterprise AI & Cloud Architect"
    preferred_daily_minutes: int = 75


class RoadmapRead(BaseModel):
    id: UUID
    title: str
    duration_days: int
    status: str
    generated_by: str
    model_config = {"from_attributes": True}
