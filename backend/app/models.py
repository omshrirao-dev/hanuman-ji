from typing import Literal

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    query: str = Field(min_length=1, max_length=500)
    language: Literal["hi", "en", "hi-en", "auto"] = "auto"
    conversation_id: str | None = None


class SourceRef(BaseModel):
    id: str
    title: str
    type: str
    source: str


class ChatResponse(BaseModel):
    response: str
    sources: list[SourceRef]
    language: str


class FeedbackRequest(BaseModel):
    message_id: str
    rating: int = Field(ge=1, le=5)
    comment: str | None = Field(default=None, max_length=1000)
