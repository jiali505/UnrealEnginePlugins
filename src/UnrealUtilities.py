from unreal import (AssetToolsHelpers,AssetTools,EditorAssetLibrary,Material,MaterialFactoryNew,MaterialProperty,MaterialEditingLibrary,MaterialExpressionTextureSampleParameter2D as TexSample2D,AssetImportTask,FbxImportUI
)#imports from unreal into python code
import os #importing operating system

class UnrealUtiity: #maing subfolder for substance materials in unreal content drawer
    def __init__(self): #making an object in unreal utility
        self.substanceRootDir = "/game/Substance/" #making folder for substance in content drawer
        self.baseMaterialsName = "M_SubstanceBase" #making folder for base materials in content drawer
        self.substanceTempDir = "game/Substance/Temp/" #temporary folder in content drawer

        self.baseMaterialPath = self.substanceRootDir + self.baseMaterialsName #substance base material name is in substance root directory
        self.baseColorName = "BaseColor" #what base colors will be named
        self.occRoughnessMetalicName = "OcclusionRoughnessMetalic" #what rough, metalic, and ao will be named
        self.normalName = "Normal" #what normal map will be named
    def FindOrCreateBaseMaterial(self): #going to check if basematerial is there
        if EditorAssetLibrary.does_asset_exist(self.baseMaterialPath): # going to check if base material exists already in unreal content drawer
            return EditorAssetLibrary.load_asset(self.baseMaterialPath) #if base material is made just return it because it already exists
        
        baseMat = AssetToolsHelpers.get_asset_tools().create_asset(self.baseMaterialsName,self.substanceRootDir,Material,MaterialFactoryNew())

        baseColor = MaterialEditingLibrary.create_material_expression(baseMat,TexSample2D,-800,0) #making normal expression on material for basecolor 
        baseColor.set_editor_property("parameter_name",self.baseColorName) #finding basecolor
        MaterialEditingLibrary.connect_material_property(baseColor, "RGB", MaterialProperty.MP_BASE_COLOR) #connecting in node editor the base color of the basecolor map to material

        normal = MaterialEditingLibrary.create_material_expression(baseMat,TexSample2D,-800,400) #making normal expression on material for normal map
        normal.set_editor_propery("parameter name", self.normalName) #finding normal map
        normal.set_editor_property("texture", EditorAssetLibrary.load_asset("/Engine/EngineMaterials/DefaultNormal")) #using texture in unreal engine materials for normal
        MaterialEditingLibrary.connect_material_property(normal, "RGB", MaterialProperty.MP_NORMAL) #connecting normal map in material

        occRoughnessMetalic = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800,800) #making roughness, metalic, and ao expression for material
        occRoughnessMetalic.set_editor_property("parameter name", self.occRoughnessMetalicName) #finding occroughnessmetalicname
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "R", MaterialProperty.MP_AMBIENT_OCCLUSION) #connecting ambient occlusion in R in material
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "G", MaterialProperty.MP_ROUGHNESS) #connecting roughness in  G in material
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic,"B", MaterialProperty.MP_METALLIC) #connecting metallic in  B in material

        EditorAssetLibrary.save_asset(baseMat.get_path_name()) #saving asset within same location
        return baseMat #returning the base material
    
    def LoadMeshFromPath(self,meshPath): #loading mesh using the meshpath
        meshName = os.path.split(meshPath)[-1].replace(".fbx","")  #extracting and giving name to the mesh
        importTask = AssetImportTask() #import will be imported into unreal
        importTask.replace_existing = True #if import exists it will replace same one
        importTask.filename = meshPath #what import will be named
        importTask.destination_path = "/game/" + meshName #where import will be stored in unreal
        importTask.save = True #the import will be saved
        importTask.automated = True  #import will run automatically

        fbxImportOptions = FbxImportUI() #Import UI of fbx file when fbx is processed
        fbxImportOptions.import_mesh = True #enabling the import of the mesh from the fbx file
        fbxImportOptions.import_as_skeletal = False #disabling the import skeletal from the fbx file when its processed
        fbxImportOptions.import_materials = False #disabling the import materials from the fbx file when its processed
        fbxImportOptions.static_mesh_import_data.combine_meshes = True #Import mesh data and combined meshes when fbx file is processed

        importTask.options = fbxImportOptions #imported task is the impoted fbx file

        AssetToolsHelpers.get_asset_tools().import_asset_tasks([importTask]) #using asset tools create objects using import task
        return importTask.get_objects()[0] #returning objects that were created

    def LoadFromDir(self,fileDir): #loading from directory
        for file in os.listdir(fileDir): #finding file in a list in our directory
            if ".fbx" in file: #finding FBX within files
                self.LoadMeshFromPath(os.path.join(fileDir,file)) #if fbx file is found add it to file directory path