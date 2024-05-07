import os
import constants as const
from cv2 import imread as cv_read_image

def path_exists(path: str):
    return os.path.exists(path)

def join_paths(folder, path):
    return os.path.join(folder, path)

def make_dir(name: str):
    os.makedirs(name)

def ls_at(path: str):
    return os.listdir(path)

def files_count_at(path: str):
    return len(ls_at(path))

def load_samples_paths(path: str) -> list[str]:
    return [const.SAMPLES_PATH + name for name in ls_at(const.SAMPLES_PATH)]

def load_samples(paths: list[str]):
    return { sample_path: cv_read_image(sample_path) for sample_path in paths }

def load_labels(maxId : int):
    labels = [str(id) for id in range(1, maxId + 1)]
    labels.append('None')
    return labels

def is_not_empty(text: str) -> bool:
    if text is None:
        return False
    if len(text) == 0:
        return False
    return True


def obtain_file_ext(filename: str):
    return filename.split(".")[-1]

def obtain_file_name(filename: str):
    return filename.split(".")[0]


def file_is_not_image(file_path: str):
    return obtain_file_ext(file_path) not in const.IMAGE_EXTS

def load_images_at(folder_path: str):
    paths = []
    if is_not_empty(folder_path) and path_exists(folder_path):
        for path in ls_at(folder_path):
            if file_is_not_image(path):
                continue
            paths.append(path)
        
    return paths
        
