#!/usr/bin/env python

###
### This file is generated automatically by SALOME v9.16.0 with dump python functionality
###

import sys
import salome

salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()
sys.path.insert(0, r'C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/ElmerFEM_Test')

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
[geomObj_1] = geompy.ExtractShapes(Auto_CLI_Export_1, geompy.ShapeType["COMPOUND"], True)
[Solid_1,Solid_2] = geompy.ExtractShapes(Auto_CLI_Export_1, geompy.ShapeType["SOLID"], True)
Input = geompy.CreateGroup(Solid_1, geompy.ShapeType["FACE"])
geompy.UnionIDs(Input, [86])
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudyInFather( Auto_CLI_Export_1, Solid_1, 'Solid_1' )
geompy.addToStudyInFather( Auto_CLI_Export_1, Solid_2, 'Solid_2' )
geompy.addToStudyInFather( Solid_1, Input, 'Input' )
geompy.addToStudy( Auto_CLI_Export_1, 'Auto_CLI_Export 1' )


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser()
