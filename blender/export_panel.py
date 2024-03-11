import bpy, os

from . import config_loader
from . import export_prop
from . import exporter

class VIEW3D_PT_angry_export_panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AES"
    bl_label = "Angry Export System"

    def _draw_collection(self, context):
        layout = self.layout.box()
        col = bpy.context.collection

        if col is None:
            layout.label(text="- No active collection -")
        else:
            layout.label(text=f"Collection: {col.name}")
            
            if 'AngryExport_Show' in col:
                to_show = obj['AngryExport_Show']
            else:
                to_show = {}
                
        #export options
        col = layout.column()
        if exporter.COLLECTION_OT_Angry_Exporter.poll(context):

            cfg = config_loader.get_default(context.scene)

            for target in cfg.export_targets:
                export_name = exporter.COLLECTION_OT_Angry_Exporter.get_export_name(context)
                arg = col.operator("object.angry_exporter", text=f"Export: {target.name}")
                arg.export_type = target.name

        else:
            col.label(text="Invalid name for export collection")
        return True

    def _draw_config(self, context):
        layout = self.layout 
        layout.prop(context.scene, "AngryExportSystem_ConfigPath")
        cfg_path = context.scene.AngryExportSystem_ConfigPath
        cfg_path = bpy.path.abspath(cfg_path)

        if not os.path.exists(cfg_path):
            layout.operator("scene.angry_export_create_config", text="Create missing config")
            return False
        return True

    def _draw_object(self, context):
        layout = self.layout.box()
        obj = bpy.context.active_object

        if obj is None:
            layout.label(text="- No active object -")
        else:
            layout.label(text=f"Object: {obj.name}")
            
            if 'AngryExport_Show' in obj:
                to_show = obj['AngryExport_Show']
            else:
                to_show = {}
                
            def show_section(custom_prop):
                if to_show.get(custom_prop, False):
                    row = layout.row()
                    row.prop(obj, custom_prop)
                    
                    row2 = row.row()
                    row2.alignment = "RIGHT"
                    props = row2.operator("object.angry_export_add_property", text="X")
                    props.adding = False
                    props.prop_name = custom_prop
                else:
                    pass
                    #row = layout.row()
                    #row.label(text=f"{custom_prop} not shown")
                
            for x in export_prop.all_properties:
                try:
                    show_section(x.id)
                except Exception as e:
                    print("Exception:", e)

            props = layout.operator_menu_enum("object.angry_export_add_property", "prop_name")
            props.adding = True

        return True


    def draw(self, context):
        layout = self.layout

        if not self._draw_config(context):
            return

        if not self._draw_collection(context):
            return

        if not self._draw_object(context):
            return
        
