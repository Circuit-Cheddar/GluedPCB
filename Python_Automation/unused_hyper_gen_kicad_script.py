import sys
import os
import time
import wx
import pcbnew


def automate_hyperlynx_generation():
    # 1. Get the current active board info
    board = pcbnew.GetBoard()
    if not board:
        print("[-] Error: No active board found. Open a PCB design first.")
        return
        
    board_path = board.GetFileName()
    output_dir = os.path.dirname(board_path)
    print(f"[+] Active board detected: {board_path}")

    # 2. Find the running KiCad PCB Editor Window
    top_windows = wx.GetTopLevelWindows()
    pcb_frame = None
    for window in top_windows:
        title = window.GetTitle()
        if "PCB Editor" in title or "Pcbnew" in title:
            pcb_frame = window
            break
            
    if not pcb_frame:
        print("[-] Error: Could not bind to the active PCB Editor frame.")
        return

    # 3. Locate the hidden internal Menu ID for HyperLynx Export
    menu_bar = pcb_frame.GetMenuBar()
    hyperlynx_menu_id = None
    
    if menu_bar:
        for menu, label in menu_bar.GetMenus():
            if "File" in label:
                for item in menu.GetMenuItems():
                    # Scan the "Export" submenu
                    if item.IsSubMenu():
                        for sub_item in item.GetSubMenu().GetMenuItems():
                            if "HyperLynx" in sub_item.GetItemLabelText():
                                hyperlynx_menu_id = sub_item.GetId()
                                break
                    if hyperlynx_menu_id: break
            if hyperlynx_menu_id: break

    # 4. Trigger the Export
    if hyperlynx_menu_id:
        print(f"[+] Programmatically triggering menu ID {hyperlynx_menu_id}...")
        
        # Fire a synthetic menu click event into the application loop
        event = wx.CommandEvent(wx.wxEVT_COMMAND_MENU_SELECTED, hyperlynx_menu_id)
        wx.PostEvent(pcb_frame, event)
        
        # KiCad will automatically default the save dialog target 
        # to your active project folder.
        print(f"[+] Action triggered. Check your project folder for the .hyp export.")
    else:
        print("[-] Error: HyperLynx menu item structure not found.")

# Run the macro inside KiCad

def process_board(board_path):
    print(f"[+] Loading board: {board_path}")
    
    # Load the board file without opening the GUI
    board = pcbnew.LoadBoard(board_path)
    
    # Example headless action: Count components/footprints
    footprints = board.GetFootprints()
    print(f"[+] Found {len(footprints)} footprints on the board.")
    
    for fp in footprints:
        print(f" - Reference: {fp.GetReference()}, Value: {fp.GetValue()}")

    # If you made edits, you can save them headlessly like this:
    # board.Save(board_path)
    # print("[+] Board saved successfully.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <path_to_kicad_pcb>")
        sys.exit(1)
        
    process_board(sys.argv[1])
    automate_hyperlynx_generation()

print("what is this")


