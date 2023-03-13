import os
import importlib
from pathlib import Path

import django
from django.test import TestCase, Client

from xml_converter.logic import xml_to_dict
from xml_converter.exceptions import InvalidXMLSyntax

TEST_DIR = Path(__file__).parent / Path('test_files')


class DjangoTestCase(TestCase):
    """ Additional test case to run specific tests with command python -m unittest -k ..."""

    def setUp(self):
        django.setup()
        os.environ['DJANGO_SETTINGS_MODULE'] = 'exercise.tests_settings'


class XMLConversionTestCase(DjangoTestCase):

    def setUp(self):
        super().setUp()
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

    # Cases test: invalid-syntax.xml
    def test_logic_xml2dict_convert_invalid_syntax_document(self):
        with (TEST_DIR / Path('invalid-syntax.xml')).open() as fp:
            with self.assertRaises(InvalidXMLSyntax) as context:
                xml_to_dict(fp.read())
            self.assertTrue('mismatched tag: line 5, column 2' in context.exception)

    def test_connected_convert_invalid_syntax_document(self):
        with (TEST_DIR / Path('invalid-syntax.xml')).open() as fp:
            response = self.client.post('/connected/', {
                'file': fp,
            })
            self.assertEqual(response.status_code, 422)
            self.assertEqual(response.json(), {
                "parse_status": "error",
                "parse_message": "mismatched tag: line 5, column 2"
            })

    def test_api_convert_invalid_syntax_document(self):
        with (TEST_DIR / Path('invalid-syntax.xml')).open() as fp:
            response = self.client.post('/api/converter/convert/', {
                'file': fp,
            })
            self.assertEqual(response.status_code, 422)
            self.assertEqual(response.json(), {
                "parse_status": "error",
                "parse_message": "mismatched tag: line 5, column 2"
            })

    # Cases test: missing-root.xml
    def test_logic_xml2dict_convert_missing_root_document(self):
        with (TEST_DIR / Path('missing-root.xml')).open() as fp:
            with self.assertRaises(InvalidXMLSyntax) as context:
                xml_to_dict(fp.read())
            self.assertTrue('no element found: line 2, column 0' in context.exception)

    def test_connected_convert_missing_root_document(self):
        with (TEST_DIR / Path('missing-root.xml')).open() as fp:
            response = self.client.post('/connected/', {
                'file': fp,
            })
            self.assertEqual(response.status_code, 422)
            self.assertEqual(response.json(), {
                "parse_status": "error",
                "parse_message": "no element found: line 2, column 0"
            })

    def test_api_convert_missing_root_document(self):
        with (TEST_DIR / Path('missing-root.xml')).open() as fp:
            response = self.client.post('/api/converter/convert/', {
                'file': fp,
            })
            self.assertEqual(response.status_code, 422)
            self.assertEqual(response.json(), {
                "parse_status": "error",
                "parse_message": "no element found: line 2, column 0"
            })

    # Cases test: zero-bytes.xml
    def test_logic_xml2dict_convert_zero_bytes_document(self):
        with (TEST_DIR / Path('zero-bytes.xml')).open() as fp:
            with self.assertRaises(InvalidXMLSyntax) as context:
                xml_to_dict(fp.read())
            self.assertTrue('no element found: line 1, column 0' in context.exception)

    def test_connected_convert_zero_bytes_document(self):
        with (TEST_DIR / Path('zero-bytes.xml')).open() as fp:
            response = self.client.post('/connected/', {
                'file': fp,
            })
            self.assertEqual(response.status_code, 422)
            self.assertEqual(response.json(), {
                "parse_status": "error",
                "parse_message": "no element found: line 1, column 0"
            })

    def test_api_convert_zero_bytes_document(self):
        with (TEST_DIR / Path('zero-bytes.xml')).open() as fp:
            response = self.client.post('/api/converter/convert/', {
                'file': fp,
            })
            self.assertEqual(response.status_code, 422)
            self.assertEqual(response.json(), {
                "parse_status": "error",
                "parse_message": "no element found: line 1, column 0"
            })
