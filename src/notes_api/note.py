from datetime import timezone, datetime

from pydantic import BaseModel, Field, field_validator


class Note(BaseModel):
    id: int
    title: str = Field(min_length=1, max_length=100)
    body: str
    tags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda : datetime.now(timezone.utc))

    @field_validator("tags")
    @classmethod
    def normalize_tags(cls, tags: list[str]) -> list[str]:
        return sorted({t.strip().lower() for t in tags if t.strip()})



'''
A Note Pydantic model: id: int, title (1–100 chars), body, tags (normalized lowercase, deduped), created_at.
'''

