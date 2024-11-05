import tkinter.filedialog #import to create windows for files
from unreal import ToolMenus,ToolMenuContext, ToolMenuEntryScript,uclass,ufunction #importing functions from unreal
import sys #importing system enviroment
import os #importing operating system
import importlib #importing python module tools
import tkinter #import to create windows


srcDir = os.path.dirname(os.path.abspath(__file__)) #gives exact location of script
if srcDir not in sys.path: #if cant find loaction fof script in path
    sys.path.append(srcDir) #find it



import UnrealUtilities #importing utilities from unreal
importlib.reload(UnrealUtilities) #reload unreal utilities after importing importlib


@uclass() #defining class to be used as a class in unreal engine
class LoadFromDirEntryScript(ToolMenuEntryScript):
    @function(override = True) #needed for unreal engine to use function
    def execute(self,context): #run this class with these parameters being the context
        window = tkinter.Tk() #create a tkinter window 
        window.withdraw()  #hides tkinter window
        fileDir = tkinter.filedialog.askdirectory() #choosing folder using file dialog
        window.destroy() #destroys tkinter window
        UnrealUtilities.UnrealUtiity().LoadFromDir(fileDir) #using function LoadFromDir from other script UnrealUtilities


@uclass() #defining class to be used as a class in unreal engine
class BuildBaseMaterialEntryScript(ToolMenuEntryScript): #building base material entry script using tool menu entry script
    @ufunction(override=True) #needed for unreal engine to use function
    def execute(self,context:ToolMenuContext) -> None: #make tool menu context
        UnrealUtilities.UnrealUtility().FindOrCreateBaseMaterial() #execute unreal utility in find or create base material in tool menu


class UnrealSubstancePlugin: #creating plugin in unreal
    def __init__ (self): #making object in unreal substance plugin
        self.subMenuName = "SubstancePlugin" #name of the menu will be called substance plugin
        self.subMenuLabel = "Substance Plugin" #the menu label will be called substance plugin
        self.InitUI() #adding to the UI

    def InitUI(self):  #creating button in UI in unreal engine
        mainMenu = ToolMenus.get().find_menu("LevelEditor.MainMenu") #opening level editor in main menu
        self.subMenu = mainMenu.add_sub_menu(mainMenu.menu_name,"","SubstancePlugin","Substance Plugin") #making submenu
        self.AddEntryScript("BuildBasematerial", "Build Base Material", BuildBaseMaterialEntryScript()) #What the button will be called, do, and the function the button has from buildbasematerialentry script
        ToolMenus.get().refresh_all_widgets() #update UI

        
        self.AddEntryScript("LoadFromDir", "Load From Directory", LoadFromDirEntryScript()) #adding identifier and explaination to object from load directory entry script
        ToolMenus.get().refresh_all_widgets() #updates UI

    def AddEntryScript(self,name,label,script: ToolMenuEntryScript): #adding attributes to object in tool menu entry script such as the name,label, and script of object
        script.init_entry(self.subMenu.menu_name,self.subMenu.menu_name,"",name,label) #starting menu entry with the attributes of the name and label of each object within the menu
        script.register_menu_entry() #create this menu entry

UnrealSubstancePlugin() #run the code

