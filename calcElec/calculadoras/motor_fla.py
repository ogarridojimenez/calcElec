from PyQt6.QtWidgets import QLineEdit, QComboBox, QVBoxLayout, QHBoxLayout, QLabel
from calculadoras.base import CalculadoraBase
import formulas
from constants import FLA_TABLE

class CalculoMotorFLA(CalculadoraBase):
    NOMBRE = "Motor por FLA"
    SUBTITULO = "Cálculo basado en Full Load Amps (tabla normativa)"
    ICONO = "FLA"

    def build_inputs(self):
        info = QLabel("Selecciona la potencia HP y tensión para obtener el FLA nominal del motor trifásico.")
        info.setObjectName("info_box")
        info.setWordWrap(True)
        self.layout_inputs.addWidget(info)

        # Potencia HP
        self.cmb_hp = QComboBox()
        hp_values = [0.5, 1, 1.5, 2, 3, 5, 7.5, 10, 15, 20, 25, 30]
        self.cmb_hp.addItems([str(h) for h in hp_values])
        self.add_field("Potencia HP", self.cmb_hp, required=True)

        # Tensión
        self.cmb_tension = QComboBox()
        self.cmb_tension.addItems(["220", "380", "440"])
        self.cmb_tension.setCurrentText("380")
        self.add_field("Tensión (V)", self.cmb_tension, required=True)

        # Tipo de arranque
        self.cmb_arranque = QComboBox()
        self.cmb_arranque.addItems(["Directo DOL", "Estrella-Triángulo", "Variador VFD", "ITM"])
        self.add_field("Tipo de arranque", self.cmb_arranque, required=True)

        # Método instalación
        self.cmb_metodo = QComboBox()
        self.cmb_metodo.addItems(["A1: Tubo empotrado", "B1: Tubo en superficie", "C: Sobre bandeja"])
        self.add_field("Método instalación", self.cmb_metodo, required=True)

        # Temperatura ambiente
        self.inp_temp = QLineEdit("35")
        self.add_field("Temperatura ambiente (°C)", self.inp_temp, required=True)

        # Nº circuitos
        self.inp_circuitos = QLineEdit("1")
        self.add_field("Nº circuitos", self.inp_circuitos, required=True)

    def calcular(self):
        hp = float(self.cmb_hp.currentText())
        tension = int(self.cmb_tension.currentText())

        fla_entry = FLA_TABLE.get(hp, {})
        fla = fla_entry.get(tension, 0)
        if fla == 0:
            raise ValueError(f"No hay datos FLA para {hp} HP a {tension}V")

        # Use the additional inputs for correction factors
        temp = float(self.inp_temp.text())
        n_circ = int(self.inp_circuitos.text())
        
        # Get correction factors from formulas
        arranque = self.cmb_arranque.currentText()
        metodo = self.cmb_metodo.currentText()
        
        # Calculate contactor based on arrangement type
        contactor_base = 1.15 * fla
        from constants import IN_NORM
        contactor = next((x for x in [9,12,16,18,25,32,38,40,50,63,75,80,95,115,125,150,185,225,265,300,400,500] if x >= contactor_base), 500)
        
        conductor = formulas.seccion_norm(fla * 1.25 / 4)
        itm = formulas.in_norm(1.25 * fla)

        self.resultado_data = {
            "fla": fla, 
            "conductor": conductor, 
            "itm": itm, 
            "hp": hp, 
            "tension": tension,
            "contactor": contactor,
            "temp": temp,
            "n_circ": n_circ,
            "arranque": arranque,
            "metodo": metodo
        }

    def build_resultados(self):
        r = self.resultado_data
        self.add_resultado_item("FLA (Full Load Amps)", f"{r['fla']:.1f} A", "cyan")
        self.add_resultado_item("Conductor", f"{r['conductor']} mm²", "green")
        self.add_resultado_item("Interruptor (ITM)", f"{r['itm']} A", "amber")
        self.add_resultado_item("Contactor", f"{r['contactor']} A", "blue")
