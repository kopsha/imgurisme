"""Another attempt to access dictionary keys like attribures"""


class ImmutableData(dict):
    """Read only dictionary using attributes"""

    def __getattr__(self, attr):
        value = self[attr]
        return self.__class__(value) if isinstance(value, dict) else value

    def __hash__(self):
        return id(self)

    def _immutable_error(self, *args, **kws):
        raise TypeError("Cannot modify immutable data")

    __delete__ = _immutable_error
    __setattr__ = _immutable_error
    __setitem__ = _immutable_error
    __delitem__ = _immutable_error
    clear = _immutable_error
    update = _immutable_error
    setdefault = _immutable_error
    pop = _immutable_error
    popitem = _immutable_error
