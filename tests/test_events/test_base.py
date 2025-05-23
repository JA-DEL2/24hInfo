from unittest import TestCase
from fastapi.testclient import TestClient
from _24hi25back.app.application import create_application


class TestBaseEventHandler(TestCase):
    def test_startup_handler(self):
        app = create_application()
        with self.assertLogs('_24hi25back', level='INFO') as cm:

            with TestClient(app):
                pass
            self.assertEqual(cm.output,
                             ['INFO:_24hi25back:Starting up ...',
                              'INFO:_24hi25back:Shutting down ...'])
