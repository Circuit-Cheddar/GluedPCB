# Take the UNV from Salome and run the ElmerFEM simulation and generate the vtk for paraview

sif_path = f"./Python Automation/Simulation"

import subprocess
import os


def generate_sif(mesh_dir, filename="case", Target_Mesh_Database = "."):
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
      f.write(sif_content.strip() + "\n")
  print(f"Successfully generated {filename}")
  return filename + ".sif"

target_pcb = "C:/Users/user/Documents/GitHub/KiCad-ElmerFEM Test/ElmerFEM Test/ElmerFEM Test.kicad_pcb"
kicad_cli = "C:/Users/user/AppData/Local/Programs/KiCad/10.0/bin/kicad-cli"
# new_step_file = "C:/Users/user/Documents/GitHub/KiCad-ElmerFEM Test/ElmerFEM Test/Auto_CLI_Export.step"
new_step_file = "Auto_CLI_Export.step"
step_dir = "C:/Users/user/Documents/GitHub/KiCad-ElmerFEM Test/ElmerFEM Test"
args = [kicad_cli,
        "pcb",
        "export",
        "step",
        "--no-extra-pad-thickness", 
        "--no-board-body", 
        "--include-pads",
        "--include-tracks",
        "--include-inner-copper",
        "--fuse-shapes",
        "--output",
        new_step_file,
        target_pcb]

print("Generating STEP File")
with open(os.path.join(step_dir, "step_gen_" + new_step_file[0:-5] +".log"), "w") as f:
    subprocess.run(args, cwd=step_dir, stdout=f, stderr=f, check=True)

elmergrid_exe = "C:/Program Files/Elmer 26.2-Release/bin/ElmerGrid.exe"
elmersolver_exe = "C:/Program Files/Elmer 26.2-Release/bin/ElmerSolver.exe"
mesh_files = ["Thin_1.unv",
              "Thick_1.unv"]
mesh_dir = "./ElmerFEM Test/Real_Test"

if len(mesh_files) > 1:  
  for file in mesh_files:
    args = [elmergrid_exe, "8", "2", file, "-autoclean"]

    # Run ElmerGrid manually using the correct flags
    print("Running ElmerGrid on UNV file...")
    with open(os.path.join(mesh_dir, "elmergrid_" + file[0:-4] +".log"), "w") as f:
        subprocess.run(args, cwd=mesh_dir, stdout=f, stderr=f, check=True)
else:
  args = [elmergrid_exe, "8", "2", mesh_files[0], "-autoclean"]
  
  # Run ElmerGrid manually using the correct flags
  print("Running ElmerGrid on UNV file...")
  with open(os.path.join(mesh_dir, "elmergrid.log"), "w") as f:
      subprocess.run(args, cwd=mesh_dir, stdout=f, stderr=f, check=True)

sif_1 = generate_sif(mesh_dir, "thick", "Thick_1/")
sif_2 = generate_sif(mesh_dir, "thin", "Thin_1/")

sif_files = [sif_1, sif_2]

print("Running ElmerSolver on UNV file...")
if len(sif_files) > 1:  
  for file in sif_files:
    args = [elmersolver_exe, file]
    with open(os.path.join(mesh_dir, "elmersolver_" + file[0:-4] +".log"), "w") as f:
      subprocess.run(args, cwd=mesh_dir, stdout=f, stderr=f, check=True)
else:
  args = [elmersolver_exe, sif_files[0]]
  with open(os.path.join(mesh_dir, "elmersolver_" + file[0:-4] +".log"), "w") as f:
      subprocess.run(args, cwd=mesh_dir, stdout=f, stderr=f, check=True)


# Run the Simulators
# if __name__ == "__main__":
    # generate_sif("case001.sif")
