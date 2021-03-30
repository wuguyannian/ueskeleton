import bpy
from .functions import templates
from .functions import utilities
from .settings import tool_tips

class UESKELETONProperties(bpy.types.PropertyGroup):
    """
    This class defines a property group that can be accessed through the blender api.
    """

     # --------------------- read only properties ---------------------
    module_name = __package__

    # template constants
    skeleton_templates_path = templates.get_skeleton_templates_path()
    default_template = 'default'

     # utility constants
    picker_name = 'picker'

    context = {}

    # --------------------- read/write properties ---------------------

    # scene variables
    source_skeleton_name: bpy.props.StringProperty(default='', update=utilities.source_skeleton_picker_update)


    # --------------------- user interface properties ------------------

    selected_skeleton_template: bpy.props.EnumProperty(
        name="Skeleton Template",
        description=tool_tips.skeleton_template_tool_tip,
        items=templates.safe_populate_templates_dropdown,
        options={'ANIMATABLE'},
        update=templates.set_template
    )


class UESKELETONSavedProperties(bpy.types.PropertyGroup):
    """
    This class defines a property group that will be stored in the blender scene. This
    data will get serialized into the blend file when it is saved.
    """


def register():
    """
    This function registers the property group class and adds it to the window manager context when the
    addon is enabled.
    """
    bpy.utils.register_class(UESKELETONProperties)
    bpy.utils.register_class(UESKELETONSavedProperties)

    bpy.types.WindowManager.ueskeleton = bpy.props.PointerProperty(type=UESKELETONProperties)
    bpy.types.Scene.ueskeleton = bpy.props.PointerProperty(type=UESKELETONSavedProperties)


def unregister():
    """
    This function unregisters the property group class and deletes it from the window manager context when the
    addon is disabled.
    """
    bpy.utils.unregister_class(UESKELETONProperties)

    del bpy.types.WindowManager.ueskeleton
    del bpy.types.Scene.ueskeleton
