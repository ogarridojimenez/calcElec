from PyQt6.QtWidgets import QLineEdit, QComboBox, QVBoxLayout, QHBoxLayout, QLabel
from calculadoras.base import CalculadoraBase
import formulas
from constants import FG_D

class CalculoAmpacidadD(CalculadoraBase):
    NOMBRE = "Ampacidad - Método D"
    SUBTITULO = "Cables directamente enterrados o en ductos subterráneos"
    ICONO = "I↓"

    def build_inputs(self):
        info = QLabel("Método D: Cables enterrados directamente o en ductos subterráneos. Iz = Ia × Ft × Fr × Fg")
        info.setObjectName("info_box")
        info.setWordWrap(True)
        self.layout_inputs.addWidget(info)

        # Sección
        self.cmb_seccion = QComboBox()
        secciones = [1.5,2.5,4,6,10,16,25,35,50,70,95,120,150,185,240,300]
        self.cmb_seccion.addItems([str(s) for s in secciones])
        self.add_field("Sección (mm²)", self.cmb_seccion, required=True)

        # Material
        self.cmb_material = QComboBox()
        self.cmb_material.addItems(["Cobre", "Aluminio"])
        self.cmb_material.currentIndexChanged.connect(self._update_secciones)
        self.add_field("Material", self.cmb_material, required=True)

        # Aislamiento
        self.cmb_aislamiento = QComboBox()
        self.cmb_aislamiento.addItems([
            "Dos_PVC",
            "Tres_PVC",
            "Dos_XLPE",
            "Tres_XLPE",
        ])
        self.add_field("Aislamiento", self.cmb_aislamiento, required=True)

        # Temperatura del terreno
        self.inp_temp = QLineEdit("20")
        self.add_field("Temperatura del terreno (°C)", self.inp_temp, hint="Default: 20°C (norma cubana para suelo)", required=True)

        # Resistividad térmica del suelo
        self.cmb_resistividad = QComboBox()
        self.cmb_resistividad.addItems([
            "0.5 — Suelo muy húmedo (turba, marisma)",
            "0.7 — Suelo húmedo (arcilla compacta)",
            "1.0 — Suelo normal húmedo",
            "1.5 — Suelo seco (arena suelta)",
            "2.0 — Suelo muy seco",
            "2.5 — Referencia NC IEC (default)",
            "3.0 — Suelo extremadamente seco (roca)",
        ])
        self.cmb_resistividad.setCurrentIndex(5)
        self.add_field("Resistividad térmica del suelo (K·m/W)", self.cmb_resistividad, required=True)

        # Nº circuitos enterrados
        self.inp_circuitos = QLineEdit("1")
        self.add_field("Nº circuitos enterrados en paralelo", self.inp_circuitos, hint="Máximo: 6 circuitos. Separación mínima: 0.7m entre circuitos", required=True)

    def _update_secciones(self):
        material = self.cmb_material.currentText()
        self.cmb_seccion.clear()
        if material == "Cobre":
            secciones = [1.5,2.5,4,6,10,16,25,35,50,70,95,120,150,185,240,300]
        else:
            secciones = [2.5,4,6,10,16,25,35,50,70,95,120,150,185,240,300]
        self.cmb_seccion.addItems([str(s) for s in secciones])

    def calcular(self):
        seccion = float(self.cmb_seccion.currentText())
        material = self.cmb_material.currentText()
        aislamiento = self.cmb_aislamiento.currentText()

        try:
            temp = float(self.inp_temp.text())
        except:
            raise ValueError("Temperatura del terreno es requerida")
        if temp < 10 or temp > 50:
            raise ValueError("Temperatura debe estar entre 10 y 50°C")

        resistividad = float(self.cmb_resistividad.currentText().split(" ")[0])

        try:
            n_circ = int(self.inp_circuitos.text())
        except:
            raise ValueError("Nº circuitos es requerido")
        if n_circ < 1 or n_circ > 6:
            raise ValueError("Nº circuitos debe estar entre 1 y 6")

        self._resultado = formulas.calcular_ampacidad_d(seccion, material, aislamiento, temp, resistividad, n_circ)

    def build_resultados(self):
        r = self._resultado

        row1 = QHBoxLayout()
        lbl1 = QLabel("Iz Corregida")
        lbl1.setObjectName("resultado_label")
        lbl1.setFixedWidth(230)
        row1.addWidget(lbl1)
        val1 = QLabel(f"{r['Iz']} A")
        val1.setObjectName("resultado_valor")
        row1.addWidget(val1)
        row1.addStretch()
        self.layout_resultado.addLayout(row1)

        self.add_resultado_item("Fórmula", r['formula'], "cyan")
        self.add_resultado_item("Ia base", f"{r['Ia']} A", "green")
        self.add_resultado_item("Ft temperatura suelo", f"{r['Ft']}", "green")
        self.add_resultado_item("Fr resistividad", f"{r['Fr']}", "green")
        self.add_resultado_item("Fg agrupamiento", f"{r['Fg']}", "green")
