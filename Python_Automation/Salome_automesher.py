#!/usr/bin/env python

###
### This file is generated automatically by SALOME v9.16.0 with dump python functionality
###

import sys
import salome

salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()
print("Hello from Salome", flush=True)
sys.path.insert(0, r'C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/ElmerFEM_Test')

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS


print("Setting Up Geometry", flush=True)
geompy = geomBuilder.New()

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
Output = "Importing Step File"
print(Output, flush=True)
Auto_CLI_Export_1 = geompy.ImportSTEP("C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/ElmerFEM_Test/Auto_CLI_Export.step", False, True)
Output = "Exploding Step File"
print(Output, flush=True)
[Solid_1,Solid_2] = geompy.ExtractShapes(Auto_CLI_Export_1, geompy.ShapeType["SOLID"], True)
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Auto_CLI_Export_1, 'Auto_CLI_Export 1' )
geompy.addToStudyInFather( Auto_CLI_Export_1, Solid_1, 'Solid_1' )
geompy.addToStudyInFather( Auto_CLI_Export_1, Solid_2, 'Solid_2' )

###
### SMESH component
###
Output = "Starting Mesher"
print(Output, flush=True)
import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New()
#smesh.SetEnablePublish( False ) # Set to False to avoid publish in study if not needed or in some particular situations:
                                 # multiples meshes built in parallel, complex and numerous mesh edition (performance)

Mesh_1 = smesh.Mesh(Solid_1,'Mesh_1')
NETGEN_1D_2D_3D = Mesh_1.Tetrahedron(algo=smeshBuilder.NETGEN_1D2D3D)
NETGEN_3D_Parameters_1 = NETGEN_1D_2D_3D.Parameters()
NETGEN_3D_Parameters_1.SetMinSize( 1.52e-05 )
NETGEN_3D_Parameters_1.SetSecondOrder( 0 )
NETGEN_3D_Parameters_1.SetOptimize( 1 )
NETGEN_3D_Parameters_1.SetFineness( 2 )
NETGEN_3D_Parameters_1.SetChordalError( -1 )
NETGEN_3D_Parameters_1.SetChordalErrorEnabled( 0 )
NETGEN_3D_Parameters_1.SetUseSurfaceCurvature( 1 )
NETGEN_3D_Parameters_1.SetFuseEdges( 1 )
NETGEN_3D_Parameters_1.SetQuadAllowed( 0 )
Mesh_2 = smesh.Mesh(Solid_2,'Mesh_2')
status = Mesh_2.AddHypothesis(NETGEN_3D_Parameters_1)
NETGEN_1D_2D_3D_1 = Mesh_2.Tetrahedron(algo=smeshBuilder.NETGEN_1D2D3D)
NETGEN_3D_Parameters_1.SetMaxSize( 0.0007 )
NETGEN_3D_Parameters_1.SetCheckChartBoundary( 88 )
isDone = Mesh_1.Compute()
Mesh_1.CheckCompute()
isDone = Mesh_2.Compute()
Mesh_2.CheckCompute()
try:
  Mesh_1.ExportUNV( r'C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/ElmerFEM_Test/Mesh_1_unv.unv', 0 )
  pass
except:
  print('ExportUNV() failed. Invalid file name?')
try:
  # Mesh_1.ExportUNV( r'C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/Python_Automation/Manual_Test_Export.unv', 0 )
  Mesh_2.ExportUNV( r'C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/ElmerFEM_Test/Mesh_2_unv.unv', 0 )
  pass
except:
  print('ExportUNV() failed. Invalid file name?')


## Set names of Mesh objects
smesh.SetName(NETGEN_3D_Parameters_1, 'NETGEN 3D Parameters_1')
smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')
smesh.SetName(Mesh_2.GetMesh(), 'Mesh_2')
smesh.SetName(NETGEN_1D_2D_3D.GetAlgorithm(), 'NETGEN 1D-2D-3D')


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser()

