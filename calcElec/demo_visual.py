"""
Demo Visual - Propuestas de Diseño para CalcEléc
Muestra 4 estilos diferentes en pestañas separadas para comparar.
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QComboBox, QFrame, QScrollArea,
    QTabWidget, QGroupBox, QRadioButton, QGridLayout, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

# ═══════════════════════════════════════════════════════════
# THEME 1: Material Design (Light)
# ═══════════════════════════════════════════════════════════
THEME_MATERIAL = """
QMainWindow {
    background-color: #f5f5f5;
}

QWidget {
    font-family: 'Segoe UI', 'Roboto', sans-serif;
    font-size: 14px;
    color: #212121;
}

QLabel#titulo {
    font-size: 28px;
    font-weight: 700;
    color: #1976D2;
    margin-bottom: 8px;
}

QLabel#subtitulo {
    font-size: 14px;
    color: #757575;
}

QLabel#label {
    font-size: 12px;
    color: #616161;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

QLabel#resultado_valor {
    font-size: 32px;
    font-weight: 700;
    color: #4CAF50;
}

QLabel#resultado_label {
    font-size: 14px;
    color: #757575;
}

QFrame#tarjeta {
    background: #ffffff;
    border-radius: 16px;
    padding: 24px;
}

QFrame#resultado_frame {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #E8F5E9, stop:1 #C8E6C9);
    border-radius: 16px;
    padding: 24px;
}

QLineEdit, QComboBox {
    border: none;
    border-bottom: 2px solid #e0e0e0;
    border-radius: 0;
    padding: 12px 8px;
    background: transparent;
    font-size: 15px;
    color: #212121;
}

QLineEdit:focus {
    border-bottom: 2px solid #1976D2;
    background: #E3F2FD;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
}

QComboBox::down-arrow {
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #757575;
}

QPushButton#btn_calcular {
    background: #1976D2;
    color: white;
    border: none;
    border-radius: 24px;
    padding: 14px 48px;
    font-size: 15px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

QPushButton#btn_calcular:hover {
    background: #1565C0;
}

QPushButton#btn_calcular:pressed {
    background: #0D47A1;
}

QPushButton#btn_guardar {
    background: #4CAF50;
    color: white;
    border: none;
    border-radius: 20px;
    padding: 12px 28px;
    font-size: 14px;
    font-weight: 500;
}

QPushButton#btn_secundario {
    background: transparent;
    color: #1976D2;
    border: 2px solid #1976D2;
    border-radius: 20px;
    padding: 10px 24px;
    font-size: 13px;
    font-weight: 500;
}

QPushButton#btn_secundario:hover {
    background: #E3F2FD;
}

QRadioButton {
    font-size: 14px;
    color: #424242;
    padding: 8px 16px;
    spacing: 8px;
}

QRadioButton::indicator {
    width: 20px;
    height: 20px;
    border-radius: 10px;
    border: 2px solid #757575;
    background: white;
}

QRadioButton::indicator:checked {
    border: 6px solid #1976D2;
    background: white;
}

QFrame#separador {
    background: #e0e0e0;
    max-height: 1px;
}
"""

# ═══════════════════════════════════════════════════════════
# THEME 2: Glassmorphism Dark (REFINADO - inputs visibles)
# ═══════════════════════════════════════════════════════════
THEME_GLASS = """
QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0f0c29, stop:0.5 #302b63, stop:1 #24243e);
}

QWidget {
    font-family: 'Segoe UI', 'Inter', sans-serif;
    font-size: 14px;
    color: #e8e8e8;
    background: transparent;
}

QLabel#titulo {
    font-size: 26px;
    font-weight: 700;
    color: #ffffff;
}

QLabel#subtitulo {
    font-size: 13px;
    color: #a0a0a0;
}

QLabel#label {
    font-size: 11px;
    color: #b0b0b0;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

QLabel#resultado_valor {
    font-size: 28px;
    font-weight: 700;
    color: #00ff88;
}

QLabel#resultado_label {
    font-size: 13px;
    color: #a0a0a0;
}

QFrame#tarjeta {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 14px;
    padding: 24px;
}

QFrame#resultado_frame {
    background: rgba(0, 255, 136, 0.08);
    border: 1px solid rgba(0, 255, 136, 0.3);
    border-left: 4px solid #00ff88;
    border-radius: 12px;
    padding: 20px;
}

QLineEdit, QComboBox {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.25);
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 14px;
    color: #ffffff;
    min-height: 24px;
}

