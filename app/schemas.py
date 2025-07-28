from pydantic import BaseModel, Field


class PostBase(BaseModel):
    title:str
    content:str
    published: bool = Field(default=True, description="Indicates if the post is published")

class PostCreate(PostBase):
    """Schema for creating a post"""
    pass