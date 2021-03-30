import bpy
import mathutils
import math

from . import utilities
from . import templates

def convert_to_epic_skeleton(properties):
    """
    This function convert the selected skeleton object to the epic skeleton.

    :param object properties: The property group that contains variables that maintain the addon's correct state.
    """
    obj = bpy.data.objects.get(properties.source_skeleton_name)
    if obj:      
        # 1.process the orientation
        orientation_data = templates.get_orientation_data(properties)       
        for orientation in orientation_data:
            bpy.ops.object.mode_set(mode='EDIT')

            bone = obj.data.edit_bones[orientation['name']]
            axis_name = orientation['axis']
            angle = orientation['angle']
            recursive = 0
            if 'recursive' in orientation:
                recursive = orientation['recursive']
            
            if 'roll_add' in orientation:
                bone.roll = bone.roll + math.radians(orientation['roll_add'])

            utilities.change_bone_orientation(bone, axis_name, angle, recursive)           

            bpy.ops.object.mode_set(mode='OBJECT')
        
        # 2.process the ik creation
        creation_data = templates.get_creation_data(properties) 
        for creation in creation_data:
            bpy.ops.object.mode_set(mode='EDIT')

            ik_bone = obj.data.edit_bones.new(creation['name'])
            
            if 'source_bone' in creation:
                utilities.copy_bone(obj.data.edit_bones[creation['source_bone']], ik_bone)
            if 'parent_bone' in creation:
                ik_bone.parent = obj.data.edit_bones[creation['parent_bone']]                    
            if 'parent_root' in creation:
                ik_bone.parent = obj
            if 'head' in creation:
                ik_bone.head = utilities.get_array_data(creation['head'])
            if 'tail' in creation:
                ik_bone.tail = utilities.get_array_data(creation['tail'])
            if 'Matrix' in creation:
                ik_bone.matrix = utilities.get_matrix_data(creation['Matrix'])

            bpy.ops.object.mode_set(mode='OBJECT')