import os
from pathlib import Path
from time import sleep
from typing import List
from uuid import uuid4

from config import spoof_threshold
from deepface import DeepFace
from domain.model import Employee
from typing_extensions import Buffer

from . import logger


class FaceRegistrator:
    def __init__(self, db: Path):
        self._spoof_threshold = spoof_threshold
        self._db = Path(db)

    def registrate(self, index: str, name: str, bfile: Buffer) -> bool:
        logger.info("registrate")
        logger.info(f"{name=}")
        temp_file = self._db / str(uuid4())
        logger.info(f"{temp_file=}")
        file_name = self._db / f"{name}.jpg"
        logger.info(f"{file_name=}")
        with open(temp_file, "wb") as file:
            file.write(bfile)
        if self._is_real(temp_file):
            logger.info(f"Is real {temp_file}")
            if os.path.exists(file_name):
                os.remove(file_name)
            os.rename(temp_file, file_name)
        else:
            logger.info(f"Is not real {temp_file}")
            if os.path.exists(file_name):
                os.remove(file_name)
            os.remove(temp_file)
        logger.info(f"{os.path.exists(file_name)=}")
        return os.path.exists(file_name)

    def get_employees(self) -> List[Employee]:
        paths = os.listdir(self._db)
        employees = [self._format_employee(path) for path in paths if "." in path]
        return employees

    def _format_employee(self, path: str) -> Employee:
        name = path.replace(str(self._db), "").replace("/", "")
        name = name.split(".")[0] if "." in name else name
        return Employee(name=name, path=path)

    def _is_real(self, path: Path) -> bool:
        try:
            response = DeepFace.extract_faces(img_path=str(path), anti_spoofing=True, enforce_detection=True)
            prediction = (
                response[0].get("is_real", False) and response[0].get("antispoof_score", 0) > self._spoof_threshold
            )
        except Exception as error:
            logger.error(error)
            prediction = False
        return prediction
