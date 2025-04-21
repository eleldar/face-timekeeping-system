import os
import shutil
from uuid import uuid4

from config import similar_model, spoof_threshold
from deepface import DeepFace
from domain.model import Candidate, MatchOutput
from typing_extensions import Buffer

from . import logger


class FaceMatcher:
    def __init__(self, db):
        self._spoof_threshold = spoof_threshold
        self._similar_model = similar_model
        self._db = db

    def match(self, db_file: str, picture: Buffer) -> MatchOutput:
        logger.info(f"{db_file=}")
        path = self._db / str(uuid4())
        shutil.copy(self._db / db_file, path)
        logger.info(f"{path=}")
        temp_file = self._db / str(uuid4())
        logger.info(f"{temp_file=}")
        with open(temp_file, "wb") as file:
            file.write(picture)
        logger.info(f"{path=}")
        try:
            logger.info(f"Try: {path=}, {temp_file=}")
            response = DeepFace.verify(img1_path=path, img2_path=temp_file, model_name=self._similar_model)
        except Exception as error:
            logger.info(f"Error: {path=}, {temp_file=}, {error=}")
            response = {"verified": False}
        fake = not self._is_real(temp_file)
        logger.info(f"{fake=}")
        access = response.get("verified", False)
        logger.info(f"{access=}")
        os.remove(path)
        os.remove(temp_file)
        return MatchOutput(fake=fake, access=access)

    def _is_real(self, path: str) -> bool:
        try:
            response = DeepFace.extract_faces(img_path=str(path), anti_spoofing=True, enforce_detection=True)
            prediction = (
                response[0].get("is_real", False) and response[0].get("antispoof_score", 0) > self._spoof_threshold
            )
        except Exception as error:
            logger.error(f"{error=}")
            logger.info(f"{path=}")
            prediction = False
        return prediction
