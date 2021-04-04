# Copyright Wuguyannian All Rights Reserved.

import bpy

from .ui import exporter
from .functions import scene
from .functions import templates
from bpy_extras.io_utils import ImportHelper

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

class ExportSkeletonTemplate(bpy.types.Operator, exporter.ExportSkeletonTemplate):
    """Export a skeleton template"""
    bl_idname = "ueskeleton.export_skeleton_template"
    bl_label = "Export Template"

    def execute(self, context):
        properties = bpy.context.window_manager.ueskeleton
        templates.export_zip(self.filepath, properties)
        return {'FINISHED'}


class ImportSkeletonTemplate(bpy.types.Operator, ImportHelper):
    """Import a skeleton template"""
    bl_idname = "ueskeleton.import_skeleton_template"
    bl_label = "Import Template"
    filename_ext = ".zip"

    def execute(self, context):
        properties = bpy.context.window_manager.ueskeleton
        templates.import_zip(self.filepath, properties)
        return {'FINISHED'}