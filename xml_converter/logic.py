import xmltodict

import xml.etree.ElementTree as ET, re


def xml_to_dict(xml_content):
    root_element = ET.fromstring(xml_content)
    response_dict = {root_element.tag: {} if root_element.attrib else ""}
    return response_dict
