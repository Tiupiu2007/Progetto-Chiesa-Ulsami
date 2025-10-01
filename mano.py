from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QGraphicsView, QGraphicsScene, QGraphicsRectItem, QSplitter
)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QBrush, QColor, QPainter
import sys


class CustomGraphicsView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setRenderHints(self.renderHints() | QPainter.RenderHint.Antialiasing)
        self.setBackgroundBrush(QBrush(QColor("#1e1e1e")))
        self.setDragMode(QGraphicsView.DragMode.NoDrag)

        self._pan = False
        self._pan_start = QPoint()

        # Niente barre visibili
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def wheelEvent(self, event):
        """Zoom con la rotellina del mouse"""
        zoom_in_factor = 1.1
        zoom_out_factor = 0.9
        if event.angleDelta().y() > 0:
            factor = zoom_in_factor
        else:
            factor = zoom_out_factor
        self.scale(factor, factor)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self._pan = True
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            self._pan_start = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._pan:
            delta = self._pan_start - event.pos()
            self._pan_start = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() + delta.y())
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self._pan = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
        else:
            super().mouseReleaseEvent(event)


class VectorBoard(QWidget):
    def __init__(self, width=800, height=600):
        super().__init__()
        self.setWindowTitle("Lavagna Vettoriale")
        self.resize(1000, 700)
        self.setStyleSheet("background-color: #1e1e1e; color: #d4d4d4; font-family: Segoe UI; font-size: 12pt;")

        self.paper_width = width
        self.paper_height = height

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Toolbar verticale
        self.toolbar = QWidget()
        self.toolbar.setStyleSheet("background-color: #252526;")
        self.toolbar.setMinimumWidth(100)
        toolbar_layout = QVBoxLayout(self.toolbar)
        toolbar_layout.setContentsMargins(10, 10, 10, 10)

        toolbar_layout.addWidget(QLabel("Larghezza:"))
        self.width_entry = QLineEdit(str(width))
        self.width_entry.setStyleSheet("background-color: #1e1e1e; color: #d4d4d4;")
        toolbar_layout.addWidget(self.width_entry)

        toolbar_layout.addWidget(QLabel("Altezza:"))
        self.height_entry = QLineEdit(str(height))
        self.height_entry.setStyleSheet("background-color: #1e1e1e; color: #d4d4d4;")
        toolbar_layout.addWidget(self.height_entry)

        self.apply_button = QPushButton("Applica")
        self.apply_button.setStyleSheet("background-color: #0e639c; color: white; padding: 5px;")
        self.apply_button.clicked.connect(self.resize_paper)
        toolbar_layout.addWidget(self.apply_button)
        toolbar_layout.addStretch()

        # Scena e view personalizzata
        self.scene = QGraphicsScene()
        BIG = 10000
        self.scene.setSceneRect(-BIG, -BIG, BIG * 2, BIG * 2)

        self.view = CustomGraphicsView(self.scene)

        # Foglio
        self.paper = QGraphicsRectItem(0, 0, self.paper_width, self.paper_height)
        self.paper.setBrush(QBrush(QColor("#f3f3f3")))
        self.paper.setPen(QColor("#cccccc"))
        self.scene.addItem(self.paper)
        self.center_paper()

        # Splitter per toolbar ridimensionabile
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.toolbar)
        splitter.addWidget(self.view)
        splitter.setSizes([220, 780])
        main_layout.addWidget(splitter)

    def center_paper(self):
        view_rect = self.view.viewport().rect()
        x = (view_rect.width() - self.paper_width) / 2
        y = (view_rect.height() - self.paper_height) / 2
        self.paper.setPos(x, y)

    def resize_paper(self):
        try:
            w = int(self.width_entry.text())
            h = int(self.height_entry.text())
            self.paper_width = w
            self.paper_height = h
            self.paper.setRect(0, 0, self.paper_width, self.paper_height)
            self.center_paper()
        except ValueError:
            print("Inserisci numeri validi")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    board = VectorBoard()
    board.show()
    sys.exit(app.exec())
