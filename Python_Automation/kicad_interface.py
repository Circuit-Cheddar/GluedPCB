import skip
import re
import subprocess
import os
import sys
import sexpdata
import json
import pprint

input_settings = {
    "kicad_cli": "C:/Users/user/AppData/Local/Programs/KiCad/10.0/bin/kicad-cli",
    "kicad_project_dir":"C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/ElmerFEM_Test",
    "schematic_path": "C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/ElmerFEM_Test/ElmerFEM Test.kicad_sch",
    "pcb_path": "C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/ElmerFEM_Test/ElmerFEM Test.kicad_pcb",
    "hyp_file": "C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/ElmerFEM_Test/ElmerFEM Test.hyp",
    "info_export": "C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/Python_Automation/kicad_sim_info.json",
    "generate_hyp": True,
    "pin_property_prefix": "CCSIM_"
}


##########################################################
#--------------Hyperlynx Generation----------------------#
##########################################################
def generate_hyperlynx():
    if settings["generate_hyp"]:
        # Unsupported at this time, due to the inability to have python reach its fingers in an do it itself
        # for now the best I can do is check the directory for any hyperlynx file and prompt the user to generate it
        # if the script can't find it. It is so stupid.
        # TODO Write a validator for the hyperlynx file.
        # TODO get a bee up my bonet and implement it in 
        pass

##########################################################
#--------------Hyperlynx Generation----------------------#
##########################################################
import io
import re

## Cleanup AI Generated Code
import re

def parse_sexp_file_to_dict(file_obj):
    """
    Parses a raw S-expression (like a .kicad_pcb file) from a file-like object 
    stream into a structured Python dictionary.
    """
    token_pattern = re.compile(r'\(|\)|"[^"]*"|[^\s()]+')

    def generate_tokens(stream):
        for line in stream:
            clean_line = line.strip()
            if not clean_line:
                continue
            for token in token_pattern.findall(clean_line):
                yield token

    def parse_token(token):
        if token.startswith('"') and token.endswith('"'):
            return token[1:-1]
        if token.lower() in ('true', 't', 'yes'):
            return True
        if token.lower() in ('false', 'nil', 'no'):
            return False
        try:
            if '.' in token:
                return float(token)
            return int(token)
        except ValueError:
            return token

    def build_tree(token_iter):
        items = []
        for token in token_iter:
            if token == '(':
                items.append(build_tree(token_iter))
            elif token == ')':
                return items
            else:
                items.append(parse_token(token))
        return items if items else []

    def to_dict(data):
        if not isinstance(data, list):
            return data
        if not data:
            return []

        # Convert nested items recursively
        processed = [to_dict(item) for item in data]

        # 1. Base key-value pair: ['type', 'copper'] -> {'type': 'copper'}
        if len(processed) == 2 and isinstance(processed[0], str) and not isinstance(processed[1], (dict, list)):
            return {processed[0]: processed[1]}

        # 2. Block with a name tag: ['layer', 'F.Cu', {'type': 'copper'}, ...]
        if isinstance(processed[0], str):
            block_name = processed[0]
            remainder = processed[1:]

            # If remainder has mixed elements, separate raw arguments from dict properties
            dict_combined = {}
            args = []

            for item in remainder:
                if isinstance(item, dict):
                    for k, v in item.items():
                        if k in dict_combined:
                            if not isinstance(dict_combined[k], list):
                                dict_combined[k] = [dict_combined[k]]
                            dict_combined[k].append(v)
                        else:
                            dict_combined[k] = v
                else:
                    args.append(item)

            # Combine positional args and key-value properties
            if dict_combined:
                if args:
                    payload = {"args": args[0] if len(args) == 1 else args, **dict_combined}
                else:
                    payload = dict_combined
                return {block_name: payload}
            
            # Simple list block without sub-dicts
            if len(args) == 1:
                return {block_name: args[0]}
            return {block_name: args} if args else block_name

        return processed

    tokens = generate_tokens(file_obj)
    tree = build_tree(tokens)
    return to_dict(tree)

