from importlib import reload


if "export_textures" in locals(): reload(export_textures)

import bpy, os
import re
import xml.etree.ElementTree as XmlEt
import time

from . import config_loader
from . import export_prop
from . import export_textures

export_regex = re.compile(r"export:\s*(.*)")

def export_options(self, context):
    cfg = config_loader.get_default(context.scene)
    for target in  cfg.export_targets:
        yield (target.name, target.name, target.name)

def export_collection(context: bpy.types.Context, col: bpy.types.Collection, export_type):
    fname = export_regex.match(col.name).groups(1)[0]

    cfg_path = context.scene.AngryExportSystem_ConfigPath
    cfg_path = bpy.path.abspath(cfg_path)
    cfg = config_loader.Config(cfg_path)

    output_dir = cfg.get_export(export_type)
    save_path = os.path.join(output_dir, f"{fname}.fbx")
    xml_path = os.path.join(output_dir, f"{fname}.fbx.xml")
    
    os.makedirs(output_dir, exist_ok=True)

    for obj in col.all_objects:
        obj.select_set(True)

    to_save = _get_selected(context)
    print(f"Found {len(to_save)} items to work with")
    _create_xml(xml_path, cfg, to_save)

    texture_path = os.path.join(output_dir, "textures")
    export_textures.export_textures_for_objects(texture_path, cfg, to_save)

    print("Saving FBX at", save_path)
    bpy.ops.export_scene.fbx(
        filepath = save_path,
        use_active_collection=True,
        apply_scale_options='FBX_SCALE_UNITS',
        object_types={'EMPTY', 'CAMERA', 'LIGHT', 'ARMATURE', 'MESH', 'OTHER'},
        use_mesh_modifiers=True)

def _get_selected(context: bpy.types.Context) -> list[bpy.types.Object]:
    selected = [ o for o in context.selected_objects ]
    return selected

def _create_xml(xml_path: str, cfg: config_loader.Config, to_save: list[bpy.types.Object]) -> None:
    base_xml = XmlEt.Element("Objects")

    for obj in to_save:
        if 'AngryExport_Show' in obj:
            to_show = obj['AngryExport_Show']
        else:
            continue

        root_xml = XmlEt.Element("Object")
        name_xml = XmlEt.SubElement(root_xml, "blender_name", attrib={"value": obj.name})

        for prop in export_prop.all_properties:
            id = prop.id

            if to_show.get(id, False):
                prop.add_to_export_xml(cfg, obj, root_xml)
        
        base_xml.append(root_xml)

    XmlEt.indent(base_xml, space='    ', level=0)
    as_string =  XmlEt.tostring(base_xml, encoding="utf-8").decode('utf-8')

    with open(xml_path, "w") as ff:
        #print(as_string)
        ff.write(as_string)



class COLLECTION_OT_Angry_Exporter(bpy.types.Operator):
    bl_idname = "collection.angry_exporter"
    bl_label = "Angry Export Base Object"

    export_type: bpy.props.EnumProperty(
        name="Prop Name",
        description = "Name of property to add",
        items = export_options
    )

    @classmethod
    def poll(cls, context):
        col = context.collection
        if col is None: return False
        return export_regex.match((col.name))
    
    @classmethod
    def get_export_name(cls, context):
        col = context.collection
        if col is None: return None
        match = export_regex.match((col.name))
        if match is None: return None
        
        return match.groups(1)[0]
            

    def execute(self, context: bpy.types.Context):
        selected = _get_selected(context)
        start_time = time.time()
        try:
            bpy.ops.object.select_all(action='DESELECT')
            col = context.collection
            if col is None: 
                return {"CANCELLED"}

            export_collection(context, col, self.export_type)

            end_time = time.time()
            print(f"Total Angry Export time for collection {col}", end_time - start_time )

        except Exception as e:
            print(e)
            raise

        finally:
            bpy.ops.object.select_all(action='DESELECT')
            for x in selected:
                x.select_set(True)
            
        return {'FINISHED'}
 
