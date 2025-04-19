import os
from pathlib import Path
from time import sleep
from uuid import uuid4

from deepface import DeepFace
from typing_extensions import Buffer

from ..config import spoof_threshold


class FaceRegistrator:
    def __init__(self, db: Path):
        self._spoof_threshold = spoof_threshold
        self._db = Path(db)

    def registrate(self, index: str, name: str, bfile: Buffer) -> bool:
        temp_file = self._db / str(uuid4)
        file_name = self._db / f"{name}.jpg"
        with open(temp_file, "wb") as file:
            file.write(bfile)
        if self._is_real(temp_file):
            os.rename(temp_file, file_name)
        else:
            os.remove(temp_file)
        return os.path.exists(file_name)

    def _is_real(self, path: Path) -> bool:
        response = DeepFace.extract_faces(img_path=str(path), anti_spoofing=True)
        prediction = response[0].get("is_real", False) and response[0].get("antispoof_score", 0) > self._spoof_threshold
        return prediction
