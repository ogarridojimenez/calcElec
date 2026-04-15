from PyQt6.QtWidgets import QLineEdit, QComboBox, QVBoxLayout, QHBoxLayout, QLabel
from calculadoras.base import CalculadoraBase
import formulas
from constants import TIPOS_SUELO

class CalculoPuestaTierra(CalculadoraBase):
    NOMBRE = "Puesta a Tierra"
    SUBTITULO = "Cálculo de resistencia de puesta a tierra · Norma NC 802"
    ICONO = "±"

    def build_inputs(self):
        info = QLabel("Resistencia de puesta a tierra debe ser ≤ 25Ω (NC 802)")
        info.setObjectName("info_box_amber")
        info.setWordWrap(True)
        self.layout_inputs.addWidget(info)

        # Tipo de suelo
        self.cmb_suelo = QComboBox()
        self.cmb_suelo.addItems([f"{t['nombre']} ({t['rho']} Ω·m)" for t in TIPOS_SUELO])
        self.cmb_suelo.setCurrentIndex(2)  # Arcilla default
        self.cmb_suelo.currentIndexChanged.connect(self._update_rho)
        self.add_field("Tipo de Suelo", self.cmb_suelo, required=True)

        # Resistividad
        self.inp_rho = QLineEdit("1000")
        self.add_field("Resistividad (Ω·m)", self.inp_rho, hint="Editable, se actualiza al cambiar tipo suelo", required=True)

        # Longitud varilla
        self.inp_l = QLineEdit("2.4")
        self.add_field("Longitud Varilla (m)", self.inp_l, hint="Máx 10m", required=True)

        # Diámetro varilla
        self.cmb_diametro = QComboBox()
        self.cmb_diametro.addItems(["12 mm (Copperweld)", "16 mm (estándar)", "20 mm (cobre sólido)"])
        self.cmb_diametro.setCurrentIndex(1)
        self.add_field("Diámetro Varilla", self.cmb_diametro, required=True)

        # Número de varillas
        self.inp_n = QLineEdit("1")
        self.add_field("Número de Varillas", self.inp_n, hint="Espaciado mínimo 2× la longitud de la varilla", required=True)

    def _update_rho(self):
        idx = self.cmb_suelo.currentIndex()
        if idx >= 0 and idx < len(TIPOS_SUELO):
            self.inp_rho.setText(str(TIPOS_SUELO[idx]['rho']))

    def calcular(self):
        try:
            rho = float(self.inp_rho.text())
        except:
            raise ValueError("Resistividad es requerida")
        if rho <= 0:
            raise ValueError("Resistividad debe ser positiva")

        try:
            L = float(self.inp_l.text())
        except:
            raise ValueError("Longitud de varilla es requerida")
        if L <= 0 or L > 10:
            raise ValueError("Longitud debe estar entre 0 y 10m")

        diametros = [12, 16, 20]
        d_mm = diametros[self.cmb_diametro.currentIndex()]

        try:
            n = int(self.inp_n.text())
        except:
            raise ValueError("Número de varillas es requerido")
        if n < 1 or n > 20:
            raise ValueError("Número de varillas debe estar entre 1 y 20")

        self.resultado_data = formulas.calcular_puesta_tierra(rho, L, d_mm, n)

    def build_resultados(self):
        r = self.resultado_data
        cumple = r['valor'] <= 25

        obj_name = "resultado_valor" if cumple else "resultado_valor_red"
        row1 = QHBoxLayout()
        lbl1 = QLabel("Resistencia")
        lbl1.setObjectName("resultado_label")
        lbl1.setFixedWidth(230)
        row1.addWidget(lbl1)
        val1 = QLabel(f"{r['valor']:.2f} {r['unidad']}")
        val1.setObjectName(obj_name)
        row1.addWidget(val1)
        row1.addStretch()
        self.layout_resultado.addLayout(row1)

        self.add_resultado_item("Fórmula", r['formula'], "cyan")
        if r.get('nota'):
            self.add_resultado_item("Detalle", r['nota'], "cyan")