QLineEdit:focus, QComboBox:focus {
    border: 1px solid #00d4ff;
    background: rgba(0, 212, 255, 0.1);
}

QLineEdit::placeholder {
    color: #707070;
}

QComboBox::drop-down {
    border: none;
    width: 32px;
    border-left: 1px solid rgba(255, 255, 255, 0.15);
}

QComboBox::down-arrow {
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #a0a0a0;
    margin-right: 8px;
}

QComboBox QAbstractItemView {
    background: #1a1a3e;
    color: #ffffff;
    border: 1px solid rgba(0, 212, 255, 0.4);
    selection-background-color: rgba(0, 212, 255, 0.3);
    selection-color: #ffffff;
    padding: 6px;
}

QPushButton#btn_calcular {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00d4ff, stop:1 #00ff88);
    color: #0f0c29;
    border: none;
    border-radius: 12px;
    padding: 14px 40px;
    font-size: 15px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

QPushButton#btn_calcular:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00ff88, stop:1 #00d4ff);
}

QPushButton#btn_guardar {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #00ff88, stop:1 #00cc6a);
    color: #0f0c29;
    border: none;
    border-radius: 10px;
    padding: 12px 28px;
    font-size: 14px;
    font-weight: 600;
}

QPushButton#btn_secundario {
    background: transparent;
    color: #00d4ff;
    border: 1px solid rgba(0, 212, 255, 0.4);
    border-radius: 10px;
    padding: 10px 24px;
    font-size: 13px;
    font-weight: 500;
}

QPushButton#btn_secundario:hover {
    background: rgba(0, 212, 255, 0.12);
    border-color: #00d4ff;
}

QRadioButton {
    font-size: 13px;
    color: #d0d0d0;
    padding: 10px 18px;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 10px;
    margin: 2px;
}

QRadioButton::indicator {
    width: 0;
    height: 0;
}

QRadioButton:checked {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00d4ff, stop:1 #00ff88);
    color: #0f0c29;
    border-color: transparent;
    font-weight: 700;
}

QFrame#separador {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 transparent, stop:0.5 rgba(255,255,255,0.25), stop:1 transparent);
    max-height: 1px;
}
"""

# ═══════════════════════════════════════════════════════════
# THEME 3: Dashboard Profesional
# ═══════════════════════════════════════════════════════════
THEME_DASHBOARD = """
QMainWindow {
    background-color: #f0f2f5;
}

QWidget {
    font-family: 'Segoe UI', 'Inter', sans-serif;
    font-size: 14px;
    color: #1a1a2e;
}

QLabel#titulo {
    font-size: 26px;
    font-weight: 800;
    color: #1a1a2e;
    letter-spacing: -0.5px;
}

QLabel#subtitulo {
    font-size: 13px;
    color: #6c757d;
}

QLabel#label {
    font-size: 11px;
    color: #495057;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

QLabel#resultado_valor {
    font-size: 30px;
    font-weight: 800;
    color: #28a745;
}

QLabel#resultado_label {
    font-size: 13px;
    color: #6c757d;
    font-weight: 500;
}

QFrame#tarjeta {
    background: #ffffff;
    border: 1px solid #dee2e6;
    border-radius: 12px;
    padding: 24px;
}

QFrame#resultado_frame {
    background: #ffffff;
    border: 2px solid #28a745;
    border-radius: 12px;
    padding: 24px;
}

QLineEdit, QComboBox {
    background: #f8f9fa;
    border: 2px solid #dee2e6;
    border-radius: 8px;
    padding: 12px 14px;
    font-size: 14px;
    color: #1a1a2e;
}

QLineEdit:focus {
    border: 2px solid #007bff;
    background: #ffffff;
}

QComboBox::drop-down {
    border: none;
    width: 32px;
    border-left: 2px solid #dee2e6;
}

QComboBox::down-arrow {
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #495057;
}

QPushButton#btn_calcular {
    background: #007bff;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 14px 36px;
    font-size: 14px;
    font-weight: 700;
}

QPushButton#btn_calcular:hover {
    background: #0056b3;
}

QPushButton#btn_calcular:disabled {
    background: #adb5bd;
}

QPushButton#btn_guardar {
    background: #28a745;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-size: 13px;
    font-weight: 600;
}

QPushButton#btn_secundario {
    background: #ffffff;
    color: #007bff;
    border: 2px solid #007bff;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 13px;
    font-weight: 600;
}

QPushButton#btn_secundario:hover {
    background: #e7f1ff;
}

