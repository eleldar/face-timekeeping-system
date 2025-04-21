import os


def get_db():
    docker_path = "/app/db/"
    local_path = "./src/db/"
    db = docker_path if os.path.exists(docker_path) else local_path
    os.makedirs(db, exist_ok=True)
    return db


spoof_threshold = 0.1
similar_model = "Facenet512"
