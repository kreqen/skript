import math
from typing import Dict, Any, Tuple

from matplotlib.figure import Figure
from matplotlib.patches import Polygon, Circle as MplCircle


APP_BG_COLOR = "#111116"
LINE_COLOR = "#FF2E88"
LABEL_COLOR = "white"
ACCENT_COLOR = "#FF74B5"


class GeometryService:
    def __init__(self) -> None:
        pass

    def create_figure(self, geometry_data: Dict[str, Any]) -> Figure:
        fig = Figure(facecolor=APP_BG_COLOR)
        ax = fig.add_subplot(111)
        ax.set_facecolor(APP_BG_COLOR)
        ax.axis("off")
        ax.set_aspect('equal', adjustable='datalim')

        shape_type = geometry_data.get("type")
        if not shape_type:
            self._show_error(ax, "Недостаточно данных для построения рисунка.")
            return fig

        try:
            if shape_type == "triangle":
                self._draw_triangle(ax, geometry_data)
            elif shape_type == "right_triangle":
                self._draw_right_triangle(ax, geometry_data)
            elif shape_type == "isosceles_triangle":
                self._draw_isosceles_triangle(ax, geometry_data)
            elif shape_type == "rectangle":
                self._draw_rectangle(ax, geometry_data)
            elif shape_type == "square":
                self._draw_square(ax, geometry_data)
            elif shape_type == "circle":
                self._draw_circle(ax, geometry_data)
            else:
                self._show_error(ax, "Недостаточно данных для построения рисунка.")
        except Exception as e:
            self._show_error(ax, f"Ошибка построения рисунка: {e}")

        return fig

    def _show_error(self, ax, message: str):
        ax.text(
            0.5, 0.5, message,
            color=LABEL_COLOR,
            fontsize=12,
            ha='center',
            va='center',
            transform=ax.transAxes,
            wrap=True
        )

    def _draw_triangle(self, ax, data: Dict[str, Any]):
        a = data.get("a")
        b = data.get("b")
        c = data.get("c")
        vertices_labels = data.get("vertices", ["A", "B", "C"])
        angles = data.get("angles", {})
        right_angle_vertex = data.get("right_angle_vertex")

        if not all(isinstance(x, (int, float)) and x > 0 for x in [a, b, c]):
            raise ValueError("Некорректные длины сторон треугольника.")

        if not (a + b > c and a + c > b and b + c > a):
            raise ValueError("Длины сторон не удовлетворяют неравенству треугольника.")

        Ax, Ay = 0, 0
        Bx, By = c, 0

        cos_angle = (a**2 + c**2 - b**2) / (2 * a * c)
        if cos_angle < -1 or cos_angle > 1:
            raise ValueError("Некорректные стороны для вычисления угла.")
        angle = math.acos(cos_angle)
        Cx = a * math.cos(angle)
        Cy = a * math.sin(angle)

        points = [(Ax, Ay), (Bx, By), (Cx, Cy)]

        polygon = Polygon(points, closed=True, fill=False, edgecolor=LINE_COLOR, linewidth=2)
        ax.add_patch(polygon)

        for (x, y), label in zip(points, vertices_labels):
            ax.text(x, y, label, color=LABEL_COLOR, fontsize=12, fontweight='bold', ha='right', va='bottom')

        midpoints = [
            ((Ax + Bx) / 2, (Ay + By) / 2),
            ((Bx + Cx) / 2, (By + Cy) / 2),
            ((Cx + Ax) / 2, (Cy + Ay) / 2),
        ]
        sides = [c, b, a]
        for (mx, my), length in zip(midpoints, sides):
            ax.text(mx, my, f"{length:.2f}", color=LABEL_COLOR, fontsize=10, ha='center', va='center')

        for i, vertex in enumerate(points):
            angle_val = angles.get(vertices_labels[i])
            if angle_val is not None:
                ax.text(vertex[0], vertex[1] + 0.1, f"{angle_val}°", color=LABEL_COLOR, fontsize=10, ha='center')

        if right_angle_vertex in vertices_labels:
            idx = vertices_labels.index(right_angle_vertex)
            self._draw_right_angle_marker(ax, points, idx)

        self._autoscale(ax, points)

    def _draw_right_angle_marker(self, ax, points: list[Tuple[float, float]], vertex_idx: int):
        size = 0.1
        p = points[vertex_idx]
        prev_p = points[(vertex_idx - 1) % 3]
        next_p = points[(vertex_idx + 1) % 3]

        v1 = (prev_p[0] - p[0], prev_p[1] - p[1])
        v2 = (next_p[0] - p[0], next_p[1] - p[1])

        def norm(v):
            return (v[0] / math.sqrt(v[0]**2 + v[1]**2), v[1] / math.sqrt(v[0]**2 + v[1]**2))

        nv1 = norm(v1)
        nv2 = norm(v2)

        p1 = (p[0] + nv1[0] * size, p[1] + nv1[1] * size)
        p2 = (p1[0] + nv2[0] * size, p1[1] + nv2[1] * size)
        p3 = (p[0] + nv2[0] * size, p[1] + nv2[1] * size)

        square = Polygon([p, p1, p2, p3], closed=True, fill=False, edgecolor=ACCENT_COLOR, linewidth=2)
        ax.add_patch(square)

    def _draw_right_triangle(self, ax, data: Dict[str, Any]):
        self._draw_triangle(ax, data)

    def _draw_isosceles_triangle(self, ax, data: Dict[str, Any]):
        a = data.get("a")
        b = data.get("b")
        c = data.get("c")
        vertices_labels = data.get("vertices", ["A", "B", "C"])
        angles = data.get("angles", {})

        if not all(isinstance(x, (int, float)) and x > 0 for x in [a, b, c]):
            raise ValueError("Некорректные длины сторон треугольника.")

        Ax, Ay = 0, 0
        Bx, By = c, 0

        height = math.sqrt(a**2 - (c/2)**2)
        Cx = c / 2
        Cy = height

        points = [(Ax, Ay), (Bx, By), (Cx, Cy)]

        polygon = Polygon(points, closed=True, fill=False, edgecolor=LINE_COLOR, linewidth=2)
        ax.add_patch(polygon)

        for (x, y), label in zip(points, vertices_labels):
            ax.text(x, y, label, color=LABEL_COLOR, fontsize=12, fontweight='bold', ha='right', va='bottom')

        midpoints = [
            ((Ax + Bx) / 2, (Ay + By) / 2),
            ((Bx + Cx) / 2, (By + Cy) / 2),
            ((Cx + Ax) / 2, (Cy + Ay) / 2),
        ]
        sides = [c, b, a]
        for (mx, my), length in zip(midpoints, sides):
            ax.text(mx, my, f"{length:.2f}", color=LABEL_COLOR, fontsize=10, ha='center', va='center')

        for i, vertex in enumerate(points):
            angle_val = angles.get(vertices_labels[i])
            if angle_val is not None:
                ax.text(vertex[0], vertex[1] + 0.1, f"{angle_val}°", color=LABEL_COLOR, fontsize=10, ha='center')

        self._autoscale(ax, points)

    def _draw_rectangle(self, ax, data: Dict[str, Any]):
        width = data.get("width")
        height = data.get("height")
        vertices_labels = data.get("vertices", ["A", "B", "C", "D"])
        angles = data.get("angles", {})

        if not (isinstance(width, (int, float)) and width > 0 and isinstance(height, (int, float)) and height > 0):
            raise ValueError("Некорректные размеры прямоугольника.")

        points = [(0, 0), (width, 0), (width, height), (0, height)]

        polygon = Polygon(points, closed=True, fill=False, edgecolor=LINE_COLOR, linewidth=2)
        ax.add_patch(polygon)

        for (x, y), label in zip(points, vertices_labels):
            ax.text(x, y, label, color=LABEL_COLOR, fontsize=12, fontweight='bold', ha='right', va='bottom')

        midpoints = [
            ((points[0][0] + points[1][0]) / 2, (points[0][1] + points[1][1]) / 2),
            ((points[1][0] + points[2][0]) / 2, (points[1][1] + points[2][1]) / 2),
            ((points[2][0] + points[3][0]) / 2, (points[2][1] + points[3][1]) / 2),
            ((points[3][0] + points[0][0]) / 2, (points[3][1] + points[0][1]) / 2),
        ]
        sides = [width, height, width, height]
        for (mx, my), length in zip(midpoints, sides):
            ax.text(mx, my, f"{length:.2f}", color=LABEL_COLOR, fontsize=10, ha='center', va='center')

        for i, vertex in enumerate(points):
            angle_val = angles.get(vertices_labels[i])
            if angle_val is not None:
                ax.text(vertex[0], vertex[1] + 0.1, f"{angle_val}°", color=LABEL_COLOR, fontsize=10, ha='center')

        self._autoscale(ax, points)

    def _draw_square(self, ax, data: Dict[str, Any]):
        side = data.get("side")
        if not (isinstance(side, (int, float)) and side > 0):
            raise ValueError("Некорректная длина стороны квадрата.")
        data_rect = {"width": side, "height": side}
        self._draw_rectangle(ax, data_rect)

    def _draw_circle(self, ax, data: Dict[str, Any]):
        radius = data.get("radius")
        center = data.get("center", (0, 0))
        if not (isinstance(radius, (int, float)) and radius > 0):
            raise ValueError("Некорректный радиус окружности.")

        circle = MplCircle(center, radius, fill=False, edgecolor=LINE_COLOR, linewidth=2)
        ax.add_patch(circle)

        ax.text(center[0], center[1], "O", color=LABEL_COLOR, fontsize=12, fontweight='bold', ha='right', va='bottom')

        ax.text(center[0] + radius / 2, center[1], f"r={radius:.2f}", color=LABEL_COLOR, fontsize=10, ha='center', va='bottom')

        self._autoscale_circle(ax, center, radius)

    def _autoscale(self, ax, points: list[Tuple[float, float]]):
        xs, ys = zip(*points)
        margin = 0.5
        ax.set_xlim(min(xs) - margin, max(xs) + margin)
        ax.set_ylim(min(ys) - margin, max(ys) + margin)
        ax.invert_yaxis()

    def _autoscale_circle(self, ax, center: Tuple[float, float], radius: float):
        margin = radius * 0.5
        ax.set_xlim(center[0] - radius - margin, center[0] + radius + margin)
        ax.set_ylim(center[1] - radius - margin, center[1] + radius + margin)
        ax.invert_yaxis()