# XML imports
import xmltodict
from collections import OrderedDict


def test_xml():
    read_file = open("test.xml", "r")
    data = xmltodict.parse(read_file.read())
    read_file.close()

    for element in data["elements"]["element"]:
        for attribute in element:
            print(attribute + ": ", element[attribute])

    data["elements"]["element"].append(OrderedDict([("@id", 4), ("@name", "Grass"), ("@strength", 1)]))

    write_file = open("test2.xml", "w")
    unparsed_data = xmltodict.unparse(data, pretty=True)
    write_file.write(unparsed_data)
    write_file.close()