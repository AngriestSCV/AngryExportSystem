from importlib import reload

import bpy
from bpy.path import abspath

import os, re
import xml.etree.ElementTree as XmlEt

if "config_loader" in locals(): reload(config_loader)
if "file_paths" in locals(): reload(file_paths)
if "export_prop" in locals(): reload(export_prop)
if "export_panel" in locals(): reload(export_panel)
if "config_loader_default_writter" in locals(): reload(config_loader_default_writter)
if "exporter" in locals(): reload(exporter)

from . import config_loader
from . import config_loader_default_writter
from . import file_paths
from . import export_prop
from . import export_panel
from . import exporter

bl_info = {
    "name": "Angry Export System",
    "blender": (3,5,1),
    "category": "Object",
    "description": "Export System for Unity world development",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
}

def get_export_items(self, context):
    all_props = export_prop.all_properties 
    
    for prop in all_props:
        id = prop.id
       
        if hasattr(prop, "name"):
            name = prop.name
        else:
            name = id
            
        if hasattr(prop, "description"):
            desc = prop.description
        else:
            desc = id

        yield (id, name, desc)

class OBJECT_OT_AddExportProperty(bpy.types.Operator):
    bl_idname = "object.angry_export_add_property"
    bl_label = "Angry Export Add Property"

    prop_name: bpy.props.EnumProperty(
        name="Prop Name",
        description = "Name of property to add",
        items = get_export_items
    )

    adding: bpy.props.BoolProperty(
        name="Add the property",
        description = "If true add the property",
        default = True,
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        if 'AngryExport_Show' not in context.active_object:
            context.active_object['AngryExport_Show'] = {}

        dd = context.active_object['AngryExport_Show']
        
        if self.adding:
            dd[self.prop_name] = self.adding
        elif self.prop_name in dd:
            del dd[self.prop_name]
            
        return {'FINISHED'}

   

addon_types = [
    export_panel.VIEW3D_PT_angry_export_panel,
    OBJECT_OT_AddExportProperty,
    exporter.OBJECT_OT_Angry_Exporter,
    config_loader_default_writter.SCENE_OT_CreateConfig,
    ]

def register():
    for prop in export_prop.all_properties:
        prop.register()

    bpy.types.Scene.AngryExportSystem_ConfigPath = bpy.props.StringProperty(
        name="Angry Export Config Path",
        subtype="FILE_PATH",
    )

    for x in addon_types:
        bpy.utils.register_class(x)

def unregister():
    for prop in export_prop.all_properties:
        prop.deregister()

    del bpy.types.Scene.AngryExportSystem_ConfigPath 

    for x in addon_types:
        bpy.utils.unregister_class(x)
        
        
if __name__ == "__main__":
    register()