## Written for Kicad 10
def get_pad_info_from_file(settings, required_pads):
    # Load and parse the .kicad_pcb file
    # print(pcb_file_path)
    pcb_file_path = settings["pcb_path"]
    with open(pcb_file_path, "r") as f:
        data_dict = parse_sexp_file_to_dict(f)[0]

    ## Write Stackup Analyzer for the board stackup
    stackup = data_dict["kicad_pcb"]["setup"]["stackup"]

    footprints = data_dict["kicad_pcb"]["footprint"]
    output_pad = []
    for footprint in footprints:
        refdes = ""
        for prop in footprint["property"]:
            if isinstance(prop, dict):
                if prop["args"][0] == "Reference":
                    refdes = prop["args"][1]
                    # print(prop["args"][1])
        # print(footprint)
        # print(footprint["layer"])
        # print(footprint["at"])
        base_x = footprint["at"][0]
        base_y = footprint["at"][1]
        if isinstance(footprint["pad"], list):
            for pad in footprint["pad"]:
                local_x = pad["at"][0]
                local_y = pad["at"][1]
                pad_name = refdes + "." + str(pad["args"][0])
                if pad_name in required_pads:
                    output_pad.append({
                        "X": local_x + base_x,
                        "Y": local_y + base_y,
                        "Layer": footprint["layer"],
                        "Name": pad_name
                    })
                # print(str(pad["args"][0]) + ": " + str(pad["at"]))
        else:
            local_x = footprint["pad"]["at"][0]
            local_y = footprint["pad"]["at"][1]
            pad_name = refdes + "." + str(footprint["pad"]["args"][0])
            if pad_name in required_pads:
                output_pad.append({
                    "X": local_x + base_x,
                    "Y": local_y + base_y,
                    "Layer": footprint["layer"],
                    "Name": pad_name
                })
            # print(str(footprint["pad"]["args"][0]) + ": " + str(footprint["pad"]["at"]))
    for item in output_pad:
        pprint.pprint(item)

    face_group_dict = {
        "Units":"mm",
        "Layer_Z_Height":{
            "F.Cu":{
                "Top":1.5562,
                "Bottom":1.5162
            },
            "In1.Cu":{
                "Top":1.3058,
                "Bottom":1.2609
            },
            "In2.Cu":{
                "Top":0.2256,
                "Bottom":0.2104
            },
            "B.Cu":{
                "Top":0,
                "Bottom":-0.04
            }
        },
        "Pads":output_pad
    }

    with open("C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/Python_Automation/kicad_face_group.json", "w") as file:
        json.dump(face_group_dict, file, indent=4)
    return None

##########################################################
#--------------Hyperlynx Generation----------------------#
##########################################################

def schematic_parser(settings):
    # Load the schematic file
    schem = skip.Schematic(settings["schematic_path"])
    # Iterate through every symbol in the schematic
    requested_pads = []
    simulation_information = []
    for symbol in schem.symbol:
        # print(f"--- Symbol: {symbol.reference_value} ---")
        needed_for_sim = False
        # Iterate through all standard and custom properties
        # print(symbol.property.Reference.value)
        for prop in symbol.property:
            name = prop.name
            sim_data = re.compile(f'^({settings["pin_property_prefix"]})([0-9\.]+)$').match(name)
            if sim_data:
                pad_name = str(symbol.property.Reference.value) + "." + sim_data.group(2)
                requested_pads.append(pad_name)
                simulation_information.append([pad_name, prop.value])
    data_to_write = {
        "sim_info": simulation_information
    }
    with open(settings["info_export"], "w") as file:
        json.dump(data_to_write, file, indent=4)
    print(requested_pads)
    print(simulation_information)
    return requested_pads

if __name__ == "__main__":
    requested_pad_list = schematic_parser(input_settings)
    get_pad_info_from_file(input_settings, requested_pad_list)
    