# Copyright (C) 2020  Tomo Michigami

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import bpy
from bpy.props import *


bl_info = {
    "name": "BakeTextureSequence",
    "author": "Tomo Michigami",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Sidebar",
    "description": "Bake lighting onto texture sequence",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
}


class BAKETEXSEQ_OT_BakeTexSeq(bpy.types.Operator):
  bl_idname = "baketexseq.bake"
  bl_label = "BakeTexSeq"
  bl_options = {'REGISTER', 'UNDO'}
  
  #--- properties ---#
  inputfolderpath: StringProperty(default = "C:\\This\\Is\\Input\\Folder\\Path", options = {'HIDDEN'})
  outputfolderpath: StringProperty(default = "C:\\This\\Is\\Output\\Folder\\Path", options = {'HIDDEN'})
  prefix: StringProperty(default = "image_", options = {'HIDDEN'})
  startframe: IntProperty(default = 1, options = {'HIDDEN'})
  endframe: IntProperty(default = 250, options = {'HIDDEN'})
  
  
  def baketexseq(self):
    objs = bpy.context.selected_objects
    if not len(objs) > 0:
        self.report({'INFO'}, "Please select mesh sequence")
    else:
        mat = objs[0].material_slots[0].material
        node = mat.node_tree.nodes['Diffuse BSDF']
        link = node.inputs['Color'].links[0]


        for i in range(self.startframe, self.endframe+1):
            framenum = i
            self.report({'INFO'}, ("BAKING FRAME %d" % framenum))
            bpy.ops.object.bake(type='COMBINED', save_mode='INTERNAL') 
            texture = link.from_node.image
            newfilename = self.prefix + "%05d" % framenum + ".png"
            texture.save_render(filepath = bpy.path.abspath(self.outputfolderpath) + newfilename)
            framenum = i+1
            if framenum == self.endframe + 1:
                self.report({'INFO'}, ("BAKE FINISHED"))
            else:
                bpy.context.scene.frame_set(framenum)
                filename = self.prefix + "%05d" % framenum + ".png"
                new_img = bpy.data.images.load(filepath = bpy.path.abspath(self.inputfolderpath) + filename)
                node.inputs['Color'].links[0].from_node.image = new_img
            
            

  #--- execute ---#
  def execute(self, context):
    self.baketexseq()
    return {'FINISHED'}


class BAKETXSEQ_PT_BakePanel(bpy.types.Panel):
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'UI'
  bl_category = "BakeTexSeq"
  bl_label = "BakeTexSeq"

  #--- draw UI ---#
  def draw(self, context):
    layout = self.layout
    
    layout.prop(context.scene, "input_folder")
    layout.prop(context.scene, "output_folder")
    layout.prop(context.scene, "prefix")
    layout.prop(context.scene, "start_frame")
    layout.prop(context.scene, "end_frame")

    op_prop = layout.operator(BAKETEXSEQ_OT_BakeTexSeq.bl_idname, text = "Bake")
    op_prop.inputfolderpath = context.scene.input_folder
    op_prop.outputfolderpath = context.scene.output_folder
    op_prop.prefix = context.scene.prefix
    op_prop.startframe = context.scene.start_frame
    op_prop.endframe = context.scene.end_frame


classes = [
  BAKETXSEQ_PT_BakePanel,
  BAKETEXSEQ_OT_BakeTexSeq
]

#
# register
#
def register():
  for c in classes:
    bpy.utils.register_class(c)
    
  bpy.types.Scene.input_folder = StringProperty(default = "", subtype='DIR_PATH')
  bpy.types.Scene.output_folder = StringProperty(default = "", subtype='DIR_PATH')
  bpy.types.Scene.prefix = StringProperty(default = "Image_")
  bpy.types.Scene.start_frame = IntProperty(default = 1)
  bpy.types.Scene.end_frame = IntProperty(default = 250)
  

#
# unregister()
#    
def unregister():
  for c in classes:
    bpy.utils.register_class(c)
    
  del bpy.types.Scene.input_folder
  del bpy.types.Scene.output_folder

#
# script entry
#    
if __name__ == "__main__":
  register()