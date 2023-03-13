import importlib
from pathlib import Path

from django.test import TestCase, Client

from xml_converter.logic import xml_to_dict

TEST_DIR = Path(__file__).parent / Path('test_files')


class XMLConversionTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    # Cases test: empty.xml
    def test_logic_xml2dict_convert_empty_document(self):
        with (TEST_DIR / Path('empty.xml')).open() as fp:
            file_content = fp.read()
            response = xml_to_dict(file_content)
            self.assertEqual(response, {
                "Root": "",
            })

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

    # Cases test: addresses.xml
    def test_logic_xml2dict_convert_addresses(self):
        with (TEST_DIR / Path('addresses.xml')).open() as fp:
            file_content = fp.read()
            response = xml_to_dict(file_content)
            self.assertEqual(response, {
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

    def test_api_convert_addresses(self):
        with (TEST_DIR / Path('addresses.xml')).open() as fp:
            response = self.client.post('/api/converter/convert/', {
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

    # Cases test: ignore-attributes.xml
    def test_logic_xml2dict_convert_ignore_attributes_document(self):
        with (TEST_DIR / Path('ignore-attributes.xml')).open() as fp:
            file_content = fp.read()
            response = xml_to_dict(file_content)
            self.assertEqual(response, {
                "Root": [
                    {
                        "MyDocument": {
                            "Has": "an element",
                            "And": {
                                "SecondElement": "as well"
                            }
                        }
                    }
                ]
            })

    def test_connected_convert_ignore_attributes_document(self):
        with (TEST_DIR / Path('ignore-attributes.xml')).open() as fp:
            response = self.client.post('/connected/', {
                'file': fp,
            })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {
                "Root": [
                    {
                        "MyDocument": {
                            "Has": "an element",
                            "And": {
                                "SecondElement": "as well"
                            }
                        }
                    }
                ]
            })

    def test_api_convert_ignore_attributes_document(self):
        with (TEST_DIR / Path('ignore-attributes.xml')).open() as fp:
            response = self.client.post('/api/converter/convert/', {
                'file': fp,
            })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {
                "Root": [
                    {
                        "MyDocument": {
                            "Has": "an element",
                            "And": {
                                "SecondElement": "as well"
                            }
                        }
                    }
                ]
            })
