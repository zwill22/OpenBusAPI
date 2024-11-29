import re
from xml.etree import ElementTree

admin_fields = (
    "ServiceDelivery",
    "ResponseTimestamp",
    "ProducerRef",
    "VehicleMonitoringDelivery",
    "ResponseTimestamp",
    "RequestMessageRef",
    "ValidUntil",
    "ShortestPossibleCycle"
)


def generate_structure(tree: ElementTree, structure: dict):
    """
    Recursive function which searches through the `tree` and updates the structure dictionary with each nodes tag, its
    child, and counts the number of occurrences of each tag.

    :param tree: Input tree structure containing genuine information.
    :param structure: Dictionary containing
    :return:
    """
    tag = re.sub(r'{.+}', r'', tree.tag)

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


def print_structure(tree: dict, depth: int = 0):
    """
    Function which prints a tree structure recursively.

    :param tree: Multi-layer dictionary (tree-structure)
    :param depth: Level of recursion
    """
    tab = depth * '\t'
    depth += 1
    for k in tree.keys():
        if k == "count":
            continue
        try:
            print(tab, k, tree[k]["count"])
            print_structure(tree[k], depth=depth)
        except AttributeError:
            pass
    depth -= 1


def field_count(structure: dict, result: dict[str, int]):
    """
    Function which recursively searches the `structure` dictionary and counts the occurrences of keys storing results in
    the `result` dictionary.

    :param structure: Dictionary describing the structure of a tree.
    :param result: Variable dictionary counting occurrences of keys in embedded dictionary.
    """
    for k in structure.keys():
        if k == "count":
            continue
        try:
            count = structure[k]["count"]
        except AttributeError:
            continue
        if k not in result.keys():
            result[k] = count
        elif k == "ResponseTimestamp":
            if result[k] != 1 or count != 1:
                raise ValueError("Multiple response timestamps")
        else:
            raise ValueError("Repeated values in result: {}".format(k))
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

def sort_string(response_string: str = None, verbose: bool = False, **kwargs) -> dict[str, int]:
    """
    Sort an XML string into an element tree, obtain the structure of the tree and then sort this into a single
    dictionary counting the number of occurrences of each node.

    :param response_string: XML file as a string
    :param verbose: Print additional information

    :return: Dictionary counting occurrences of each key in `response_string`
    """

    if verbose:
        print("Loading file to element tree")
    root = ElementTree.fromstring(response_string)

    structure = get_structure(root)
    if verbose:
        print_structure(structure)
    return count_fields(structure)


def analyse_result(result: dict[str, int]):
    """
    Sort through a results dictionary contains the number of occurrences of each field in the XML file and checking
    this against the expected frequency of each field.

    :param result: Dictionary where the values are the number of occurrences of each key.
    """
    n_vehicles = 0
    for field, count in result.items():
        if field == "Siri":
            if count < 1:
                raise ValueError("No result")
            elif count > 1:
                raise ValueError("Response contains multiple results")
        elif field in admin_fields:
            assert count > 0
            if count != 1:
                raise ValueError("Multiple entries ({0}) for field {1}".format(count, field))
        elif field == "VehicleActivity":
            n_vehicles = count
            print("Result contains data on {} buses".format(n_vehicles))
            print()
        else:
            if count < n_vehicles:
                print("Only {0:2d} results for field {1}".format(count, field))
            elif count > n_vehicles:
                raise ValueError("Too many results for field {0}: {1}".format(field, count))


def analyse_response(**kwargs):
    """
    Sort the string into a dictionary counting the occurrences of each field and analyse the results to check that they
    are consistent with the expected structure of the XML file.
    """
    result = sort_string(**kwargs)
    analyse_result(result)


def load_file(filename: str) -> str:
    """
    Load file `filename` to string

    :param filename: File to load
    :return: File contents as string
    """
    with open(filename, 'r') as f:
        content = f.read()

    return content


def main(file: str = None, **kwargs):
    """
    Analyse XML `file` checking whether it meets the specifications for the OpenBusLocationAPI

    :param file: path to xml file
    :param kwargs:
    """
    response_string = load_file(file)
    analyse_response(response_string, **kwargs)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="File containing api response")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")

    main(**vars(parser.parse_args()))