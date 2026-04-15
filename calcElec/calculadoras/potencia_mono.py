from PyQt6.QtWidgets import QLineEdit, QButtonGroup, QRadioButton, QHBoxLayout, QVBoxLayout, QLabel
from calculadoras.base import CalculadoraBase
import formulas

class CalculoPotenciaMonofasica(CalculadoraBase):
    NOMBRE = "Potencia Monofásica"
    SUBTITULO = "P = V × I × cos(φ) · Norma NC 800"
    ICONO = "⚡"

    def build_inputs(self):
        info = QLabel("Sistema monofásico: Común en instalaciones residenciales y comerciales pequeñas.")
        info.setObjectName("info_box")
        info.setWordWrap(True)
        self.layout_inputs.addWidget(info)

        lbl = QLabel("¿Qué valor desea calcular?")
        lbl.setObjectName("label")
        self.layout_inputs.addWidget(lbl)
        radio_row = QHBoxLayout()
        self.radio_group = QButtonGroup()
        self.radios = {}
        for i, (key, text) in enumerate([("potencia","Potencia (W)"),("voltaje","Voltaje (V)"),("corriente","Corriente (A)")]):
            rb = QRadioButton(text)
            self.radio_group.addButton(rb, i)
            self.radios[key] = rb
            radio_row.addWidget(rb)
        self.radios["potencia"].setChecked(True)
        self.radio_group.buttonClicked.connect(self._update_fields)
        self.layout_inputs.addLayout(radio_row)

        grid = QHBoxLayout()
        self.inp_v = QLineEdit()
        self.inp_v.setPlaceholderText("Ej: 220")
        self.inp_i = QLineEdit()
        self.inp_i.setPlaceholderText("Ej: 10")
        self.inp_p = QLineEdit()
        self.inp_p.setPlaceholderText("Ej: 1000")
        self.inp_fp = QLineEdit("0.9")
        self.inp_fp.setPlaceholderText("0-1")
        for lbl_txt, inp in [("Voltaje (V)",self.inp_v),("Corriente (A)",self.inp_i),("Potencia (W)",self.inp_p)]:
            col = QVBoxLayout()
            l = QLabel(lbl_txt)
            l.setObjectName("label")
            col.addWidget(l)
            col.addWidget(inp)
            grid.addLayout(col)
        fp_col = QVBoxLayout()
        fp_col.addWidget(QLabel("Factor de Potencia cosφ"))
        fp_col.addWidget(self.inp_fp)
        grid.addLayout(fp_col)
        self.layout_inputs.addLayout(grid)
        self._update_fields()

    def _update_fields(self):
        checked = [k for k,rb in self.radios.items() if rb.isChecked()][0]
        for k, inp in [("voltaje",self.inp_v),("corriente",self.inp_i),("potencia",self.inp_p)]:
            inp.setDisabled(k == checked)
            inp.setPlaceholderText("Resultado" if k == checked else "")
            if k == checked:
                inp.clear()

    def calcular(self):
        checked = [k for k,rb in self.radios.items() if rb.isChecked()][0]
        vals = {}
        for k, inp, nombre in [("voltaje",self.inp_v,"Voltaje"),("corriente",self.inp_i,"Corriente"),("potencia",self.inp_p,"Potencia")]:
            if k != checked:
                try:
                    vals[k] = float(inp.text())
                except:
                    raise ValueError(f"{nombre} es requerido")
                if vals[k] <= 0:
                    raise ValueError(f"{nombre} debe ser positivo")
                if k == "voltaje" and vals[k] > 1000:
                    raise ValueError("Voltaje máximo 1000V")
        try:
            fp = float(self.inp_fp.text())
        except:
            raise ValueError("Factor de Potencia requerido")
        if fp <= 0 or fp > 1:
            raise ValueError("Factor de Potencia debe estar entre 0 y 1")
        vals["fp"] = fp
        self.resultado_data = formulas.calcular_potencia_monofasica(checked, vals)

    def build_resultados(self):
        r = self.resultado_data
        labels = {"potencia":"Potencia (W)","voltaje":"Voltaje (V)","corriente":"Corriente (A)"}
        checked = [k for k,rb in self.radios.items() if rb.isChecked()][0]
        self.add_resultado_item(labels[checked], f"{r['valor']:.4f} {r['unidad']}", "green")
        self.add_resultado_item("Fórmula", r['formula'], "green")
        if r.get('nota'):
            self.add_resultado_item("Detalle", r['nota'], "green")
