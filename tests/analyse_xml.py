import os
import re
import xmlschema

from xml.etree import ElementTree


def fetch_schema(
    schema_source: str = "http://www.siri.org.uk/schema/2.0/xsd/siri.xsd",
    schema_dir: str = "my_schemas",
) -> xmlschema.XMLSchema:
    """
    Fetches the schema to compare against. It tries to find it locally but downloads it if
    necessary.

    Args:
        schema_source (str): URL to load schema from
        schema_dir (str): Local directory to save schema to

    Returns: XML Schema
    """
    schema_name = schema_source.split("/")[-1]
    schema_path = os.path.join(schema_dir, schema_name)
    try:
        return xmlschema.XMLSchema(schema_path)
    except xmlschema.exceptions.XMLResourceOSError:
        schema = xmlschema.XMLSchema(schema_source)
        schema.export(target=schema_dir, save_remote=True)
        return schema


def validate_xml(
    xml_str: str, schema: xmlschema.XMLSchema | None = None, **kwargs
) -> bool:
    """
    Validates XML against a schema

    Args:
        xml_str (str): XML string to validate
        schema (xmlschema.XML, optional): XML schema to validate against, if none is provided, a new one is created.
        kwargs: Arguments to pass to `fetch_schema`

    Returns: Whether XML is valid
    """
    if not schema:
        schema = fetch_schema(**kwargs)
    if xml_str == "":
        return False
    try:
        schema.validate(xml_str)
    except xmlschema.validators.exceptions.XMLSchemaValidationError:
        return False
    except xmlschema.exceptions.XMLResourceParseError:
        return False

    return True


def generate_structure(tree: ElementTree, structure: dict):
    """
    Recursive function which searches through the `tree` and updates the structure
    dictionary with each nodes tag, its child, and counts the number of occurrences of each tag.

    :param tree: Input tree structure containing genuine information.
    :param structure: Dictionary containing
    """
    tag = re.sub(r"{.+}", r"", tree.tag)

    if tag not in structure:
        structure[tag] = {"count": 1}
    else:
        structure[tag]["count"] += 1

    for child in tree:
        generate_structure(child, structure[tag])


def get_structure(tree: ElementTree) -> dict:
    """
    Obtain the structure of an element tree in the form of a dictionary where repeated fields are counted.

    :param tree: Input tree for analysis

    :return: The structure dictionary detailing the connections in the tree.
    """
    structure = {}
    generate_structure(tree, structure)

    return structure


def field_count(structure: dict, result: dict[str, int]):
    """
    Function which recursively searches the `structure` dictionary and counts the occurrences
    of keys storing results in the `result` dictionary.

    :param structure: Dictionary describing the structure of a tree.
    :param result: Variable dictionary counting occurrences of keys in embedded dictionary.
    """
    for k in structure.keys():
        if k == "count":
            continue

        count = structure[k]["count"]

        if k not in result.keys():
            result[k] = count
        field_count(structure[k], result)


def count_fields(structure: dict) -> dict[str, int]:
    """
    Count the occurrences of each field in the dictionary `structure`

    :param structure: A multi-layer dictionary describing the structure of an XML file.

    :return: The result of the field count.
    """
    result = {}
    field_count(structure, result)

    return result


def analyse_response(response_string: str, **kwargs) -> dict[str, int]:
    """
    Sort an XML string into an element tree, obtain the structure of the tree
    sorted into a single dictionary counting the number of occurrences of each node.

    :param response_string: XML file as a string

    :return: Dictionary counting occurrences of each key in `response_string`
    """
    valid = validate_xml(response_string, **kwargs)
    if not valid:
        raise ValueError("XML is not valid")
    root = ElementTree.fromstring(response_string)

    structure = get_structure(root)

    return count_fields(structure)
