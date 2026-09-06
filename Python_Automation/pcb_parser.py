from kipy.board import Board

# Load your board
board = Board.load("path_to_your_project.kicad_pcb")

# Iterate through footprints and their pads (pins)
for footprint in board.footprints:
    print(f"Footprint: {footprint.reference}")
    
    for pad in footprint.pads:
        print(f"  Pin/Pad Number: {pad.number}")
        print(f"  Pin/Pad Name:   {pad.name}")
        print(f"  Shape:          {pad.shape}")
        print(f"  Position:       {pad.position}")
        print("-" * 20)
