import os.path

import xmlschema


def fetch_schema(
    schema_source="http://www.siri.org.uk/schema/2.0/xsd/siri.xsd",
    schema_dir="my_schemas",
) -> xmlschema.XMLSchema:
    """
    Fetches the schema to compare against. It tries to find it locally but downloads it if
    necessary.

    Args:
        schema_source: URL to load schema from
        schema_dir: Local to save schema to

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


def validate_xml(xml_str: str, schema=None, **kwargs) -> bool:
    """
    Validates XML against a schema

    Args:
        xml_str: XML string to validate
        schema: XML schema to validate against, if none is provided, a new one is created.
        **kwargs: Arguments to pass to `fetch_schema`

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
