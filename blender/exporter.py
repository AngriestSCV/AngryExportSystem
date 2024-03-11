import bpy, os
import re
import xml.etree.ElementTree as XmlEt

from . import config_loader
from . import export_prop

def export_options(self, context):
    cfg = config_loader.get_default(context.scene)
    for target in  cfg.export_targets:
        yield (target.name, target.name, target.name)

class COLLECTION_OT_Angry_Exporter(bpy.types.Operator):
    bl_idname = "collection.angry_exporter"
    bl_label = "Angry Export Base Object"
    export_regex = re.compile(r"export:\s*(.*)")

    export_type: bpy.props.EnumProperty(
        name="Prop Name",
        description = "Name of property to add",
        items = export_options
    )

    @classmethod
    def poll(cls, context):
        col = context.collection
        if col is None: return False
        return cls.export_regex.match((col.name))
    
    @classmethod
    def get_export_name(cls, context):
        col = context.collection
        if col is None: return None
        match = cls.export_regex.match((col.name))
        if match is None: return None
        
        return match.groups(1)[0]
            
    def update_properties(self, cfg, obj_list):
        for obj in obj_list:
            if 'AngryExport_Show' in obj:
                to_show = obj['AngryExport_Show']
            else:
                continue

            root_xml = XmlEt.Element("Components")
            name_xml = XmlEt.SubElement(root_xml, "blender_name", attrib={"value": obj.name})

            for prop in export_prop.all_properties:
                id = prop.id

                if to_show.get(id, False):
                    prop.add_to_export_xml(cfg, obj, root_xml)
                elif id in obj:
                    print(f"Purgin [{id}] on [{obj.name}]")
                    del obj[id]

            as_string =  XmlEt.tostring(root_xml, encoding="utf-8").decode('utf-8')
            obj["AngryExportSystem_Xml"] = as_string
            print(f"Setting xml to: [{as_string}]")

    def _get_selected(self, context: bpy.types.Context):
        selected = [ o for o in context.selectable_objects ]
        return selected

        
    def execute(self, context: bpy.types.Context):
        selected = self._get_selected(context)
        try:
            bpy.ops.object.select_all(action='DESELECT')
            col = context.collection
            if col is None: 
                return {"CANCELLED"}
            
            fname = self.export_regex.match(col.name).groups(1)[0]

            cfg_path = context.scene.AngryExportSystem_ConfigPath
            cfg_path = bpy.path.abspath(cfg_path)
            cfg = config_loader.Config(cfg_path)

            output_dir = cfg.get_export(self.export_type)
            save_path = os.path.join(output_dir, f"{fname}.fbx")
            xml_path = os.path.join(output_dir, f"{fname}.fbx.xml")
            
            #self.update_properties(cfg, col.objects)
            
            os.makedirs(output_dir, exist_ok=True)

            for obj in bpy.data.objects:
                if col.name in obj.users_collection:
                    print(obj.users_collection)
                    obj.select_set(True)

            to_save = self._get_selected(context)
            print(f"Found {len(to_save)} items to work with")
            self._create_xml(xml_path, cfg, to_save)

            print("Saving FBX at", save_path)
            bpy.ops.export_scene.fbx(
                filepath = save_path,
                use_active_collection=True,
                apply_scale_options='FBX_SCALE_UNITS',
                use_mesh_modifiers=True)

        except Exception as e:
            print(e)
            raise

        finally:
            bpy.ops.object.select_all(action='DESELECT')
            for x in selected:
                x.select_set(True)
            
        return {'FINISHED'}
 

    def _create_xml(self, xml_path: str, cfg: config_loader.Config, to_save: list[bpy.types.Object]) -> None:
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

