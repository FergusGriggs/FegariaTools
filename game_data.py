# XML imports
import xmltodict
from collections import OrderedDict


tile_data = None
item_data = None


# Tile data
def load_tile_data():
    global tile_data
    read_file = open("res/data/tile_data.xml", "r")
    tile_data = xmltodict.parse(read_file.read())
    read_file.close()


def unload_tile_data():
    global tile_data
    tile_data = None


def save_tile_data():
    write_file = open("res/data/tile_data.xml", "w")
    unparsed_data = xmltodict.unparse(tile_data, pretty=True)
    write_file.write(unparsed_data)
    write_file.close()


# Item data
def load_item_data():
    global item_data
    read_file = open("res/data/item_data.xml", "r")
    item_data = xmltodict.parse(read_file.read())
    read_file.close()


def unload_item_data():
    global item_data
    item_data = None


def save_item_data():
    write_file = open("res/data/item_data.xml", "w")
    unparsed_data = xmltodict.unparse(item_data, pretty=True)
    write_file.write(unparsed_data)
    write_file.close()


def find_element_by_attribute(elements, attribute_name, attribute_value):
    for element in elements:
        for attribute in element:
            if attribute == attribute_name and element[attribute] == attribute_value:
                return element


def edit_test():
    global tile_data
    for element in tile_data["elements"]["element"]:
        for attribute in element:
            print(attribute + ": ", element[attribute])

    tile_data["elements"]["element"].append(OrderedDict([("@id", 4), ("@name", "Grass"), ("@strength", 1)]))