QRadioButton {
    font-size: 13px;
    color: #495057;
    padding: 10px 18px;
    background: #f8f9fa;
    border: 2px solid #dee2e6;
    border-radius: 8px;
    margin: 2px;
}

QRadioButton::indicator {
    width: 0;
    height: 0;
}

QRadioButton:checked {
    background: #007bff;
    color: white;
    border-color: #007bff;
    font-weight: 700;
}

QFrame#separador {
    background: #dee2e6;
    max-height: 2px;
}
"""

# ═══════════════════════════════════════════════════════════
# THEME 4: Cyberpunk Terminal
# ═══════════════════════════════════════════════════════════
THEME_CYBER = """
QMainWindow {
    background-color: #0a0a0a;
}

QWidget {
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 13px;
    color: #00ff41;
}

QLabel#titulo {
    font-size: 28px;
    font-weight: bold;
    color: #00ff41;
    font-family: 'Consolas', monospace;
}

QLabel#subtitulo {
    font-size: 12px;
    color: #0088ff;
    font-family: 'Consolas', monospace;
}

QLabel#label {
    font-size: 11px;
    color: #ff00ff;
    font-weight: bold;
    font-family: 'Consolas', monospace;
}

QLabel#resultado_valor {
    font-size: 32px;
    font-weight: bold;
    color: #00ff41;
    font-family: 'Consolas', monospace;
}

QLabel#resultado_label {
    font-size: 12px;
    color: #0088ff;
    font-family: 'Consolas', monospace;
}

QFrame#tarjeta {
    background: #0d0d0d;
    border: 2px solid #00ff41;
    border-radius: 4px;
    padding: 20px;
}

QFrame#resultado_frame {
    background: #0d0d0d;
    border: 2px solid #00ff41;
    border-radius: 4px;
    padding: 20px;
}

QLineEdit, QComboBox {
    background: #000000;
    border: 1px solid #00ff41;
    border-radius: 2px;
    padding: 10px 12px;
    font-size: 14px;
    font-family: 'Consolas', monospace;
    color: #00ff41;
}

QLineEdit:focus {
    border: 2px solid #00ff41;
    background: #0a0a0a;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
    border-left: 1px solid #00ff41;
}

QComboBox::down-arrow {
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #00ff41;
}

QPushButton#btn_calcular {
    background: #00ff41;
    color: #000000;
    border: 2px solid #00ff41;
    border-radius: 2px;
    padding: 14px 36px;
    font-size: 14px;
    font-weight: bold;
    font-family: 'Consolas', monospace;
    text-transform: uppercase;
}

QPushButton#btn_calcular:hover {
    background: #000000;
    color: #00ff41;
}

QPushButton#btn_guardar {
    background: #0088ff;
    color: #000000;
    border: 2px solid #0088ff;
    border-radius: 2px;
    padding: 12px 24px;
    font-size: 13px;
    font-weight: bold;
    font-family: 'Consolas', monospace;
}

QPushButton#btn_secundario {
    background: #000000;
    color: #ff00ff;
    border: 2px solid #ff00ff;
    border-radius: 2px;
    padding: 10px 20px;
    font-size: 12px;
    font-family: 'Consolas', monospace;
}

QPushButton#btn_secundario:hover {
    background: #ff00ff;
    color: #000000;
}

QRadioButton {
    font-size: 12px;
    color: #00ff41;
    padding: 8px 14px;
    background: #000000;
    border: 1px solid #00ff41;
    border-radius: 2px;
    margin: 2px;
    font-family: 'Consolas', monospace;
}

QRadioButton::indicator {
    width: 0;
    height: 0;
}

QRadioButton:checked {
    background: #00ff41;
    color: #000000;
    border-color: #00ff41;
    font-weight: bold;
}

