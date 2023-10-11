import bpy

class AngryExportProp(object):
    def register(self):
        setattr(bpy.types.Object, self.prop_name, self.blender_property)
        pass

    def deregister(self):
        delattr(bpy.types.Ob, self.prop_name)
        pass

    """Add the property to the XML to be exported to Unity"""
    def add_to_export_xml(self, obj, root_xml):
        new_val = str(getattr(obj, self.prop_name))
        component_xml = XmlEt.SubElement(root_xml, self.prop_name, attrib={"value": new_val})
 
class PrefabLink(AngryExportProp):
    prop_name: "AngryExportSystem_PrefabLink"
    blender_property: bpy.props.StringProperty(
        name="PrefabLink",
        subtype="FILE_PATH"
    )

    def add_to_export_xml(self, obj, root_xml):
        #print(f"Working on {obj.name}")
        prefab = str(getattr(obj, self.prop_name))
        #print(f"Starting prefab: {prefab}")
        prefab = bpy.path.abspath(prefab)
        #print(f"Abs prefab: {prefab}")
        prefab = file_paths.path_to_unity_path(cfg, prefab)
        #print(f"Updated prefab: {prefab}")
        component_xml = XmlEt.SubElement(root_xml, prop_name, attrib={"value": prefab})
        
        prefab = os.path.join(cfg.config_dir, cfg.unity_path, prefab)
        #print(f"update join: {prefab}")
        prefab = bpy.path.relpath(prefab)
        #print(f"new rel path:", prefab)
        setattr(obj, prop_name, prefab)


class Render(AngryExportProp):
    prop_name: "AngryExportSystem_Render"
    blender_property: bpy.props.BoolProperty(
        name="Render",
        default = False,
    )

class Collider(AngryExportProp):
    prop_name: "AngryExportSystem_Collider"
    blender_property: bpy.props.EnumProperty(
        name = "Collider",
        description = "Unity collider type to add",
        items = [
            ("None", "None", "No collider"),
            ("Mesh", "Mesh", "Concave Mesh Collider"),
            ("Box", "Box", "Bounding box collider"),
        ],
        default = "Box"
    )

all_properties = [
    PrefabLink(),
    Render(),
    Collider(),
]