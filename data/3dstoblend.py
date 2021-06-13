#!/usr/bin/env python3

import os
import bpy
from sys import argv

context = bpy.context

# arguments #
# [blender, --background, --python, script, 3ds]
# model_path = argv[4]

# prepare scene #

for obj in context.scene.objects:
	obj.select = True

bpy.ops.object.delete()

# import #

export_model = argv[4]
bpy.ops.import_scene.autodesk_3ds(filepath=export_model)

# join objects #

context.scene.objects.active = context.selected_objects[0]
bpy.ops.object.join()

# normalize transforms #
bpy.ops.object.transform_apply(
	location = True,
	rotation = True,
	scale = True
)

# add smooth shade and edge split modifiers #

bpy.ops.object.shade_smooth()
bpy.ops.object.modifier_add(
	type = "EDGE_SPLIT"
)

# remove doubles #

bpy.ops.object.editmode_toggle()
bpy.ops.mesh.remove_doubles()

# remove loose vertices #

bpy.ops.mesh.select_loose()
bpy.ops.mesh.delete(type='VERT')

bpy.ops.mesh.normals_make_consistent(
	inside = False
)
bpy.ops.object.editmode_toggle()

# Set light

def add_light(name, pos):
    # create light datablock, set attributes
    light_data = bpy.data.lamps.new(name=name, type='POINT')
    light_data.energy = 30

    # create new object with our light datablock
    light_object = bpy.data.objects.new(name=name, object_data=light_data)

    # link light object
    bpy.context.scene.objects.link(light_object)

    # make it active 
    bpy.context.scene.objects.active = light_object

    # change location
    light_object.location = pos

add_light("light1", (50,50,50))
add_light("light2", (0,50,0))
add_light("light3", (0,0,50))

# Set camera

from math import radians

cam1 = bpy.data.cameras.new("Camera")
cam1.lens = 35
cam_obj1 = bpy.data.objects.new("Camera", cam1)
cam_obj1.location = (30/(2**.5), -30, 30/(2**.5))
cam_obj1.rotation_euler = (radians(0), radians(60), radians(-55))
context.scene.objects.link(cam_obj1)
context.scene.camera = context.object
bpy.context.scene.camera = bpy.data.objects['Camera']

# save #

blend_file = export_model.replace(".3ds",".blend")
bpy.ops.wm.save_as_mainfile(
	filepath = blend_file,
	compress = True
)

# render #

print("saved as:", blend_file)

bpy.ops.render.render(write_still=True)

bpy.ops.wm.quit_blender()
PYTHON
