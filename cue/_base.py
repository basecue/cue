from __future__ import annotations

import dataclasses
import functools
from logging import getLogger
from typing import Any, Callable, Generic, List, NamedTuple, Optional, Type, \
    TypeVar, \
    Union, \
    overload

T = TypeVar('T')

PublisherReturnValue = TypeVar('PublisherReturnValue')
SubscriberReturnValue = TypeVar('SubscriberReturnValue')

# class PublisherFunc(Protocol[PublisherReturnValue]):
#     _subscribers: List[Callable[[PublisherReturnValue], SubscriberReturnValue]]
#     __call__: Callable[..., PublisherReturnValue]

PublisherFunc = Callable[..., PublisherReturnValue]

PublisherClass = TypeVar('PublisherClass')

FuncT = Callable[..., Any]

logger = getLogger(__name__)


class _Subscriber(Generic[PublisherReturnValue]):

    def __init__(
        self,
        func: Callable[[PublisherReturnValue], Any],
    ):
        self.__call__ = func
        self.specific_publisher_subscribers_set = set()

    def subscribe(self, specific_publisher_subscribers):
        specific_publisher_subscribers.append(self.__call__)
        self.specific_publisher_subscribers_set.add(specific_publisher_subscribers)

    # def __call__(self, *args, **kwargs):
    #     """
    #     To support also cls.__call__(instance, ...)
    #     """
    #     return self.__call__(*args, **kwargs)

    def __get__(
        self,
        instance: Optional[object], owner: Type[object]
    ) -> _Subscriber[PublisherReturnValue]:
        if instance is not None:
            self.__call__ = self.__call__.__get__(instance, owner)
        return self

    def __set_name__(self, owner: Type[object], name: str) -> None:
        # for method decorator it should be bind to instance
        for specific_publisher_subscribers in self.specific_publisher_subscribers_set:
            specific_publisher_subscribers.remove(self.__call__)

        if isinstance(self.__call__, (staticmethod, classmethod)):
            for specific_publisher_subscribers in self.specific_publisher_subscribers_set:
                specific_publisher_subscribers.append(
                    self.__call__.__get__(None, owner)
                )
            return

        if hasattr(owner, '__init__'):
            def init_wrapper(init_func):
                @functools.wraps(init_func)
                def _wrapper(instance, *args, **kwargs):
                    for specific_publisher_subscribers in self.specific_publisher_subscribers_set:
                        specific_publisher_subscribers.append(
                            self.__call__.__get__(instance, instance.__class__)
                        )
                    init_func(instance, *args, **kwargs)

                return _wrapper

            owner.__init__ = init_wrapper(owner.__init__)
        else:
            def _init(instance, *args, **kwargs):
                for specific_publisher_subscribers in self.specific_publisher_subscribers_set:
                    _subscribe(specific_publisher_subscribers)(
                        self.__call__.__get__(instance, instance.__class__)
                    )
                super().__init__(*args, **kwargs)

            owner.__init__ = _init


class SubscriberList(list):
    def __hash__(self):
        return id(self)


class Subscribers(NamedTuple):
    before: List[SubscriberFunc[PublisherReturnValue]]
    after: List[SubscriberFunc[PublisherReturnValue]]


