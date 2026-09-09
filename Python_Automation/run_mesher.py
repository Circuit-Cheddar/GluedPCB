import subprocess
import os
import json

# salome_dir = "C:/SALOME-9.16.0/W64/Python"
# generation_dir = "C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/Python_Automation"

# settings_file_path = "C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/Python_Automation/mesher_settings.json"

# args = ["C:/SALOME-9.16.0/W64/Python/python3.exe",
#         "C:/SALOME-9.16.0/salome", 
#         "-t", 
#         "C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/Python_Automation/Salome_automesher.py",
#         "args:" + settings_file_path]

# Your data structure (dictionary or list)
data = {
    # Steps of the Script
    "import_step": True,
    "explode_step": True,
    "expected_solids": 0,
    # TODO Need a way of connecting the exploded solids to a net
    "exploded_solids_names": ["Thin", "Thick"],
    "assign_face_groups": True,
    "run_mesher": False,
    "mesher_settings": False,
    "target_step": "C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/ElmerFEM_Test/Auto_CLI_Export.step",
    "face_group_settings": "C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/Python_Automation/kicad_face_group.json",
    "surface_information": "C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/Python_Automation/kicad_face_information.json",
    "settings_file_path": "C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/Python_Automation/mesher_settings.json",
    "generation_dir": "C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/Python_Automation",
    "salome_dir": "C:/SALOME-9.16.0/W64/Python",
    "args": ["C:/SALOME-9.16.0/W64/Python/python3.exe",
        "C:/SALOME-9.16.0/salome", 
        "-t", 
        "C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/Python_Automation/Salome_automesher.py",
        "args:"]
}

def write_mesher_settings(file_path):
    # Open a file in write mode ('w') and save the JSON data
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

def run_mesher(input_settings):
    args = input_settings["args"]
    args[-1] += input_settings["settings_file_path"]
    print("Running the Mesher File")
    with open(os.path.join(input_settings["generation_dir"], "generator.log"), "w") as f:
        process = subprocess.Popen(args, cwd=input_settings["salome_dir"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        for line in process.stdout:
            f.write(line)
            if line != "BFGS update error2\n":
                print(line[:-1])
            f.flush()  # Forces Python to write to the physical file immediately

    process.wait()
    print("Process completed and file fully synced!")

if __name__ == "__main__":
    write_mesher_settings(data["settings_file_path"])
    run_mesher(data)