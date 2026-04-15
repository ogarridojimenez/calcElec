from PyQt6.QtWidgets import QLineEdit, QComboBox, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from calculadoras.base import CalculadoraBase
import formulas

class CalculoCaidaTension(CalculadoraBase):
    NOMBRE = "Caída de Tensión"
    SUBTITULO = "Cálculo de ΔV% en conductores · Norma NC 800"
    ICONO = "ΔV"

    def build_inputs(self):
        info = QLabel("Límites de caída de tensión: ≤3% Iluminación, ≤5% Fuerza, ≤5% Motores")
        info.setObjectName("info_box_amber")
        info.setWordWrap(True)
        self.layout_inputs.addWidget(info)

        # Voltaje
        self.inp_v = QLineEdit("220")
        self.add_field("Voltaje (V)", self.inp_v, hint="Máx 1000V", required=True)

        # Corriente
        self.inp_i = QLineEdit()
        self.inp_i.setPlaceholderText("Ej: 15")
        self.add_field("Corriente (A)", self.inp_i, required=True)

        # Longitud
        self.inp_l = QLineEdit()
        self.inp_l.setPlaceholderText("Ej: 50")
        self.add_field("Longitud del conductor (m)", self.inp_l, hint="Máx 500m", required=True)

        # Sección del conductor
        self.cmb_seccion = QComboBox()
        secciones = [1.5,2.5,4,6,10,16,25,35,50,70,95,120,150,185,240]
        self.cmb_seccion.addItems([str(s) for s in secciones])
        self.add_field("Sección del conductor (mm²)", self.cmb_seccion, required=True)

        # Material
        self.cmb_material = QComboBox()
        self.cmb_material.addItems(["Cobre (ρ=0.0178 Ω·mm²/m)", "Aluminio (ρ=0.0282 Ω·mm²/m)"])
        self.add_field("Material del conductor", self.cmb_material, required=True)

        # Factor de potencia
        self.inp_fp = QLineEdit("1")
        self.add_field("Factor de potencia cosφ", self.inp_fp, required=True)

        # Factor de corrección FC
        self.inp_fc = QLineEdit("1")
        self.add_field("Factor correc. FC", self.inp_fc, hint="FC=1 para 3% (ilum), FC=1.67 para 5% (fuerza)", required=True)

    def calcular(self):
        try:
            voltaje = float(self.inp_v.text())
        except:
            raise ValueError("Voltaje es requerido")
        if voltaje <= 0 or voltaje > 1000:
            raise ValueError("Voltaje debe estar entre 0 y 1000V")

        try:
            corriente = float(self.inp_i.text())
        except:
            raise ValueError("Corriente es requerida")
        if corriente <= 0:
            raise ValueError("Corriente debe ser positiva")

        try:
            longitud = float(self.inp_l.text())
        except:
            raise ValueError("Longitud es requerida")
        if longitud <= 0 or longitud > 500:
            raise ValueError("Longitud debe estar entre 0 y 500m")

        seccion = float(self.cmb_seccion.currentText())
        material = "cobre" if self.cmb_material.currentIndex() == 0 else "aluminio"

        try:
            cosfi = float(self.inp_fp.text())
        except:
            raise ValueError("Factor de potencia es requerido")
        if cosfi <= 0 or cosfi > 1:
            raise ValueError("Factor de potencia debe estar entre 0 y 1")

        try:
            fc = float(self.inp_fc.text())
        except:
            raise ValueError("Factor de corrección es requerido")
        if fc <= 0:
            raise ValueError("Factor de corrección debe ser positivo")

        resultado = formulas.calcular_caida_tension(voltaje, corriente, longitud, seccion, material, cosfi, fc)
        resultado['voltaje'] = voltaje
        resultado['corriente'] = corriente
        self._resultado = resultado

    def build_resultados(self):
        r = self._resultado
        dv_pct = r['valor']

        # Determinar estado
        if dv_pct <= 3:
            color = "green"
            estado = "✓ Cumple (Iluminación)"
            frame_style = "resultado_frame"
        elif dv_pct <= 5:
            color = "amber"
            estado = "⚠ Cumple (Fuerza)"
            frame_style = "resultado_frame_warning"
        else:
            color = "red"
            estado = "✗ No cumple"
            frame_style = "resultado_frame_error"

        # Cambiar estilo del frame
        self.frame_resultado.setObjectName(frame_style)
        self.frame_resultado.style().unpolish(self.frame_resultado)
        self.frame_resultado.style().polish(self.frame_resultado)

        obj_name = {"green":"resultado_valor","amber":"resultado_valor_amber","red":"resultado_valor_red"}.get(color, "resultado_valor")
        row1 = QHBoxLayout()
        lbl1 = QLabel("% Caída de Tensión")
        lbl1.setObjectName("resultado_label")
        lbl1.setFixedWidth(230)
        row1.addWidget(lbl1)
        val1 = QLabel(f"{dv_pct:.2f}%")
        val1.setObjectName(obj_name)
        row1.addWidget(val1)
        row1.addStretch()
        self.layout_resultado.addLayout(row1)

        row2 = QHBoxLayout()
        lbl2 = QLabel("Voltios caída")
        lbl2.setObjectName("resultado_label")
        lbl2.setFixedWidth(230)
        row2.addWidget(lbl2)
        # Extraer voltios de la nota
        nota = r.get('nota', '')
        val2 = QLabel(nota.split('\n')[0].replace('ΔV = ',''))
        val2.setObjectName("resultado_label")
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
