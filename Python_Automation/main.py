# Take the UNV from Salome and run the ElmerFEM simulation and generate the vtk for paraview

sif_path = f"./Python Automation/Simulation"

import subprocess
import os
from pathlib import Path
import kicad_interface
import run_mesher
import json
import re
import pyvista as pv


## Program flow
# Run kicad schematic get simulation information
# run kicad pcb to get pad locations
# run mesher to get unv files and pad size
# run unv file converter
# generate sif file
# run elmer solver
# combine all vtu files
# launch salome paraview

mesher_data = {
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

kicad_input_settings = {
    "kicad_cli": "C:/Users/user/AppData/Local/Programs/KiCad/10.0/bin/kicad-cli",
    "kicad_project_dir":"C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/ElmerFEM_Test",
    "schematic_path": "C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/ElmerFEM_Test/ElmerFEM Test.kicad_sch",
    "pcb_path": "C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/ElmerFEM_Test/ElmerFEM Test.kicad_pcb",
    "hyp_file": "C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/ElmerFEM_Test/ElmerFEM Test.hyp",
    "info_export": "C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/Python_Automation/kicad_sim_info.json",
    "generate_hyp": True,
    "pin_property_prefix": "CCSIM_"
}

#generate header based on where the files should be pulled from
def sif_header(Target_Mesh_Database):
	return f"""
Header
CHECK KEYWORDS Warn
Mesh DB "." "{Target_Mesh_Database}"
Include Path ""
Results Directory "./result"
End
"""

#file name should be the name of the solid
def sif_Simulation(filename):
	return f"""
Simulation
Max Output Level = 5
Coordinate System = Cartesian
Coordinate Mapping(3) = 1 2 3
Simulation Type = Steady state
Steady State Max Iterations = 1
Output Intervals(1) = 1
Solver Input File = {filename}.sif
Post File = {filename}.vtu
End
"""

#currentl contains information on the solver will likely need to improve this later
def sif_boilerplate():
	return"""
Constants
Gravity(4) = 0 -1 0 9.82
Stefan Boltzmann = 5.670374419e-08
Permittivity of Vacuum = 8.85418781e-12
Permeability of Vacuum = 1.25663706e-6
Boltzmann Constant = 1.380649e-23
Unit Charge = 1.6021766e-19
End

Body 1
Target Bodies(1) = 1
Name = "Body Property 1"
Equation = 1
Material = 1
End

Solver 1
Equation = Static Current Conduction
Calculate Volume Current = True
Procedure = "StatCurrentSolve" "StatCurrentSolver"
Calculate Joule Heating = True
Variable = Potential
Exec Solver = Always
Stabilize = True
Optimize Bandwidth = True
Steady State Convergence Tolerance = 1.0e-5
Nonlinear System Convergence Tolerance = 1.0e-7
Nonlinear System Max Iterations = 20
Nonlinear System Newton After Iterations = 3
Nonlinear System Newton After Tolerance = 1.0e-3
Nonlinear System Relaxation Factor = 1
Linear System Solver = Direct
Linear System Direct Method = Umfpack
End

Equation 1
Name = "Equation 1"
Active Solvers(1) = 1
End

Material 1
Name = "Material 1"
Electric Conductivity = 47e6
End
"""

def sif_boundary(BC_index, target_boundary, name, type, value, area):
	value_information = ""
	if type == "Voltage":
		value_information = f"Potential = {value}"
	elif type == "Current":
		value_information = f"Current Density = {value/area}"

	return f"""
Boundary Condition {BC_index}
Target Boundaries(1) = {target_boundary} 
Name = "{name}"
{value_information}
End
"""

def generate_sif(mesh_dir, BAI, filename="case", Target_Mesh_Database = "."):
	file_contents = sif_header(Target_Mesh_Database)
	file_contents = file_contents + sif_Simulation(filename)
	file_contents = file_contents + sif_boilerplate()
	BC_Index = 0
	for boundary_info in BAI:
		print(boundary_info)
		BC_Index += 1
		# TODO Change this to use a dict for readability
		file_contents = file_contents + sif_boundary(BC_Index, boundary_info[0], boundary_info[1], boundary_info[2], boundary_info[3], boundary_info[4])
		

	sif_content = f"""Header
CHECK KEYWORDS Warn
Mesh DB "." "{Target_Mesh_Database}"
Include Path ""
Results Directory "./result"
End

Simulation
Max Output Level = 5
Coordinate System = Cartesian
Coordinate Mapping(3) = 1 2 3
Simulation Type = Steady state
Steady State Max Iterations = 1
Output Intervals(1) = 1
Solver Input File = {filename}.sif
Post File = {filename}.vtu
End

Constants
Gravity(4) = 0 -1 0 9.82
Stefan Boltzmann = 5.670374419e-08
Permittivity of Vacuum = 8.85418781e-12
Permeability of Vacuum = 1.25663706e-6
Boltzmann Constant = 1.380649e-23
Unit Charge = 1.6021766e-19
End

Body 1
Target Bodies(1) = 1
Name = "Body Property 1"
Equation = 1
Material = 1
End

Solver 1
Equation = Static Current Conduction
Calculate Volume Current = True
Procedure = "StatCurrentSolve" "StatCurrentSolver"
Calculate Joule Heating = True
Variable = Potential
Exec Solver = Always
Stabilize = True
Optimize Bandwidth = True
Steady State Convergence Tolerance = 1.0e-5
Nonlinear System Convergence Tolerance = 1.0e-7
Nonlinear System Max Iterations = 20
Nonlinear System Newton After Iterations = 3
Nonlinear System Newton After Tolerance = 1.0e-3
Nonlinear System Relaxation Factor = 1
Linear System Solver = Direct
Linear System Direct Method = Umfpack
End

Equation 1
Name = "Equation 1"
Active Solvers(1) = 1
End

Material 1
Name = "Material 1"
Electric Conductivity = 47e6
End

Boundary Condition 1
Target Boundaries(1) = 1 
Name = "Input"
Potential = 5
End

Boundary Condition 2
Target Boundaries(1) = 2 
Name = "Output"
Current Density = -96154
End

"""

	with open(mesh_dir+ "\\" + filename + ".sif", "w") as f:
			f.write(file_contents + "\n")
	# print(f"Successfully generated {filename}")
	return filename + ".sif"



target_pcb = "C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/ElmerFEM_Test/ElmerFEM Test.kicad_pcb"
kicad_cli = "C:/Users/user/AppData/Local/Programs/KiCad/10.0/bin/kicad-cli"
# new_step_file = "C:/Users/user/Documents/GitHub/KiCad-ElmerFEM Test/ElmerFEM Test/Auto_CLI_Export.step"
new_step_file = "Auto_CLI_Export.step"
step_dir = "C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/ElmerFEM_Test"

args = [kicad_cli,
	"pcb",
	"export",
	"step",
	# "--no-extra-pad-thickness", 
	"--no-board-body",
	"--no-components", 
	"--include-pads",
	"--include-tracks",
	"--include-inner-copper",
	"--fuse-shapes",
	"--output",
	new_step_file,
	target_pcb]


# surface_information = "C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/Python_Automation/kicad_face_information.json"

elmergrid_exe = "C:/Program Files/Elmer 26.2-Release/bin/ElmerGrid.exe"
elmersolver_exe = "C:/Program Files/Elmer 26.2-Release/bin/ElmerSolver.exe"



def process_unv_files():
	
	with open(mesher_data["surface_information"], "r") as file:
			data = json.load(file)
	mesh_files = data["Unv_Files"]
	mesh_dir = "C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/ElmerFEM_Test"
	if len(mesh_files) > 1:  
		for file in mesh_files:
			args = [elmergrid_exe, "8", "2", file, "-autoclean"]

			# Run ElmerGrid manually using the correct flags
			print("Running ElmerGrid on UNV file...")
			with open(file[0:-4] +".log", "w") as f:
					subprocess.run(args, stdout=f, stderr=f, check=True)
	else:
		args = [elmergrid_exe, "8", "2", mesh_files[0], "-autoclean"]
		
		# Run ElmerGrid manually using the correct flags
		print("Running ElmerGrid on UNV file...")
		with open(file[0:-4] +".log", "w") as f:
							subprocess.run(args, stdout=f, stderr=f, check=True)

def generate_step():
	print("Generating STEP File")
	with open(os.path.join(step_dir, "step_gen_" + new_step_file[0:-5] +".log"), "w") as f:
		subprocess.run(args, cwd=step_dir, stdout=f, stderr=f, check=True)

def generate_sifs():
	output_files = []
	with open("C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/Python_Automation/kicad_sim_info.json", "r") as file:
		sim_info = json.load(file)
	with open("C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/Python_Automation/kicad_face_information.json", "r") as file:
		face_info = json.load(file)
	print(sim_info)
	reference = face_info["Size_Dict"]
	# print(face_info["Size_Dict"])
	sif_dir = "C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/ElmerFEM_Test"
	for item in reference.keys():
		target_folder = sif_dir + "/" + item
		with open(target_folder + "/mesh.names", "r") as file:
			boundstuff = []
			for line in file:
				expected_boundary_pattern = re.compile(r'^\$\s([A-z0-9]+\.[0-9]+)\s=\s(-?[0-9\.]+)$')
				value_regex = re.compile(r'^(-?[0-9\.]+)([A-z]+)$')
				boundary_info = expected_boundary_pattern.match(line)
				if boundary_info:
					boundstuff.append([boundary_info.group(1), boundary_info.group(2)])
		BAI_stuff = []
		for bound in boundstuff:
			for info in sim_info["sim_info"]:
				if bound[0] == info[0]:
					value_type = "Voltage"
					value = value_regex.match(info[1])
					if(value.group(2) == "A"):
						value_type = "Current"
					# TODO there is no handling for engineering prefixes, like milliamp kilovolt. Need to fix this
					# print([value.group(1), ])
					BAI_stuff.append([bound[1], bound[0],value_type, float(value.group(1)), float(reference[item][bound[0]])])
					
					# target_boundary, name, type, value, area
		output_files.append(sif_dir + "/" + generate_sif(sif_dir, BAI_stuff, item, item))
	return output_files

def run_solvers(sif_files):
	sif_dir = "C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/ElmerFEM_Test"
	print("Running ElmerSolver on UNV files...") 
	for file in sif_files:
		print(file)
		args = [elmersolver_exe, file]
		with open(file[0:-4] +".log", "w") as f:
			subprocess.run(args, cwd=sif_dir, stdout=f, stderr=f, check=True)

def combine_vtus():
	directory = Path("C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/ElmerFEM_Test/result")
	# Change "*.txt" to whichever extension you need
	files = [str(file) for file in directory.glob("*.vtu")]

	print(files)
	# List your VTU files

	# Read each file into a PyVista dataset
	datasets = [pv.read(f) for f in files]

	# Merge them into a single unstructured grid
	combined_grid = datasets[0].merge(datasets[1:])

	# Save the result to a new VTU file
	combined_grid.save(str(directory)+'/combined_output.vtu')

# Run the Simulators
if __name__ == "__main__":

	requested_pad_list = kicad_interface.schematic_parser(kicad_input_settings)
	kicad_interface.get_pad_info_from_file(kicad_input_settings, requested_pad_list)
	# generate_step()
	# run_mesher.write_mesher_settings(mesher_data["settings_file_path"])
	# run_mesher.run_mesher(mesher_data)
		
	process_unv_files()
	sif_files = generate_sifs()
	run_solvers(sif_files)
	combine_vtus()
