import xmlschema


def fetch_schema():
    try:
        return xmlschema.XMLSchema("schemas/siri.xsd")
    except xmlschema.exceptions.XMLResourceOSError:
        schema = xmlschema.XMLSchema("http://www.siri.org.uk/schema/2.0/xsd/siri.xsd")
        schema.export(target="my_schemas", save_remote=True)
        return schema


def validate_xml(xml_str: str, schema=None, **kwargs):
    if not schema:
        schema = fetch_schema()
    schema.validate(xml_str)

    return True
