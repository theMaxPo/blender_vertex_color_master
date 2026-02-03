#  ***** GPL LICENSE BLOCK *****
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  All rights reserved.
#  ***** GPL LICENSE BLOCK *****

# <pep8 compliant>

"""
Blender version compatibility layer for Vertex Color Master.

This module abstracts Blender API differences across versions:
- Blender 2.80 - 3.1: Uses mesh.vertex_colors API
- Blender 3.2 - 4.x: Uses mesh.color_attributes API (vertex_colors deprecated)
- Blender 5.0+: Uses mesh.color_attributes API (vertex_colors removed)
"""

from typing import Optional, Any, List, Tuple
import bpy

# =============================================================================
# Version Detection
# =============================================================================

BLENDER_VERSION: Tuple[int, int, int] = bpy.app.version
BLENDER_3_2: bool = BLENDER_VERSION >= (3, 2, 0)
BLENDER_4_0: bool = BLENDER_VERSION >= (4, 0, 0)
BLENDER_4_1: bool = BLENDER_VERSION >= (4, 1, 0)
BLENDER_5_0: bool = BLENDER_VERSION >= (5, 0, 0)

# Use new color_attributes API from Blender 3.2+
USE_COLOR_ATTRIBUTES: bool = BLENDER_3_2


# =============================================================================
# Shader Compatibility
# =============================================================================

def get_shader_builtin(name: str) -> Any:
    """
    Get GPU shader with version-appropriate name.
    
    Blender 4.0 removed the '2D_' prefix from shader names.
    
    Args:
        name: Shader name without '2D_' prefix (e.g., 'SMOOTH_COLOR', 'UNIFORM_COLOR')
    
    Returns:
        GPU shader object
    """
    import gpu
    if BLENDER_4_0:
        return gpu.shader.from_builtin(name)
    else:
        return gpu.shader.from_builtin(f'2D_{name}')


# =============================================================================
# Vertex Color Layer Access
# =============================================================================

def get_vertex_colors(mesh: bpy.types.Mesh) -> Optional[Any]:
    """
    Get the vertex colors collection from a mesh.
    
    Args:
        mesh: Blender mesh data
    
    Returns:
        Vertex colors collection or None if not available
    """
    if USE_COLOR_ATTRIBUTES:
        return mesh.color_attributes
    else:
        return mesh.vertex_colors


def get_active_vcol(mesh: bpy.types.Mesh) -> Optional[Any]:
    """
    Get the active vertex color layer from a mesh.
    
    Args:
        mesh: Blender mesh data
    
    Returns:
        Active vertex color layer or None
    """
    if USE_COLOR_ATTRIBUTES:
        attrs = mesh.color_attributes
        if attrs and len(attrs) > 0:
            return attrs.active_color
        return None
    else:
        vcols = mesh.vertex_colors
        if vcols and len(vcols) > 0:
            return vcols.active
        return None


def set_active_vcol(mesh: bpy.types.Mesh, vcol: Any) -> None:
    """
    Set the active vertex color layer on a mesh.
    
    Args:
        mesh: Blender mesh data
        vcol: Vertex color layer to make active
    """
    if USE_COLOR_ATTRIBUTES:
        mesh.color_attributes.active_color = vcol
    else:
        mesh.vertex_colors.active = vcol


def create_vcol(mesh: bpy.types.Mesh, name: Optional[str] = None) -> Any:
    """
    Create a new vertex color layer on a mesh.
    
    Args:
        mesh: Blender mesh data
        name: Optional name for the layer
    
    Returns:
        The newly created vertex color layer
    """
    if USE_COLOR_ATTRIBUTES:
        # color_attributes.new(name, type, domain)
        # type: 'FLOAT_COLOR' or 'BYTE_COLOR'
        # domain: 'POINT' (per-vertex) or 'CORNER' (per-loop/face-corner)
        if name:
            return mesh.color_attributes.new(name=name, type='BYTE_COLOR', domain='CORNER')
        else:
            return mesh.color_attributes.new(name="Color", type='BYTE_COLOR', domain='CORNER')
    else:
        if name:
            vcol = mesh.vertex_colors.new(name=name)
        else:
            vcol = mesh.vertex_colors.new()
        return vcol


def remove_vcol(mesh: bpy.types.Mesh, vcol: Any) -> None:
    """
    Remove a vertex color layer from a mesh.
    
    Args:
        mesh: Blender mesh data
        vcol: Vertex color layer to remove
    """
    if USE_COLOR_ATTRIBUTES:
        mesh.color_attributes.remove(vcol)
    else:
        mesh.vertex_colors.remove(vcol)


def vcol_exists(mesh: bpy.types.Mesh, name: str) -> bool:
    """
    Check if a vertex color layer with the given name exists.
    
    Args:
        mesh: Blender mesh data
        name: Name to search for
    
    Returns:
        True if layer exists, False otherwise
    """
    vcols = get_vertex_colors(mesh)
    if vcols is None:
        return False
    return name in vcols


