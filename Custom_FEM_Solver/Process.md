# Introduction

I've entered a very deep and dark rabbit hole and this is my attempt to create a trail to find my way out and back in this process

The original goal of this project was to create a workflow using existing opensource softwares to take a KiCad project and run thermal and electromagnetic simulations on the board natively within KiCad. The intent would be to mimic/replicate/improve the process that KeySight has for Altium.

# Current Thermal Simulation Toolchain
KiCad --> Salome --> ElmerFEM --> ParaView
Currently KiCad can export a step file of the individual nets. This can then be importated into Salome for meshing and then handed over to ElmerFEM for simulating and then rendered in ParaView. The workflow workes well except I have not been able to get the Elmer FEM simulation to converge to something reasonable for a simple trace with a through hole pad on either end. This is the simple case and the simulator should have no problems with this. Salome has no problems generating the mesh for the software. Somewhere between Salome and ElmerFEM, things are breaking down. So now I want to build an integrated Mesher and Solver, where the solver will dynamically update the mesh as it works to converge on a solution. The problem is I have no experience with writing a mesher or solver, let alone the indepth workings of and FEM simulator.

# Phase 1 - Python Mesher
I guess we are starting here. I need to take a model and break it up into the the simpliest form of tetrahedrons. I probably want a visualizer? Or maybe I should do this with the simpliest way and just import brep files (I believe these to be the easiest format; I just googled it and it looks like step is a wrapper for BRep so lets just use STEP files). From the STEP File I want to create the simpliest tetrahedrons. For any curved surfaces, I'll have to specify a segment density? (Maybe specify an absolute deviation metric, in Area per length) to keep things simple but accurate. The native way of handling that is gmsh. I don't know how I'm going to futhur refine a gmsh file. It feels like that isn't in the spirit of what I'm trying todo.
