"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.core.handlers.base import BaseHandler
from django.test import TestCase
from django.test.client import Client, RequestFactory

from feature import Feature

# via https://gist.github.com/925270
# Necessary because Django's request object has no sessions unless you run it through middleware
class RequestMock(RequestFactory):
    def request(self, **request):
        "Construct a generic request object."
        request = RequestFactory.request(self, **request)
        handler = BaseHandler()
        handler.load_middleware()
        for middleware_method in handler._request_middleware:
            if middleware_method(request):
                raise Exception("Couldn't create request mock object - "
                                "request middleware returned a response")
        return request

def fake_request():
    return RequestMock().get("/")

class TestFeatureAPI(TestCase):
    def setUp(self):
        self.feature = Feature("test_feature")

    def test_features_disabled_by_default(self):
        self.assertFalse(self.feature.is_enabled(fake_request()))

    def test_can_enable_features(self):
        request = fake_request()
        self.feature.enable(request)
        self.assertTrue(self.feature.is_enabled(request))

    def test_can_disable_features(self):
        request = fake_request()
        self.feature.enable(request)

        self.feature.disable(request)
        self.assertFalse(self.feature.is_enabled(request))

    def test_can_enable_two_features(self):
        feature2 = Feature("second_test_feature")
        request = fake_request()

        self.feature.enable(request)
        feature2.enable(request)

        self.assertTrue(self.feature.is_enabled(request))
        self.assertTrue(feature2.is_enabled(request))

class TestFeatureGUI(TestCase):
    def setUp(self):
        self.feature = Feature("test_feature")
        self.client = Client()

    def test_feature_disabled_by_default(self):
        response = self.client.get("/feature/")
        self.assertContains(response, "test_feature: Disabled")

    def test_can_enabled_features(self):
        self.client.post("/feature/set_enabled", {'name': self.feature.name, 'enabled': 'True'})

        response = self.client.get("/feature/")
        self.assertContains(response, "test_feature: Enabled")

    def test_can_disable_enabled_features(self):
        self.client.post("/feature/set_enabled", {'name': self.feature.name, 'enabled': 'True'})
        self.client.post("/feature/set_enabled", {'name': self.feature.name, 'enabled': 'False'})

        response = self.client.get("/feature/")
        self.assertContains(response, "test_feature: Disabled")
