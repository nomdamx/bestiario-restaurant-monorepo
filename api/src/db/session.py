from collections.abc import Generator
from contextlib import contextmanager
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Session, declarative_base, sessionmaker

from src.config import get_config
from src.core.custom_errors import ValidationError

CONFIG = get_config()

DATABASE_URL = CONFIG.DB_URL

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    except IntegrityError as e:
        db.rollback()
        raise ValidationError(details="Data provided is incorrect") from e
    except:
        db.rollback()
        raise
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db)]

BASE: type[DeclarativeBase] = declarative_base()


@contextmanager
def db_context() -> Generator[Session, None, None]:
    gen = get_db()
    session = next(gen)
    try:
        yield session
    except Exception:
        gen.throw(*__import__("sys").exc_info())
    finally:
        gen.close()
