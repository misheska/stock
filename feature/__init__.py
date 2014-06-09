
class Feature(object):
    features = set()

    def __init__(self, name):
        assert isinstance(name, (str, unicode))
        self.name = str(name)
        self.features.add(name)

    @property
    def session_key(self):
        return "feature_" + self.name

    def is_enabled(self, request):
        return bool(request.session.get(self.session_key, False))

    def enable(self, request):
        request.session[self.session_key] = True

    def disable(self, request):
        request.session[self.session_key] = False