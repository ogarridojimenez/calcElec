from PyQt6.QtWidgets import QLineEdit, QComboBox, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from calculadoras.base import CalculadoraBase
import formulas
import math
from constants import TIPOS_LOCALES_NC803

class CalculoIluminacion(CalculadoraBase):
    NOMBRE = "Iluminación"
    SUBTITULO = "Cálculo de luminarias según NC 803"
    ICONO = "lux"

    def build_inputs(self):
        # SECCIÓN PRINCIPAL
        lbl_sec = QLabel("DATOS DEL LOCAL")
        lbl_sec.setObjectName("label")
        self.layout_inputs.addWidget(lbl_sec)

        # Tipo de local
        self.cmb_tipo = QComboBox()
        self.cmb_tipo.addItems([f"{t['nombre']} ({t['lux_min']}-{t['lux_rec']} lux)" for t in TIPOS_LOCALES_NC803])
        self.cmb_tipo.currentIndexChanged.connect(self._on_tipo_change)
        self.add_field("Tipo de local", self.cmb_tipo, required=True)

        # Iluminancia requerida
        self.inp_lux = QLineEdit()
        self.inp_lux.setPlaceholderText("Se autocompleta según tipo")
        self.add_field("Iluminancia requerida (lux)", self.inp_lux, required=True)

        # Área
        self.inp_area = QLineEdit()
        self.inp_area.setPlaceholderText("Ej: 25")
        self.add_field("Área del local (m²)", self.inp_area, required=True)

        # Factor de utilización
        self.inp_eta = QLineEdit("0.5")
        self.add_field("Factor de utilización η", self.inp_eta, hint="Rango: 0.01 - 1.0", required=True)

        # Factor de mantenimiento
        self.inp_fm = QLineEdit("0.8")
        self.add_field("Factor de mantenimiento fm", self.inp_fm, hint="Rango: 0.01 - 1.0", required=True)

        # Flujo luminaria (opcional)
        self.inp_flujo = QLineEdit()
        self.inp_flujo.setPlaceholderText("Opcional")
        self.add_field("Flujo luminaria (lm)", self.inp_flujo, hint="Opcional", required=False)

        # Potencia luminaria (opcional)
        self.inp_potencia_lum = QLineEdit()
        self.inp_potencia_lum.setPlaceholderText("Opcional")
        self.add_field("Potencia luminaria (W)", self.inp_potencia_lum, hint="Opcional", required=False)

        # SECCIÓN SECUNDARIA
        sep = QFrame()
        sep.setObjectName("separador")
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFixedHeight(1)
        self.layout_inputs.addWidget(sep)

        lbl_sec2 = QLabel("ÍNDICE DEL LOCAL (OPCIONAL)")
        lbl_sec2.setObjectName("label")
        self.layout_inputs.addWidget(lbl_sec2)

        # Largo, Ancho, Altura montaje
        grid = QHBoxLayout()
        self.inp_largo = QLineEdit()
        self.inp_largo.setPlaceholderText("m")
        self.inp_ancho = QLineEdit()
        self.inp_ancho.setPlaceholderText("m")
        self.inp_h = QLineEdit()
        self.inp_h.setPlaceholderText("m")
        for lbl_txt, inp in [("Largo (m)", self.inp_largo), ("Ancho (m)", self.inp_ancho), ("Altura montaje (m)", self.inp_h)]:
            col = QVBoxLayout()
            l = QLabel(lbl_txt)
            l.setObjectName("label")
            col.addWidget(l)
            col.addWidget(inp)
            grid.addLayout(col)
        self.layout_inputs.addLayout(grid)

        self._on_tipo_change()

    def _on_tipo_change(self):
        idx = self.cmb_tipo.currentIndex()
        if idx >= 0 and idx < len(TIPOS_LOCALES_NC803):
            rec = TIPOS_LOCALES_NC803[idx]['lux_rec']
            self.inp_lux.setText(str(rec))

    def calcular(self):
        try:
            E = float(self.inp_lux.text())
        except:
            raise ValueError("Iluminancia requerida es necesaria")
        if E <= 0:
            raise ValueError("Iluminancia debe ser positiva")

        try:
            area = float(self.inp_area.text())
        except:
            raise ValueError("Área del local es requerida")
        if area <= 0:
            raise ValueError("Área debe ser positiva")

        try:
            eta = float(self.inp_eta.text())
        except:
            raise ValueError("Factor de utilización es requerido")
        if eta <= 0 or eta > 1:
            raise ValueError("Factor de utilización debe estar entre 0.01 y 1.0")

        try:
            fm = float(self.inp_fm.text())
        except:
            raise ValueError("Factor de mantenimiento es requerido")
        if fm <= 0 or fm > 1:
            raise ValueError("Factor de mantenimiento debe estar entre 0.01 y 1.0")

        flujo_lum = None
        if self.inp_flujo.text().strip():
            try:
                flujo_lum = float(self.inp_flujo.text())
                if flujo_lum <= 0:
                    raise ValueError("Flujo luminaria debe ser positivo")
            except ValueError as e:
                if "could not convert" in str(e):
                    raise ValueError("Flujo luminaria debe ser un número")
                raise

        potencia_lum = None
        if self.inp_potencia_lum.text().strip():
            try:
                potencia_lum = float(self.inp_potencia_lum.text())
                if potencia_lum <= 0:
                    raise ValueError("Potencia luminaria debe ser positiva")
            except ValueError as e:
                if "could not convert" in str(e):
                    raise ValueError("Potencia luminaria debe ser un número")
                raise

        largo, ancho, h = None, None, None
        if self.inp_largo.text().strip() and self.inp_ancho.text().strip() and self.inp_h.text().strip():
            try:
                largo = float(self.inp_largo.text())
                ancho = float(self.inp_ancho.text())
                h = float(self.inp_h.text())
                if largo <= 0 or ancho <= 0 or h <= 0:
                    raise ValueError("Dimensiones deben ser positivas")
            except ValueError as e:
                if "could not convert" in str(e):
                    raise ValueError("Dimensiones deben ser números")
                raise

        res = formulas.calcular_iluminacion(E, area, eta, fm, flujo_lum, largo, ancho, h)
        if flujo_lum and potencia_lum and 'N_ceil' in res:
            res['P_total'] = res['N_ceil'] * potencia_lum
        self._resultado = res

    def build_resultados(self):
        r = self._resultado

        self.add_resultado_item("Flujo Luminoso Total", f"{r['flujo_total']:.0f} lm", "cyan")

        if 'N_ceil' in r:
            self.add_resultado_item("Número de Luminarias", f"{r['N_ceil']} uds", "green")

        if 'k' in r:
            self.add_resultado_item("Índice del Local k", f"{r['k']:.2f}", "cyan")

        if 'P_total' in r:
            self.add_resultado_item("Potencia Instalada", f"{r['P_total']:.0f} W", "amber")
