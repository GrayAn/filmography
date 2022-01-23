from sqlalchemy import create_engine
from sqlalchemy.orm import create_session

_engine = None
_url = "sqlite:///db"


def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(url=_url)

    return _engine


def get_session():
    engine = get_engine()

    return create_session(bind=engine, autoflush=False)
