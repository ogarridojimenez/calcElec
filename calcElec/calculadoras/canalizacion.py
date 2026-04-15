from PyQt6.QtWidgets import (
    QLineEdit, QComboBox, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame
)
from PyQt6.QtCore import Qt
from calculadoras.base import CalculadoraBase
import formulas
import math

# Áreas de conductores (diámetro exterior真正的)
AREAS_COND = {1.5:8.11, 2.5:13.48, 4:20.43, 6:28.89, 10:51.87, 16:81.07, 25:126.7, 35:166.3}

# Áreas interiores de tubos (mm²)
TUBOS = [
    ("DN16 - Ø16mm (Área: 113mm²)", 16),
    ("DN20 - Ø20mm (Área: 201mm²)", 20),
    ("DN25 - Ø25mm (Área: 314mm²)", 25),
    ("DN32 - Ø32mm (Área: 615mm²)", 32),
    ("DN40 - Ø40mm (Área: 962mm²)", 40),
    ("DN50 - Ø50mm (Área: 1590mm²)", 50),
]

class CalculoCanalizacion(CalculadoraBase):
    NOMBRE = "Canalizaciones (NC 800)"
    SUBTITULO = "Cálculo de ocupación de tubos"
    ICONO = "%"

    def build_inputs(self):
        info = QLabel("Límite máximo de ocupación: ≤40% según NC 800")
        info.setObjectName("info_box")
        info.setWordWrap(True)
        self.layout_inputs.addWidget(info)

        # Lista dinámica de conductores
        self._conductores_widgets = []
        self._btn_add = QPushButton("[ + agregar conductor ]")
        self._btn_add.setObjectName("btn_agregar")
        self._btn_add.setFixedHeight(36)
        self._btn_add.clicked.connect(self._agregar_conductor)
        self.layout_inputs.addWidget(self._btn_add)
        self._agregar_conductor()

        # Separador
        sep = QFrame()
        sep.setObjectName("separador")
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFixedHeight(1)
        self.layout_inputs.addWidget(sep)

        # Tubo seleccionado
        self.cmb_tubo = QComboBox()
        for nombre, _ in TUBOS:
            self.cmb_tubo.addItem(nombre)
        self.cmb_tubo.setCurrentIndex(2)

        self.add_field("Tubo seleccionado", self.cmb_tubo, required=True)

    def _agregar_conductor(self):
        row = QHBoxLayout()
        row.setSpacing(10)

        cmb = QComboBox()
        secciones = [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120]
        cmb.addItems([str(s) for s in secciones])

        inp = QLineEdit("1")
        inp.setPlaceholderText("Cant.")
        inp.setFixedWidth(80)

        btn_del = QPushButton("✕")
        btn_del.setObjectName("btn_eliminar")
        btn_del.setFixedWidth(32)
        btn_del.setFixedHeight(32)
        btn_del.clicked.connect(lambda checked, r=row, c=cmb, i=inp: self._eliminar_conductor(r, c, i))

        lbl = QLabel("mm²:")
        lbl.setObjectName("label")
        row.addWidget(lbl)
        row.addWidget(cmb, 1)
        row.addWidget(inp, 0)
        row.addWidget(btn_del)

        self._conductores_widgets.append((cmb, inp, row))
        self.layout_inputs.addLayout(row)

    def _eliminar_conductor(self, row_layout, cmb, inp):
        # Hide all widgets in the row
        for i in range(row_layout.count()):
            widget = row_layout.itemAt(i).widget()
            if widget:
                widget.hide()
                widget.deleteLater()
        
        # Remove from tracking list
        for item in self._conductores_widgets[:]:
            if item[2] == row_layout:  # Match by row layout reference
                self._conductores_widgets.remove(item)
                break
        
        # Delete the layout itself to prevent orphan layout
        row_layout.setParent(None)
        del row_layout

    def calcular(self):
        conductores = []
        for cmb, inp, row in self._conductores_widgets:
            if not cmb.isVisible():
                continue
            if inp.text().strip():
                try:
                    cant = int(inp.text())
                except:
                    cant = 0
                if cant > 0:
                    conductores.append({
                        "seccion": float(cmb.currentText()),
                        "cantidad": cant
                    })
        if not conductores:
            raise ValueError("Agregue al menos un conductor")

        _, d_tubo = TUBOS[self.cmb_tubo.currentIndex()]
        self._resultado = formulas.calcular_canalizacion(conductores, d_tubo)
        self._resultado['tubo_nom'] = TUBOS[self.cmb_tubo.currentIndex()][0]

        # Si no cumple, buscar siguiente
        if not self._resultado['cumple']:
            for nombre, d in TUBOS:
                res_alt = formulas.calcular_canalizacion(conductores, d)
                if res_alt['cumple']:
                    self._resultado['recomendado'] = nombre
                    break

    def build_resultados(self):
        r = self._resultado
        cumple = r['cumple']

        row1 = QHBoxLayout()
        lbl1 = QLabel("% Ocupación")
        lbl1.setObjectName("resultado_label")
        lbl1.setFixedWidth(230)
        row1.addWidget(lbl1)
        val1 = QLabel(f"{r['pct']:.1f}%")
        val1.setObjectName("resultado_valor" if cumple else "resultado_valor_red")
        row1.addWidget(val1)
        row1.addStretch()
        self.layout_resultado.addLayout(row1)

        row2 = QHBoxLayout()
        lbl2 = QLabel("Estado")
        lbl2.setObjectName("resultado_label")
        lbl2.setFixedWidth(230)
        row2.addWidget(lbl2)
        val2 = QLabel("✓ CUMPLE (≤40%)" if cumple else "✗ NO CUMPLE (>40%)")
        val2.setObjectName("cumple" if cumple else "no_cumple")
        row2.addWidget(val2)
        row2.addStretch()
        self.layout_resultado.addLayout(row2)

        if not cumple and 'recomendado' in r:
            row3 = QHBoxLayout()
            lbl3 = QLabel("Recomendación")
            lbl3.setObjectName("resultado_label")
            lbl3.setFixedWidth(230)
            row3.addWidget(lbl3)
            val3 = QLabel(f"Se recomienda usar {r['recomendado']}")
            val3.setObjectName("resultado_valor_amber")
            row3.addWidget(val3)
            row3.addStretch()
            self.layout_resultado.addLayout(row3)
