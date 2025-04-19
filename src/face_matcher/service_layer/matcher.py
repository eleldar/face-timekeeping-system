import os
from pathlib import Path

from config import similar_model, spoof_threshold
from deepface import DeepFace
from domain.model import Candidate

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # to-do fix


class FaceMatcher:
    def __init__(self, db):
        self._spoof_threshold = spoof_threshold
        self._similar_model = similar_model
        self._db = db

    def access(self, path: str) -> bool:
        if not self.is_real(path):
            return False
        candidate = self.search(path)
        if candidate.found_path and candidate.name:
            return self.is_similar(path, candidate.found_path)
        return False

    def is_real(self, path: str) -> bool:
        response = DeepFace.extract_faces(img_path=path, anti_spoofing=True)
        prediction = response[0].get("is_real", False) and response[0].get("antispoof_score", 0) > self._spoof_threshold
        return prediction

    def is_similar(self, path1: str, path2: str) -> bool:
        response = DeepFace.verify(img1_path=path1, img2_path=path2, model_name=self._similar_model)
        prediction = response.get("verified", False)
        return prediction

    def search(self, path: str) -> Candidate:
        response = DeepFace.find(
            img_path=path,
            db_path=self._db,
            distance_metric="cosine",
        )[0]
        if response.shape[0]:
            max_value = response["distance"].max()
            path = response[response["distance"] == max_value]["identity"].iat[0]
            name = path.replace(str(self._db), "").replace("/", "")
            name = name.split(".")[0] if "." in name else name
            return Candidate(found_path=path, name=name)
        return Candidate(found_path=None, name=None)
