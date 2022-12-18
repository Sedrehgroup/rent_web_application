import os
from rest_framework.serializers import ValidationError


def validate_format(image):
    valid_formats = [".jpg", ".jpeg", ".png"]
    ext = os.path.splitext(image.name)[1]
    if ext in valid_formats:
        return True
    return False

def validate_size(image):
    if image.size > 5*(10**6):
        return False
    return True

def is_valid_image(list_images):
    for image in list_images:
        if not validate_format(image):
            raise ValidationError("format image not valid")
        elif not validate_size(image):
            raise ValidationError("size image not valid")
    return True
