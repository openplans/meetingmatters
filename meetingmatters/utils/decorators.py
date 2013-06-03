from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from djpjax import pjax

# http://djangosnippets.org/snippets/2495/
def ClassDecorator(decorator, cls=None, *decorator_args, **decorator_kwargs):
    """
    Apply the ``decorator`` to all the handlers in a class-based view that
    delegate to the ``dispatch`` method.

    """
    if cls is not None:
        # Check that the View class is a class-based view. This can either be
        # done by checking inheritance from django.views.generic.View, or by
        # checking that the ViewClass has a ``dispatch`` method.
        if not hasattr(cls, 'dispatch'):
            raise TypeError(('View class is not valid: %r.  Class-based views '
                             'must have a dispatch method.') % cls)

        original = cls.dispatch
        modified = method_decorator(decorator(*decorator_args, **decorator_kwargs))(original)
        cls.dispatch = modified

        return cls

    else:
        # If ViewClass is None, then this was applied as a decorator with
        # parameters. An inner decorator will be used to capture the ViewClass,
        # and return the actual decorator method.
        def inner_decorator(inner_cls):
            return ClassDecorator(decorator, cls=inner_cls, *decorator_args, **decorator_kwargs)

        return inner_decorator


def Pjax(cls=None, *pjax_args):
    """
    Apply the ``pjax`` decorator to all the handlers in a class-based
    view that delegate to the ``dispatch`` method.
    """
    return ClassDecorator(pjax, cls=cls, *pjax_args)


def LoginRequired(cls=None, **login_args):
    """
    Apply the ``login_required`` decorator to all the handlers in a class-based
    view that delegate to the ``dispatch`` method.

    Optional arguments
    ``redirect_field_name`` -- Default is ``django.contrib.auth.REDIRECT_FIELD_NAME``
    ``login_url`` -- Default is ``None``

    See the documentation for the ``login_required`` [#]_ for more information
    about the keyword arguments.

    Usage:
      @LoginRequired
      class MyListView (ListView):
        ...

    .. [#] https://docs.djangoproject.com/en/dev/topics/auth/#the-login-required-decorator

    """
    return ClassDecorator(login_required, cls=cls, **login_args)
