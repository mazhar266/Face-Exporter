# USAGE
# python recognize_faces_image.py --encodings encodings.pickle --image examples/example_01.png

# import the necessary packages
import face_recognition
import argparse
import pickle
import cv2
import ntpath
import os

from tqdm import tqdm
from shutil import copyfile

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-e", "--encodings", required=True,
                help="path to serialized db of facial encodings")
ap.add_argument("-i", "--images", required=True,
                help="path to input images")
ap.add_argument("-o", "--output", required=True,
                help="path to save image")
ap.add_argument("-n", "--name", required=True,
                help="name of the person")
ap.add_argument("-d", "--detection-method", type=str, default="cnn",
                help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())


def collect_image(image_url, data):
    # load the input image and convert it from BGR to RGB
    image = cv2.imread(
        os.path.join(
            args['images'],
            image_url
        )
    )
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # detect the (x, y)-coordinates of the bounding boxes corresponding
    # to each face in the input image, then compute the facial embeddings
    # for each face
    boxes = face_recognition.face_locations(rgb,
                                            model=args["detection_method"])
    encodings = face_recognition.face_encodings(rgb, boxes)

    # initialize the list of names for each face detected
    names = []

    # loop over the facial embeddings
    for encoding in encodings:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(data["encodings"],
                                                 encoding)
        name = "Unknown"

        # check to see if we have found a match
        if True in matches:
            # find the indexes of all matched faces then initialize a
            # dictionary to count the total number of times each face
            # was matched
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            # determine the recognized face with the largest number of
            # votes (note: in the event of an unlikely tie Python will
            # select first entry in the dictionary)
            name = max(counts, key=counts.get)

        # update the list of names
        names.append(name)

    if args['name'] in names:
        # copy the images
        copyfile(
            os.path.join(
                args['images'],
                image_url
            ),
            os.path.join(
                args['output'],
                ntpath.basename(image_url)
            )
        )


# call the func in main
if __name__ == '__main__':
    # load the known faces and embeddings
    print("[INFO] loading encodings...")
    print("[INFO] finding faces...")
    data = pickle.loads(open(args["encodings"], "rb").read())
    # Iterate through files
    for filename in tqdm([filename for filename in os.listdir(args['images']) if
                          os.path.isfile(os.path.join(args['images'], filename))]):
        try:
            # test the faces
            collect_image(filename, data)
        except Exception as e:
            pass
