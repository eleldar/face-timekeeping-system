import os
from pathlib import Path
from random import randint

import pytest
from conftest import e1fake, e1p1, e1p2, e2p1, e3unk

from face_matcher.config import get_db
from face_matcher.service_layer.matcher import FaceMatcher
from face_matcher.service_layer.registrator import FaceRegistrator

db = Path(get_db())


class TestMatching:
    def setup_class(self):
        self._matcher = FaceMatcher(db=db)
        self._registrator = FaceRegistrator(db=db)
        self._registrator.registrate(
            index=randint(0, 100), name="Ivanov Ivan Ivanovich", bfile=self._read_bfile(self, path=e1p1)
        )
        self._registrator.registrate(
            index=randint(0, 100), name="Petrov Petr Petrovich", bfile=self._read_bfile(self, path=e2p1)
        )

    def teardown_class(self):
        for file in os.listdir(db):
            os.remove(db / file)
        del self._matcher

    def test_spoofing(self):
        spoof_examples = [
            {"id": 1, "path": e1p1, "true": True},
            {"id": 2, "path": e1p2, "true": True},
            {"id": 3, "path": e2p1, "true": True},
            {"id": 4, "path": e1fake, "true": False},
        ]
        for example in spoof_examples:
            pred = self._matcher.is_real(example["path"])
            assert example["true"] == pred

    def test_verify(self):
        verify_examples = [
            {"id": 1, "path1": e1p1, "path2": db / "Ivanov Ivan Ivanovich.jpg", "true": True},
            {"id": 2, "path1": e1p1, "path2": db / "Petrov Petr Petrovich.jpg", "true": False},
        ]
        for example in verify_examples:
            pred = self._matcher.is_similar(example["path1"], example["path2"])
            assert example["true"] == pred

    def test_search(self):
        search_examples = [
            {
                "id": 1,
                "path": e1p1,
                "name": "Ivanov Ivan Ivanovich",
                "found_path": str(db / "Ivanov Ivan Ivanovich.jpg"),
            },
            {"id": 2, "path": e3unk, "name": None, "found_path": None},
        ]
        assert os.path.exists(db / "Ivanov Ivan Ivanovich.jpg")
        assert os.path.exists(db / "Petrov Petr Petrovich.jpg")
        for example in search_examples:
            pred = self._matcher.search(example["path"])
            assert example["name"] == pred.name
            assert example["found_path"] == pred.found_path

    def test_access(self):
        access_examples = [
            {"id": 1, "path": e1p1, "name": "Ivanov Ivan Ivanovich", "true": True},
            {"id": 2, "path": e1fake, "name": "Ivanov Ivan Ivanovich", "true": False},
            {"id": 3, "path": e3unk, "name": "Ivanov Ivan Ivanovich", "true": False},
        ]
        for example in access_examples:
            pred = self._matcher.access(example["path"])
            assert example["true"] == pred

    def _read_bfile(self, path):
        with open(path, "rb") as bfile:
            return bfile.read()
