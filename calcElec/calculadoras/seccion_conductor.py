from PyQt6.QtWidgets import QLineEdit, QComboBox, QVBoxLayout, QLabel
from calculadoras.base import CalculadoraBase
import formulas
from constants import K_CU, K_AL, seccion_norm

class CalculoSeccionConductor(CalculadoraBase):
    NOMBRE = "Sección de Conductor"
    SUBTITULO = "Cálculo de sección mínima basada en densidad de corriente"
    ICONO = "mm²"

    def build_inputs(self):
        info = QLabel(f"K = {K_CU} A/mm² para Cobre, K = {K_AL} A/mm² para Aluminio")
        info.setObjectName("info_box")
        info.setWordWrap(True)
        self.layout_inputs.addWidget(info)

        # Corriente de diseño
        self.inp_corriente = QLineEdit()
        self.inp_corriente.setPlaceholderText("Ej: 30")
        self.inp_corriente.textChanged.connect(self._update_hint)
        self.add_field("Corriente de Diseño (A)", self.inp_corriente, hint="Máx 1000A", required=True)

        # Hint dinámico
        self.lbl_hint_seccion = QLabel("")
        self.lbl_hint_seccion.setObjectName("hint_text")
        self.layout_inputs.addWidget(self.lbl_hint_seccion)

        # Material
        self.cmb_material = QComboBox()
        self.cmb_material.addItems(["Cobre (K=56 A/mm²)", "Aluminio (K=35 A/mm²)"])
        self.add_field("Material del Conductor", self.cmb_material, required=True)

    def _update_hint(self):
        try:
            i = float(self.inp_corriente.text())
            material = "cobre" if self.cmb_material.currentIndex() == 0 else "aluminio"
            K = K_CU if material == "cobre" else K_AL
            s = i / K
            sn = seccion_norm(s)
            self.lbl_hint_seccion.setText(f"Sección mínima calculada: {s:.2f} mm² → {sn} mm²")
        except:
            self.lbl_hint_seccion.setText("")

    def calcular(self):
        try:
            corriente = float(self.inp_corriente.text())
        except:
            raise ValueError("Corriente de Diseño es requerida")
        if corriente <= 0:
            raise ValueError("Corriente debe ser positiva")
        if corriente > 1000:
            raise ValueError("Corriente máxima 1000A")

        material = "cobre" if self.cmb_material.currentIndex() == 0 else "aluminio"
        self.resultado_data = formulas.calcular_seccion_conductor(corriente, material)

    def build_resultados(self):
        r = self.resultado_data
        self.add_resultado_item("Sección Recomendada", f"{r['valor']} {r['unidad']}", "cyan")
        self.add_resultado_item("Fórmula", r['formula'], "cyan")
        if r.get('nota'):
            self.add_resultado_item("Detalle", r['nota'], "cyan")
