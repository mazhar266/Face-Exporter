# USES: python export_faces.py --images-dir=images_folder --faces-dir=faces_folder
# USES: python export_faces.py -i=images_folder -f=faces_folder

import os
import cv2
import argparse
from tqdm import tqdm

# get the arguments from command line
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images-dir", required=True, help="path to directory that contains images")
ap.add_argument("-f", "--faces-dir", required=True, help="path to directory to generate faces")
args = vars(ap.parse_args())

# the directory where the images are
images_dir = args['images_dir']
# the directory where the faces will be saved
faces_dir = args['faces_dir']


def minus(operand_1, operand_2):
    """
    Minuses if possible, else returns 0 / lower limit
    :param operand_1: a
    :param operand_2: b
    :return: a - b, 0
    """
    if operand_1 > operand_2:
        return operand_1 - operand_2
    return 0


def add(operand_1, operand_2, limit):
    """
    Adds if possible, else returns upper limit
    :param operand_1: a
    :param operand_2: b
    :param limit: l
    :return: a + b, l
    """
    if operand_1 + operand_2 > limit:
        return limit
    return operand_1 + operand_2


def find_sub_image(x, y, w, h, l_w, l_h):
    """
    Returns the sub image's position
    :param x: start x position
    :param y: start y position
    :param w: width
    :param h: height
    :param l_w: maximum allowed width
    :param l_h: maximum allowed height
    :return: sub image size x1, x2, y1, y2
    """
    ratio = 0.5
    x_1 = minus(x, int(w * ratio))
    x_2 = add(x, int(w * (ratio + 1)), l_w)
    y_1 = minus(y, int(h * ratio))
    y_2 = add(y, int(h * (ratio + 1)), l_h)
    return x_1, x_2, y_1, y_2


def save_faces(cascade, imgname):
    # open the image first
    img = cv2.imread(os.path.join(images_dir, imgname))
    # get the height and width
    img_height, img_width, _ = img.shape

    # now find the faces in the image
    for i, face in enumerate(cascade.detectMultiScale(img)):
        # get the face position
        x, y, w, h = face
        # find the sub image for that face
        x_1, x_2, y_1, y_2 = find_sub_image(x, y, w, h, img_width, img_height)
        # extract the sub image
        sub_face = img[y_1:y_2, x_1:x_2]
        # write the sub image to file
        cv2.imwrite(os.path.join(faces_dir, "{}_{}.jpg".format(imgname, i)), sub_face)


# call the func in main
if __name__ == '__main__':
    # load the config file for opencv face recognition
    face_cascade = "config/haarcascade_frontalface_alt2.xml"
    cascade = cv2.CascadeClassifier(face_cascade)

    # Iterate through files
    for f in tqdm([f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))]):
        try:
            # save the faces
            save_faces(cascade, f)
        except:
            pass
