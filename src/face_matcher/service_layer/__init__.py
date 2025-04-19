from pathlib import Path

from config import get_db

from .matcher import FaceMatcher
from .registrator import FaceRegistrator

db = get_db()

registrator = FaceRegistrator(db=Path(db))
matcher = FaceMatcher(db=Path(db))

__all__ = ["registrator", "matcher"]
