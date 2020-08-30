import pytest

from tests import subscribers as test_subscribers
from cue import publisher as cue_publisher

@pytest.fixture
def publisher_class():
    class PublishingList(list):
        append = cue_publisher(list.append)

    class Cls:
        property = PublishingList()

    return Cls


@pytest.fixture
def publisher(publisher_class):
    return publisher_class()


@pytest.fixture
def publisher_object(publisher_class):
    return publisher_class.property.append


@pytest.fixture
def expected_arguments(publisher):
    return ((publisher.property, 999), {})


pytest_mark_parametrize_exception_cls = pytest.mark.parametrize('exception_cls',
    [None, ValueError])
pytest_mark_parametrize_subscriber_object = pytest.mark.parametrize(
    'subscriber_object_factory',
    [
        test_subscribers.subscriber_function,
        test_subscribers.subscriber_object_method,
        pytest.param(
            test_subscribers.subscriber_object_classmethod_above,
            marks=pytest.mark.xfail(reason='classmethod_above is not supported')
        ),
        test_subscribers.subscriber_object_classmethod_under,
        pytest.param(
            test_subscribers.subscriber_class_classmethod_above,
            marks=pytest.mark.xfail(reason='classmethod_above is not supported')
        ),
        test_subscribers.subscriber_class_classmethod_under,
        test_subscribers.subscriber_multiple_functions_same_behavior,
        test_subscribers.subscriber_multiple_functions_different_behavior,
        test_subscribers.subscriber_multiple_method_different_behavior,
        test_subscribers.subscriber_multiple_method_same_behavior,
    ],
    ids=['subscriber_function',
        'subscriber_object_method',
        'subscriber_object_classmethod_above',
        'subscriber_object_classmethod_under',
        'subscriber_class_classmethod_above',
        'subscriber_class_classmethod_under',
        'subscriber_multiple_functions_same_behavior',
        'subscriber_multiple_functions_different_behavior',
        'subscriber_multiple_method_different_behavior',
        'subscriber_multiple_method_same_behavior',
    ]
)


@pytest_mark_parametrize_exception_cls
@pytest_mark_parametrize_subscriber_object
def test_property_write(
    publisher,
    subscriber_object,
    exception_cls
):
    if exception_cls:
        with pytest.raises(exception_cls):
            publisher.property.append(999)
    else:
        publisher.property.append(999)
        assert publisher.property == [999]
