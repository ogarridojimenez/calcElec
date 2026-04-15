from PyQt6.QtWidgets import QLineEdit, QVBoxLayout, QLabel
from PyQt6.QtCore import QTimer
from calculadoras.base import CalculadoraBase
import formulas
import math

class CalculoFactorPotencia(CalculadoraBase):
    NOMBRE = "Corrección del Factor de Potencia"
    SUBTITULO = "Cálculo de banco de capacitores"
    ICONO = "%"

    def build_inputs(self):
        info = QLabel("Requisito mínimo: FP ≥ 0.90. Fórmula: Qc = P × (tan(φ₁) - tan(φ₂))")
        info.setObjectName("info_box")
        info.setWordWrap(True)
        self.layout_inputs.addWidget(info)

        # Potencia Activa
        self.inp_potencia = QLineEdit()
        self.inp_potencia.setPlaceholderText("Ej: 100")
        self.add_field("Potencia Activa (kW)", self.inp_potencia, required=True)

        # FP Actual
        self.inp_fp_actual = QLineEdit("0.7")
        self.lbl_angulo1 = QLabel("φ₁ = {:.1f}°".format(math.degrees(math.acos(0.7))))
        self.lbl_angulo1.setObjectName("hint_text")
        col_fp1 = QVBoxLayout()
        lbl1 = QLabel("FP Actual cosφ₁")
        lbl1.setObjectName("label")
        col_fp1.addWidget(lbl1)
        col_fp1.addWidget(self.inp_fp_actual)
        col_fp1.addWidget(self.lbl_angulo1)
        self.layout_inputs.addLayout(col_fp1)

        # FP Deseado
        self.inp_fp_deseado = QLineEdit("0.95")
        self.lbl_angulo2 = QLabel("φ₂ = {:.1f}°".format(math.degrees(math.acos(0.95))))
        self.lbl_angulo2.setObjectName("hint_text")
        col_fp2 = QVBoxLayout()
        lbl2 = QLabel("FP Deseado cosφ₂")
        lbl2.setObjectName("label")
        col_fp2.addWidget(lbl2)
        col_fp2.addWidget(self.inp_fp_deseado)
        col_fp2.addWidget(self.lbl_angulo2)
        self.layout_inputs.addLayout(col_fp2)

        # Actualizar ángulos dinámicamente
        self.inp_fp_actual.textChanged.connect(self._update_angulos)
        self.inp_fp_deseado.textChanged.connect(self._update_angulos)

    def _update_angulos(self):
        try:
            fp1 = float(self.inp_fp_actual.text())
            if 0.01 <= fp1 <= 1.0:
                self.lbl_angulo1.setText("φ₁ = {:.1f}°".format(math.degrees(math.acos(fp1))))
            else:
                self.lbl_angulo1.setText("")
        except:
            self.lbl_angulo1.setText("")
        try:
            fp2 = float(self.inp_fp_deseado.text())
            if 0.01 <= fp2 <= 1.0:
                self.lbl_angulo2.setText("φ₂ = {:.1f}°".format(math.degrees(math.acos(fp2))))
            else:
                self.lbl_angulo2.setText("")
        except:
            self.lbl_angulo2.setText("")

    def calcular(self):
        try:
            p_kw = float(self.inp_potencia.text())
        except:
            raise ValueError("Potencia Activa es requerida")
        if p_kw <= 0:
            raise ValueError("Potencia Activa debe ser positiva")
        try:
            fp1 = float(self.inp_fp_actual.text())
        except:
            raise ValueError("FP Actual es requerido")
        if fp1 < 0.01 or fp1 > 1.0:
            raise ValueError("FP Actual debe estar entre 0.01 y 1.0")
        try:
            fp2 = float(self.inp_fp_deseado.text())
        except:
            raise ValueError("FP Deseado es requerido")
        if fp2 < 0.01 or fp2 > 1.0:
            raise ValueError("FP Deseado debe estar entre 0.01 y 1.0")
        if fp2 <= fp1:
            raise ValueError("FP Deseado DEBE ser mayor que FP Actual")

        self.resultado_data = formulas.calcular_factor_potencia(p_kw, fp1, fp2)

    def build_resultados(self):
        r = self.resultado_data
        self.add_resultado_item("Capacitor Qc", f"{r['valor']:.3f} {r['unidad']}", "cyan")
        self.add_resultado_item("Fórmula", r['formula'], "cyan")
        if r.get('nota'):
            self.add_resultado_item("Detalle", r['nota'], "cyan")
