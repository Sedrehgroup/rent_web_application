import os
from django.conf import settings


def validate_format_image(image):
        valid_formats = ["jpg", "jpeg", "png"]
        try:
            format_image = image.name.split(".")[1].lower()
        except IndexError:
            return False

        if format_image in valid_formats:
            return True
        return False


def validate_size_image(image):
    5*(10**6)
    if image.size > 14000:
        return False
    return True


def vlalidate_path_image(property_id):
    path = os.path.join(settings.MEDIA_ROOT, f"property/{property_id}")
    try:
        os.listdir(path)
    except FileNotFoundError:
        return False
    return True
