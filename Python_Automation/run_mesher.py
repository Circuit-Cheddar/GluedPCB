import subprocess
import os

salome_dir = "C:/SALOME-9.16.0/W64/Python"
generation_dir = "C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/Python_Automation"

args = ["C:/SALOME-9.16.0/W64/Python/python3.exe", "C:/SALOME-9.16.0/salome", "-t", "C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/Python_Automation/Salome_automesher.py"]
# args = ["C:/SALOME-9.16.0/W64/Python/python3.exe", "C:/SALOME-9.16.0/salome", "C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/Python_Automation/Salome_automesher.py"]

print("Running the Mesher File")
with open(os.path.join(generation_dir, "generator.log"), "w") as f:
    process = subprocess.Popen(args, cwd=salome_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    for line in process.stdout:
        f.write(line)
        print(line)
        f.flush()  # Forces Python to write to the physical file immediately

process.wait()
print("Process completed and file fully synced!")