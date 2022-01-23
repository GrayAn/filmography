from sqlalchemy import Column, ForeignKey, Integer, String

from .base import Base

metadata = Base.metadata


class Actor(Base):
    __tablename__ = "actor"

    id = Column(Integer, primary_key=True)
    name = Column(String(1))

    def __repr__(self):
        return f"Actor(id={self.id}, name={repr(self.name)})"


class ActorMovie(Base):
    __tablename__ = "actor_movie"

    id = Column(Integer, primary_key=True)
    actor_id = Column(ForeignKey("actor.id"), nullable=False)
    movie_id = Column(ForeignKey("movie.id"), nullable=False)
