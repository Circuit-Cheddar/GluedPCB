# import wx
# import pcbnew

# def trigger_hyperlynx_export():
#     # 1. Locate the main KiCad window frame running pcbnew
#     top_windows = wx.GetTopLevelWindows()
#     pcb_frame = None
    
#     for window in top_windows:
#         # Look for the main PCB Editor frame
#         if "PCB Editor" in window.GetTitle() or "Pcbnew" in window.GetTitle():
#             pcb_frame = window
#             break
            
#     if not pcb_frame:
#         print("[-] Error: Could not find the active PCB Editor window.")
#         return

#     # 2. Look up the specific menu item ID for HyperLynx export
#     # KiCad handles this via its structural File -> Export menu IDs
#     menu_bar = pcb_frame.GetMenuBar()
#     hyperlynx_id = None
    
#     if menu_bar:
#         for menu, label in menu_bar.GetMenus():
#             if "File" in label:
#                 for item in menu.GetMenuItems():
#                     # Check for export submenu items
#                     if item.IsSubMenu():
#                         for sub_item in item.GetSubMenu().GetMenuItems():
#                             if "HyperLynx" in sub_item.GetItemLabelText():
#                                 hyperlynx_id = sub_item.GetId()
#                                 break
#                     if hyperlynx_id:
#                         break
#             if hyperlynx_id:
#                 break

#     # 3. Simulate the click event if the ID was found
#     if hyperlynx_id:
#         print(f"[+] Found HyperLynx Export ID: {hyperlynx_id}. Triggering...")
#         event = wx.CommandEvent(wx.wxEVT_COMMAND_MENU_SELECTED, hyperlynx_id)
#         wx.PostEvent(pcb_frame, event)
#     else:
#         print("[-] Error: Could not programmatically locate the HyperLynx export option in the menu.")

# # Run the macro
# trigger_hyperlynx_export()

import subprocess
args = ["C:/Users/user/AppData/Local/Programs/KiCad/10.0/bin/python.exe", "C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/Python_Automation/hyper_gen_kicad_script.py", "C:/Users/user/Documents/GitHub/KiCad-ElmerFEM_Test/ElmerFEM_Test/ElmerFEM Test.kicad_pcb"]
with open("pcb_control.log", "w") as f:
    subprocess.run(args, stdout=f, stderr=f, check=True)
print("this is bullshit")