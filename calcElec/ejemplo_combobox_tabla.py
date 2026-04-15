"""
Ejemplo funcional: QComboBox en QTableWidget
PyQt6 - Valores seleccionados visibles
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QComboBox, QHBoxLayout, QPushButton,
    QLineEdit, QLabel
)
from PyQt6.QtCore import Qt

class EjemploComboBox(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QComboBox en QTableWidget - Ejemplo")
        self.resize(500, 300)
        
        layout = QVBoxLayout(self)
        
        # Tabla
        self.tabla = QTableWidget(3, 3)
        self.tabla.setHorizontalHeaderLabels(["Sección mm²", "Cantidad", "Área"])
        layout.addWidget(self.tabla)
        
        # Agregar filas con QComboBox
        for row in range(3):
            self.agregar_fila(row)
        
        # Botón agregar
        btn = QPushButton("[ + agregar ]")
        btn.clicked.connect(self.agregar_nueva_fila)
        layout.addWidget(btn)
    
    def agregar_fila(self, row):
        # COMBOBOX - con estilos inline
        combo = QComboBox()
        combo.addItems(["1.5", "2.5", "4", "6", "10", "16", "25", "35"])
        combo.setCurrentIndex(1)  # Default a 2.5
        
        # ESTILOS CRÍTICOS para visibilidad
        combo.setStyleSheet("""
            QComboBox {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 6px 10px;
                font-size: 13px;
                font-family: Consolas, monospace;
                min-width: 80px;
            }
            QComboBox::drop-down {
                border: none;
                width: 25px;
                background: #2d2d2d;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 5px solid #888;
                margin-right: 6px;
            }
            QComboBox QAbstractItemView {
                background-color: #1e1e1e;
                color: #ffffff;
                selection-background-color: #264f78;
                border: 1px solid #3c3c3c;
                padding: 4px;
            }
        """)
        
        # Insertar en celda
        self.tabla.setCellWidget(row, 0, combo)
        
        # INPUT - también con estilos
        input_cant = QLineEdit("1")
        input_cant.setStyleSheet("""
            QLineEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 6px 10px;
                font-size: 13px;
                font-family: Consolas, monospace;
                min-width: 50px;
            }
        """)
        self.tabla.setCellWidget(row, 1, input_cant)
        
        # Label resultado
        lbl = QLabel("-")
        lbl.setStyleSheet("color: #569cd6; background: transparent;")
        self.tabla.setCellWidget(row, 2, lbl)
        
        # Conectar cambio para actualizar área
        combo.currentIndexChanged.connect(
            lambda idx, r=row: self.actualizar_area(r)
        )
    
    def actualizar_area(self, row):
        combo = self.tabla.cellWidget(row, 0)
        lbl = self.tabla.cellWidget(row, 2)
        area = float(combo.currentText()) * 10  # Ejemplo
        lbl.setText(f"{area:.1f}")
    
    def agregar_nueva_fila(self):
        row = self.tabla.rowCount()
        self.tabla.insertRow(row)
        self.agregar_fila(row)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Estilo global para la app
    app.setStyle("Fusion")
    app.setStyleSheet("""
        QMainWindow, QWidget {
            background-color: #121212;
            color: #ffffff;
            font-family: Consolas, monospace;
        }
    """)
    w = EjemploComboBox()
    w.show()
    sys.exit(app.exec())