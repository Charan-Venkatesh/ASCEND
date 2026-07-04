from uuid import UUID

from pydantic import BaseModel, Field


class MissionTaskRead(BaseModel):
    id: UUID
    type: str
    title: str
    instructions: str
    skill_improved: str
    completion_criteria: str
    status: str
    model_config = {"from_attributes": True}


class MissionRead(BaseModel):
    id: UUID
    day_number: int
    title: str
    objective: str
    business_context: str
    learning_topic: str
    practical_task: str
    documentation_prompt: str
    reflection_prompt: str
    interview_question: str
    difficulty: int
    estimated_minutes: int
    status: str
    tasks: list[MissionTaskRead] = []
    model_config = {"from_attributes": True}


class EvidenceRequest(BaseModel):
    evidence_type: str = Field(pattern="^(note|journal|github|file|interview|text)$")
    url: str | None = None
    summary: str = Field(min_length=5, max_length=4000)
