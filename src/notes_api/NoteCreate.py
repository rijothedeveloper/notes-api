from pydantic import BaseModel, Field

class NoteCreate(BaseModel):          # what the CLIENT may send
    title: str = Field(min_length=1, max_length=100)
    body: str = ""
    tags: list[str] = []