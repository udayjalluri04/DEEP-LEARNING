from io import BytesIO
from pathlib import Path

import pandas as pd
import streamlit as st
from PIL import Image, UnidentifiedImageError
from ultralytics import YOLO


VEHICLE_CLASS_IDS = [1, 2, 3, 5, 7]
MODEL_NAME = "yolov8n.pt"

st.set_page_config(page_title="Road Scene Detector", layout="wide")


@st.cache_resource
def load_model(weights_path: str) -> YOLO:
    return YOLO(weights_path)


st.title("Road Scene Detector")
st.write(
    "Upload a road image to detect vehicles with a pretrained YOLOv8 model. "
    "The model runs on this computer; the first run downloads its weights."
)

with st.sidebar:
    st.header("Detection settings")
    confidence = st.slider("Minimum confidence", min_value=0.05, max_value=0.95, value=0.4, step=0.05)
    vehicles_only = st.checkbox("Show vehicles only", value=True)
    use_custom_weights = st.checkbox("Use a local YOLO .pt weights file", value=False)
    custom_weights = ""
    if use_custom_weights:
        custom_weights = st.text_input(
            "Weights file path",
            placeholder=r"C:\path\to\best.pt",
            help="Enter the path to an existing Ultralytics-compatible .pt model file.",
        )

uploaded_image = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png", "bmp", "webp"],
    help="Supported formats: JPG, PNG, BMP, and WebP.",
)

if uploaded_image is not None:
    try:
        image = Image.open(uploaded_image).convert("RGB")
    except UnidentifiedImageError:
        st.error("The selected file is not a readable image.")
        st.stop()

    st.image(image, caption="Uploaded image", use_container_width=True)

    if st.button("Detect vehicles" if vehicles_only else "Detect objects", type="primary"):
        weights_path = MODEL_NAME
        if use_custom_weights:
            weights_path = str(Path(custom_weights).expanduser())
            if not custom_weights.strip() or not Path(weights_path).is_file():
                st.error("Enter the path to an existing YOLO .pt weights file.")
                st.stop()

        with st.spinner("Loading the model and analyzing the image..."):
            model = load_model(weights_path)
            class_ids = VEHICLE_CLASS_IDS if vehicles_only else None
            result = model.predict(
                source=image,
                conf=confidence,
                classes=class_ids,
                verbose=False,
            )[0]

        annotated_image = Image.fromarray(result.plot()[..., ::-1])
        detections = []
        if result.boxes is not None:
            for box in result.boxes:
                class_id = int(box.cls.item())
                detections.append(
                    {
                        "Object": result.names[class_id],
                        "Confidence": round(float(box.conf.item()) * 100, 2),
                        "Box (x1, y1, x2, y2)": ", ".join(
                            str(round(float(value), 1)) for value in box.xyxy[0].tolist()
                        ),
                    }
                )

        st.subheader(f"Detection result ({len(detections)} found)")
        st.image(annotated_image, caption="Detected objects", use_container_width=True)
        if detections:
            st.dataframe(pd.DataFrame(detections), hide_index=True, use_container_width=True)
        else:
            st.info("No objects matched the selected settings.")

        download_buffer = BytesIO()
        annotated_image.save(download_buffer, format="PNG")
        st.download_button(
            "Download annotated image",
            data=download_buffer.getvalue(),
            file_name="road-scene-detections.png",
            mime="image/png",
        )
else:
    st.info("Choose an image to get started.")
