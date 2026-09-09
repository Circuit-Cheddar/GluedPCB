#!/usr/bin/env python

###
### This file is generated automatically by SALOME v9.16.0 with dump python functionality
###

import sys
import salome

salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()
sys.path.insert(0, r'C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/Python_Automation')

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS


geompy = geomBuilder.New()

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
Auto_CLI_Export_1 = geompy.ImportSTEP("C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/ElmerFEM_Test/Auto_CLI_Export.step", False, True)
[Solid_1,Solid_2] = geompy.ExtractShapes(Auto_CLI_Export_1, geompy.ShapeType["SOLID"], True)
[geomObj_1,geomObj_2,geomObj_3,geomObj_4,geomObj_5,geomObj_6,geomObj_7,geomObj_8,geomObj_9,geomObj_10,geomObj_11,geomObj_12,geomObj_13,geomObj_14,geomObj_15,geomObj_16,geomObj_17,geomObj_18,geomObj_19,geomObj_20,geomObj_21,geomObj_22,geomObj_23,geomObj_24,geomObj_25,geomObj_26,geomObj_27,geomObj_28,geomObj_29,geomObj_30,geomObj_31,geomObj_32,geomObj_33,geomObj_34] = geompy.SubShapeAll(Solid_1, geompy.ShapeType["FACE"])
geomObj_35 = geompy.MakeCDG(geomObj_1)
geomObj_36 = geompy.MakeCDG(geomObj_2)
geomObj_37 = geompy.MakeCDG(geomObj_3)
geomObj_38 = geompy.MakeCDG(geomObj_4)
geomObj_39 = geompy.MakeCDG(geomObj_5)
geomObj_40 = geompy.MakeCDG(geomObj_6)
geomObj_41 = geompy.MakeCDG(geomObj_7)
geomObj_42 = geompy.MakeCDG(geomObj_8)
geomObj_43 = geompy.MakeCDG(geomObj_9)
geomObj_44 = geompy.MakeCDG(geomObj_10)
geomObj_45 = geompy.MakeCDG(geomObj_11)
geomObj_46 = geompy.MakeCDG(geomObj_12)
geomObj_47 = geompy.MakeCDG(geomObj_13)
geomObj_48 = geompy.MakeCDG(geomObj_14)
geomObj_49 = geompy.MakeCDG(geomObj_15)
geomObj_50 = geompy.MakeCDG(geomObj_16)
geomObj_51 = geompy.MakeCDG(geomObj_17)
geomObj_52 = geompy.MakeCDG(geomObj_18)
geomObj_53 = geompy.MakeCDG(geomObj_19)
geomObj_54 = geompy.MakeCDG(geomObj_20)
geomObj_55 = geompy.MakeCDG(geomObj_21)
geomObj_56 = geompy.MakeCDG(geomObj_22)
geomObj_57 = geompy.MakeCDG(geomObj_23)
geomObj_58 = geompy.MakeCDG(geomObj_24)
geomObj_59 = geompy.MakeCDG(geomObj_25)
geomObj_60 = geompy.MakeCDG(geomObj_26)
geomObj_61 = geompy.MakeCDG(geomObj_27)
geomObj_62 = geompy.MakeCDG(geomObj_28)
geomObj_63 = geompy.MakeCDG(geomObj_29)
geomObj_64 = geompy.MakeCDG(geomObj_30)
geomObj_65 = geompy.MakeCDG(geomObj_31)
geomObj_66 = geompy.MakeCDG(geomObj_32)
geomObj_67 = geompy.MakeCDG(geomObj_33)
geomObj_68 = geompy.MakeCDG(geomObj_34)
J1_1 = geompy.CreateGroup(Solid_1, geompy.ShapeType["FACE"])
geompy.UnionIDs(J1_1, [61])
J3_1 = geompy.CreateGroup(Solid_1, geompy.ShapeType["FACE"])
geompy.UnionIDs(J3_1, [86])
[geomObj_1, geomObj_2, geomObj_3, geomObj_4, geomObj_5, geomObj_6, geomObj_7, geomObj_8, geomObj_9, geomObj_10, geomObj_11, geomObj_12, geomObj_13, geomObj_14, geomObj_15, geomObj_16, geomObj_17, geomObj_18, geomObj_19, geomObj_20, geomObj_21, geomObj_22, geomObj_23, geomObj_24, geomObj_25, geomObj_26, geomObj_27, geomObj_28, geomObj_29, geomObj_30, geomObj_31, geomObj_32, geomObj_33, geomObj_34, J1_1, J3_1] = geompy.GetExistingSubObjects(Solid_1, False)
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Auto_CLI_Export_1, 'Auto_CLI_Export 1' )
geompy.addToStudyInFather( Auto_CLI_Export_1, Solid_1, 'Solid_1' )
geompy.addToStudyInFather( Auto_CLI_Export_1, Solid_2, 'Solid_2' )
geompy.addToStudyInFather( Solid_1, J1_1, 'J1.1' )
geompy.addToStudyInFather( Solid_1, J3_1, 'J3.1' )

###
### SMESH component
###

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
isDone = Mesh_1.Compute()
Mesh_1.CheckCompute()
isDone = Mesh_2.Compute()
Mesh_2.CheckCompute()
try:
  Mesh_1.ExportUNV( r'C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/ElmerFEM_Test/Mesh_1_unv.unv', 1 )
  pass
except:
  print('ExportUNV() failed. Invalid file name?')
try:
  Mesh_2.ExportUNV( r'C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/ElmerFEM_Test/Mesh_2_unv.unv', 1 )
  pass
except:
  print('ExportUNV() failed. Invalid file name?')
Mesh_3 = smesh.Mesh(Solid_1,'Mesh_3')
status = Mesh_3.AddHypothesis(NETGEN_3D_Parameters_1)
NETGEN_1D_2D_3D_2 = Mesh_3.Tetrahedron(algo=smeshBuilder.NETGEN_1D2D3D)
J1_1_1 = Mesh_3.GroupOnGeom(J1_1,'J1.1',SMESH.FACE)
J3_1_1 = Mesh_3.GroupOnGeom(J3_1,'J3.1',SMESH.FACE)
isDone = Mesh_3.Compute()
Mesh_3.CheckCompute()
[ J1_1_1, J3_1_1 ] = Mesh_3.GetGroups()


## Set names of Mesh objects
smesh.SetName(J1_1_1, 'J1.1')
smesh.SetName(NETGEN_3D_Parameters_1, 'NETGEN 3D Parameters_1')
smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')
smesh.SetName(Mesh_2.GetMesh(), 'Mesh_2')
smesh.SetName(J3_1_1, 'J3.1')
smesh.SetName(Mesh_3.GetMesh(), 'Mesh_3')
smesh.SetName(NETGEN_1D_2D_3D.GetAlgorithm(), 'NETGEN 1D-2D-3D')


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser()
