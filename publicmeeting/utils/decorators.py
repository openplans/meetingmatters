# http://djangosnippets.org/snippets/2495/
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


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
    if cls is not None:
        # Check that the View class is a class-based view. This can either be
        # done by checking inheritance from django.views.generic.View, or by
        # checking that the ViewClass has a ``dispatch`` method.
        if not hasattr(cls, 'dispatch'):
            raise TypeError(('View class is not valid: %r.  Class-based views '
                             'must have a dispatch method.') % cls)

        original = cls.dispatch
        modified = method_decorator(login_required(**login_args))(original)
        cls.dispatch = modified

        return cls

    else:
        # If ViewClass is None, then this was applied as a decorator with
        # parameters. An inner decorator will be used to capture the ViewClass,
        # and return the actual decorator method.
        def inner_decorator(inner_cls):
            return LoginRequired(inner_cls, **login_args)

        return inner_decorator
