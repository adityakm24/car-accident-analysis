# backend/main.py
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from ultralytics import YOLO
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
import torch
from PIL import Image
import io

app = FastAPI()

# Load models
damage_model_path = "./models/faster_rcnn_model.pth"
part_model_path = "./models/best.pt"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load YOLO model for part detection
part_model = YOLO(part_model_path)

# Load Faster R-CNN for damage detection
num_classes = 7
damage_model = fasterrcnn_resnet50_fpn(weights=None)
in_features = damage_model.roi_heads.box_predictor.cls_score.in_features
damage_model.roi_heads.box_predictor = FastRCNNPredictor(
    in_features, num_classes)
damage_model.load_state_dict(torch.load(damage_model_path))
damage_model.to(device)
damage_model.eval()


@app.post("/analyze-images")
async def analyze_images(files: list[UploadFile]):
    results = []
    for file in files:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        image_tensor = transforms.ToTensor()(image).unsqueeze(0).to(device)

        # Run part detection with YOLO
        yolo_results = part_model(image, save=False)
        parts_detected = yolo_results[0].boxes

        # Run damage detection with Faster R-CNN
        with torch.no_grad():
            damage_results = damage_model(image_tensor)
        damage_boxes = damage_results[0]['boxes'].cpu().numpy()
        damage_labels = damage_results[0]['labels'].cpu().numpy()

        # Process results and append to output
        image_results = {"filename": file.filename, "parts": [], "damages": []}
        for part_box in parts_detected:
            image_results["parts"].append(
                {"box": part_box.xyxy[0].tolist(), "label": int(part_box.cls[0].cpu())})

        for damage_box, damage_label in zip(damage_boxes, damage_labels):
            image_results["damages"].append(
                {"box": damage_box.tolist(), "label": int(damage_label)})

        results.append(image_results)

    return JSONResponse(content=results)
