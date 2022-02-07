import pytest
from django.contrib.auth.models import User


def test_lol():
    assert 1 == 1


@pytest.mark.django_db
def test_superuser():
    User.objects.create_superuser(
        username='genag',
        password='qwer'
    )
    me = User.objects.get(username='genag')
    assert me.is_superuser
