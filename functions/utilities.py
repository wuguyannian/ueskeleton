# Copyright Wuguyannian All Rights Reserved.
import bpy
from mathutils import Vector, Euler, Quaternion
from math import radians

def set_to_title(text):
    """
    This function takes text and converts it to titles.

    :param str text: The original text to convert to a title.
    :return str: The new title text.
    """
    return ' '.join([word.capitalize() for word in text.lower().split('_')])


def get_picker_object():
    """
    This function gets or creates a new picker object if needed.

    :return object: The blender picker object.
    """
    properties = bpy.context.window_manager.ueskeleton
    picker_object = bpy.data.objects.get(properties.picker_name)
    if not picker_object:
        picker_object = bpy.data.objects.new(properties.picker_name, None)
        picker_object.constraints.new('COPY_TRANSFORMS')

    return picker_object


def remove_picker_object():
    """
    This function removes the picker object.
    """
    properties = bpy.context.window_manager.ueskeleton
    picker_object = bpy.data.objects.get(properties.picker_name)
    if picker_object:
        bpy.data.objects.remove(picker_object)


def source_skeleton_picker_update(self=None, context=None):
    """
    This function is called every time the source skeleton picker value updates. It updates the available modes
    in the mode selection and sets the picker object to have a fake user so it won't get deleted when the
    file is closed.

    :param object self: This is a reference to the class this functions in appended to.
    :param object context: The context of the object this function is appended to.
    """
    picker_object = get_picker_object()
    picker_object.use_fake_user = True


def validate_source_skeleton_object(properties):
    """
    This function checks to see if the selected source skeleton is an object with armature data.

    :param object properties: The property group that contains variables that maintain the addon's correct state.
    :return [bool, bool]:  [1.whether the selected source skeleton is an object with armature data, 2.whether the object is selected]
    """
    # check if the source skeleton is the right type
    source_skeleton_object = bpy.data.objects.get(properties.source_skeleton_name)
    is_armature = False
    is_object_selected = False

    if source_skeleton_object:
        is_object_selected = True
        if source_skeleton_object.type == 'ARMATURE':
            is_armature = True
    return [
        is_armature, 
        is_object_selected
    ]


def validate_source_skeleton_rotation(properties):
    """
    This function checks whether rotation is required to apply to the selected source skeleton.

    :param object properties: The property group that contains variables that maintain the addon's correct state.
    :return bool: True or False depending on whether rotation is required to apply to the selected source skeleton.
    """
    # check if the source skeleton is the right type
    source_skeleton_object = bpy.data.objects.get(properties.source_skeleton_name)

    if source_skeleton_object:
        rotation = source_skeleton_object.rotation_euler
        return  rotation.x == 0 and rotation.y == 0 and rotation.z == 0
    else:
        return False


def get_array_data(array_object):
    """
    This function destructures any of the array object data types into a list.

    :param object array_object: A object array such as Color, Euler, Quaternion, Vector.
    :return list: A list of values.
    """
    array_data = []
    for value in array_object:
        array_data.append(value)

    return array_data


def get_matrix_data(matrix_object):
    """
    This function destructures a matrix object into a list of lists.

    :param object matrix_object:
    :return list: A list of lists that represents a matrix.
    """
    matrix_data = []
    for column in matrix_object:
        col_values = []
        for col_value in column:
            col_values.append(col_value)

        matrix_data.append(col_values)

    return matrix_data

def report_error(error_header, error_message, confirm_message=None, clean_up_action=None, width=500):
    """
    This function dynamically defines an operator class with a properties dialog to report error messages to the user.

    :param str error_header: The title of the error in the modal header.
    :param str error_message: The body text with the error message.
    :param str confirm_message: An optional confirm message if the user would like to let the clean up action fix the
    issue.
    :param lambda clean_up_action: An optional function to be run to fix the issue if the user confirms.
    :param int width: The width of the modal.
    """
    class_name = 'ReportError'
    error_class = object

    def execute(self, context):
        if clean_up_action:
            clean_up_action()
        bpy.utils.unregister_class(error_class)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=width)

    def draw(self, context):
        layout = self.layout
        for line in error_message.split('\n'):
            row = layout.row()
            row.label(text=line)

        layout.row()
        layout.row()
        layout.row()

        if confirm_message:
            for line in confirm_message.split('\n'):
                row = layout.row()
                row.label(text=line)

    error_class = type(
        class_name,
        (bpy.types.Operator,),
        {
            'bl_idname': 'wm.report_error',
            'bl_label': error_header,
            'execute': execute,
            'invoke': invoke,
            'draw': draw
        }
    )
    bpy.utils.register_class(error_class)
    bpy.ops.wm.report_error('INVOKE_DEFAULT')


# -------------- functions that handle the bone editing --------------
def copy_bone(source_bone, target_bone):
    target_bone.parent = source_bone.parent
    target_bone.head = Vector(source_bone.head)
    target_bone.tail = Vector(source_bone.tail)
    target_bone.layers = list(source_bone.layers)
    target_bone.use_connect = source_bone.use_connect
    target_bone.use_deform =  source_bone.use_deform
    target_bone.roll = source_bone.roll
    target_bone.use_inherit_rotation = source_bone.use_inherit_rotation
    target_bone.use_local_location = source_bone.use_local_location
    target_bone.inherit_scale = source_bone.inherit_scale

    target_bone.use_deform = source_bone.use_deform
    target_bone.bbone_segments = source_bone.bbone_segments
    target_bone.bbone_easein = source_bone.bbone_easein
    target_bone.bbone_easeout = source_bone.bbone_easeout


def change_bone_orientation(target_bone, axis_name, angle, recursive): 
    if axis_name == 'x':
        axis = target_bone.x_axis
    if axis_name == 'y':
        axis = target_bone.y_axis
    if axis_name == 'z':
        axis = target_bone.z_axis
    quat = Quaternion(axis, radians(angle))
    tail = Vector(target_bone.tail) - Vector(target_bone.head)
    tail.rotate(quat)
    target_bone.tail = target_bone.head + tail

    if recursive > 0:
        recursive = recursive - 1
        for child in target_bone.children:
            change_bone_orientation(child, axis_name, angle, recursive)