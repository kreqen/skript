import math
import pytest
from app.services.geometry_service import GeometryService

# Removed import of GeometryCanvas to avoid UI dependency in service tests

def test_triangle_coordinates():
    service = GeometryService()
    # Test right triangle with sides 6,8,10 and right angle at B
    data = {
        "type": "right_triangle",
        "a": 6,
        "b": 8,
        "c": 10,
        "vertices": ["A", "B", "C"],
        "angles": {"B": 90},
        "right_angle_vertex": "B"
    }
    fig = service.create_figure(data)
    ax = fig.axes[0]
    assert len(ax.patches) > 0

def test_regular_triangle():
    service = GeometryService()
    data = {
        "type": "triangle",
        "a": 5,
        "b": 7,
        "c": 8,
        "vertices": ["A", "B", "C"]
    }
    fig = service.create_figure(data)
    ax = fig.axes[0]
    assert len(ax.patches) > 0

def test_isosceles_triangle():
    service = GeometryService()
    data = {
        "type": "isosceles_triangle",
        "a": 13,
        "b": 13,
        "c": 10,
        "vertices": ["A", "B", "C"]
    }
    fig = service.create_figure(data)
    ax = fig.axes[0]
    assert len(ax.patches) > 0

def test_rectangle():
    service = GeometryService()
    data = {
        "type": "rectangle",
        "width": 8,
        "height": 5,
        "vertices": ["A", "B", "C", "D"]
    }
    fig = service.create_figure(data)
    ax = fig.axes[0]
    assert len(ax.patches) > 0

def test_square():
    service = GeometryService()
    data = {
        "type": "square",
        "side": 6,
        "vertices": ["A", "B", "C", "D"]
    }
    fig = service.create_figure(data)
    ax = fig.axes[0]
    assert len(ax.patches) > 0

def test_circle():
    service = GeometryService()
    data = {
        "type": "circle",
        "radius": 5,
        "center": (0, 0)
    }
    fig = service.create_figure(data)
    ax = fig.axes[0]
    assert len(ax.patches) > 0

def test_invalid_triangle():
    service = GeometryService()
    data = {
        "type": "triangle",
        "a": 2,
        "b": 3,
        "c": 10
    }
    fig = service.create_figure(data)
    ax = fig.axes[0]
    # Should show error text, no patches
    assert len(ax.texts) > 0

def test_empty_geometry_data():
    service = GeometryService()
    data = {}
    fig = service.create_figure(data)
    ax = fig.axes[0]
    assert len(ax.texts) > 0

def test_unknown_figure_type():
    service = GeometryService()
    data = {"type": "pentagon"}
    fig = service.create_figure(data)
    ax = fig.axes[0]
    assert len(ax.texts) > 0

# Additional tests for clearing and saving could be added with mocks if needed
