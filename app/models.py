from .database import  Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP,text


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True,nullable = False)
    title = Column(String, index=True,nullable = False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)



