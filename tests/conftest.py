import pytest


@pytest.fixture
def subscriber_object(publisher_object, exception_cls, subscriber_object_factory, expected_arguments):
    return subscriber_object_factory(publisher_object, exception_cls, expected_arguments)