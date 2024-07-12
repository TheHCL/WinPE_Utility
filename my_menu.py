# Import the necessary packages
from consolemenu import *
from consolemenu.items import *
from consolemenu.prompt_utils import PromptUtils
from tkinter import filedialog
import os,time,subprocess



def showvol():
    try:
        # Run the "list disk" command and capture the output
        f=open("list_vol_script.txt","w")
        f.write("lis vol\nexit")
        f.close()
        output = subprocess.check_output("diskpart /s list_vol_script.txt ", shell=True, text=True)

        # Print the captured output
        print(output)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def ffu_clean(disk_vol):
    try:
        f=open("clean_disk.txt","w")
        f.write("sel disk "+disk_vol+"\n")
        f.write("clean\n")
        output = subprocess.check_output("diskpart /s clean_disk.txt ", shell=True, text=True)

        # Print the captured output
        print(output)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def showdisk():
    try:
        # Run the "list disk" command and capture the output
        f=open("list_disk_script.txt","w")
        f.write("lis disk\nexit")
        f.close()
        output = subprocess.check_output("diskpart /s list_disk_script.txt ", shell=True, text=True)

        # Print the captured output
        print(output)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def create_parition(disk_vol):
    try:
        f=open("CreatePartitions-UEFI.txt","w")
        f.write("sel disk "+disk_vol+"\n")
        f.write("clean\n")
        f.write("convert gpt\n")
        f.write("Create partition EFI size=2048\n")
        f.write("Format quick fs=fat32 Label=EFI\n")
        f.write("Assign letter=S\n")
        f.write("Create partition primary\n")
        f.write("Format quick fs=NTFS Label=OS\n")
        f.write("Assign letter=W\n")
        f.write("Exit")
        f.close()
        output = subprocess.check_output("diskpart /s CreatePartitions-UEFI.txt", shell=True, text=True)

        # Print the captured output
        print(output)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")







def backup_wimfile():
    showdvol()
    x = input("Select A Disk to backup WIM : ")
    #a = filedialog.askdirectory(title="Save WIM file to")
    a=filedialog.asksaveasfile(title="Save WIM file",filetypes=[("WIM file", ".wim")],defaultextension=".wim")
    #print(a.name)
    if a:
        a.close()
        a_path=a.name.replace("/","\\")
       # print(a_path)
        os.remove(a_path)
    else:
        PromptUtils(Screen()).enter_to_continue()
        return


    name = ((os.path.split(a.name)[1]).split("."))[0]
    
    #optimzie failure
    #os.system("DISM /image:"+x+":\\ /optimize-image /boot")
    time.sleep(5)
    os.system('Dism /Capture-Image /ImageFile:"'+a_path+'" /CaptureDir:"'+x+'":\\ /Name:'+name)
    os.remove("list_vol_script.txt")
    PromptUtils(Screen()).enter_to_continue()

def restore_wimfile():
    showdisk()
    x=input("select DISK to clean and restore: ")
    create_parition(x)
    a=filedialog.askopenfilename(title="Select WIM file to restore",filetypes=[("WIM file", ".wim")],defaultextension=".wim")
    a=a.replace("/","\\")
    f=open("applyimage.bat","w")
    f.write("dism /Apply-Image /ImageFile:%1 /Index:1 /ApplyDir:W:\\\n")
    f.write("bcdboot W:\\Windows /s S: /f UEFI")
    f.close()
    os.system('applyimage.bat "'+a+'"')

    os.remove("list_disk_script.txt")
    os.remove("CreatePartitions-UEFI.txt")
    os.remove("applyimage.bat")

    PromptUtils(Screen()).enter_to_continue()

def backup_ffufile():
    showdisk()
    x=input("select DISK to backup FFU : ")
    a=filedialog.asksaveasfile(title="Save FFU file",filetypes=[("FFU file", ".ffu")],defaultextension=".ffu")
    #print(a.name)
    if a:
        a.close()
        a_path=a.name.replace("/","\\")
       # print(a_path)
        os.remove(a_path)
    else:
        PromptUtils(Screen()).enter_to_continue()
        return


    name = ((os.path.split(a.name)[1]).split("."))[0]
    os.system('dism /Capture-Ffu /ImageFile:"'+a_path+'" /CaptureDrive:\\\\.\\PhysicalDrive'+x+' /Name:'+name)

    os.remove("list_disk_script.txt")

    PromptUtils(Screen()).enter_to_continue()

def restore_ffufile():
    showdisk()
    x=input("select DISK to Restore FFU : ")
    ffu_clean(x)
    a=filedialog.askopenfilename(title="Select FFU file to restore",filetypes=[("FFU file", ".ffu")],defaultextension=".ffu")
    a=a.replace("/","\\")
    os.system('dism /apply-ffu /ImageFile="'+a+'" /ApplyDrive:\\\\.\\PhysicalDrive'+x)

    os.remove("clean_disk.txt")
    os.remove("list_disk_script.txt")
    PromptUtils(Screen()).enter_to_continue()

def wpe_shutdown():
    os.system("wpeutil shutdown")

def wpe_reboot():
    os.system("wpeutil reboot")

# Create the menu
menu = ConsoleMenu("FFU Maker", "Easily to backup/restore FFU \nThe source/target ssd Must be the same",epilogue_text="Copyright 2024 Compal Electronic Inc. All right reserved.\nDesigned by Software Application 17 and limited to be used in Compal internal only.")

###################################################################################
# Create some items

# MenuItem is the base class for all items, it doesn't do anything when selected
#menu_item = MenuItem("Menu Item")

# A FunctionItem runs a Python function when selected
#function_item = FunctionItem("Call a Python function", hello)

# A CommandItem runs a console command
#command_item = CommandItem("Run a console command",  "touch hello.txt")

# A SelectionMenu constructs a menu from a list of strings

#selection_menu = SelectionMenu([backup_wim,backup_wim2, backup_wim3])



# A SubmenuItem lets you add a menu (the selection_menu above, for example)
# as a submenu of another menu
#submenu_item = SubmenuItem("Submenu item", selection_menu, menu)

# Once we're done creating them, we just add the items to the menu
#menu.append_item(menu_item)
#menu.append_item(function_item)
#menu.append_item(command_item)
#menu.append_item(submenu_item)

##################################################################################
backup_wim = FunctionItem("Backup WIM",backup_wimfile)
restore_wim = FunctionItem("Restore WIM",restore_wimfile)
backup_ffu = FunctionItem("Backup FFU",backup_ffufile)
restore_ffu = FunctionItem("Restore FFU",restore_ffufile)
reboot = FunctionItem("Reboot System",wpe_reboot)
shutdown = FunctionItem("Shutdown System",wpe_shutdown)

menu.append_item(backup_wim)
menu.append_item(restore_wim)
menu.append_item(backup_ffu)
menu.append_item(restore_ffu)
menu.append_item(reboot)
menu.append_item(shutdown)

# Finally, we call show to show the menu and allow the user to interact
menu.show()