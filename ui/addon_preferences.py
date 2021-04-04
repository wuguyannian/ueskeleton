# Copyright Wuguyannian All Rights Reserved.

import bpy


class UESkeletonAddonPreferences(bpy.types.AddonPreferences):
    """
    This class subclasses the AddonPreferences class to create the addon preferences interface.
    """
    bl_idname = __package__.split('.')[0]

    def draw(self, context):
        """
        This function overrides the draw method in the AddonPreferences class. The draw method is the function
        that defines the user interface layout and gets updated routinely.

        :param object context: The addon preferences context.
        """
        layout = self.layout

        row = layout.row()
        row.operator('ueskeleton.import_skeleton_template', icon='IMPORT')
        row.operator('ueskeleton.export_skeleton_template', icon='EXPORT')
