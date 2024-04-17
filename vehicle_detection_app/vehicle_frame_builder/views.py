from ultralytics import YOLO
from django.conf import settings
import os

from django.shortcuts import render, redirect
from .models import Vehicle


def upload_and_process_image(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        temp_image_path = os.path.join(settings.MEDIA_ROOT, image.name)

        # Save uploaded image to a temporary file
        with open(temp_image_path, 'wb') as temp_image:
            for chunk in image.chunks():
                temp_image.write(chunk)

        plate_detection_model = YOLO('license_plate_detector.pt')
        plate_results = plate_detection_model.track(source=temp_image_path, show=False, save=True, project='media',
                                                    name='plates',
                                                    exist_ok=True,
                                                    persist=True)
        # Use the temporary image path to run the object detection
        vehicle_detection_model = YOLO('yolov8x.pt')
        vehicle_results = vehicle_detection_model.track(source=f'media/plates/{image}', show=False, save=True,
                                                        project='media',
                                                        name='vehicles',
                                                        exist_ok=True,
                                                        persist=True, classes=2)

        os.remove(temp_image_path)

        # Save the car bounding box coordinates to the database
        plate_coords = [plate.boxes.xyxy[0].tolist() for plate in plate_results]
        vehicle_coords = [vehicle.boxes.xyxy[0].tolist() for vehicle in vehicle_results]
        vehicle = Vehicle(
            image=f'vehicles/{image}',
            vehicle_coords=vehicle_coords,
            plate_coords=plate_coords,
        )
        vehicle.save()

    return render(request, 'vehicle_frame_builder/upload.html')


def result(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'vehicle_frame_builder/results.html', {'vehicles': vehicles})
