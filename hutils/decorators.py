# -*- coding: utf-8 -*-
import contextlib
import functools
from typing import Callable, Union

from hutils import log_error


def obj_cache(key):
    """ 使用对象的属性来充当方法缓存。use object attribute as cache.

    Examples::

        class A:
            @obj_cache('_value')
            def get_value(self, *args):
                ...

    :type key: str
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(obj, *args, **kwargs):
            if hasattr(obj, key):
                return getattr(obj, key)
            value = func(obj, *args, **kwargs)
            setattr(obj, key, value)
            return value

        return wrapper

    return decorator


@contextlib.contextmanager
def catches(*exceptions, raises: Union[BaseException, Callable[[Exception], BaseException]], log=False, logger=None):
    """ 封装转换错误类。transfer exceptions to a different type.

    Examples::

        with self.assertRaises(IOError), catches(ValueError, TypeError, raises=IOError()):
            raise ValueError('should wrap this error')

        @catches(raises=get_validation_error, log=True)
        def raise_io_error():
            raise ValueError('should wrap this error')
    """
    exceptions = exceptions or (Exception,)
    try:
        yield
    except exceptions as ex:
        if callable(raises):
            raises = raises(ex)
        if log:
            log_error(logger or __name__, raises)
        raise raises from ex