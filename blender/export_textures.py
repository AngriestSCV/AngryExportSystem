#!/usr/bin/env python3
import os, sys
import bpy
import time
import shutil


def export_textures_for_objects(texture_path: str, cfg, to_save: list[bpy.types.Object]):
    start_time = time.time()

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
    
    images_found = time.time()
    save_images(texture_path, images)
    end_time = time.time()

    time_to_find = images_found - start_time
    time_to_save = end_time - images_found

    print("image find time:", time_to_find, "image save time:", time_to_save)

# Function to extract images used in a material
def extract_material_images(material: bpy.types.Material):
    images = set()
    if material is None:
        return images
    if material.node_tree:
        for node in material.node_tree.nodes:
            if node.type == 'TEX_IMAGE':
                if node.image:
                    #print("found image", node.image.name)
                    images.add(node.image)
    return images

# Function to save images to a directory
def save_images(path, images):

    for image in images:
        save_one_image(image, path)

def save_one_image(image: bpy.types.Image, path: str):
    new_path = os.path.join(path, image.name)

    if not try_copy_image(image, new_path):
        print("Failed to cpy image from", image.name)
        if not new_path.endswith(new_path):
            new_path += ".png"
        image.save(filepath=new_path)


def try_copy_image(image: bpy.types.Image, new_path:str):
    old_path = bpy.path.abspath(image.filepath)

    if not os.path.exists(old_path):
        return False

    try:
        print("Copying from", old_path, "to", new_path)
        shutil.copyfile(old_path, new_path)
        return True
    except Exception as e:
        print("Exception copying image", old_path, e)
        return False

