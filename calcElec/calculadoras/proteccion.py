from PyQt6.QtWidgets import QLineEdit, QComboBox, QVBoxLayout, QLabel
from calculadoras.base import CalculadoraBase
import formulas

class CalculoProteccion(CalculadoraBase):
    NOMBRE = "Protección Magnetotérmica"
    SUBTITULO = "Cálculo de interruptor automático · Norma NC 801"
    ICONO = "In"

    def build_inputs(self):
        info = QLabel("×1.15 → Circuitos generales\n×1.25 → Motores\n×1.50 → Transformadores\n\nCurva B: protección resistiva · Curva C: protección inductiva")
        info.setObjectName("info_box")
        info.setWordWrap(True)
        self.layout_inputs.addWidget(info)

        # Corriente de carga
        self.inp_corriente = QLineEdit()
        self.inp_corriente.setPlaceholderText("Ej: 25")
        self.inp_corriente.textChanged.connect(self._update_hint)
        self.add_field("Corriente de Carga (A)", self.inp_corriente, hint="Máx 630A", required=True)

        # Hint dinámico
        self.lbl_hint_ajustada = QLabel("")
        self.lbl_hint_ajustada.setObjectName("hint_text")
        self.layout_inputs.addWidget(self.lbl_hint_ajustada)

        # Tipo de carga
        self.cmb_tipo = QComboBox()
        self.cmb_tipo.addItems([
            "Circuitos Generales (×1.25) - NC 801",
            "Motores Eléctricos (×1.25) - NC 804",
            "Transformadores (×1.50) - NC 801",
        ])
        self.cmb_tipo.currentIndexChanged.connect(self._update_hint)
        self.add_field("Tipo de Carga", self.cmb_tipo, required=True)

    def _update_hint(self):
        try:
            i = float(self.inp_corriente.text())
            mult = [1.15, 1.25, 1.50][self.cmb_tipo.currentIndex()]
            self.lbl_hint_ajustada.setText(f"Corriente ajustada: {i * mult:.2f} A")
        except:
            self.lbl_hint_ajustada.setText("")

    def calcular(self):
        try:
            corriente = float(self.inp_corriente.text())
        except:
            raise ValueError("Corriente de Carga es requerida")
        if corriente <= 0:
            raise ValueError("Corriente debe ser positiva")
        if corriente > 630:
            raise ValueError("Corriente máxima 630A")

        idx = self.cmb_tipo.currentIndex()
        tipo_map = {0: "general", 1: "motores", 2: "transformador"}
        tipo_carga = tipo_map[idx]

        self.resultado_data = formulas.calcular_proteccion(corriente, tipo_carga)

    def build_resultados(self):
        r = self.resultado_data
        self.add_resultado_item("Interruptor Magnetotérmico", f"{r['valor']} {r['unidad']}", "cyan")
        self.add_resultado_item("Fórmula", r['formula'], "cyan")
        if r.get('nota'):
            self.add_resultado_item("Detalle", r['nota'], "cyan")
