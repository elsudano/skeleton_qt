import math

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QColor, QFont, QLinearGradient, QPainter, QPen, QPolygonF
from PySide6.QtWidgets import QWidget


class SpeedometerProgress(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 0
        self.setMinimumSize(250, 220)

    def value(self):
        return self._value

    def setValue(self, value):
        self._value = max(0, min(100, value))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        width, height = self.width(), self.height()
        size = min(width, height) - 20
        center_x = width / 2
        center_y = height / 2 + 20
        radius = size / 2
        start_angle = 180 * 16
        span_angle = -180 * 16
        pen_bg = QPen(QColor("#2d3139"), 12)
        pen_bg.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen_bg)
        painter.drawArc(center_x - radius, center_y - radius,
                        size, size, start_angle, span_angle)
        if self._value > 0:
            gradient = QLinearGradient(
                center_x - radius, center_y, center_x + radius, center_y)
            gradient.setColorAt(0.0, QColor("#ef233c"))
            gradient.setColorAt(0.5, QColor("#ffb703"))
            gradient.setColorAt(1.0, QColor("#2a9d8f"))
            pen_progress = QPen(gradient, 12)
            pen_progress.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(pen_progress)
            progress_span = int((-180 * 16) * (self._value / 100.0))
            painter.drawArc(center_x - radius, center_y - radius,
                            size, size, start_angle, progress_span)
        painter.setPen(QPen(QColor("#a0a5b0"), 2))
        font = QFont("Arial", 10, QFont.Weight.Bold)
        painter.setFont(font)
        for i in range(11):
            angle_rad = math.pi - (i * (math.pi / 10))
            cos_a, sin_a = math.cos(angle_rad), math.sin(angle_rad)
            p1 = QPointF(center_x + (radius - 12) * cos_a,
                         center_y - (radius - 12) * sin_a)
            p2 = QPointF(center_x + (radius - 22) * cos_a,
                         center_y - (radius - 22) * sin_a)
            painter.drawLine(p1, p2)
            text_p = QPointF(center_x + (radius - 38) * cos_a -
                             10, center_y - (radius - 38) * sin_a + 5)
            painter.drawText(text_p, str(i * 10))
        painter.setPen(QColor("#ffffff"))
        painter.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter |
                         Qt.AlignmentFlag.AlignBottom, f"{self._value}%")
        needle_angle = math.pi - (self._value / 100.0 * math.pi)
        cos_n, sin_n = math.cos(needle_angle), math.sin(needle_angle)
        tip = QPointF(center_x + (radius - 15) * cos_n,
                      center_y - (radius - 15) * sin_n)
        base_left = QPointF(center_x + 6 * math.cos(needle_angle + math.pi/2),
                            center_y - 6 * math.sin(needle_angle + math.pi/2))
        base_right = QPointF(center_x + 6 * math.cos(needle_angle - math.pi/2),
                             center_y - 6 * math.sin(needle_angle - math.pi/2))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#ffffff"))
        painter.drawPolygon(QPolygonF([tip, base_left, base_right]))
        painter.drawEllipse(QPointF(center_x, center_y), 10, 10)
        painter.setBrush(QColor("#1e222b"))
        painter.drawEllipse(QPointF(center_x, center_y), 5, 5)
