from cue import subscribe


def subscriber_function(publisher_object, exception_cls, expected_arguments):
    called = 0
    @subscribe(publisher_object)
    def function(*args, **kwargs) -> None:
        nonlocal called
        called += 1
        assert called == 1
        arguments = args, kwargs
        assert arguments == expected_arguments
        if exception_cls:
            raise exception_cls(arguments)

    return function


def subscriber_object_method(publisher_object, exception_cls, expected_arguments):
    called = 0

    class Cls:
        @subscribe(publisher_object)
        def on_publish(self, *args, **kwargs):
            nonlocal called
            called += 1
            assert called == 1
            arguments = args, kwargs
            assert arguments == expected_arguments
            assert isinstance(self, Cls)
            if exception_cls:
                raise exception_cls(arguments)

    obj = Cls()
    return obj


def subscriber_object_classmethod_above(publisher_object, exception_cls, expected_arguments):
    called = 0

    class Cls:
        @classmethod
        @subscribe(publisher_object)
        def on_publish(cls, *args, **kwargs):
            nonlocal called
            called += 1
            assert called == 1
            arguments = args, kwargs
            assert arguments == expected_arguments
            assert cls is Cls
            if exception_cls:
                raise exception_cls(arguments)


    obj = Cls()
    return obj


def subscriber_object_classmethod_under(publisher_object, exception_cls, expected_arguments):
    called = 0

    class Cls:
        @subscribe(publisher_object)
        @classmethod
        def on_publish(cls, *args, **kwargs) -> None:
            nonlocal called
            called += 1
            assert called == 1
            arguments = args, kwargs
            assert arguments == expected_arguments
            assert cls is Cls
            if exception_cls:
                raise exception_cls(arguments)


    obj = Cls()
    return obj


def subscriber_class_classmethod_above(publisher_object, exception_cls, expected_arguments):
    called = 0

    class Cls:
        @classmethod
        @subscribe(publisher_object)
        def on_publish(cls, *args, **kwargs) -> None:
            nonlocal called
            called += 1
            assert called == 1
            arguments = args, kwargs
            assert arguments == expected_arguments
            assert cls is Cls
            if exception_cls:
                raise exception_cls(arguments)


    return Cls


def subscriber_class_classmethod_under(publisher_object, exception_cls, expected_arguments):
    called = 0

    class Cls:
        @subscribe(publisher_object)
        @classmethod
        def on_publish(cls, *args, **kwargs) -> None:
            nonlocal called
            called += 1
            assert called == 1
            arguments = args, kwargs
            assert arguments == expected_arguments
            assert cls is Cls
            if exception_cls:
                raise exception_cls(arguments)


    return Cls


def subscriber_multiple_functions_same_behavior(publisher_object, exception_cls, expected_arguments):
    called_1 = 0

    @subscribe(publisher_object)
    def on_publish_1(*args, **kwargs) -> None:
        nonlocal called_1
        called_1 += 1
        assert called_1 == 1
        arguments = args, kwargs
        assert arguments == expected_arguments
        if exception_cls:
            raise exception_cls(arguments)

    called_2 = 0

    @subscribe(publisher_object)
    def on_publish_2(*args, **kwargs) -> None:
        nonlocal called_2
        called_2 += 1
        assert called_2 == 1
        arguments = args, kwargs
        assert arguments == expected_arguments
        if exception_cls:
            raise exception_cls(arguments)


    return on_publish_1, on_publish_2


def subscriber_multiple_functions_different_behavior(publisher_object, exception_cls, expected_arguments):
    called_1 = 0

    @subscribe(publisher_object)
    def on_publish_1(*args, **kwargs) -> None:
        nonlocal called_1
        called_1 += 1
        assert called_1 == 1
        arguments = args, kwargs
        assert arguments == expected_arguments
        if exception_cls:
            raise exception_cls(arguments)

    called_2 = 0

    @subscribe(publisher_object)
    def on_publish_2(*args, **kwargs) -> None:
        nonlocal called_2
        called_2 += 1
        assert called_2 == 1
        arguments = args, kwargs
        assert arguments == expected_arguments

    return on_publish_1, on_publish_2


def subscriber_multiple_method_same_behavior(publisher_object, exception_cls, expected_arguments):
    called_1 = 0
    called_2 = 0

    class Cls:
        @subscribe(publisher_object)
        def on_publish_1(self, *args, **kwargs) -> None:
            nonlocal called_1
            called_1 += 1
            assert called_1 == 1
            arguments = args, kwargs
            assert arguments == expected_arguments
            assert isinstance(self, Cls)
            if exception_cls:
                raise exception_cls(arguments)


        @subscribe(publisher_object)
        def on_publish_2(self, *args, **kwargs) -> None:
            nonlocal called_2
            called_2 += 1
            assert called_2 == 1
            arguments = args, kwargs
            assert isinstance(self, Cls)
            if exception_cls:
                raise exception_cls(arguments)


    obj = Cls()
    return obj


def subscriber_multiple_method_different_behavior(publisher_object, exception_cls, expected_arguments):
    called_1 = 0
    called_2 = 0

    class Cls:
        @subscribe(publisher_object)
        def on_publish_1(self, *args, **kwargs) -> None:
            nonlocal called_1
            called_1 += 1
            assert called_1 == 1
            arguments = args, kwargs
            assert arguments == expected_arguments
            if exception_cls:
                raise exception_cls(arguments)


        @subscribe(publisher_object)
        def on_publish_2(self, *args, **kwargs) -> None:
            nonlocal called_2
            called_2 += 1
            assert called_2 == 1
            arguments = args, kwargs
            assert arguments == expected_arguments


    obj = Cls()
    return obj