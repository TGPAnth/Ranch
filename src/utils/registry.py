__all__ = ('get_registry', )


class Registry(object):
    """Global registry"""

__registry = Registry()


def get_registry():
    return __registry

def create_registry():
    return type('registry', (), {})()