QFrame#separador {
    background: #00ff41;
    max-height: 2px;
}
"""


class DemoPanel(QWidget):
    """Panel reutilizable que simula una calculadora con un tema"""
    def __init__(self, theme_name, stylesheet, parent=None):
        super().__init__(parent)
        self.setStyleSheet(stylesheet)
        self.setup_ui(theme_name)

    def setup_ui(self, theme_name):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Title section
        title = QLabel("⚡ Caída de Tensión")
        title.setObjectName("titulo")
        layout.addWidget(title)

        subtitle = QLabel("Cálculo según IEC 60364-5-52")
        subtitle.setObjectName("subtitulo")
        layout.addWidget(subtitle)

        # Separator
        sep = QFrame()
        sep.setObjectName("separador")
        layout.addWidget(sep)

        # Input Card
        card = QFrame()
        card.setObjectName("tarjeta")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(16)

        # Add shadow to card (only for Material)
        if "Material" in theme_name:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(25)
            shadow.setXOffset(0)
            shadow.setYOffset(8)
            shadow.setColor(QColor(0, 0, 0, 40))
            card.setGraphicsEffect(shadow)

        # Row 1
        row1 = QHBoxLayout()
        col1 = QVBoxLayout()
        col1.addWidget(QLabel("POTENCIA (W)"))
        inp1 = QLineEdit()
        inp1.setPlaceholderText("1500")
        col1.addWidget(inp1)
        row1.addLayout(col1)

        col2 = QVBoxLayout()
        col2.addWidget(QLabel("LONGITUD (m)"))
        inp2 = QLineEdit()
        inp2.setPlaceholderText("50")
        col2.addWidget(inp2)
        row1.addLayout(col2)
        card_layout.addLayout(row1)

        # Row 2
        row2 = QHBoxLayout()
        col3 = QVBoxLayout()
        col3.addWidget(QLabel("SECCIÓN (mm²)"))
        combo = QComboBox()
        combo.addItems(["1.5", "2.5", "4", "6", "10"])
        col3.addWidget(combo)
        row2.addLayout(col3)

        col4 = QVBoxLayout()
        col4.addWidget(QLabel("TENSIÓN (V)"))
        inp4 = QLineEdit()
        inp4.setPlaceholderText("230")
        col4.addWidget(inp4)
        row2.addLayout(col4)
        card_layout.addLayout(row2)

        layout.addWidget(card)

        # Radio buttons
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(QLabel("MATERIAL:"))
        r1 = QRadioButton("Cobre")
        r2 = QRadioButton("Aluminio")
        r1.setChecked(True)
        radio_layout.addWidget(r1)
        radio_layout.addWidget(r2)
        layout.addLayout(radio_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_calc = QPushButton("▶ CALCULAR")
        btn_calc.setObjectName("btn_calcular")
        btn_layout.addWidget(btn_calc)

        btn_sec = QPushButton("Guardar")
        btn_sec.setObjectName("btn_secundario")
        btn_layout.addWidget(btn_sec)
        layout.addLayout(btn_layout)

        # Result Card
        result_frame = QFrame()
        result_frame.setObjectName("resultado_frame")
        result_layout = QVBoxLayout(result_frame)

        if "Material" in theme_name:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(25)
            shadow.setXOffset(0)
            shadow.setYOffset(8)
            shadow.setColor(QColor(0, 0, 0, 40))
            result_frame.setGraphicsEffect(shadow)

        res_label = QLabel("Caída de tensión calculada")
        res_label.setObjectName("resultado_label")
        result_layout.addWidget(res_label)

        res_valor = QLabel("3.42 V (1.48%)")
        res_valor.setObjectName("resultado_valor")
        result_layout.addWidget(res_valor)

        layout.addWidget(result_frame)

        layout.addStretch()


class DemoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎨 Demo Visual - CalcEléc")
        self.setMinimumSize(1200, 800)
        self.setup_ui()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # Header
        header = QLabel("🎨 Comparador de Estilos - CalcEléc")
        header.setStyleSheet("""
            font-size: 24px; font-weight: bold; color: #1976D2;
            padding: 20px; background: #f5f5f5; border-bottom: 3px solid #1976D2;
            font-family: 'Segoe UI', sans-serif;
        """)
        main_layout.addWidget(header)

        # Tabs
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane { border: none; }
            QTabBar::tab {
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
                font-family: 'Segoe UI', sans-serif;
            }
            QTabBar::tab:selected {
                background: #1976D2;
                color: white;
            }
        """)

        # Add 4 themes as tabs
        themes = [
            ("1️⃣ Material Design", THEME_MATERIAL),
            ("2️⃣ Glassmorphism", THEME_GLASS),
            ("3️⃣ Dashboard Pro", THEME_DASHBOARD),
            ("4️⃣ Cyberpunk Terminal", THEME_CYBER),
        ]

        for name, style in themes:
            panel = DemoPanel(name, style)
            tabs.addTab(panel, name)

        main_layout.addWidget(tabs)

        # Footer
        footer = QLabel("Selecciona cada pestaña para ver el estilo • Todos los controles son funcionales")
        footer.setStyleSheet("""
            font-size: 12px; color: #757575; padding: 12px 20px;
            background: #f5f5f5; text-align: center;
        """)
        main_layout.addWidget(footer)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Better QSS support
    w = DemoWindow()
    w.show()
    sys.exit(app.exec())
