from rest_framework import serializers
from .models import Property
from .validators import *
from account.models import User
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from uuid import uuid4


class PropertyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ("id" ,"title", "mortgage_amount", "rent_amount",
         "county", "city", "province", "area")


class PropertySerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    upload_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )
    images = serializers.SerializerMethodField(read_only=True)
    image = serializers.CharField(write_only=True, required=False) # for delete image

    class Meta:
        model = Property
        fields = "__all__"

    def get_owner(self, obj):
        owner = User.objects.filter(id=obj.owner_id).only("first_name", "last_name").first()
        return {"owner_id": owner.id, "first_name": owner.first_name, "last_name": owner.last_name}

    def get_images(self, obj):
        images = []
        path = os.path.join(settings.MEDIA_ROOT, f"property/{obj.id}")
        if os.path.isdir(path): 
            image_files = os.listdir(path) 
            for image in image_files:
                images.append(f"/media/property/{obj.id}/{image}")
        return images

    def save_images(self, list_images, id):
        for image in list_images:
            ext = os.path.splitext(image.name)[1]
            default_storage.save(f"property/{id}/{str(uuid4())}{ext}", ContentFile(image.read()))

    def delete_images(self, name, property_id):
        path = os.path.join(settings.MEDIA_ROOT, f"property/{property_id}/{name}")
        if os.path.isfile(path):
            os.remove(path)

    def create(self, validated_data):
        list_images = validated_data.get("upload_images")

        if not list_images:
            return super().create(validated_data)

        if is_valid_image(list_images):
            list_images = validated_data.pop("upload_images")
            new_property = super().create(validated_data)
            self.save_images(list_images, new_property.id)
            return new_property

    def update(self, instance, validated_data):
        list_images = validated_data.get("upload_images")
        image = validated_data.get("image")
        update_proeprty = super().update(instance, validated_data)

        if image:
            self.delete_images(image, update_proeprty.id)

        if list_images:
            if is_valid_image(list_images):
                list_images = validated_data.pop("upload_images")
                self.save_images(list_images, update_proeprty.id)
                return update_proeprty
        return update_proeprty


class LeasePropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = (
            "type", "province", "county", "city", "address", "unit_floor",
            "zip", "use", "area", "Skeleton_type", "construction_year",
            "floors_number", "units_per_floor", "building_side", "description",
            "Sub_registration_plate", "Original_registration_plate", "phone_lines"
        )
