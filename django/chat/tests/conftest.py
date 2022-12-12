import pytest
from property.models import Property
from chat.models import Chat
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_create_2():
    user = User.objects.create(
        phone_number="+989399202914",
        password="something",
        national_code="018",
        first_name="something",
        last_name="something",
    )
    return user


@pytest.fixture
def property_create():
    user = User.objects.create(
        phone_number="+989399202913",
        password="something",
        national_code="017",
        first_name="something",
        last_name="something",
    )

    property = Property.objects.create(
        owner=user,
        title="something",
        mortgage_amount=100,
        rent_amount=100,
        type=1,
        use=1,
        area=100,
        province="something",
        county="something",
        city="something",
        neighbourhood="something",
        convertible=True,
        construction_year=1,
        bedrooms=1,
    )
    return property.id
