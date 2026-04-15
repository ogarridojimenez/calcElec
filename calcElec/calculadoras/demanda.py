from PyQt6.QtWidgets import (
    QLineEdit, QComboBox, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QStackedWidget
)
from calculadoras.base import CalculadoraBase
import formulas
import math
from constants import TIPOS_CARGA_DEMANDA

class CalculoDemanda(CalculadoraBase):
    NOMBRE = "Demanda Máxima"
    SUBTITULO = "Cálculo de demanda según NC 800"
    ICONO = "D"

    def build_inputs(self):
        # Toggle buttons
        toggle_row = QHBoxLayout()
        self.btn_detallado = QPushButton("Método Detallado")
        self.btn_detallado.setObjectName("btn_secundario")
        self.btn_detallado.setCheckable(True)
        self.btn_detallado.setChecked(True)
        self.btn_residencial = QPushButton("Residencial Simplificado")
        self.btn_residencial.setObjectName("btn_secundario")
        self.btn_residencial.setCheckable(True)
        self.btn_residencial.setChecked(False)
        
        self.btn_detallado.clicked.connect(lambda: self._toggle_mode(True))
        self.btn_residencial.clicked.connect(lambda: self._toggle_mode(False))
        toggle_row.addWidget(self.btn_detallado)
        toggle_row.addWidget(self.btn_residencial)
        self.layout_inputs.addLayout(toggle_row)
        
        # Actualizar estilos iniciales
        self._update_button_styles()

        # Stacked widget para alternar entre métodos
        self.stack_metodos = QStackedWidget()

        # Página método detallado
        self.page_detallado = QFrame()
        self.page_detallado.setObjectName("tarjeta")
        layout_det = QVBoxLayout(self.page_detallado)
        layout_det.setSpacing(12)
        layout_det.setContentsMargins(16, 16, 16, 16)

        self._cargas_widgets = []
        self._btn_add = QPushButton("+ Agregar carga")
        self._btn_add.setObjectName("btn_agregar")
        self._btn_add.clicked.connect(self._agregar_carga)
        layout_det.addWidget(self._btn_add)

        # Agregar primera fila
        self._agregar_carga()

        # Factor de potencia
        self.inp_fp = QLineEdit("0.9")
        row_fp = QHBoxLayout()
        lbl_fp = QLabel("Factor de potencia")
        lbl_fp.setObjectName("label")
        row_fp.addWidget(lbl_fp)
        row_fp.addWidget(self.inp_fp)
        layout_det.addLayout(row_fp)

        # Sistema
        self.cmb_sistema = QComboBox()
        self.cmb_sistema.addItems(["Monofásico", "Trifásico"])
        row_sist = QHBoxLayout()
        lbl_sist = QLabel("Sistema")
        lbl_sist.setObjectName("label")
        row_sist.addWidget(lbl_sist)
        row_sist.addWidget(self.cmb_sistema)
        layout_det.addLayout(row_sist)

        # Tensión
        self.cmb_tension = QComboBox()
        self.cmb_tension.addItems(["127", "220", "380"])
        row_ten = QHBoxLayout()
        lbl_ten = QLabel("Tensión (V)")
        lbl_ten.setObjectName("label")
        row_ten.addWidget(lbl_ten)
        row_ten.addWidget(self.cmb_tension)
        layout_det.addLayout(row_ten)

        self.stack_metodos.addWidget(self.page_detallado)

        # Página residencial
        self.page_residencial = QFrame()
        self.page_residencial.setObjectName("tarjeta")
        layout_res = QVBoxLayout(self.page_residencial)
        layout_res.setSpacing(12)
        layout_res.setContentsMargins(16, 16, 16, 16)

        lbl_info = QLabel("Demanda = 1500 + 0.4 × (P_total - 1500) para P > 1500W")
        lbl_info.setObjectName("info_box")
        lbl_info.setWordWrap(True)
        layout_res.addWidget(lbl_info)

        self.inp_p_total = QLineEdit()
        self.inp_p_total.setPlaceholderText("Ej: 8000")
        row_p = QHBoxLayout()
        lbl_p = QLabel("Potencia instalada de la vivienda (W)")
        lbl_p.setObjectName("label")
        row_p.addWidget(lbl_p)
        row_p.addWidget(self.inp_p_total)
        layout_res.addLayout(row_p)

        self.stack_metodos.addWidget(self.page_residencial)

        # Agregar stacked widget al layout
        self.layout_inputs.addWidget(self.stack_metodos)
        self.stack_metodos.setCurrentIndex(0)  # Mostrar página detallada por defecto

    def _toggle_mode(self, detallado):
        if detallado:
            self.btn_detallado.setChecked(True)
            self.btn_residencial.setChecked(False)
            self.stack_metodos.setCurrentIndex(0)  # Página detallada
        else:
            self.btn_detallado.setChecked(False)
            self.btn_residencial.setChecked(True)
            self.stack_metodos.setCurrentIndex(1)  # Página residencial
        
        self._update_button_styles()

    def _update_button_styles(self):
        # Theme handles styling via QRadioButton:checked state
        pass

    def _agregar_carga(self):
        row = QHBoxLayout()
        cmb = QComboBox()
        cmb.addItems([f"{t['tipo']} (fd={t['fd']})" for t in TIPOS_CARGA_DEMANDA])
        inp = QLineEdit()
        inp.setPlaceholderText("Potencia (W)")
        btn_del = QPushButton("✕")
        btn_del.setObjectName("btn_eliminar")
        btn_del.setFixedWidth(30)
        btn_del.clicked.connect(lambda checked, r=row, c=cmb, i=inp: self._eliminar_carga(r, c, i))
        row.addWidget(cmb, 1)
        row.addWidget(inp, 1)
        row.addWidget(btn_del)
        self._cargas_widgets.append((cmb, inp, row))
        # Insert before btn_agregar
        layout_det = self.page_detallado.layout()
        layout_det.insertLayout(layout_det.count() - 1, row)

    def _eliminar_carga(self, row_layout, cmb, inp):
        # Hide all widgets in the row
        for i in range(row_layout.count()):
            widget = row_layout.itemAt(i).widget()
            if widget:
                widget.hide()
        
        # Remove from tracking list
        for item in self._cargas_widgets[:]:
            if item[2] == row_layout:  # Match by row layout reference
                self._cargas_widgets.remove(item)
                break

    def calcular(self):
        if self.stack_metodos.currentIndex() == 0:  # Método detallado
            # Método detallado
            cargas = []
            for cmb, inp, row in self._cargas_widgets:
                if not cmb.isVisible():
                    continue
                if inp.text().strip():
                    try:
                        p = float(inp.text())
                    except:
                        continue
                    idx = cmb.currentIndex()
                    tipo = TIPOS_CARGA_DEMANDA[idx]['tipo']
                    cargas.append({"tipo": tipo, "potencia": p})
            if not cargas:
                raise ValueError("Agregue al menos una carga")

            try:
                fp = float(self.inp_fp.text())
            except:
                raise ValueError("Factor de potencia es requerido")
            if fp <= 0 or fp > 1:
                raise ValueError("Factor de potencia debe estar entre 0 y 1")

            sistema = "trifasico" if self.cmb_sistema.currentIndex() == 1 else "monofasico"
            tension = float(self.cmb_tension.currentText())

            self._resultado = formulas.calcular_demanda_detallada(cargas, fp, sistema, tension)
        else:  # Residencial
            try:
                p_total = float(self.inp_p_total.text())
            except:
                raise ValueError("Potencia instalada es requerida")
            if p_total <= 0:
                raise ValueError("Potencia debe ser positiva")
            self._resultado = formulas.calcular_demanda_residencial(p_total)

    def build_resultados(self):
        r = self._resultado
        if self.stack_metodos.currentIndex() == 0:  # Método detallado
            self.add_resultado_item("Demanda Máxima", f"{r['D_kW']:.2f} kW", "cyan")
            self.add_resultado_item("Potencia Aparente", f"{r['S_kVA']:.2f} kVA", "green")
            self.add_resultado_item("Corriente Acometida", f"{r['I']:.2f} A", "amber")
        else:  # Residencial
            self.add_resultado_item("Demanda", f"{r['D_kW']:.2f} kW", "cyan")
