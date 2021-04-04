# Copyright Wuguyannian All Rights Reserved.

import bpy
from bpy_extras.io_utils import ExportHelper


class ExportSkeletonTemplate(ExportHelper):
    """
    This class subclasses the export helper to define a custom file browser
    """
    bl_idname = "ueskeleton.export_skeleton_template"
    bl_label = "Export Template"
    filename_ext = ".zip"

    def draw(self, context):
        """
        This function overrides the draw method in the ExportHelper class. The draw method is the function that
        defines the user interface layout and gets updated routinely.

        :param object context: The window context.
        """
        properties = bpy.context.window_manager.ueskeleton

        layout = self.layout
        row = layout.row()
        row.label(text="Exported Template:")
        row = layout.row()
        row.prop(properties, "selected_export_template", text='')
