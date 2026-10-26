# Road Scene Detector for Windows

This local browser application detects objects in uploaded images using an Ultralytics YOLO model. By default it uses the lightweight pretrained `yolov8n.pt` model and filters detections to common vehicle classes. The model weights are downloaded on first use. You can also provide a local Ultralytics-compatible `.pt` file, such as custom trained weights.

## Requirements

- Windows 10 or 11
- Python 3.12 installed and available through the `py` launcher
- An internet connection for installing packages and downloading the default model on its first run

## Run

1. Double-click `run_app.bat` in this folder. On the first run it creates a local virtual environment and installs the required packages.
2. The launcher opens the app in your browser at `http://127.0.0.1:8501`.
3. Upload a road image and click **Detect vehicles**.
4. Review the annotated image and detection table, or download the result.

The application runs on your computer. Uploaded images are processed locally and are not sent to an application server.

## Notes

- The included `data.yaml` refers to dataset paths from Google Colab. It does not include the dataset or trained model weights.
- The default pretrained model uses COCO classes, not the custom eight-class labels in `data.yaml`. To use a model trained for those classes, enable **Use a local YOLO .pt weights file** and enter its path.
- The original `.py` files are exported notebook code and still contain Google Colab-specific commands; this app is the Windows-friendly image detection entry point.
