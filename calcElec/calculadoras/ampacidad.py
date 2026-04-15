from PyQt6.QtWidgets import QLineEdit, QComboBox, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from calculadoras.base import CalculadoraBase
import formulas
from constants import FG

class CalculoAmpacidad(CalculadoraBase):
    NOMBRE = "Ampacidad Corregida"
    SUBTITULO = "NC IEC 60364-5-52 (Métodos A-F)"
    ICONO = "Iz"

    def build_inputs(self):
        info = QLabel("Iz = Ia × Ft × Fg — Ampacidad corregida por temperatura y agrupamiento")
        info.setObjectName("info_box")
        info.setWordWrap(True)
        self.layout_inputs.addWidget(info)

        # Sección
        self.cmb_seccion = QComboBox()
        secciones = [1.5,2.5,4,6,10,16,25,35,50,70,95,120,150,185,240]
        self.cmb_seccion.addItems([str(s) for s in secciones])
        self.add_field("Sección (mm²)", self.cmb_seccion, required=True)

        # Material
        self.cmb_material = QComboBox()
        self.cmb_material.addItems(["Cobre", "Aluminio"])
        self.add_field("Material", self.cmb_material, required=True)

        # Método de instalación
        self.cmb_metodo = QComboBox()
        self.cmb_metodo.addItems([
            "A1: Unipolar en tubo empotrado en pared",
            "A2: Multiconductor en tubo empotrado en pared",
            "B1: Unipolar en tubo en superficie o bandeja",
            "B2: Multiconductor en tubo en superficie",
            "C: Cable sobre pared o bandeja",
            "E: Cable al aire libre horizontal",
            "F: Cable al aire libre vertical",
        ])
        self.add_field("Método de instalación", self.cmb_metodo, required=True)

        # Tipo de aislamiento
        self.cmb_aislamiento = QComboBox()
        self.cmb_aislamiento.addItems([
            "2 conductores PVC (monofásico)",
            "3 conductores PVC (trifásico)",
            "2 conductores XLPE (monofásico)",
            "3 conductores XLPE (trifásico)",
        ])
        self.cmb_aislamiento.setCurrentIndex(1)
        self.add_field("Tipo de aislamiento", self.cmb_aislamiento, required=True)

        # Temperatura ambiente
        self.inp_temp = QLineEdit("35")
        self.add_field("Temperatura ambiente (°C)", self.inp_temp, hint="Rango: 10-60", required=True)

        # Nº circuitos agrupados
        self.inp_circuitos = QLineEdit("1")
        self.lbl_max_circ = QLabel("")
        self.lbl_max_circ.setObjectName("hint_text")
        col_circ = QVBoxLayout()
        lbl_circ = QLabel("Nº circuitos agrupados")
        lbl_circ.setObjectName("label")
        col_circ.addWidget(lbl_circ)
        col_circ.addWidget(self.inp_circuitos)
        col_circ.addWidget(self.lbl_max_circ)
        self.layout_inputs.addLayout(col_circ)

        # Disposición de cables
        self.cmb_disposicion = QComboBox()
        self.cmb_disposicion.addItems([
            "Empotrados o encerrados",
            "Una capa sobre paredes, pisos o bandejas no perforadas",
            "Una capa fijada directamente debajo del techo",
            "Una capa sobre bandejas horizontales perforadas o bandejas verticales",
            "Una capa sobre soporte de cables tipo escalera o abrazaderas",
        ])
        self.cmb_disposicion.currentTextChanged.connect(self._actualizar_max_circuitos)
        self.add_field("Disposición de cables", self.cmb_disposicion, required=True)
        
        # Actualizar hint inicial
        self._actualizar_max_circuitos()

        # Separador
        sep = QFrame()
        sep.setObjectName("separador")
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFixedHeight(1)
        self.layout_inputs.addWidget(sep)

        # Corriente de diseño (opcional)
        self.inp_id = QLineEdit()
        self.inp_id.setPlaceholderText("Opcional - para verificar cumplimiento")
        self.add_field("Corriente de diseño Id (A)", self.inp_id, hint="Opcional", required=False)

    def calcular(self):
        seccion = float(self.cmb_seccion.currentText())
        material = self.cmb_material.currentText()

        metodo_key = self.cmb_metodo.currentText().split(":")[0].strip()

        idx_aisl = self.cmb_aislamiento.currentIndex()
        aisl_map = {0: "Dos_PVC", 1: "Tres_PVC", 2: "Dos_XLPE", 3: "Tres_XLPE"}
        aislamiento = aisl_map[idx_aisl]

        try:
            temp = float(self.inp_temp.text())
        except:
            raise ValueError("Temperatura ambiente es requerida")
        if temp < 10 or temp > 60:
            raise ValueError("Temperatura debe estar entre 10 y 60°C")

        try:
            n_circ = int(self.inp_circuitos.text())
        except:
            raise ValueError("Nº circuitos es requerido")
        if n_circ < 1:
            raise ValueError("Nº circuitos debe ser al menos 1")

        disposicion = self.cmb_disposicion.currentText()

        id_val = None
        if self.inp_id.text().strip():
            try:
                id_val = float(self.inp_id.text())
            except:
                raise ValueError("Corriente de diseño debe ser un número")

        self._resultado = formulas.calcular_ampacidad(seccion, material, metodo_key, aislamiento, temp, n_circ, disposicion)
        self._resultado['Id'] = id_val

    def _actualizar_max_circuitos(self):
        disposicion = self.cmb_disposicion.currentText()
        # According to NC 800, different dispositions have different max circuit limits
        max_circ = {
            "Empotrados o encerrados": 20,
            "Una capa sobre paredes, pisos o bandejas no perforadas": 9,
            "Una capa fijada directamente debajo del techo": 9,
            "Una capa sobre bandejas horizontales perforadas o bandejas verticales": 9,
            "Una capa sobre soporte de cables tipo escalera o abrazaderas": 9,
        }.get(disposicion, 9)
        
        self.lbl_max_circ.setText(f"Máximo: {max_circ} circuitos")

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
        self.add_resultado_item("Ft temperatura", f"{r['Ft']}", "green")
        self.add_resultado_item("Fg agrupamiento", f"{r['Fg']}", "green")

        # Verificación con Id
        id_val = r.get('Id')
        if id_val is not None:
            iz_val = r['Iz']
            if id_val <= iz_val * 0.8:
                estado = "✓ Cumple (Id ≤ 80% Iz)"
                color = "cumple"
            elif id_val <= iz_val:
                estado = "⚠ Límite (80% < Id ≤ Iz)"
                color = "resultado_valor_amber"
            else:
                estado = "✗ No cumple (Id > Iz)"
                color = "no_cumple"

            row_id = QHBoxLayout()
            lbl_id = QLabel("Verificación")
            lbl_id.setObjectName("resultado_label")
            lbl_id.setFixedWidth(230)
            row_id.addWidget(lbl_id)
            val_id = QLabel(estado)
            val_id.setObjectName(color)
            row_id.addWidget(val_id)
            row_id.addStretch()
            self.layout_resultado.addLayout(row_id)
