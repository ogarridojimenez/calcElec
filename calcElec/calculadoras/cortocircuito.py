from PyQt6.QtWidgets import QLineEdit, QComboBox, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from calculadoras.base import CalculadoraBase
import formulas
import math

class CalculoCortocircuito(CalculadoraBase):
    NOMBRE = "Cortocircuito (NC 801)"
    SUBTITULO = "Cálculo de corrientes de cortocircuito"
    ICONO = "Icc"

    def build_inputs(self):
        info = QLabel("Cálculo de corriente de cortocircuito trifásica y monofásica mínima para verificación del poder de corte del interruptor.")
        info.setObjectName("info_box")
        info.setWordWrap(True)
        self.layout_inputs.addWidget(info)

        # Tensión de línea
        self.cmb_vl = QComboBox()
        self.cmb_vl.addItems(["220", "380", "440"])
        self.cmb_vl.setCurrentText("380")
        self.add_field("Tensión de línea (V)", self.cmb_vl, required=True)

        # Tensión de fase
        self.cmb_vf = QComboBox()
        self.cmb_vf.addItems(["127", "220"])
        self.cmb_vf.setCurrentText("220")
        self.add_field("Tensión de fase (V)", self.cmb_vf, required=True)

        # Longitud del conductor
        self.inp_l = QLineEdit()
        self.inp_l.setPlaceholderText("Ej: 50")
        self.add_field("Longitud del conductor (m)", self.inp_l, required=True)

        # Sección del conductor
        self.inp_seccion = QLineEdit()
        self.inp_seccion.setPlaceholderText("Ej: 10")
        self.add_field("Sección del conductor (mm²)", self.inp_seccion, required=True)

        # Material del conductor
        self.cmb_material = QComboBox()
        self.cmb_material.addItems(["Cobre", "Aluminio"])
        self.add_field("Material del conductor", self.cmb_material, required=True)

        # Poder de corte del interruptor
        self.cmb_poder_corte = QComboBox()
        poderes = [6, 10, 16, 25, 36, 50, 100]
        self.cmb_poder_corte.addItems([str(p) for p in poderes])
        self.cmb_poder_corte.setCurrentText("25")
        self.add_field("Poder de corte del interruptor (kA)", self.cmb_poder_corte, required=True)

    def calcular(self):
        vl = float(self.cmb_vl.currentText())
        vf = float(self.cmb_vf.currentText())

        try:
            longitud = float(self.inp_l.text())
        except:
            raise ValueError("Longitud del conductor es requerida")
        if longitud <= 0:
            raise ValueError("Longitud debe ser positiva")

        try:
            seccion = float(self.inp_seccion.text())
        except:
            raise ValueError("Sección del conductor es requerida")
        if seccion <= 0:
            raise ValueError("Sección debe ser positiva")

        material = "cobre" if self.cmb_material.currentIndex() == 0 else "aluminio"
        poder_corte = float(self.cmb_poder_corte.currentText())

        self._resultado = formulas.calcular_cortocircuito(vl, vf, longitud, seccion, material)
        self._resultado['poder_corte'] = poder_corte

    def build_resultados(self):
        r = self._resultado

        # Grid 2 columnas
        grid = QHBoxLayout()
        grid.setSpacing(12)

        col1 = QVBoxLayout()
        lbl1 = QLabel("Icc Trifásico")
        lbl1.setObjectName("resultado_label")
        col1.addWidget(lbl1)
        val1 = QLabel(f"{r['Icc_3f']:.2f} kA")
        val1.setObjectName("resultado_valor_red")
        col1.addWidget(val1)
        grid.addLayout(col1)

        col2 = QVBoxLayout()
        lbl2 = QLabel("Icc Monofásico Mín.")
        lbl2.setObjectName("resultado_label")
        col2.addWidget(lbl2)
        val2 = QLabel(f"{r['Icc_1f']:.0f} A")
        val2.setObjectName("resultado_valor_amber")
        col2.addWidget(val2)
        grid.addLayout(col2)

        self.layout_resultado.addLayout(grid)

        # Separador
        sep = QFrame()
        sep.setObjectName("separador")
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFixedHeight(1)
        self.layout_resultado.addWidget(sep)

        # Verificación
        apto = r['poder_corte'] >= r['Icc_3f']

        row_v = QHBoxLayout()
        lbl_v = QLabel("Verificación")
        lbl_v.setObjectName("resultado_label")
        lbl_v.setFixedWidth(230)
        row_v.addWidget(lbl_v)
        if apto:
            val_v = QLabel(f"✓ Interruptor de {r['poder_corte']} kA vs Icc de {r['Icc_3f']:.2f} kA")
            val_v.setObjectName("cumple")
        else:
            val_v = QLabel(f"✗ Interruptor de {r['poder_corte']} kA vs Icc de {r['Icc_3f']:.2f} kA")
            val_v.setObjectName("no_cumple")
        row_v.addWidget(val_v)
        row_v.addStretch()
        self.layout_resultado.addLayout(row_v)
