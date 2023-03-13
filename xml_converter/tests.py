from pathlib import Path

from django.test import TestCase, Client


TEST_DIR = Path(__file__).parent / Path('test_files')


class XMLConversionTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_connected_convert_empty_document(self):
        with (TEST_DIR / Path('empty.xml')).open() as fp:
            response = self.client.post('/connected/', {
                'file': fp,
            })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {
                "Root": "",
            })

    def test_api_convert_empty_document(self):
        with (TEST_DIR / Path('empty.xml')).open() as fp:
            response = self.client.post('/api/converter/convert/', {
                'file': fp,
            })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {
                "Root": "",
            })

    def test_connected_convert_addresses(self):
        with (TEST_DIR / Path('addresses.xml')).open() as fp:
            response = self.client.post('/connected/', {
                'file': fp,
            })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {
                "Root": [
                    {
                        "Address": [
                            {"StreetLine1": "123 Main St."},
                            {"StreetLine2": "Suite 400"},
                            {"City": "San Francisco"},
                            {"State": "CA"},
                            {"PostCode": "94103"},
                        ]
                    },
                    {
                        "Address": [
                            {"StreetLine1": "400 Market St."},
                            {"City": "San Francisco"},
                            {"State": "CA"},
                            {"PostCode": "94108"},
                        ]
                    },
                ],
            })
