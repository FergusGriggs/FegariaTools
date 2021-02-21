# XML imports
import xmltodict
from collections import OrderedDict


tile_data = None
item_data = None
sound_data = None
loot_data = None
structure_data = None
ai_data = None
crafting_data = None
entity_data = None
world_gen_data = None

item_id_strs = []
tile_id_strs = []
sound_id_strs = []
loot_id_strs = []
structure_id_strs = []
ai_id_strs = []
crafting_id_strs = []
entity_id_strs = []
world_gen_id_strs = []


# Tile data
def update_tile_id_strs():
    global tile_id_strs
    tile_id_strs.clear()
    for entry in tile_data["tiles"]["tile"]:
        tile_id_strs.append(entry["@id_str"])


def load_tile_data():
    global tile_data
    read_file = open("res/data/tile_data.xml", "r")
    tile_data = xmltodict.parse(read_file.read())
    read_file.close()

    update_tile_id_strs()


def save_tile_data():
    write_file = open("res/data/tile_data.xml", "w")
    unparsed_data = xmltodict.unparse(tile_data, pretty=True)
    write_file.write(unparsed_data)
    write_file.close()

    update_tile_id_strs()


def unload_tile_data():
    global tile_data
    tile_data = None


# Item data
def update_item_id_strs():
    global item_id_strs
    item_id_strs.clear()
    for entry in item_data["items"]["item"]:
        item_id_strs.append(entry["@id_str"])


def load_item_data():
    global item_data
    read_file = open("res/data/item_data.xml", "r")
    item_data = xmltodict.parse(read_file.read())
    read_file.close()

    update_item_id_strs()


def save_item_data():
    write_file = open("res/data/item_data.xml", "w")
    unparsed_data = xmltodict.unparse(item_data, pretty=True)
    write_file.write(unparsed_data)
    write_file.close()

    update_item_id_strs()


def unload_item_data():
    global item_data
    item_data = None


# Sound data
def update_sound_id_strs():
    global sound_id_strs
    sound_id_strs.clear()
    for entry in sound_data["sounds"]["sound"]:
        sound_id_strs.append(entry["@id_str"])


def load_sound_data():
    global sound_data
    read_file = open("res/data/sound_data.xml", "r")
    sound_data = xmltodict.parse(read_file.read())
    read_file.close()

    update_sound_id_strs()


def save_sound_data():
    write_file = open("res/data/sound_data.xml", "w")
    unparsed_data = xmltodict.unparse(sound_data, pretty=True)
    write_file.write(unparsed_data)
    write_file.close()

    update_sound_id_strs()


def unload_sound_data():
    global sound_data
    sound_data = None


# Loot data
def update_loot_id_strs():
    global loot_id_strs
    loot_id_strs.clear()
    for entry in loot_data["lootgroups"]["loot"]:
        loot_id_strs.append(entry["@id_str"])


def load_loot_data():
    global loot_data
    read_file = open("res/data/loot_data.xml", "r")
    loot_data = xmltodict.parse(read_file.read())
    read_file.close()

    update_loot_id_strs()


def save_loot_data():
    write_file = open("res/data/loot_data.xml", "w")
    unparsed_data = xmltodict.unparse(loot_data, pretty=True)
    write_file.write(unparsed_data)
    write_file.close()

    update_loot_id_strs()


def unload_loot_data():
    global loot_data
    loot_data = None


# Structure data
def update_structure_id_strs():
    global structure_id_strs
    structure_id_strs.clear()
    for entry in structure_data["structures"]["structure"]:
        structure_id_strs.append(entry["@id_str"])


def load_structure_data():
    global structure_data
    read_file = open("res/data/structure_data.xml", "r")
    structure_data = xmltodict.parse(read_file.read())
    read_file.close()

    update_structure_id_strs()


def save_structure_data():
    write_file = open("res/data/structure_data.xml", "w")
    unparsed_data = xmltodict.unparse(structure_data, pretty=True)
    write_file.write(unparsed_data)
    write_file.close()

    update_structure_id_strs()


def unload_structure_data():
    global structure_data
    structure_data = None


# Ai
def update_ai_id_strs():
    global ai_id_strs
    ai_id_strs.clear()
    for entry in ai_data["ais"]["ai"]:
        ai_id_strs.append(entry["@id_str"])


def load_ai_data():
    global ai_data
    read_file = open("res/data/ai_data.xml", "r")
    ai_data = xmltodict.parse(read_file.read())
    read_file.close()

    update_ai_id_strs()


def save_ai_data():
    write_file = open("res/data/ai_data.xml", "w")
    unparsed_data = xmltodict.unparse(ai_data, pretty=True)
    write_file.write(unparsed_data)
    write_file.close()

    update_ai_id_strs()


def unload_ai_data():
    global ai_data
    ai_data = None


# Crafting
def update_crafting_id_strs():
    global crafting_id_strs
    crafting_id_strs.clear()
    for entry in crafting_data["crafting_recipes"]["crafting_recipe"]:
        crafting_id_strs.append(entry["@id_str"])


def load_crafting_data():
    global crafting_data
    read_file = open("res/data/crafting_data.xml", "r")
    crafting_data = xmltodict.parse(read_file.read())
    read_file.close()

    update_crafting_id_strs()


def save_crafting_data():
    write_file = open("res/data/crafting_data.xml", "w")
    unparsed_data = xmltodict.unparse(crafting_data, pretty=True)
    write_file.write(unparsed_data)
    write_file.close()

    update_crafting_id_strs()


def unload_crafting_data():
    global crafting_data
    crafting_data = None


# Entity Data
def update_entity_id_strs():
    global entity_id_strs
    entity_id_strs.clear()
    for entry in entity_data["entities"]["entity"]:
        entity_id_strs.append(entry["@id_str"])


def load_entity_data():
    global entity_data
    read_file = open("res/data/entity_data.xml", "r")
    entity_data = xmltodict.parse(read_file.read())
    read_file.close()

    update_entity_id_strs()


def save_entity_data():
    write_file = open("res/data/entity_data.xml", "w")
    unparsed_data = xmltodict.unparse(entity_data, pretty=True)
    write_file.write(unparsed_data)
    write_file.close()

    update_entity_id_strs()


def unload_entity_data():
    global entity_data
    entity_data = None


# World Gen Data
def update_world_gen_id_strs():
    global world_gen_id_strs
    world_gen_id_strs.clear()
    for entry in world_gen_data["world_gens"]["world_gen"]:
        world_gen_id_strs.append(entry["@id_str"])


def load_world_gen_data():
    global world_gen_data
    read_file = open("res/data/world_gen_data.xml", "r")
    world_gen_data = xmltodict.parse(read_file.read())
    read_file.close()

    update_world_gen_id_strs()


def save_world_gen_data():
    write_file = open("res/data/world_gen_data.xml", "w")
    unparsed_data = xmltodict.unparse(world_gen_data, pretty=True)
    write_file.write(unparsed_data)
    write_file.close()

    update_world_gen_id_strs()


def unload_world_gen_data():
    global world_gen_data
    world_gen_data = None


def find_element_by_attribute(elements, attribute_name, attribute_value):
    for element in elements:
        for attribute in element:
            if attribute == attribute_name and element[attribute] == attribute_value:
                return element


def reassign_element_ids(elements):
    correct_id = 0
    for element in elements:
        element["@id"] = str(correct_id)
        correct_id += 1


def remove_element_by_attribute(elements, attribute_name, attribute_value):
    for element in elements:
        for attribute in element:
            if attribute == attribute_name and element[attribute] == attribute_value:
                elements.remove(element)
