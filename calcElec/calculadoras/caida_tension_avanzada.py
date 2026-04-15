from PyQt6.QtWidgets import QLineEdit, QComboBox, QRadioButton, QButtonGroup, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from calculadoras.base import CalculadoraBase
import formulas
import math

class CalculoCaidaTensionAvanzada(CalculadoraBase):
    NOMBRE = "Caída de Tensión Avanzada"
    SUBTITULO = "Con resistencia y reactancia del conductor"
    ICONO = "ΔVz"

    def build_inputs(self):
        info = QLabel("Cálculo avanzado: Considera resistencia R y reactancia X del conductor. Más preciso para secciones ≥ 35mm².")
        info.setObjectName("info_box")
        info.setWordWrap(True)
        self.layout_inputs.addWidget(info)

        # Sección
        self.cmb_seccion = QComboBox()
        secciones = [1.5,2.5,4,6,10,16,25,35,50,70,95,120,150,185,240]
        self.cmb_seccion.addItems([str(s) for s in secciones])
        self.add_field("Sección (mm²)", self.cmb_seccion, required=True)

        # Longitud
        self.inp_l = QLineEdit("100")
        self.add_field("Longitud (m)", self.inp_l, required=True)

        # Corriente
        self.inp_i = QLineEdit("30")
        self.add_field("Corriente (A)", self.inp_i, required=True)

        # Tensión nominal
        self.cmb_tension = QComboBox()
        self.cmb_tension.addItems(["127", "220", "380", "440"])
        self.cmb_tension.setCurrentText("380")
        self.add_field("Tensión nominal (V)", self.cmb_tension, required=True)

        # Factor de potencia
        self.inp_fp = QLineEdit("0.85")
        self.add_field("Factor de potencia cosφ", self.inp_fp, hint="0.5 - 1.0", required=True)

        # Sistema
        lbl_sist = QLabel("Sistema")
        lbl_sist.setObjectName("label")
        self.layout_inputs.addWidget(lbl_sist)
        radio_row = QHBoxLayout()
        self.radio_group = QButtonGroup()
        self.rb_mono = QRadioButton("Monofásico")
        self.rb_tri = QRadioButton("Trifásico")
        self.rb_tri.setChecked(True)
        for rb in [self.rb_mono, self.rb_tri]:
            self.radio_group.addButton(rb)
            radio_row.addWidget(rb)
        self.layout_inputs.addLayout(radio_row)

    def calcular(self):
        seccion = float(self.cmb_seccion.currentText())

        try:
            longitud = float(self.inp_l.text())
        except:
            raise ValueError("Longitud es requerida")
        if longitud <= 0:
            raise ValueError("Longitud debe ser positiva")

        try:
            corriente = float(self.inp_i.text())
        except:
            raise ValueError("Corriente es requerida")
        if corriente <= 0:
            raise ValueError("Corriente debe ser positiva")

        voltaje = float(self.cmb_tension.currentText())

        try:
            cosfi = float(self.inp_fp.text())
        except:
            raise ValueError("Factor de potencia es requerido")
        if cosfi < 0.5 or cosfi > 1:
            raise ValueError("Factor de potencia debe estar entre 0.5 y 1.0")

        sistema = "monofasico" if self.rb_mono.isChecked() else "trifasico"

        self._resultado = formulas.calcular_caida_tension_rx(seccion, longitud, corriente, voltaje, cosfi, sistema)

    def build_resultados(self):
        r = self._resultado
        dv_pct = r['valor']

        if dv_pct <= 3:
            color = "green"
            estado = "✓ Cumple iluminación y fuerza"
            frame_style = "resultado_frame"
        elif dv_pct <= 5:
            color = "amber"
            estado = "⚠ Solo fuerza motriz"
            frame_style = "resultado_frame_warning"
        else:
            color = "red"
            estado = "✗ No cumple NC 800"
            frame_style = "resultado_frame_error"

        self.frame_resultado.setObjectName(frame_style)
        self.frame_resultado.style().unpolish(self.frame_resultado)
        self.frame_resultado.style().polish(self.frame_resultado)

        obj_name = {"green":"resultado_valor","amber":"resultado_valor_amber","red":"resultado_valor_red"}.get(color, "resultado_valor")

        row1 = QHBoxLayout()
        lbl1 = QLabel("% Caída de Tensión")
        lbl1.setObjectName("resultado_label")
        lbl1.setFixedWidth(230)
        row1.addWidget(lbl1)
        val1 = QLabel(f"{dv_pct:.3f}%")
        val1.setObjectName(obj_name)
        row1.addWidget(val1)
        row1.addStretch()
        self.layout_resultado.addLayout(row1)

        row2 = QHBoxLayout()
        lbl2 = QLabel("Detalle")
        lbl2.setObjectName("resultado_label")
        lbl2.setFixedWidth(230)
        row2.addWidget(lbl2)
        val2 = QLabel(r.get('nota', ''))
        val2.setObjectName("resultado_label")
        val2.setWordWrap(True)
        row2.addWidget(val2)
        row2.addStretch()
        self.layout_resultado.addLayout(row2)

        row3 = QHBoxLayout()
        lbl3 = QLabel("Estado")
        lbl3.setObjectName("resultado_label")
        lbl3.setFixedWidth(230)
        row3.addWidget(lbl3)
        obj_estado = "cumple" if dv_pct <= 5 else "no_cumple"
        val3 = QLabel(estado)
        val3.setObjectName(obj_estado)
        row3.addWidget(val3)
        row3.addStretch()
        self.layout_resultado.addLayout(row3)

        # Leyenda
        leyenda = QLabel("Verde: 0-3%  |  Ámbar: 3-5%  |  Rojo: >5%")
        leyenda.setObjectName("hint_text")
        self.layout_resultado.addWidget(leyenda)
