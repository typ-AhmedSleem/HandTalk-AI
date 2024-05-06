import os
import constants as const
from cv2 import imread as cv_read_image

def path_exists(path: str):
    return os.path.exists(path)

def ls_at(path: str):
    return os.listdir(path)

def files_count_at(path: str):
    return len(ls_at(path))

def load_samples_paths(path: str) -> list[str]:
    return [const.SAMPLES_PATH + name for name in ls_at(const.SAMPLES_PATH)]

def load_samples(paths: list[str]):
    return { sample_path: cv_read_image(sample_path) for sample_path in paths }