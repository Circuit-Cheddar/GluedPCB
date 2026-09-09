import sys
import salome
import json

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder


############################################################
#-----------------------Import Setting---------------------#
############################################################
if __name__ == '__main__':
  # This is where we need to load the json file
  print("Arguments:", sys.argv[1:])


try:
  # Open the file in read mode ('r')
  with open(sys.argv[1], "r") as file:
    data = json.load(file)
  face_group_file = data["face_group_settings"]
  face_size_file = data["surface_information"]

  with open(face_group_file, "r") as file:
      face_group_data = json.load(file)
except:
  print("Unable to load settings", flush=True)
  sys.exit(1)

# 'data' is now a standard Python dictionary
# print(data)
# print(face_group_data)
unit_scaler = 1

if face_group_data["Units"] == "mm":
  unit_scaler = 0.001
if face_group_data["Units"] == "in":
  unit_scaler = 0.0254

top_copper_ref = face_group_data["Layer_Z_Height"]["F.Cu"]["Top"] * unit_scaler
bottom_copper_ref = face_group_data["Layer_Z_Height"]["B.Cu"]["Bottom"] * unit_scaler
pad_array = face_group_data["Pads"]
# print(data["run_mesher"])

salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()
print("Hello from Salome", flush=True)
sys.path.insert(0, r'C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/ElmerFEM_Test')

###
### GEOM component
###

geompy = geomBuilder.New()
smesh = smeshBuilder.New()

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)

geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )

Auto_CLI_Export_1 = geompy.ImportSTEP(data["target_step"], False, True)

geompy.addToStudy( Auto_CLI_Export_1, 'Auto_CLI_Export 1' )

# TODO Setup an intellegent way of knowing what Net these are to improve the Face Applying Algorithm
size_information = {}
exported_unvs = []
solids = geompy.ExtractShapes(Auto_CLI_Export_1, geompy.ShapeType["SOLID"], True)
for solid in solids:
  print("Starting Work on " + solid.GetName(), flush=True)
  solid_size_info = {}
  # Add Solid to the Solid
  geompy.addToStudyInFather( Auto_CLI_Export_1, solid, solid.GetName())
  print(solid.GetName())

  # Get all faces of the solid
  faces = geompy.SubShapeAll(solid, geompy.ShapeType["FACE"])

  # On large models a search algorithm might be needed
  face_groups_to_add = []
  for i, face in enumerate(faces):
    # Calculate Center of Gravity (CDG)
    center_point = geompy.MakeCDG(face)
    
    # Extract X, Y, Z coordinates
    x, y, z = geompy.PointCoordinates(center_point)
    for target_pad in pad_array:
      # TODO Work through the logic on if there ever needs to be volage or current sources on any other surface
      # Get the Z height. Assumes only two surfaces for now
      if target_pad["Layer"] == "F.Cu":
        z_ref = top_copper_ref

      name = target_pad["Name"]
      if(abs(x - target_pad["X"]*unit_scaler) < 0.00001) and (abs(y + target_pad["Y"]*unit_scaler) < 0.00001) and (abs(z - z_ref) < 0.000001):
        face_groups_to_add.append([[geompy.GetSubShapeID(solid, face)], solid, name])
        (length, area, volume) = geompy.BasicProperties(face)

        # This data needs to be exported so the solver knows what the current density will be based on the surface area and current
        print(f"{name} face grounp found at face {i} with a surface area of {area}")
        solid_size_info[name] = area

  # Get the Mesh Setup
  solid_groups = []
  for set in face_groups_to_add:
    temp_group = geompy.CreateGroup(set[1], geompy.ShapeType["FACE"])
    solid_groups.append(temp_group)
    geompy.UnionIDs(temp_group, set[0])
    geompy.addToStudyInFather( set[1], temp_group, set[2] )

  # Something here
  temp_mesh = smesh.Mesh(solid,solid.GetName())
  NETGEN_1D_2D_3D = temp_mesh.Tetrahedron(algo=smeshBuilder.NETGEN_1D2D3D)
  # TODO Need to develop a process for determining these values. Mesh Size is heavily dependant when meshing through hole components
  NETGEN_3D_Parameters_1 = NETGEN_1D_2D_3D.Parameters()
  NETGEN_3D_Parameters_1.SetMaxSize( 0.0002 ) 
  NETGEN_3D_Parameters_1.SetMinSize( 1.52e-05 )
  NETGEN_3D_Parameters_1.SetSecondOrder( 0 )
  NETGEN_3D_Parameters_1.SetOptimize( 1 )
  NETGEN_3D_Parameters_1.SetFineness( 2 )
  NETGEN_3D_Parameters_1.SetChordalError( -1 )
  NETGEN_3D_Parameters_1.SetChordalErrorEnabled( 0 )
  NETGEN_3D_Parameters_1.SetUseSurfaceCurvature( 1 )
  NETGEN_3D_Parameters_1.SetFuseEdges( 1 )
  NETGEN_3D_Parameters_1.SetQuadAllowed( 0 )
  NETGEN_3D_Parameters_1.SetCheckChartBoundary( 88 )

  Mesh_Groups = []
  for group in solid_groups:
    Mesh_Groups.append(temp_mesh.GroupOnGeom(group,group.GetName(),SMESH.FACE))

  Meshed_Groups = temp_mesh.GetGroups()
  for meshed_group in Meshed_Groups:
    smesh.SetName(meshed_group, meshed_group.GetName())

  isDone = temp_mesh.Compute()
  temp_mesh.CheckCompute()

  try:
    file_name = "C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/ElmerFEM_Test/" + solid.GetName() + ".unv"
    temp_mesh.ExportUNV( file_name, 0 )
    exported_unvs.append(file_name)
  except:
    print('ExportUNV() failed. Invalid file name?')

  smesh.SetName(NETGEN_3D_Parameters_1, 'NETGEN 3D Parameters_1')
  smesh.SetName(temp_mesh.GetMesh(), solid.GetName())
  smesh.SetName(NETGEN_1D_2D_3D.GetAlgorithm(), 'NETGEN 1D-2D-3D')
  size_information[solid.GetName()] = solid_size_info


data_to_write = {
  "Units":"m",
  "Size_Dict":size_information,
  "Unv_Files":exported_unvs
}
with open(face_size_file, 'w') as file:
  json.dump(data_to_write, file, indent=4)


