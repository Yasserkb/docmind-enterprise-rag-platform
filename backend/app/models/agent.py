from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class AgentStep(BaseModel):
    name: str
    description: str
    output: dict[str, Any] = Field(default_factory=dict)


class AgentRun(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    collection_id: UUID
    task: str
    status: str = "COMPLETED"
    steps: list[AgentStep] = Field(default_factory=list)
    result: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
