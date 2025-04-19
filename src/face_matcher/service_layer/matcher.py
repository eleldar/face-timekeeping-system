import os

from deepface import DeepFace

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


class FaceMatcher:
    def __init__(self, db):
        self._spoof_threshold = 0.5
        self._similar_model = "Facenet512"
        self._db = db

    def is_real(self, path: str) -> bool:
        response = DeepFace.extract_faces(img_path=path, anti_spoofing=True)
        prediction = response[0].get("is_real", False) and response[0].get("antispoof_score", 0) > self._spoof_threshold
        return prediction

    def is_similar(self, path1: str, path2: str) -> bool:
        response = DeepFace.verify(img1_path=path1, img2_path=path2, model_name=self._similar_model)
        prediction = response.get("verified", False)
        return prediction

    def search(self, path: str) -> str | None:
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
            return name
        return
        return response[0][response[0]["distance"] == max_value]
        print(dfs[0][dfs[0]["distance"] == max_value]["identity"].iat[0])
