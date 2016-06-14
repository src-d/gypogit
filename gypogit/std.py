from six import string_types

from .go_object import GoObject


class StringMap(GoObject):
    def dict(self, cls):
        return {k: cls(self[k]) for k in self.keys()}

    def __len__(self):
        return self.lib.c_std_map_len(self.handle)

    def keys(self):
        return self._string_slice(self.lib.c_std_map_keys_str(self.handle))

    def __getitem__(self, item):
        assert isinstance(item, string_types)
        go_key = self._string(item, self)
        return self.lib.c_std_map_get_str_obj(self.handle, go_key)

    def __delitem__(self, key):
        self.lib.c_std_map_set_str(
            self.handle, self._string(key, self), self.INVALID_HANDLE)

    def __setitem__(self, key, value):
        self.lib.c_std_map_set_str(
            self.handle, self._string(key, self), value.handle)


class TypedStringMap(StringMap):
    def __init__(self, handle, cls):
        super(TypedStringMap, self).__init__(handle)
        self.cls = cls

    def dict(self):
        return {k: self[k] for k in self.keys()}

    def __getitem__(self, item):
        assert isinstance(item, string_types)
        go_key = self._string(item, self)
        return self.cls(self.lib.c_std_map_get_str_obj(self.handle, go_key))


class ReadCloser(GoObject):
    pass
