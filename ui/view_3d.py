# Copyright Wuguyannian All Rights Reserved.

import bpy
from ..functions import utilities

class UE_SKELETON_PT_Panel(bpy.types.Panel):
    """
    This class defines the user interface for the panel in the tab in the 3d view
    """
    bl_label = 'UE Skeleton Toolkit'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'UE Skeleton'

    def draw(self, context):
        """
        This function overrides the draw method in the Panel class. The draw method is the function that
        defines the user interface layout and gets updated routinely.

        :param object context: The 3d view context.
        """

        properties = bpy.context.window_manager.ueskeleton

        # set source skeleton name to the object picker
        object_picker = utilities.get_picker_object().constraints[0]
        if object_picker.target:
            if properties.source_skeleton_name != object_picker.target.name:
                properties.source_skeleton_name = object_picker.target.name
        else:
            if properties.source_skeleton_name != '':
                properties.source_skeleton_name = ''

        layout = self.layout

        # source skeleton selector
        box = layout.box()
        row = box.row()
        row = row.split(factor=0.90, align=True)
        row.prop(object_picker, 'target', text='Source')

         # enable the layout if an armature is selected
        validate_results = utilities.validate_source_skeleton_object(properties)
        layout = layout.column()
        layout.enabled = validate_results[0]

        if validate_results[1] and not layout.enabled:
            row = layout.row()
            row.alert = True
            row.label(text= 'It is not a skeleton object!')

         # apply the root rotation
        if layout.enabled and not utilities.validate_source_skeleton_rotation(properties):
            row = layout.row()
            row.alert = True
            row.label(text= 'needed to applay the rotation!')

        # template dropdown
        row = layout.row()
        row.label(text='Template:')
        if properties.selected_skeleton_template in [properties.default_template]:
            row = layout.row()
            row.prop(properties, 'selected_skeleton_template', text='')
        else:
            row = layout.split(factor=0.90, align=True)
            row.prop(properties, 'selected_skeleton_template', text='')
            row.operator('ueskeleton.remove_template_folder', icon='PANEL_CLOSE')

        box = layout.box()
        row = box.row()
        row.scale_y = 2.0
        row.operator('ueskeleton.convert_to_epic_skeleton', text='Convert')