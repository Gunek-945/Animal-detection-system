from ultralytics import YOLO
import cv2
import supervision as sv
import random

# #Own Image

model= YOLO('XDreamv1(m).pt')
image = cv2.imread(f'Content/Augmented images/aug_0_1358.jpeg')
results = model(image)[0]
detections = sv.Detections.from_ultralytics(results)

bounding_box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()

annotated_image = bounding_box_annotator.annotate(
    scene=image, detections=detections)
annotated_image = label_annotator.annotate(
    scene=annotated_image, detections=detections)

sv.plot_image(annotated_image)

# # Random from validation set

# #Train

# model = YOLO('runs/detect/train/weights/best.pt')

# dataset = sv.DetectionDataset.from_yolo(
#     images_directory_path=f"datasets/auto-animals-2/valid/images",
#     annotations_directory_path=f"datasets/auto-animals-2/valid/labels",
#     data_yaml_path=f"datasets/auto-animals-2/data.yaml"
# )

# bounding_box_annotator = sv.BoundingBoxAnnotator()
# label_annotator = sv.LabelAnnotator()

# random_image = random.choice(list(dataset.images.keys()))
# random_image = dataset.images[random_image]

# results = model(source=random_image, conf=0.35)[0]
# detections = sv.Detections.from_ultralytics(results)

# annotated_image = bounding_box_annotator.annotate(
#     scene=random_image, detections=detections)
# annotated_image = label_annotator.annotate(
#     scene=annotated_image, detections=detections)

# sv.plot_image(annotated_image)
