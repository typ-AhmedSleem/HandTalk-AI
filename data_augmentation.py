import os
import random
import cv2 as cv

import helper
import constants as const

# * Required params
INPUT_FOLDER = "augmentation-dataset-source"
OUTPUT_FOLDER = const.DATASET_FOLDER_NAME
NUM_AUGMENTATIONS = 100
ROTATION_RANGE = (-45, 45)


def rotate_image(image, angle):
    """
    Rotate the input image by a specified angle.
    """
    rows, cols = image.shape[:2]
    rotation_matrix = cv.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    rotated_image = cv.warpAffine(image, rotation_matrix, (cols, rows))
    return rotated_image


def augment_images(inputs_imgs: list[str], labels: list[str]):
    for img_path, label in zip(input_imgs, labels):
        folder_name = label
        output_folder_path = helper.join_paths(OUTPUT_FOLDER, folder_name)
        # * Ensure output subfolder exists
        if not helper.path_exists(output_folder_path):
            helper.make_dir(output_folder_path)
            print("Created folder for label:", folder_name)

        # * Perform augmentation
        img = cv.imread(helper.join_paths(INPUT_FOLDER, img_path))
        for c in range(1, NUM_AUGMENTATIONS + 1):
            out_img_filename = f"{label}_aug_{c}.jpg"
            aug_image_path = helper.join_paths(output_folder_path, out_img_filename)
            if helper.path_exists(aug_image_path):
                continue
            # Rotate the image
            rotation_angle = random.uniform(ROTATION_RANGE[0], ROTATION_RANGE[1])
            rotated_image = rotate_image(img, rotation_angle)
            # Save augmented image
            cv.imwrite(aug_image_path, rotated_image)
            print(f"Augmented {c} image of label '{label}'")
        print("------------------------")


if __name__ == "__main__":
    # * Ensure input and output folders exist
    if not helper.path_exists(INPUT_FOLDER):
        print("Input folder doesn't exist.")
        exit(1)
    if not helper.path_exists(OUTPUT_FOLDER):
        print("Output folder doesn't exist. Creating it...")
        helper.make_dir(const.DATASET_FOLDER_NAME)
        print("Output folder has been created under name:", const.DATASET_FOLDER_NAME)

    # * Load images from input folder
    input_imgs = helper.load_images_at(INPUT_FOLDER)
    if len(input_imgs) == 0:
        print("Input folder has no images inside.")
        exit(1)

    # * Populate labels from images
    labels = []
    for img in input_imgs:
        lbl = helper.obtain_file_name(img).strip().lower()
        if helper.is_not_empty(lbl):
            labels.append(lbl)

    # * Augment input images
    augment_images(input_imgs, labels)

    # * Finished
    print("============")
    print(
        f"Augmented {len(labels)} labels with total {NUM_AUGMENTATIONS * len(labels)} of generated image."
    )
    print("Program finished.")
