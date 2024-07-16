# from ultralytics import YOLO
# from products import furniture_classes_list, complementary_items

# def get_complementary_items(detected_items):
#     suggestions = set()
#     for item in detected_items:
#         if item in complementary_items:
#             suggestions.update(complementary_items[item])
#     # Remove detected items from suggestions to avoid redundancy
#     suggestions.difference_update(detected_items)
#     return list(suggestions)

# # Load the YOLOv9 model
# model = YOLO('yolov9s.pt')

# # Run predictions
# results = model.predict('f1.jpg')

# detected_classes = [model.names[int(cls)] for cls in results[0].boxes.cls]
# filtered_classes = [cls for cls in detected_classes if cls in furniture_classes_list]

# # Display results
# results[0].show()

# # Print the list of filtered detected objects
# print("Filtered Detected Objects: ", filtered_classes)

# # Get complementary items
# complementary_furniture = get_complementary_items(filtered_classes)
# print("Suggested Complementary Furniture: ", complementary_furniture)

furniture_classes_list = [
    "bench", "chair", "couch", "potted plant", 
    "bed", "dining table", "clock", "vase"
]

complementary_items = {
    "bench": ["vase", "potted plant", "clock", "cabinet", "shelf", "sideboard"],
    "chair": ["dining table", "potted plant", "vase", "desk", "shelf", "wing_chair"],
    "couch": ["vase", "potted plant", "bench", "sideboard", "tv_bench", "chaise"],
    "potted plant": ["bench", "couch", "dining table", "shelf", "cabinet", "desk"],
    "bed": ["vase", "clock", "shelf", "cabinet", "sideboard", "sleeper"],
    "dining table": ["chairs", "vase", "potted plant", "sideboard", "cabinet", "bench"],
    "clock": ["bench", "couch", "vase", "shelf", "desk", "tv_bench"],
    "vase": ["couch", "dining table", "bench", "shelf", "desk", "sideboard"]
}

from ultralytics import YOLO
# Load the YOLOv9 model
model = YOLO('yolov9s.pt')
# print(model)

def detect_furniture(image):
    # Run predictions
    results = model.predict(image)

    # Filter detected classes
    detected_classes = [model.names[int(cls)] for cls in results[0].boxes.cls]
    filtered_classes = [cls for cls in detected_classes if cls in furniture_classes_list]

    return filtered_classes