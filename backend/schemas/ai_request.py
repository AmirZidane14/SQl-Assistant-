from pydantic import BaseModel, Field


class AIQueryRequest(BaseModel):
    prompt: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Natural language question about the database",
    )