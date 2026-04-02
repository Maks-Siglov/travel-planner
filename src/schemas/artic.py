from pydantic import BaseModel


class Artwork(BaseModel):
    id: int
    title: str | None = None
