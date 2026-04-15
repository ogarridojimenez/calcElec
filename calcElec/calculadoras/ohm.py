from PyQt6.QtWidgets import QLineEdit, QButtonGroup, QRadioButton, QHBoxLayout, QVBoxLayout, QLabel
from calculadoras.base import CalculadoraBase
import formulas

class CalculoOhm(CalculadoraBase):
    NOMBRE = "Ley de Ohm"
    SUBTITULO = "Cálculo de V, I y R"
    ICONO = "🔢"

    def build_inputs(self):
        # Info box
        info = QLabel("Ley de Ohm: V = I × R. Seleccione qué valor desea calcular y proporcione los otros dos.")
        info.setObjectName("info_box")
        info.setWordWrap(True)
        self.layout_inputs.addWidget(info)
        # Radio buttons
        lbl = QLabel("¿Qué valor desea calcular?")
        lbl.setObjectName("label")
        self.layout_inputs.addWidget(lbl)
        radio_row = QHBoxLayout()
        self.radio_group = QButtonGroup()
        self.radios = {}
        for i, (key, txt) in enumerate([("v","Voltaje (V)"), ("i","Corriente (A)"), ("r","Resistencia (Ω)")]):
            rb = QRadioButton(txt)
            self.radio_group.addButton(rb, i)
            self.radios[key] = rb
            radio_row.addWidget(rb)
        self.radios["v"].setChecked(True)
        self.radio_group.buttonClicked.connect(self._update_fields)
        self.layout_inputs.addLayout(radio_row)
        # Inputs grid
        grid = QHBoxLayout()
        self.inp_v = QLineEdit(); self.inp_v.setPlaceholderText("V (Voltios)")
        self.inp_i = QLineEdit(); self.inp_i.setPlaceholderText("I (Amperios)")
        self.inp_r = QLineEdit(); self.inp_r.setPlaceholderText("R (Ohmios)")
        for lbl_txt, inp in [("Voltaje (V)", self.inp_v), ("Corriente (A)", self.inp_i), ("Resistencia (Ω)", self.inp_r)]:
            col = QVBoxLayout()
            l = QLabel(lbl_txt); l.setObjectName("label"); col.addWidget(l)
            col.addWidget(inp)
            grid.addLayout(col)
        self.layout_inputs.addLayout(grid)
        self._update_fields()

    def _update_fields(self):
        checked = [k for k, rb in self.radios.items() if rb.isChecked()][0]
        for k, inp in [("v", self.inp_v), ("i", self.inp_i), ("r", self.inp_r)]:
            inp.setDisabled(k == checked)
            inp.setPlaceholderText("Resultado" if k == checked else "0.0")
            if k == checked:
                inp.clear()

    def calcular(self):
        checked = [k for k, rb in self.radios.items() if rb.isChecked()][0]
        vals = {}
        for k, inp in [("v", self.inp_v), ("i", self.inp_i), ("r", self.inp_r)]:
            if k != checked:
                try:
                    vals[k] = float(inp.text())
                except:
                    raise ValueError(f"El campo {'Voltaje' if k=='v' else 'Corriente' if k=='i' else 'Resistencia'} es requerido")
                if vals[k] <= 0:
                    raise ValueError("El valor debe ser positivo y no cero")
        self.resultado_data = formulas.calcular_ohm(checked, vals)

    def build_resultados(self):
        r = self.resultado_data
        self.add_resultado_item("Resultado", f"{r['valor']:.4f} {r['unidad']}", "cyan")
        self.add_resultado_item("Fórmula", r['formula'], "cyan")
