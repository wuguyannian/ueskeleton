# Copyright Wuguyannian All Rights Reserved.

import bpy
import sys
import importlib

from . import properties, operators
from .settings import tool_tips
from .functions import scene, templates, utilities
from .ui import view_3d, addon_preferences, exporter


bl_info = {
    "name" : "UE Skeleton",
    "author" : "Wuguyannian",
    "description" : "Help to Contert a given Skeleton to Epic Skeleton",
    "blender" : (2, 80, 0),
    "version" : (1, 0, 0),
    "location": "3D View > Tools > UE Skeleton",
    "warning" : "",
    "category" : "Pipeline"
}


modules = (
    scene,
    view_3d,
    exporter,
    tool_tips,
    utilities,
    operators,
    templates,
    properties,
    addon_preferences
)

classes = (
    operators.RemoveTemplateFolder,
    operators.ConvertToEpicSkeleton,
    operators.ExportSkeletonTemplate,
    operators.ImportSkeletonTemplate,
    addon_preferences.UESkeletonAddonPreferences,
    view_3d.UE_SKELETON_PT_Panel
)


def register():
    """
    This function registers the addon classes when the addon is enabled.
    """
    # add an index in the system path that will be swapped during the tools use to load metarigs
    sys.path.insert(0, '')

    # reload submodules
    for module in modules:
        importlib.reload(module)

    properties.register()

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    """
    This function unregisters the addon classes when the addon is disabled.
    """

     # remove the added system path
    sys.path.pop(0)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    utilities.remove_picker_object()
    properties.unregister()

