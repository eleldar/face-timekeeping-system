import os
from pathlib import Path

import pytest
from conftest import e1fake, e1p1, e1p2, e2p1, e3unk

from face_matcher.config import get_db
from face_matcher.service_layer.registrator import FaceRegistrator


class TestRegistration:
    def setup_class(self):
        self._db = Path(get_db())
        # shutil.copy(e1p2, db / "Ivanov Ivan Ivanovich.jpg")
        # shutil.copy(e2p1, db / "Petrov Petr Petrovich.jpg")
        self._registrator = FaceRegistrator(db=self._db)

    def teardown_class(self):
        for file in os.listdir(self._db):
            os.remove(self._db / file)
        del self._registrator

    def test_real_registration(self):
        real_examples = [
            {"id": 1, "path": e1p1, "name": "Ivanov Ivan Ivanovich"},
            {"id": 2, "path": e2p1, "name": "Petrov Petr Petrovich"},
        ]
        for example in real_examples:
            with open(example["path"], "rb") as bfile:
                assert self._registrator.registrate(index=example["id"], name=example["name"], bfile=bfile.read())

    def test_fake_registration(self):
        with open(e1fake, "rb") as bfile:
            assert False == self._registrator.registrate(index=0, name="Fake Fake Fake", bfile=bfile.read())
