import os
import shutil
from pathlib import Path

import pytest

from face_matcher.config import get_db
from face_matcher.service_layer.matcher import FaceMatcher

root_dir = Path("tests/datasets")
e1p1 = root_dir / "employee1photo1.jpg"
e1p2 = root_dir / "employee1photo2.jpg"
e2p1 = root_dir / "employee2photo1.jpg"
e1fake = root_dir / "employee1fake.jpg"
e3unk = root_dir / "employee3unknown.jpg"

spoof_examples = [
    {"id": 1, "path": e1p1, "true": True},
    {"id": 2, "path": e1p2, "true": True},
    {"id": 3, "path": e2p1, "true": True},
    {"id": 4, "path": e1fake, "true": False},
]

db = Path(get_db())
verify_examples = [
    {"id": 1, "path1": e1p1, "path2": db / "Ivanov Ivan Ivanovich.jpg", "true": True},
    {"id": 2, "path1": e1p1, "path2": db / "Petrov Petr Petrovich.jpg", "true": False},
]

search_examples = [
    {"id": 1, "path": e1p1, "name": "Ivanov Ivan Ivanovich", "found_path": str(db / "Ivanov Ivan Ivanovich.jpg")},
    {"id": 2, "path": e3unk, "name": None, "found_path": None},
]

access_examples = [
    {"id": 1, "path": e1p1, "name": "Ivanov Ivan Ivanovich", "true": True},
    {"id": 2, "path": e1fake, "name": "Ivanov Ivan Ivanovich", "true": False},
    {"id": 3, "path": e3unk, "name": "Ivanov Ivan Ivanovich", "true": False},
]


class TestMatching:
    def setup_class(self):
        shutil.copy(e1p2, db / "Ivanov Ivan Ivanovich.jpg")
        shutil.copy(e2p1, db / "Petrov Petr Petrovich.jpg")
        self._matcher = FaceMatcher(db=db)

    def teardown_class(self):
        os.remove(db / "Ivanov Ivan Ivanovich.jpg")
        os.remove(db / "Petrov Petr Petrovich.jpg")
        del self._matcher

    def test_spoofing(self):
        for example in spoof_examples:
            pred = self._matcher.is_real(example["path"])
            assert example["true"] == pred

    def test_verify(self):
        for example in verify_examples:
            pred = self._matcher.is_similar(example["path1"], example["path2"])
            assert example["true"] == pred

    def test_search(self):
        assert os.path.exists(db / "Ivanov Ivan Ivanovich.jpg")
        assert os.path.exists(db / "Petrov Petr Petrovich.jpg")
        for example in search_examples:
            pred = self._matcher.search(example["path"])
            assert example["name"] == pred.name
            assert example["found_path"] == pred.found_path

    def test_access(self):
        for example in access_examples:
            pred = self._matcher.access(example["path"])
            assert example["true"] == pred
