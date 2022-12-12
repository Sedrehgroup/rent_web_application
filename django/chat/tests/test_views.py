import pytest
from django.urls import reverse
from rest_framework import status


pytestmark = pytest.mark.django_db


def test_list_create_chat_http_201(api_client, property_create, user_create_2):
    api_client.force_authenticate(user=user_create_2)
    CHAT_CREATE = {
        "tenant": user_create_2.id,
        "property": property_create,
    }

    response = api_client.post(reverse("chat:list_chats"), CHAT_CREATE, format="json")
    assert response.status_code == status.HTTP_201_CREATED, response.data