def get_vcol_by_name(mesh: bpy.types.Mesh, name: str) -> Optional[Any]:
    """
    Get a vertex color layer by name.
    
    Args:
        mesh: Blender mesh data
        name: Name of the layer
    
    Returns:
        Vertex color layer or None if not found
    """
    vcols = get_vertex_colors(mesh)
    if vcols is None:
        return None
    if name in vcols:
        return vcols[name]
    return None


def get_vcol_count(mesh: bpy.types.Mesh) -> int:
    """
    Get the number of vertex color layers on a mesh.
    
    Args:
        mesh: Blender mesh data
    
    Returns:
        Number of vertex color layers
    """
    vcols = get_vertex_colors(mesh)
    if vcols is None:
        return 0
    return len(vcols)


def has_vertex_colors(mesh: bpy.types.Mesh) -> bool:
    """
    Check if a mesh has any vertex color layers.
    
    Args:
        mesh: Blender mesh data
    
    Returns:
        True if mesh has vertex colors, False otherwise
    """
    return get_vcol_count(mesh) > 0


def get_or_create_vcol(mesh: bpy.types.Mesh) -> Any:
    """
    Get active vertex color layer, creating one if none exists.
    
    This is the most common pattern used throughout the addon.
    
    Args:
        mesh: Blender mesh data
    
    Returns:
        Active or newly created vertex color layer
    """
    vcol = get_active_vcol(mesh)
    if vcol is None:
        vcol = create_vcol(mesh)
        set_active_vcol(mesh, vcol)
    return vcol


def iter_vertex_colors(mesh: bpy.types.Mesh):
    """
    Iterate over all vertex color layers on a mesh.
    
    Args:
        mesh: Blender mesh data
    
    Yields:
        Each vertex color layer
    """
    vcols = get_vertex_colors(mesh)
    if vcols is not None:
        for vcol in vcols:
            yield vcol


# =============================================================================
# Mesh Compatibility
# =============================================================================

def set_auto_smooth(mesh: bpy.types.Mesh, enabled: bool) -> None:
    """
    Set auto smooth on a mesh (deprecated in Blender 4.1+).
    
    Args:
        mesh: Blender mesh data
        enabled: Whether to enable auto smooth
    """
    if not BLENDER_4_1:
        mesh.use_auto_smooth = enabled


def has_auto_smooth(mesh: bpy.types.Mesh) -> bool:
    """
    Check if mesh has auto smooth enabled (deprecated in Blender 4.1+).
    
    Args:
        mesh: Blender mesh data
    
    Returns:
        True if auto smooth is enabled, False otherwise
    """
    if BLENDER_4_1:
        return True  # Always smooth in 4.1+
    return mesh.use_auto_smooth


# =============================================================================
# BMesh Color Layer Access
# =============================================================================

def get_bmesh_color_layer(bm: Any, vcol_name: Optional[str] = None):
    """
    Get the active color layer from a BMesh.
    
    In Blender 3.2+, color attributes can be stored as either:
    - float_color: FLOAT_COLOR type (32-bit per channel)
    - color: BYTE_COLOR type (8-bit per channel)
    
    This function checks both layer types and returns the active or named layer.
    
    Args:
        bm: BMesh object
        vcol_name: Optional name of specific layer to get
    
    Returns:
        Active color layer or None
    """
    if USE_COLOR_ATTRIBUTES:
        # In Blender 3.2+, check float_color first (more common with new API)
        # then fall back to byte color
        if vcol_name:
            # Get by name
            if vcol_name in bm.loops.layers.float_color:
                return bm.loops.layers.float_color[vcol_name]
            if vcol_name in bm.loops.layers.color:
                return bm.loops.layers.color[vcol_name]
        else:
            # Get active layer - try float_color first
            layer = bm.loops.layers.float_color.active
            if layer is not None:
                return layer
            # Fall back to byte color
            layer = bm.loops.layers.color.active
            if layer is not None:
                return layer
        return None
    else:
        # Legacy API - just use color
        if vcol_name and vcol_name in bm.loops.layers.color:
            return bm.loops.layers.color[vcol_name]
        return bm.loops.layers.color.active


# =============================================================================
# Color Data Access Helpers
# =============================================================================

def get_vcol_data(vcol: Any):
    """
    Get the color data from a vertex color layer.
    
    In both APIs, the data is accessed via .data property.
    
    Args:
        vcol: Vertex color layer
    
    Returns:
        Color data collection
    """
    return vcol.data


def get_loop_color(vcol: Any, loop_index: int) -> List[float]:
    """
    Get color at a specific loop index.
    
    Args:
        vcol: Vertex color layer
        loop_index: Index of the loop
    
    Returns:
        Color as list [R, G, B, A]
    """
    return list(vcol.data[loop_index].color)


def set_loop_color(vcol: Any, loop_index: int, color: List[float]) -> None:
    """
    Set color at a specific loop index.
    
    Args:
        vcol: Vertex color layer
        loop_index: Index of the loop
        color: Color as list [R, G, B, A] or [R, G, B]
    """
    vcol.data[loop_index].color = color
