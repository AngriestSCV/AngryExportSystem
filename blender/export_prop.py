import bpy
import xml.etree.ElementTree as XmlEt
from . import file_paths
import os
import pathlib

class ExportProp(object):
    def register(self):
        setattr(bpy.types.Object, self.id, self.blender_property)
        pass

    def deregister(self):
        delattr(bpy.types.Object, self.id)
        pass

    """Add the property to the XML to be exported to Unity"""
    def add_to_export_xml(self, cfg, obj, root_xml):
        new_val = str(getattr(obj, self.id))
        component_xml = XmlEt.SubElement(root_xml, self.id, attrib={"value": new_val})
 
class PrefabLink(ExportProp):
    id = "AngryExportSystem_PrefabLink"
    name = "Prefab Link"
    description = "The path to the prefab to replace this object with"
    blender_property = bpy.props.StringProperty(
        name="PrefabLink",
        subtype="FILE_PATH",
        override = {"LIBRARY_OVERRIDABLE"}
    )

    def add_to_export_xml(self, cfg, obj, root_xml):
        def vprint(s):
            pass
            #print(s)

        vprint(f"Working on {obj.name}")
        prefab = str(getattr(obj, self.id))
        vprint(f"Starting prefab: {prefab}")
        prefab = bpy.path.abspath(prefab)
        vprint(f"blender abs: {prefab}")
        prefab = prefab.replace("\\", "/")
        vprint(f"Normalize slashes: {prefab}")
        prefab = pathlib.PurePath(prefab)
        vprint(f"Abs prefab: {prefab}")

        prefab = file_paths.path_to_unity_path(cfg, prefab)
        vprint(f"Updated prefab: {prefab}")
        component_xml = XmlEt.SubElement(root_xml, self.id, attrib={"value": prefab})
        
        prefab = os.path.join(cfg.config_dir, cfg.unity_path, prefab)
        print(f"update join: {prefab}")
        prefab = bpy.path.relpath(prefab)
        print(f"new rel path:", prefab)
        setattr(obj, self.id, prefab)

class Render(ExportProp):
    id = "AngryExportSystem_Render"
    name = "Render"
    description = "To enable / disable render generation in Unity"
 
    blender_property = bpy.props.BoolProperty(
        name="Render",
        default = False,
    )

class Collider(ExportProp):
    id = "AngryExportSystem_Collider"
    name = "Collider"
    description = "The unity Colider object that will be added"
 
    blender_property = bpy.props.EnumProperty(
        name = "Collider",
        description = "Unity collider type to add",
        override = {"LIBRARY_OVERRIDABLE"},
        items = [
            ("None", "None", "No collider"),
            ("Mesh", "Mesh", "Concave Mesh Collider"),
            ("Box", "Box", "Bounding box collider"),
        ],
        default = "Box"
    )

class StaticFlags(ExportProp):
    _flag_source = [
        ("ContributeGI", "ContributeGI", "ContributeGI"),
        ("LightmapStatic", "Light Map Static", "Light Map Static"),
        ("OccluderStatic", "OccluderStatic", "OccluderStatic"),
        ("BatchingStatic", "Batching Static", "Batching Static"),
        ("NavigationStatic", "Navigation Static", "Navigation Static"),
        ("OccludeeStatic", "OccludeeStatic", "OccludeeStatic"),
        ("OffMeshLinkGeneration", "Off Mesh Link Generation", "Off Mesh Link Generation"),
        ("ReflectionProbeStatic", "Reflection Probe Static", "Reflection Probe Static"),
    ]

    id = "AngryExportSystem_StaticFlags"
    name = "Static Flags"
    description = "The static flags used on this object and it's children"
 
    blender_property = bpy.props.EnumProperty(
        name="Static Flags",
        description = "Static flags",
        override = {"LIBRARY_OVERRIDABLE"},
        items = _flag_source,
        options = {"ENUM_FLAG"},
    )
    
    """Add the property to the XML to be exported to Unity"""
    def add_to_export_xml(self, cfg, obj, root_xml):
        new_val = getattr(obj, self.id)
        component_xml = XmlEt.SubElement(root_xml, self.id)
        for flag in new_val:
            flag_xml = XmlEt.SubElement(component_xml, "flag")
            flag_xml.text = flag
            
class LightmapScale(ExportProp):
    id = "AngryExportSystem_LightmapScale"
    name = "Lightmap Scale"
    description = "The scale to use on this object for light mapping"

    blender_property = bpy.props.FloatProperty(
        name="Lightmap Scale",
        description = "Scale of render in lightmap",
        min = 0.0,
        soft_max = 10,
        max = 1000,
        precision = 3,
        default = 1.0,
        override = {"LIBRARY_OVERRIDABLE"}
    )
    
all_properties = [
    PrefabLink(),
    Render(),
    Collider(),
    StaticFlags(),
    LightmapScale(),
]
