# Face Exporter

Face Exporter to export faces from images.

### Requirements

- Python
- OpenCV

### How to

- Install OpenCV (for Ubuntu: `./install_opencv.sh`)
- Run `pip install -r requirements.txt`
- Place your photos in the `images` folder
- To extract photos from video place your `video.mp4` in `from_video` folder
- Run `.export.sh` in that folder
- Grab the exported images in the `images` folder
- Run `python export_faces.py --images-dir=images --faces-dir=faces`
- Look into the `faces` folder for exported faces
- Now take some face samples from them as your selected person's face
- Place / copy them in the `dataset` folder in sub-folder named by that person
- Keep in mind this name of that person (case sensitive, without space and special chars)
- Encode the recognized faces like `python encode_faces.py --dataset dataset --encodings encodings/encodings.pickle`
- Now that you have recognition model ready, run the collect_faces to remove unnecessary faces
- Run `python recognize_faces_image.py --encodings encodings.pickle --images faces --output tested --name name`
- Now the faces are in `tested` folder ready for your project

### Credits

Mazhar Ahmed -
[github.com/mazhar266](https://github.com/mazhar266)

### Special Thanks

Face Recognition OpenCV by [**PyImageSearch**](https://www.pyimagesearch.com)

> Keep in mind that, you have to run face recognition / export in your project again on the faces in `tested` folder. This project copies the whole face for you to analyze.