class _Publisher(Generic[PublisherReturnValue]):
    def __init__(
        self,
        func: PublisherFunc[PublisherReturnValue],
        ignore_first=False,
    ) -> None:
        self._ignore_first = ignore_first
        self._ignore_first_set = set()
        self._subscribers = Subscribers(SubscriberList(), SubscriberList())
        self._func = func
        self._instance: Any = None
        self._owner = None

    def __call__(self, *args: Any, **kwargs: Any) -> PublisherReturnValue:
        if isinstance(self._func, (staticmethod, classmethod)):
            args_with_instance = (self._owner,) + args
        else:
            if self._instance is None:
                args_with_instance = args
            else:
                args_with_instance = (self._instance,) + args

        logger.debug(
            'EVENT: %s.%s %s %s', getattr(self._func, "__module__", "builtin"),
            self._func.__qualname__, args_with_instance, kwargs)

        for subscriber in self._subscribers.before:
            logger.debug('BEFORE: %s.%s', subscriber.__module__, subscriber.__qualname__)
            subscriber(*args_with_instance, **kwargs)

        if self._instance is not None or self._owner is not None:
            func = self._func.__get__(self._instance, self._owner)
        else:
            func = self._func


        ret = func(*args, **kwargs)

        for subscriber in self._subscribers.after:
            logger.debug('AFTER: %s.%s', subscriber.__module__, subscriber.__qualname__)
            subscriber(*args_with_instance, **kwargs)
        return ret

    def __set__(self, instance, value):
        if self._ignore_first and id(instance) not in self._ignore_first_set:
            self._ignore_first_set.add(id(instance))
            return self._func.__set__(instance, value)

        for subscriber in self._subscribers.before:
            subscriber(instance, value)
        ret = self._func.__set__(instance, value)
        for subscriber in self._subscribers.after:
            subscriber(instance, value)
        return ret

    def __get__(
        self,
        instance: Optional[object],
        owner: Type[object]
    ) -> publisher[PublisherReturnValue]:
        if instance is not None and isinstance(self._func, property):
            return self._func.__get__(instance)
        self._instance = instance
        self._owner = owner
        return self

    def __repr__(self):
        return repr(self._func)


def _getter(p_field_name):
    def getter(self):
        return getattr(self, p_field_name)

    return getter


def _setter(p_field_name):
    def setter(self, value):
        setattr(self, p_field_name, value)

    return setter


def publisher(obj):
    if isinstance(obj, type):
        if dataclasses.is_dataclass(obj):
            for field in dataclasses.fields(obj):
                p_field_name = f"_{field.name}"
                p_property = property(_getter(p_field_name))
                p_property = p_property.setter(_setter(p_field_name))
                setattr(obj, field.name, _Publisher(p_property, ignore_first=True))

            return obj
    else:
        return _Publisher(obj)


# @overload
# def subscribe(
#     publisher: PublisherFunc[PublisherReturnValue]
# ) -> Callable[
#     [Callable[[PublisherReturnValue], SubscriberReturnValue]],
#     Callable[[PublisherReturnValue], SubscriberReturnValue]
# ]:
#     ...


def _subscribe(
    specific_publisher_subscribers: List
) -> Union[
    Callable[
        [Callable[[PublisherClass, PublisherReturnValue], SubscriberReturnValue]],
        Callable[[PublisherClass, PublisherReturnValue], SubscriberReturnValue]
    ],
    Callable[
        [Callable[[PublisherReturnValue], SubscriberReturnValue]],
        Callable[[PublisherReturnValue], SubscriberReturnValue]
    ]
]:
    @overload
    def __subscribe(
        func: Callable[[PublisherClass], SubscriberReturnValue]
    ) -> Callable[[PublisherClass, PublisherReturnValue], SubscriberReturnValue]:
        ...

    @overload
    def __subscribe(
        func: Callable[[PublisherReturnValue], SubscriberReturnValue]
    ) -> Callable[[PublisherReturnValue], SubscriberReturnValue]:
        ...

    def __subscribe(
        func: Union[
            Callable[[PublisherClass], SubscriberReturnValue],
            Callable[[PublisherReturnValue], SubscriberReturnValue]
        ]
    ) -> Union[
        Callable[[Any, PublisherReturnValue], SubscriberReturnValue],
        Callable[[PublisherReturnValue], SubscriberReturnValue]
    ]:
        if isinstance(func, _Subscriber):
            subscriber = func
        else:
            subscriber = _Subscriber(func)

        subscriber.subscribe(specific_publisher_subscribers)
        return subscriber

    return __subscribe


class _MetaSubscribe(type):
    def __call__(self, publisher: Union[
        Cue[PublisherClass, PublisherReturnValue],
        PublisherFunc[PublisherReturnValue]
    ]):
        return _subscribe(publisher._subscribers.after)


class subscribe(metaclass=_MetaSubscribe):
    @staticmethod
    def before(publisher: Union[
        Cue[PublisherClass, PublisherReturnValue],
        PublisherFunc[PublisherReturnValue]
    ]):
        return _subscribe(publisher._subscribers.before)
