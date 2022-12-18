from rest_framework import serializers
from .models import Property
from .validators import *
from account.models import User
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings


class PropertySerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    upload_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )
    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Property
        fields = "__all__"

    def get_owner(self, obj):
        owner = User.objects.filter(id=obj.owner_id).only("first_name", "last_name").first()
        return {"owner_id": owner.id, "first_name": owner.first_name, "last_name": owner.last_name}

    def get_images(self, obj):
        images = []
        if vlalidate_path_image(obj.id):
            path = os.path.join(settings.MEDIA_ROOT, f"property/{obj.id}")
            image_files = os.listdir(path)    
            for image in image_files:
                images.append(image)
        return images

    def save_images(self, list_images, id):
        for image in list_images:
            path = default_storage.save(f"property/{id}/{image.name}", ContentFile(image.read()))
            os.path.join(settings.MEDIA_ROOT, path)

    def create(self, validated_data):
        list_images = validated_data.get("upload_images")

        if not list_images:
            new_property = Property.objects.create(**validated_data)
            return new_property

        if is_valid_image(list_images):
            list_images = validated_data.pop("upload_images")
            new_property = Property.objects.create(**validated_data)
            self.save_images(list_images, new_property.id)
            return new_property


class PropertyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ("id" ,"title", "mortgage_amount", "rent_amount",
         "county", "city", "province", "area")
