import sys, json, os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout,
    QVBoxLayout, QListWidget, QListWidgetItem, QStackedWidget,
    QLabel, QPushButton, QToolBar, QSizePolicy, QLineEdit, QFrame
)
from PyQt6.QtCore import Qt, QTimer

from theme import LIGHT, DARK

CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".calcElec_config.json")

# Importar todas las calculadoras
from calculadoras.ohm import CalculoOhm
from calculadoras.potencia_mono import CalculoPotenciaMonofasica
from calculadoras.potencia_tri import CalculoPotenciaTrifasica
from calculadoras.factor_potencia import CalculoFactorPotencia
from calculadoras.motor import CalculoMotor
from calculadoras.motor_fla import CalculoMotorFLA
from calculadoras.caida_tension import CalculoCaidaTension
from calculadoras.caida_tension_avanzada import CalculoCaidaTensionAvanzada
from calculadoras.seccion_conductor import CalculoSeccionConductor
from calculadoras.iluminacion import CalculoIluminacion
from calculadoras.demanda import CalculoDemanda
from calculadoras.canalizacion import CalculoCanalizacion
from calculadoras.ampacidad import CalculoAmpacidad
from calculadoras.ampacidad_d import CalculoAmpacidadD
from calculadoras.conduit import CalculoConduit
from calculadoras.proteccion import CalculoProteccion
from calculadoras.puesta_tierra import CalculoPuestaTierra
from calculadoras.cortocircuito import CalculoCortocircuito
from history_manager import HistoryManager
from toast import ToastManager

