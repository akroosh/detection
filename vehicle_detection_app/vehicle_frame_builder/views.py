from ultralytics import YOLO
from django.conf import settings
from django.http import HttpResponseBadRequest
import os

from django.shortcuts import render
from vehicle_frame_builder.models import Vehicle


def upload_and_process_image(request):
    if request.method == "POST":
        image = request.FILES.get("image", None)
        if image is None:
            return HttpResponseBadRequest("No image file was provided.")
        temp_image_path = os.path.join(settings.MEDIA_ROOT, image.name)

        # Save uploaded image to a temporary file
        with open(temp_image_path, "wb") as temp_image:
            for chunk in image.chunks():
                temp_image.write(chunk)

        vehicle_detection_model = YOLO(settings.VEHICLE_DETECTION_MODEL)
        vehicle_results = vehicle_detection_model.track(
            source=temp_image_path,
            show=False,
            save=True,
            project="media",
            name="vehicles",
            exist_ok=True,
            persist=True,
            classes=settings.CLASS,
        )
        if vehicle_results[0].boxes.xyxy.numel() == 0:
            os.remove(temp_image_path)
            os.remove(f"{vehicle_results[0].save_dir}/{image.name}")
            return HttpResponseBadRequest(
                "No vehicle detected in the uploaded image, try to load another image."
            )

        plate_detection_model = YOLO(settings.PLATE_DETECTION_MODEL)
        plate_results = plate_detection_model.track(
            source=f"media/vehicles/{image}",
            show=False,
            save=True,
            project="media",
            name="plates",
            exist_ok=True,
            persist=True,
        )
        # Use the temporary image path to run the object detection

        os.remove(temp_image_path)

        # Save the car bounding box coordinates to the database
        vehicle_coords = [vehicle.boxes.xyxy[0].tolist() for vehicle in vehicle_results]
        plate_coords = [plate.boxes.xyxy[0].tolist() for plate in plate_results]
        vehicle = Vehicle(
            image=f"plates/{image}",
            vehicle_coords=vehicle_coords,
            plate_coords=plate_coords,
        )
        vehicle.save()

    return render(request, "vehicle_frame_builder/upload.html")


def result(request):
    vehicles = Vehicle.objects.all()
    return render(request, "vehicle_frame_builder/results.html", {"vehicles": vehicles})
