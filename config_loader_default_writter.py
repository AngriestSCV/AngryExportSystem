import bpy
import os

class SCENE_OT_CreateConfig(bpy.types.Operator):
    bl_idname = "scene.angry_export_create_config"
    bl_label = "Angry Export Create Config"

    @classmethod
    def poll(cls, context):
        cfg_path = context.scene.AngryExportSystem_ConfigPath
        if os.path.exists(cfg_path):
            return False

        par_dir = os.path.dirname(cfg_path)
        if os.path.exists(par_dir):
            return True

        return False

    def execute(self, context):
        with open(context.scene.AngryExportSystem_ConfigPath, "w") as cfile:
            cfile.write(""" 
            <angry_export_config version="0">
                <unity_directory>unity</unity_directory>
                <export_target dir="Assets/base_export" name="base" />
                <export_target dir="Assets/blender_props" name="props" />
            </angry_export_config>
            """)

        return {'FINISHED'}
