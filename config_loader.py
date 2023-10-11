#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import pathlib
import bpy

import os

def get_xml(path):
    tree = ET.parse(path)
    root = tree.getroot()
    
    if root.tag != "angry_export_config":
        return None
    return root
import bpy

def get_default(scene):
    cfg_path =  scene.AngryExportSystem_ConfigPath
    cfg_path = bpy.path.abspath(cfg_path)
    cfg_path = os.path.abspath(cfg_path)

    return Config(cfg_path)

class ExportTarget(object):
    def __init__(self, _unity_dir, _name):
        self.unity_dir = _unity_dir
        self.name = _name

class Config(object):
    def __init__(self, path):
        self.config_path = pathlib.PurePath(path)

        if not self.config_path.is_absolute():
            raise ValueError("Absolute paths are required")

        xml = get_xml(path)
        
        #as the xml loaded we know it was a path to a file so we can take part of the path for the directory
        parts = list(self.config_path.parts)[:-1]
        self.config_dir =  pathlib.PurePath(*parts)

        self.version = xml.attrib.get("version", None)
        self.version = int(self.version)

        self.unity_path =  xml.find("unity_directory").text

        self.export_targets = []

        for x in xml.findall("export_target"):
            name = x.attrib["name"]
            path = x.attrib["dir"]

            self.export_targets.append(ExportTarget(path, name))
        
    def xml_string(self):
        root = ET.Element("angry_export_config", {"version": self.version})
        def add_sub(tag, val):
            sub = ET.SubElement(root, tag)
            sub.text = val
            
        add_sub("unity_directory", self.unity_path)
        add_sub("base_export", self.base_export)
        add_sub("prop_export", self.prop_export)
        
        ET.indent(root)
        return ET.tostring(root).decode(encoding='utf-8')

    def get_target_entry(self, export_type):
        for x in self.export_targets:
            if x.name == export_type:
                return x

    def get_export(self, export_type):
        entry = self.get_target_entry(export_type)
        return os.path.join(self.get_unity_path(), entry.unity_dir)

    def get_unity_path(self):
        return self.config_dir / self.unity_path

if __name__ == "__main__":
    cfg = Config("../angry-export-system.xml")
    print("version", cfg.version)
    print("unity path", cfg.unity_path)
    print("base path", cfg.base_export)
    print("prop path", cfg.prop_export)
    
    print("save xml\n", cfg.xml_string(), sep='')
    
    
