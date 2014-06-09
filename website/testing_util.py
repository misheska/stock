import platform

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from django.test import LiveServerTestCase

class SeleniumTestCase(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        super(SeleniumTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(SeleniumTestCase, cls).tearDownClass()

    def wait_for(self, method, *args, **kwargs):
        wait_for = lambda _: method(*args, **kwargs)
        return WebDriverWait(None, 10).until(wait_for)


def monkeypatch_wsgiref_on_windows():
    """
    On windows Django live test cases have the bad habbit of spewing Error 10045 into the console.
    This monkeypatch makes wsgiref's server (used in live test cases) handle 10045 properly.
    """
    if platform.system() != "Windows":
        return

    import socket
    from wsgiref.simple_server import ServerHandler, WSGIRequestHandler

    def monkeypatch_handle(self):
        """Handle a single HTTP request"""

        try:
            self.raw_requestline = self.rfile.readline()
        except socket.error, err:
            if err.errno == 10054:
                return
            else:
                raise

        if not self.parse_request(): # An error code has been sent, just exit
            return

        handler = ServerHandler(
            self.rfile, self.wfile, self.get_stderr(), self.get_environ()
        )
        handler.request_handler = self      # backpointer for logging
        handler.run(self.server.get_app())

    WSGIRequestHandler.handle = monkeypatch_handle

monkeypatch_wsgiref_on_windows()
