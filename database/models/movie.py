from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base

metadata = Base.metadata


class Movie(Base):
    __tablename__ = "movie"

    id = Column(Integer, primary_key=True)
    title = Column(String(1))
    year = Column(Integer)

    actors = relationship("Actor", secondary="actor_movie", backref="movies")
    genres = relationship("Genre", secondary="genre_movie")

    def __repr__(self):
        return f"Movie(id={self.id}, title={repr(self.title)}, year={self.year})"
