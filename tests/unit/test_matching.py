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
    {"id": 1, "path": e1p1, "name": "Ivanov Ivan Ivanovich"},
    {"id": 2, "path": e3unk, "name": None},
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
            print(pred)
            assert example["name"] == pred


"""
from deepface import DeepFace

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


root_dir = Path("tests/datasets")
# real
e1p1 = root_dir / "employee1photo1.jpg"
e1p2 = root_dir / "employee1photo2.jpg"
e2p1 = root_dir / "employee2photo1.jpg"

# fake
e1fake = root_dir / "employee1fake.jpg"

# check
face_objs_e1p1 = DeepFace.extract_faces(img_path=e1p1, anti_spoofing=True)
face_objs_e1p2 = DeepFace.extract_faces(img_path=e1p2, anti_spoofing=True)
face_objs_e2p1 = DeepFace.extract_faces(img_path=e2p1, anti_spoofing=True)
face_objs_e1fake = DeepFace.extract_faces(img_path=e1fake, anti_spoofing=True)

assert face_objs_e1p1[0]["is_real"]
assert face_objs_e1p2[0]["is_real"]
assert face_objs_e2p1[0]["is_real"]
assert not face_objs_e1fake[0]["is_real"]

# comparation
similar = DeepFace.verify(img1_path=e1p1, img2_path=e1p2, model_name="Facenet512")
assert similar["verified"]
unsimilar = DeepFace.verify(img1_path=e1p1, img2_path=e2p1, model_name="Facenet512")
assert not unsimilar["verified"]

# find
dfs = DeepFace.find(
    img_path=e1p1,
    db_path=root_dir,
    distance_metric="cosine",
)
max_value = dfs[0]["distance"].max()
print(dfs[0][dfs[0]["distance"] == max_value]["identity"].iat[0])
"""
