import os
from django.conf import settings
from rest_framework.serializers import ValidationError


def validate_format(image):
    valid_formats = ["jpg", "jpeg", "png"]
    try:
        format_image = image.name.split(".")[1].lower()
    except IndexError:
        return False

    if format_image in valid_formats:
        return True
    return False

def validate_size(image):
    if image.size > 14000:
        return False
    return True

def is_valid_image(list_images):
    for image in list_images:
        if not validate_format(image):
            raise ValidationError("format image not valid")
        elif not validate_size(image):
            raise ValidationError("size image not valid")
    return True


def vlalidate_path_image(property_id):
    path = os.path.join(settings.MEDIA_ROOT, f"property/{property_id}")
    try:
        os.listdir(path)
    except FileNotFoundError:
        return False
    return True
