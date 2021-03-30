# Copyright Wuguyannian All Rights Reserved.

import bpy

from .functions import scene
from .functions import templates

class RemoveTemplateFolder(bpy.types.Operator):
    """Remove this template from the addon"""
    bl_idname = "ueskeleton.remove_template_folder"
    bl_label = "Delete this template?"

    def execute(self, context):
        properties = bpy.context.window_manager.ueskeleton
        templates.remove_template_folder(properties)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_confirm(self, event)

class ConvertToEpicSkeleton(bpy.types.Operator):
    """Convert the source skeleton to a epic skeleton"""
    bl_idname = "ueskeleton.convert_to_epic_skeleton"
    bl_label = "Convert"

    def execute(self, context):
        properties = bpy.context.window_manager.ueskeleton
        scene.convert_to_epic_skeleton(properties)
        print("convert execute")
        return {'FINISHED'}


class NullOperator(bpy.types.Operator):
    """This is an operator that changes nothing, but it used to clear the undo stack"""
    bl_idname = "ueskeleton.null_operator"
    bl_label = "Null Operator"

    def execute(self, context):
        return {'FINISHED'}