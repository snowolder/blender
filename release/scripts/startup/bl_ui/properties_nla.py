# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>
import bpy 
from bpy.types import Panel
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       EnumProperty,
                       PointerProperty,
                       CollectionProperty,
                       FloatVectorProperty,
                       IntVectorProperty,
                       )
def get_active_strip(context):
    items =  [strip for strip in context.selected_nla_strips if strip.active]
    return items[0] if items else None 

class OBJECT_OT_nla_add_preblend(bpy.types.Operator):
    bl_idname = "object.nla_add_preblend"
    bl_label = "Add Preblend Transform"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls,context):
        return context.selected_nla_strips

    def execute(self, context):
        active_strip = get_active_strip(context)
        print(dict(active_strip.preblend_transforms))
        k = active_strip.preblend_transforms.add()

        # print(k.path_from_id("location"))
        # print(active_strip.path_resolve("preblend_transforms"))
        # print(k.id_data)
        return {'FINISHED'}
class OBJECT_OT_nla_remove_preblend(bpy.types.Operator):
    bl_idname = "object.nla_remove_preblend"
    bl_label = "Remove Preblend Transform"
    bl_options = {'REGISTER', 'UNDO'}

    preblend_index : IntProperty()

    @classmethod
    def poll(cls,context):
        return context.selected_nla_strips

    def execute(self, context):
        active_strip = get_active_strip(context)
        active_strip.preblend_transforms.remove_at(self.preblend_index)

        return {'FINISHED'}

class OBJECT_OT_nla_preblend_add_bone(bpy.types.Operator):
    bl_idname = "object.preblend_add_bone"
    bl_label = "Preblend Add Bone"
    bl_options = {'REGISTER', 'UNDO'}

    preblend_index : IntProperty()

    @classmethod
    def poll(cls,context):
        return context.selected_nla_strips

    def execute(self, context):
        active_strip = get_active_strip(context)
        preblend = active_strip.preblend_transforms[self.preblend_index]
        bone = preblend.bones.add()
        bone.name ="Hips"
        return {'FINISHED'}
class OBJECT_OT_nla_preblend_remove_bone(bpy.types.Operator):
    bl_idname = "object.preblend_remove_bone"
    bl_label = "Preblend Remove Bone"
    bl_options = {'REGISTER', 'UNDO'}

    preblend_index : IntProperty()
    bone_index : IntProperty()

    @classmethod
    def poll(cls,context):
        return context.selected_nla_strips

    def execute(self, context):
        active_strip = get_active_strip(context)
        preblend = active_strip.preblend_transforms[self.preblend_index]
        preblend.bones.remove_at(self.bone_index)

        return {'FINISHED'}

class OBJECT_PT_nla_alignment(Panel):
    bl_space_type = 'NLA_EDITOR'
    bl_region_type = 'UI'
    bl_label = "Alignment"
    bl_category = "Alignment"
    bl_context = "object"
    

    def draw(self, context):
        #Q:   not in a poll() so it doesnt disappear on nla strip deselection (annoying)
        if not context.selected_nla_strips:
            return 

        layout = self.layout
        active_strip = get_active_strip(context)


        layout.prop(active_strip,"preblend_transforms")
        
        layout.prop(active_strip,"frame_start")
        layout.prop(context.active_object,"location")
        layout.prop(context.active_object.pose.bones["Hips"],"location")
        if(context.active_pose_bone):
            c = context.active_pose_bone.constraints
            if(c):
                layout.prop(c[0],'type')
        layout.operator(OBJECT_OT_nla_add_preblend.bl_idname,text='New Transform',icon='ADD')
        box = layout.box()
        for i,preblend in enumerate(active_strip.preblend_transforms):
            row = box.row(align=True)
            row.label(text="World Transform")
            row.operator(OBJECT_OT_nla_remove_preblend.bl_idname,text='',icon='REMOVE').preblend_index = i 

            box.prop(preblend,"location")
            box.prop(preblend,"euler")
            box.prop(preblend,"scale")

            col = box.column(align=True)
            row = col.row(align=True)
            #todo: support for objects?
            row.label(text="Bones")
            row.operator(OBJECT_OT_nla_preblend_add_bone.bl_idname,text='',icon='ADD').preblend_index = i 
            for j,bone in enumerate(preblend.bones):
                row = col.row(align=True)
                # print([b for b in context.active_object.data.bones])
                # row.prop_search(bone,"name",context.active_object.data,"bones",text='')
                row.prop(bone,"name")
                op = row.operator(OBJECT_OT_nla_preblend_remove_bone.bl_idname,text='',icon='REMOVE')
                op.preblend_index = i 
                op.bone_index = j 


classes = (
    # Object Panels
    OBJECT_PT_nla_alignment,
    OBJECT_OT_nla_add_preblend,
    OBJECT_OT_nla_remove_preblend,
    OBJECT_OT_nla_preblend_remove_bone,
    OBJECT_OT_nla_preblend_add_bone,
)

if __name__ == "__main__":  # only for live edit.
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
