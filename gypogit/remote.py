from six import string_types

from .go_object import GoObject
from .common import AuthMethod, GitUploadPackInfo, GitUploadPackRequest, \
    Capabilities
from .std import ReadCloser, StringMap


class Remote(GoObject):
    @classmethod
    def New(cls, url):
        assert isinstance(url, string_types)
        go_url, c_url = cls._string(url)
        handle = cls._checked(cls.lib.c_NewRemote(go_url))
        remote = Remote(handle)
        remote._deps[go_url] = c_url
        return remote

    @classmethod
    def NewAuthenticated(cls, url, auth):
        assert isinstance(url, string_types)
        assert auth is None or isinstance(auth, AuthMethod)
        go_url, c_url = cls._string(url)
        handle = cls._checked(cls.lib.c_NewAuthenticatedRemote(
            go_url, auth.handle))
        remote = Remote(handle)
        remote._deps[go_url] = c_url
        return remote

    @property
    def Endpoint(self):
        return self._string(self.lib.c_Remote_get_Endpoint(self.handle))

    @Endpoint.setter
    def Endpoint(self, value):
        assert isinstance(value, string_types)
        self.lib.c_Remote_set_Endpoint(self.handle, self._string(value, self))

    @property
    def Auth(self):
        return AuthMethod(self.lib.c_Remote_get_Auth(self.handle))

    @Auth.setter
    def Auth(self, value):
        assert isinstance(value, AuthMethod)
        return self.lib.c_Remote_set_Auth(self.handle, value.handle)

    def Connect(self):
        self._checked(self.lib.c_Remote_Connect)

    def Info(self):
        return GitUploadPackInfo(self.lib.c_Remote_Info(self.handle))

    def Capabilities(self):
        return Capabilities(self.lib.c_Remote_Capabilities(self.handle))

    def DefaultBranch(self):
        return self._string(self.lib.c_Remote_DefaultBranch(self.handle))

    def Head(self):
        return self._bytes(self._checked(self.lib.c_Remote_Head(self.handle),
                                         size=20))

    def Fetch(self, request):
        assert isinstance(request, GitUploadPackRequest)
        return ReadCloser(self._checked(self.lib.c_Remote_Fetch(
            self.handle, request.handle)))

    def FetchDefaultBranch(self):
        return ReadCloser(self._checked(self.lib.c_Remote_FetchDefaultBranch(
            self.handle)))

    def Ref(self, name):
        return self._bytes(self._checked(self.lib.c_Remote_Ref(
            self.handle, self._string(name, self))), size=20)

    def Refs(self):
        mh = self.lib.c_Remote_Refs(self.handle)
        keys = self._string_slice(self.lib.c_std_map_keys_str(mh))
        refs = {k: self._bytes(self.lib.c_std_map_get_str_str(
            mh, self._string(k, self)), size=20) for k in keys}
        self.lib.c_dispose(mh)
        return refs

    def __getitem__(self, item):
        return self.Ref(item)
