import xml.etree.ElementTree as ET


def lxml_element_to_dict(root_element):
    response_dict = {root_element.tag: {}}

    # iter sub elements on recursion
    found_children_elements = list(root_element)
    if found_children_elements:
        response_dict[root_element.tag] = [lxml_element_to_dict(children_element)
                                           for children_element in found_children_elements]

    # add final text
    else:
        found_text = root_element.text.strip() if root_element.text else ""
        response_dict[root_element.tag] = found_text

    return response_dict


def xml_to_dict(xml_content):
    root_element = ET.fromstring(xml_content)
    return lxml_element_to_dict(root_element)
