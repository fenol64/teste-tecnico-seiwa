from typing import Callable
from fastapi import Depends
from sqlalchemy.orm import Session
from src.infrastructure.database.connection import get_db
from src.bootstrap.container import Container

def usecase_factory(usecase_name: str):
    def _get_usecase(db: Session = Depends(get_db)) -> Callable:
        container = Container(db=db)
        try:
            attr =  getattr(container, usecase_name)
            return attr
        except AttributeError:
            raise ValueError(f"Use case '{usecase_name}' not found in container.")
    return _get_usecase