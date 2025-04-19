import os


def get_db():
    docker_path = "/src/db/"
    local_path = "./src/db/"
    db = docker_path if os.path.exists(docker_path) else local_path
    os.makedirs(db, exist_ok=True)
    return db
