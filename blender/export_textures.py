#!/usr/bin/env python3
import os, sys
import bpy


def export_textures_for_objects(texture_path: str, cfg, to_save: list[bpy.types.Object]):
    os.makedirs(texture_path, exist_ok=True)

    images = set()

    if len(to_save) == 0:
        print("Nothing to save textures for")
        return

    for obj in to_save:
        #print("testure exporting object", obj.name)
        slots = obj.material_slots
        for slot in slots:
            mat = slot.material
            #print("testure exporting material", mat.name)
            images = images.union( extract_material_images(mat))

    save_images(texture_path, images)

# Function to extract images used in a material
def extract_material_images(material: bpy.types.Material):
    images = set()
    if material.node_tree:
        for node in material.node_tree.nodes:
            if node.type == 'TEX_IMAGE':
                if node.image:
                    #print("found image", node.image.name)
                    images.add(node.image)
    return images

# Function to save images to a directory
def save_images(path, images: set[bpy.types.Image]):
    #print("To save images", images)
    for image in images:
        image_copy = image.copy()
        fname = image.name
        if not fname.endswith(".png"):
            fname += ".png"
        image_copy.file_format = 'PNG'
        image_copy.save_render(os.path.join(path, fname))

