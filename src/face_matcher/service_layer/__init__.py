import logging
import os
import sys
from pathlib import Path

import torch
from config import get_db

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # to-do fix
torch.classes.__path__ = []

from .matcher import FaceMatcher
from .registrator import FaceRegistrator

db = get_db()

registrator = FaceRegistrator(db=Path(db))
matcher = FaceMatcher(db=Path(db))

__all__ = ["registrator", "matcher", "logger"]
