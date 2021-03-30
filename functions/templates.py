# Copyright Wuguyannian All Rights Reserved.

import os
import re
import bpy
import json
import shutil
from mathutils import Color, Euler, Matrix, Quaternion, Vector

from . import utilities
from ..settings.tool_tips import *

_result_reference_populate_templates_dropdown = []


# -------------- functions that handle the skeleton templating --------------
def get_skeleton_templates_path():
    """
    This function returns the path to the addons skeleton template directory.

    :return str: The full path to the addons skeleton template directory.
    """
    addons = bpy.utils.user_resource('SCRIPTS', 'addons')
    return os.path.join(addons, __package__.split('.')[0], 'resources', 'skeleton_templates')


def get_skeleton_templates(self=None, context=None):
    """
    This function gets the enumeration for the skeleton template selection.

    :param object self: This is a reference to the class this functions in appended to.
    :param object context: The context of the object this function is appended to.
    :return list: A list of tuples that define the skeleton template enumeration.
    """
    skeleton_templates = []
    skeleton_template_directories = next(os.walk(get_skeleton_templates_path()))[1]

    for index, skeleton_template in enumerate(skeleton_template_directories):
        skeleton_templates.append((
            skeleton_template,
            utilities.set_to_title(skeleton_template),
            template_tool_tip.format(template_name=utilities.set_to_title(skeleton_template)),
            'OUTLINER_OB_ARMATURE',
            index
        ))
    return skeleton_templates


def get_template_file_path(template_file_name, properties):
    """
    This function get the the full path to a template file based on the provided template file name.

    :param str template_file_name: The name of the template file.
    :param object properties: The property group that contains variables that maintain the addon's correct state.
    :return str: The full path to a template file.
    """
    template_name = properties.selected_skeleton_template

    return os.path.join(
        properties.skeleton_templates_path,
        template_name,
        template_file_name
    )


def remove_template_folder(properties):
    """
    This function removes the active template from the addon's skeleton templates folder.

    :param object properties: The property group that contains variables that maintain the addon's correct state.
    """

    # delete the selected skeleton template folder
    selected_template_path = os.path.join(properties.skeleton_templates_path, properties.selected_skeleton_template)
    try:
        original_umask = os.umask(0)
        if os.path.exists(selected_template_path):
            os.chmod(selected_template_path, 0o777)
        shutil.rmtree(selected_template_path)
    finally:
        os.umask(original_umask)

    # set the selected skeleton template to the default
    properties.selected_skeleton_template = properties.default_template


def populate_templates_dropdown(self=None, context=None):
    """
    This function is called every time a the template dropdown is interacted with. It lists all the templates in the
    skeleton_templates folder.

    :param object self: This is a reference to the class this functions in appended to.
    :param object context: The context of the object this function is appended to.
    """
    skeleton_templates = get_skeleton_templates()
    return skeleton_templates

#
# Dynamic EnumProperty item list workaround:
# https://docs.blender.org/api/current/bpy.props.html?highlight=bpy%20props%20enumproperty#bpy.props.EnumProperty
#

def safe_populate_templates_dropdown(self, context):
    """
    This function is an EnumProperty safe wrapper for populate_templates_dropdown.

    :param object self: This is a reference to the class this functions in appended to.
    :param object context: The context of the object this function is appended to.
    :return list: Result of populate_templates_dropdown.
    """
    items = populate_templates_dropdown()
    global _result_reference_populate_templates_dropdown
    _result_reference_populate_templates_dropdown = items
    return items


def set_template(self=None, context=None):
    """
    This function is called every time a new template is selected. If create new is selected it switch to edit metarig
    mode, but if anything else is selected it defaults to source mode.

    :param object self: This is a reference to the class this functions in appended to.
    :param object context: The context of the object this function is appended to.
    """
    properties = bpy.context.window_manager.ueskeleton


def get_creation_data(properties):
    """
    This function reads from disk a list of dictionaries that are used to create ik.

    :param object properties: The property group that contains variables that maintain the addon's correct state.
    """
    creation_data = {}
    creation_path = get_template_file_path('creation.json', properties)
    if os.path.exists(creation_path):
        creation_file = open(creation_path)
        creation_data = json.load(creation_file)
        creation_file.close()

    return creation_data


def get_orientation_data(properties):
    """
    This function reads from disk a list of dictionaries that are used to modify orientation.

    :param object properties: The property group that contains variables that maintain the addon's correct state.
    """
    orientation_data = {}
    orientation_path = get_template_file_path('orientation.json', properties)
    if os.path.exists(orientation_path):
        orientation_file = open(orientation_path)
        orientation_data = json.load(orientation_file)
        orientation_file.close()

    return orientation_data


def save_json_file(data, file_path):
    """
    This function saves json data to a file provided a full file path.

    :param dict data: A dictionary to be saved as json.
    :param str file_path: The full file path to where the file will be saved.
    """
    if '.json' in os.path.basename(file_path):
        try:
            original_umask = os.umask(0)
            if os.path.exists(file_path):
                os.chmod(file_path, 0o777)
            file = open(file_path, 'w+')
        finally:
            os.umask(original_umask)
        json.dump(data, file, indent=1)
        file.close()