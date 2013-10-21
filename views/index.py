from common.base_request_handler import BaseRequestHandler


class IndexHandler(BaseRequestHandler):
    """
    Render main page.
    """
    def get(self):
        self.render('index.html')