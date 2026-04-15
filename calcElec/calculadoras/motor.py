from PyQt6.QtWidgets import QLineEdit, QComboBox, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from calculadoras.base import CalculadoraBase
import formulas
import math

class CalculoMotor(CalculadoraBase):
    NOMBRE = "Motor Eléctrico"
    SUBTITULO = "Cálculo completo de instalación de motor trifásico"
    ICONO = "HP"

    def build_inputs(self):
        info = QLabel("Cálculo completo: Corriente nominal, arranque, protección, conductor y contactor para motor trifásico.")
        info.setObjectName("info_box")
        info.setWordWrap(True)
        self.layout_inputs.addWidget(info)

        # Potencia del motor
        self.inp_potencia = QLineEdit()
        self.inp_potencia.setPlaceholderText("Ej: 7.5")
        self.add_field("Potencia del motor (kW)", self.inp_potencia, required=True)

        # Tensión de línea
        self.cmb_tension = QComboBox()
        self.cmb_tension.addItems(["220 V", "380 V", "440 V"])
        self.cmb_tension.setCurrentText("380 V")
        self.add_field("Tensión de línea (V)", self.cmb_tension, required=True)

        # Rendimiento η
        self.inp_eta = QLineEdit("0.85")
        self.add_field("Rendimiento η", self.inp_eta, hint="Rango: 0.01 - 1.0", required=True)

        # Factor de potencia cosφ
        self.inp_fp = QLineEdit("0.85")
        self.add_field("Factor de potencia cosφ", self.inp_fp, hint="Rango: 0.01 - 1.0", required=True)

        # Tipo de arranque
        self.cmb_arranque = QComboBox()
        self.cmb_arranque.addItems([
            "Directo (DOL) - K_arr = 6",
            "Estrella-Triángulo - K_arr = 2.15",
            "Variador de frecuencia (VFD) - K_arr = 1.25",
        ])
        self.add_field("Tipo de arranque", self.cmb_arranque, required=True)

    def calcular(self):
        try:
            p_kw = float(self.inp_potencia.text())
        except:
            raise ValueError("Potencia del motor es requerida")
        if p_kw <= 0:
            raise ValueError("Potencia del motor debe ser positiva")

        vl_str = self.cmb_tension.currentText().replace(" V", "")
        vl = float(vl_str)

        try:
            eta = float(self.inp_eta.text())
        except:
            raise ValueError("Rendimiento η es requerido")
        if eta <= 0 or eta > 1:
            raise ValueError("Rendimiento η debe estar entre 0.01 y 1.0")

        try:
            fp = float(self.inp_fp.text())
        except:
            raise ValueError("Factor de potencia es requerido")
        if fp <= 0 or fp > 1:
            raise ValueError("Factor de potencia debe estar entre 0.01 y 1.0")

        idx_arr = self.cmb_arranque.currentIndex()
        tipo_map = {0: "directo", 1: "estrella-triangulo", 2: "variador"}
        tipo_arranque = tipo_map.get(idx_arr, "directo")

        self.resultado_data = formulas.calcular_motor(p_kw, vl, eta, fp, tipo_arranque)

    def build_resultados(self):
        r = self.resultado_data
        # Grid 2 columnas
        grid = QHBoxLayout()
        grid.setSpacing(12)

        # Corriente nominal
        col1 = QVBoxLayout()
        lbl1 = QLabel("Corriente Nominal")
        lbl1.setObjectName("resultado_label")
        col1.addWidget(lbl1)
        val1 = QLabel(f"{r['In']:.2f} A")
        val1.setObjectName("resultado_valor_cyan")
        col1.addWidget(val1)
        grid.addLayout(col1)

        # Corriente de arranque
        col2 = QVBoxLayout()
        lbl2 = QLabel("Corriente de Arranque")
        lbl2.setObjectName("resultado_label")
        col2.addWidget(lbl2)
        val2 = QLabel(f"{r['I_arr']:.2f} A")
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

        grid2 = QHBoxLayout()
        grid2.setSpacing(12)

        # Protección térmica
        col3 = QVBoxLayout()
        lbl3 = QLabel("Protección Térmica")
        lbl3.setObjectName("resultado_label")
        col3.addWidget(lbl3)
        val3 = QLabel(f"{r['prot']} A")
        val3.setObjectName("resultado_valor")
        col3.addWidget(val3)
        grid2.addLayout(col3)

        # Conductor
        col4 = QVBoxLayout()
        lbl4 = QLabel("Conductor")
        lbl4.setObjectName("resultado_label")
        col4.addWidget(lbl4)
        val4 = QLabel(f"{r['conductor']} mm²")
        val4.setObjectName("resultado_valor_cyan")
        col4.addWidget(val4)
        grid2.addLayout(col4)

        self.layout_resultado.addLayout(grid2)

        # Contactor (span 2 cols)
        cat = "AC-4" if self.cmb_arranque.currentIndex() == 2 else "AC-3"
        row_contact = QHBoxLayout()
        lbl5 = QLabel("Contactor")
        lbl5.setObjectName("resultado_label")
        lbl5.setFixedWidth(230)
        row_contact.addWidget(lbl5)
        val5 = QLabel(f"{r['contactor']} A ({cat})")
        val5.setObjectName("resultado_valor")
        row_contact.addWidget(val5)
        row_contact.addStretch()
        self.layout_resultado.addLayout(row_contact)
