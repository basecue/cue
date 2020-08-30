import pytest

from cue import publisher
from tests import subscribers as test_subscribers


def publisher_function():
    @publisher
    def function(x: int) -> int:
        return x

    return function


def _class_factory():
    class Cls:
        @publisher
        def method(self, x: int) -> int:
            assert isinstance(self, Cls)
            return x

        @classmethod
        @publisher
        def classmethod_above(cls, x: int) -> int:
            assert cls is Cls
            return x

        @publisher
        @classmethod
        def classmethod_under(cls, x: int) -> int:
            assert cls is Cls
            return x

        @publisher
        @staticmethod
        def staticmethod(x: int) -> int:
            return x

    return Cls


def publisher_class_method(method_name):
    def _factory():
        cls = _class_factory()
        return getattr(cls, method_name)

    return _factory


def publisher_object_method(method_name):
    def _factory():
        cls = _class_factory()
        model = cls()
        return getattr(model, method_name)

    return _factory


@pytest.fixture
def publisher_object(publisher_object_factory):
    return publisher_object_factory()


@pytest.fixture
def expected_arguments(publisher_object):
    return ((publisher_object, 999,), {})


@pytest.mark.parametrize('exception_cls', [None, ValueError])
@pytest.mark.parametrize(
    'publisher_object_factory',
    [
        publisher_function,
        publisher_object_method('method'),
        pytest.param(
            publisher_object_method('classmethod_above'),
            marks=pytest.mark.xfail(reason='classmethod_above is not supported')
        ),
        publisher_object_method('classmethod_under'),
        pytest.param(
            publisher_class_method('classmethod_above'),
            marks=pytest.mark.xfail(reason='classmethod_above is not supported')
        ),
        publisher_class_method('classmethod_under'),
        pytest.param(
            publisher_object_method('staticmethod'),
            marks=pytest.mark.xfail(reason='staticmethod is not supported')
        ),
        pytest.param(
            publisher_class_method('staticmethod'),
            marks=pytest.mark.xfail(reason='staticmethod is not supported')
        ),
    ],
    ids=['publisher_function',
        'publisher_object_method',
        'publisher_object_classmethod_above',
        'publisher_object_classmethod_under',
        'publisher_class_classmethod_above',
        'publisher_class_classmethod_under',
        'publisher_object_staticmethod',
        'publisher_class_staticmethod'
    ]
)
@pytest.mark.parametrize(
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
def test_publisher_subscriber(
    publisher_object,
    subscriber_object,
    exception_cls,
) -> None:
    if exception_cls:
        with pytest.raises(exception_cls):
            publisher_object(999)
    else:
        assert publisher_object(999) == 999