# Professional icon mapping for each calculator
# Format: (icon, label, class)
MENU_GRUPOS = [
    ("-- Cálculos Básicos --", None, None),
    ("⚡", "Ley de Ohm",               CalculoOhm),
    ("🔌", "Potencia Monofásica",      CalculoPotenciaMonofasica),
    ("⚡", "Potencia Trifásica",       CalculoPotenciaTrifasica),
    ("📊", "Factor de Potencia",       CalculoFactorPotencia),
    ("⚙️", "Motor Eléctrico",          CalculoMotor),
    ("🔄", "Motor por FLA",            CalculoMotorFLA),
    ("-- Distribución --", None, None),
    ("📉", "Caída de Tensión",         CalculoCaidaTension),
    ("📐", "Caída Tensión RX",         CalculoCaidaTensionAvanzada),
    ("📏", "Sección de Conductor",     CalculoSeccionConductor),
    ("💡", "Iluminación",              CalculoIluminacion),
    ("📈", "Demanda Máxima",           CalculoDemanda),
    ("📦", "Canalización",             CalculoCanalizacion),
    ("🔥", "Ampacidad Corregida",      CalculoAmpacidad),
    ("⬇️", "Ampacidad Enterrada",      CalculoAmpacidadD),
    ("🔧", "Selección Conduit",        CalculoConduit),
    ("-- Protección --", None, None),
    ("🛡️", "Protección Magnetotérmica", CalculoProteccion),
    ("⏚", "Puesta a Tierra",           CalculoPuestaTierra),
    ("💥", "Cortocircuito",            CalculoCortocircuito),
]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dark_mode = self.load_config()
        self.history = HistoryManager()
        self.setWindowTitle("CalcEléc // Calculadora Eléctrica")
        self.setMinimumSize(1200, 750)
        self.resize(1360, 850)
        self.setup_ui()
        self.toast = ToastManager(self)
        for c in self.calculadoras_widgets:
            if c:  # Check if not None
                c.toast = self.toast
                c.history = self.history
        self.apply_theme()

    def setup_ui(self):
        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setup_toolbar()
        
        # Initialize button text based on current mode
        self.btn_dark.setText("Claro" if self.dark_mode else "Oscuro")

        # Sidebar
        self.sidebar = QWidget()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(280)
        sb_layout = QVBoxLayout(self.sidebar)
        sb_layout.setContentsMargins(0, 0, 0, 0)
        sb_layout.setSpacing(0)
        
        # Header with gradient background
        header_frame = QFrame()
        header_frame.setObjectName("sidebar_header")
        header_frame.setFixedHeight(70)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(16, 8, 16, 8)
        
        logo = QLabel("⚡ CalcEléc")
        logo.setObjectName("logo")
        header_layout.addWidget(logo)
        header_layout.addStretch()
        
        sb_layout.addWidget(header_frame)
        
        # Search box
        self.search_box = QLineEdit()
        self.search_box.setObjectName("search_box")
        self.search_box.setPlaceholderText("Buscar calculadora...")
        self.search_box.textChanged.connect(self.filter_menu)
        sb_layout.addWidget(self.search_box)
        sb_layout.addSpacing(12)
        
        # Menu list
        self.menu = QListWidget()
        self.menu.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.calculadoras_widgets = []
        self.menu_items = []  # Store (label, cls, icon) tuples
        page_idx = 0
        
        for icon, label, cls in MENU_GRUPOS:
            if cls is None:
                # Section header
                item = QListWidgetItem(f"{icon}")
                item.setFlags(Qt.ItemFlag.NoItemFlags)
                f = item.font()
                if f.pointSize() > 0:
                    f.setPointSize(11)
                f.setBold(True)
                f.setFamily("Inter")
                item.setFont(f)
                self.menu.addItem(item)
                self.menu_items.append((icon, label, None))
            else:
                # Calculator item
                item_text = f"{label}"
                item = QListWidgetItem(item_text)
                item.setData(Qt.ItemDataRole.UserRole, page_idx)
                item.setToolTip(label)
                f = item.font()
                f.setFamily("Inter")
                item.setFont(f)
                self.menu.addItem(item)
                self.menu_items.append((icon, label, cls))
                page_idx += 1

        self.menu.currentItemChanged.connect(self.on_menu_change)
        sb_layout.addWidget(self.menu)
        layout.addWidget(self.sidebar)

        # Stack - create all calculators at startup
        self.stack = QStackedWidget()
        for icon, label, cls in MENU_GRUPOS:
            if cls is not None:
                w = cls()
                self.stack.addWidget(w)
                self.calculadoras_widgets.append(w)
        layout.addWidget(self.stack)

        # Select first valid
        for i in range(self.menu.count()):
            item = self.menu.item(i)
            if item.flags() & Qt.ItemFlag.ItemIsEnabled:
                self.menu.setCurrentItem(item)
                break
    
    def filter_menu(self, search_text):
        """Filter menu items based on search text"""
        search = search_text.lower().strip()
        
        for i in range(self.menu.count()):
            item = self.menu.item(i)
            icon, label, cls = self.menu_items[i]
            
            if cls is None:
                # Section header - show if search is empty
                item.setHidden(bool(search))
            else:
                # Calculator item - filter by name
                if not search or search in label.lower():
                    item.setHidden(False)
                else:
                    item.setHidden(True)

    def setup_toolbar(self):
        tb = QToolBar()
        tb.setMovable(False)
        tb.setFixedHeight(48)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        # Theme toggle
        self.btn_dark = QPushButton("Tema")
        self.btn_dark.setObjectName("btn_darkmode")
        self.btn_dark.setFixedHeight(32)
        self.btn_dark.clicked.connect(self.toggle_dark)

        # History button
        btn_hist = QPushButton("Historial")
        btn_hist.setObjectName("btn_secundario")
        btn_hist.setFixedHeight(32)
        btn_hist.clicked.connect(self.show_history)

        # Help button
        btn_help = QPushButton("Ayuda")
        btn_help.setObjectName("btn_secundario")
        btn_help.setFixedHeight(32)
        btn_help.clicked.connect(self.show_help)

        tb.addWidget(spacer)
        tb.addWidget(btn_help)
        tb.addWidget(self.btn_dark)
        tb.addWidget(btn_hist)
        self.addToolBar(tb)

    def on_menu_change(self, current, _):
        if current:
            idx = current.data(Qt.ItemDataRole.UserRole)
            if idx is not None:
                self.stack.setCurrentIndex(idx)

    def toggle_dark(self):
        self.dark_mode = not self.dark_mode
        self.save_config()
        self.apply_theme()
        self.btn_dark.setText("Claro" if self.dark_mode else "Oscuro")
        if self.toast:
            mode = "oscuro" if self.dark_mode else "claro"
            self.toast.show_toast(f"Tema {mode}", "success")

    def apply_theme(self):
        self.setStyleSheet(DARK if self.dark_mode else LIGHT)
        
    def show_history(self):
        from history_manager import HistoryDialog
        HistoryDialog(self.history, self.dark_mode, self).exec()
    
    def show_help(self):
        """Show help dialog"""
        from PyQt6.QtWidgets import QMessageBox
        msg = QMessageBox(self)
        msg.setWindowTitle("Ayuda - CalcEléc Pro")
        msg.setText("<h2>⚡ CalcEléc Pro</h2>"
                    "<p>Calculadora Eléctrica Profesional</p>"
                    "<h3>Características:</h3>"
                    "<ul>"
                    "<li>18 calculadoras eléctricas</li>"
                    "<li>Historial de cálculos con exportación PDF</li>"
                    "<li>Temas claro y oscuro</li>"
                    "<li>Búsqueda rápida de calculadoras</li>"
                    "<li>Validación visual de entradas</li>"
                    "<li>Presets configurables</li>"
                    "</ul>"
                    "<p><b>Atajos de teclado:</b></p>"
                    "<ul>"
                    "<li><b>Ctrl+B</b> - Buscar calculadora</li>"
                    "<li><b>Ctrl+D</b> - Cambiar tema</li>"
                    "<li><b>Ctrl+H</b> - Ver historial</li>"
                    "<li><b>Enter</b> - Calcular</li>"
                    "</ul>")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()

    def load_config(self):
        try:
            with open(CONFIG_FILE) as f:
                return json.load(f).get("dark_mode", False)
        except Exception:
            return False

    def save_config(self):
        with open(CONFIG_FILE, "w") as f:
            json.dump({"dark_mode": self.dark_mode}, f)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())