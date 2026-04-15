from PyQt6.QtWidgets import (
    QLineEdit, QComboBox, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QTableWidget, QTableWidgetItem, QHeaderView,
    QWidget
)
from PyQt6.QtCore import Qt
from calculadoras.base import CalculadoraBase
import formulas
from constants import AREAS_CONDUCTORES_MM2, TABLA_TUBERIAS

class CalculoConduit(CalculadoraBase):
    NOMBRE = "Selección de Conduit"
    SUBTITULO = "NEC Art. 358 - Factor llenado: 1 cond=53%, 2=31%, 3+=40%"
    ICONO = "Ø"

    def build_inputs(self):
        info = QLabel("Calcula el conduit mínimo necesario según área total de conductores y factores de llenado normativos.")
        info.setObjectName("info_box")
        info.setWordWrap(True)
        self.layout_inputs.addWidget(info)

        # Tabla de conductores
        self._conductores = []
        self._tbl_frame = QFrame()
        self._tbl_frame.setObjectName("tarjeta")
        tbl_layout = QVBoxLayout(self._tbl_frame)
        tbl_layout.setSpacing(8)
        tbl_layout.setContentsMargins(12, 12, 12, 12)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Sección mm²", "Cantidad", "Área mm²", ""])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(3, 40)
        tbl_layout.addWidget(self.table)

        btn_add = QPushButton("[ + agregar conductor ]")
        btn_add.setObjectName("btn_agregar")
        btn_add.setFixedHeight(32)
        btn_add.clicked.connect(self._agregar_fila)
        tbl_layout.addWidget(btn_add)

        self.layout_inputs.addWidget(self._tbl_frame)
        self._agregar_fila()

    def _agregar_fila(self):
        row = self.table.rowCount()
        self.table.insertRow(row)

        # ComboBox for section
        cmb = QComboBox()
        secciones = sorted(AREAS_CONDUCTORES_MM2.keys())
        cmb.addItems([str(s) for s in secciones])
        cmb.currentIndexChanged.connect(lambda: self._update_area(row))
        self.table.setCellWidget(row, 0, cmb)

        # Input for quantity
        inp = QLineEdit("1")
        inp.textChanged.connect(lambda: self._update_area(row))
        self.table.setCellWidget(row, 1, inp)

        # Label for calculated area
        lbl_area = QLabel("-")
        lbl_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_area.setObjectName("resultado_label")
        self.table.setCellWidget(row, 2, lbl_area)

        btn_del = QPushButton("✕")
        btn_del.setObjectName("btn_eliminar")
        btn_del.setFixedWidth(35)
        btn_del.setFixedHeight(28)
        btn_del.clicked.connect(lambda: self._eliminar_fila(row))
        self.table.setCellWidget(row, 3, btn_del)

        self._update_area(row)
        self._conductores.append((cmb, inp))

    def _eliminar_fila(self, row):
        if self.table.rowCount() <= 1:
            return
        self.table.removeRow(row)
        if row < len(self._conductores):
            self._conductores.pop(row)

    def _update_area(self, row):
        if row >= self.table.rowCount():
            return
        cmb = self.table.cellWidget(row, 0)
        inp = self.table.cellWidget(row, 1)
        lbl_area = self.table.cellWidget(row, 2)
        if cmb and inp and lbl_area:
            try:
                seccion = float(cmb.currentText())
                cant = int(inp.text()) if inp.text() else 0
                area = AREAS_CONDUCTORES_MM2.get(seccion, 0) * cant
                lbl_area.setText(f"{area:.2f}")
            except:
                lbl_area.setText("-")

    def calcular(self):
        conductores = []
        for row in range(self.table.rowCount()):
            cmb = self.table.cellWidget(row, 0)
            inp = self.table.cellWidget(row, 1)
            if cmb and inp:
                try:
                    seccion = float(cmb.currentText())
                    cant = int(inp.text()) if inp.text() else 0
                    if cant > 0:
                        conductores.append({"seccion": seccion, "cantidad": cant})
                except:
                    pass
        if not conductores:
            raise ValueError("Agregue al menos un conductor")

        self._resultado = formulas.calcular_conduit(conductores)

def build_resultados(self):
        r = self._resultado

        # Resultado principal - Conduit recomendado
        self.add_resultado_item("Conduit Recomendado", f"{r['recomendado']['nombre']}", "green")
        self.add_resultado_item("% Ocupación", f"{r['valor']:.1f}%", "cyan")
        
        # Detalles
        self.add_resultado_item("Área Conductores", f"{r['area_conductores']:.1f} mm²", "cyan")
        self.add_resultado_item("N° Conductores", f"{r['n_conductores']}", "cyan")
        self.add_resultado_item("Fórmula", r['formula'], "cyan")
        if r.get('nota'):
            self.add_resultado_item("Detalle", r['nota'], "cyan")
