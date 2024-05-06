from cv2 import imwrite, imread, error as cv_error
from os import path, listdir as list_files, mkdir as make_directory
from time import sleep

IMAGE_EXTS = ["jpg", "jpeg", "png", "webp", "gif"]
DEFAULT_INPUT_FOLDER_PATH = "/Users/typ/Data/HandTalk/Signs/Unordered/"
DEFAULT_OUTPUT_FOLDER_PATH = "/Users/typ/Data/HandTalk/Signs/Ordered/"
FAILED_IMAGES_PATH = f"{DEFAULT_OUTPUT_FOLDER_PATH}/failed.txt"


def log(tag, msg, delay=0.0):
    print(f"[{tag}]: {msg}")
    if delay:
        sleep(delay)


def is_not_empty(text: str) -> bool:
    if text is None:
        return False
    if len(text) == 0:
        return False
    return True


def obtain_file_ext(filename: str):
    return filename.split(".")[-1]


def file_is_not_image(file_path: str):
    return obtain_file_ext(file_path) not in IMAGE_EXTS


def rename_image_file(input_path, output_path):
    if path.exists(output_path):
        overwrite = input("Found an existing image file with same name. Overwrite (y/n): ")
        if overwrite.strip().lower() == 'n':
            print("Interrupted tokenizing due to overlapping with an existing image file.")
            exit(123)
    imwrite(output_path, imread(input_path))


def get_most_recent_id(output_images: list[str]) -> int:
    most_recent_id = 0
    try:
        for filename in output_images:
            if (file_is_not_image(output_folder + filename)):
                continue
            id = int(filename.split(".")[0])
            if id > most_recent_id:
                most_recent_id = id
                
        return most_recent_id + 1
    except Exception as e:
        print("Failed to get most recent id. Reason=", e)
        exit(most_recent_id)

if __name__ == "__main__":
    try:
        # Obtain folder path from user input
        input_folder = input(
            f"Enter the unordered folder path ({DEFAULT_INPUT_FOLDER_PATH}): "
        )
        output_folder = DEFAULT_OUTPUT_FOLDER_PATH
        # Use default input path if path not specified
        if not is_not_empty(input_folder):
            input_folder = "/Users/typ/Data/HandTalk/Signs/Unordered/"
        if not input_folder.endswith("/"):
            input_folder += "/"
        # Validate folder path exists
        assert path.exists(input_folder), f"Folder at '{input_folder}' doesn't exist."
        # Get list of images within the input folder
        input_images = sorted(list_files(input_folder))
        # Create output folder if not exists
        if not path.exists(output_folder):
            make_directory(output_folder)
            log("INFO", f"Created output folder at '{output_folder}'", 1)
        # Obtain the most recent numeric index in output images folder
        most_recent_id = 0
        output_images = sorted(list_files(output_folder))
        log("INFO", f"Found {len(input_images)} image at input folder.", 0.5)
        if len(output_images) > 0:
            most_recent_id = get_most_recent_id(output_images)
        log("INFO", f"Most recent id is set to {most_recent_id}", 0.5)
        # Tokenize input images and save into output
        failed_images_paths = []
        for image_filename in input_images:
            try:
                # Validate the file is image
                if file_is_not_image(image_filename):
                    continue
                # Build paths
                final_filename = (
                    str(most_recent_id) + "." + obtain_file_ext(image_filename)
                )
                input_path = input_folder + image_filename
                output_path = output_folder + final_filename
                most_recent_id += 1
                # Rename the image and write it to output
                rename_image_file(input_path, output_path)
                log(
                    "INFO",
                    f"Renamed image at '{image_filename}' to '{final_filename}'",
                    0.01,
                )
            except cv_error as cve:
                log(
                    "Error",
                    f"Failed to renamed image '{image_filename}'. Reason: {cve}",
                )
                # Add failed image to failed images
                failed_images_paths.append(f"{image_filename}\n")
                continue
        print()
        log(
            "INFO", f"Tokenized {most_recent_id - len(failed_images_paths) - len(output_images)} sign image."
        )
        if len(failed_images_paths) > 0:
            # Save the failed images paths inside a text file
            with open(FAILED_IMAGES_PATH) as folder:
                folder.writelines(failed_images_paths)
            log(
                "INFO",
                f"Failed images are {len(failed_images_paths)} image. Paths saved at {FAILED_IMAGES_PATH}",
            )
        log("INFO", "Program finished.")
    except AssertionError as assertion:
        log("Error", assertion)
        exit(1)
    except KeyboardInterrupt as ki:
        log("Error", "Program is interrupted. Exiting...")
        exit(2)
    except FileNotFoundError as fnf:
        log("Error", fnf)
        exit(3)
    except TypeError as te:
        log("Error", te)
        exit(4)
