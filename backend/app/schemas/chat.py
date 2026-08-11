from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="Legal question",
    )


class Source(BaseModel):
    source: str
    page: int | None = None
    chunk_id: str | None = None
    chunk_index: int | None = None


class AskResponse(BaseModel):
    question: str
    answer: str
    sources: list[Source]