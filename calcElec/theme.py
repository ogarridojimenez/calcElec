# CalcEléc Theme — Panel Técnico
# Engineering workspace aesthetic
# Palette derived from electrical panel colors, copper conductors, insulation materials

# ═══════════════════════════════════════════════════════════════
# COLOR PRIMITIVES (all tokens trace back to these)
# ═══════════════════════════════════════════════════════════════
#
# SURFACES (panel gray progression)
#   --panel-canvas:       #37474f  (base canvas)
#   --panel-surface-1:    #455a64  (cards, inputs — elevation 1)
#   --panel-surface-2:    #546e7a  (hover states — elevation 2)
#   --panel-inset:        #263238  (input fields — recessed)
#
# FOREGROUNDS (text hierarchy)
#   --fg-primary:         #eceff1  (headlines, primary text)
#   --fg-secondary:       #b0bec5  (labels, supporting text)
#   --fg-tertiary:        #78909c  (metadata, hints)
#   --fg-muted:           #546e7a  (disabled, placeholders)
#
# SEMANTIC (compliance colors — desaturated for dark bg)
#   --compliance-pass:    #66bb6a  (meets code / OK)
#   --compliance-warn:    #ffa726  (review needed)
#   --compliance-fail:    #ef5350  (does not comply)
#   --compliance-info:    #42a5f5  (informational)
#
# ACCENT
#   --copper:             #c87533  (primary action — conductor identity)
#   --insulation:         #1e88e5  (focus, links — wire insulation)
#   --arc:                #00bcd4  (secondary accent — energy)
#
# BORDERS (separation hierarchy)
#   --border-subtle:      rgba(255,255,255,0.06)  (faint division)
#   --border-standard:    rgba(255,255,255,0.12)  (card edges)
#   --border-strong:      rgba(255,255,255,0.22)  (input borders)
#   --border-focus:       #1e88e5                  (active element)
#
# ═══════════════════════════════════════════════════════════════

LIGHT = """
/* ═══════════════════════════════════════════════════════════════
   THEME: Panel Técnico — Light Mode
   Engineering workspace — clean, precise, authoritative
   ═══════════════════════════════════════════════════════════════ */

/* === BASE === */
QMainWindow, QWidget {
    background-color: #eceff1;
    font-family: 'Inter', 'Segoe UI', 'Noto Sans', sans-serif;
    font-size: 14px;
    color: #263238;
}

/* === SIDEBAR === */
QWidget#sidebar {
    background-color: #eceff1;
    border-right: 1px solid #cfd8dc;
}

QWidget#sidebar QFrame#sidebar_header {
    background-color: #f5f5f5;
    border-bottom: 1px solid #cfd8dc;
    border: none;
}

QWidget#sidebar QLabel#logo {
    font-size: 18px;
    font-weight: 700;
    color: #263238;
    padding: 4px;
    letter-spacing: -0.3px;
}

QWidget#sidebar QLineEdit#search_box {
    background-color: #ffffff;
    border: 1px solid #cfd8dc;
    border-radius: 6px;
    padding: 9px 12px;
    font-size: 13px;
    color: #37474f;
}

QWidget#sidebar QLineEdit#search_box:focus {
    border: 1px solid #1e88e5;
    background-color: #ffffff;
}

/* === CALCULATOR HEADER === */
QFrame#icon_box {
    background-color: #f5f5f5;
    border: 1px solid #cfd8dc;
    border-radius: 8px;
}

QLabel#icon_label {
    font-size: 20px;
    font-weight: 600;
    color: #263238;
    background: transparent;
}

QLabel#compliance_icon {
    font-size: 16px;
    font-weight: 700;
    color: #2e7d32;
    background: transparent;
}

QLabel#resultado_titulo {
    font-size: 14px;
    font-weight: 600;
    color: #546e7a;
    background: transparent;
}

/* === RESULT CARDS === */
QFrame#resultado_card_green {
    background-color: #ffffff;
    border: 1px solid #cfd8dc;
    border-left: 4px solid #2e7d32;
    border-radius: 6px;
    padding: 10px 14px;
}

QFrame#resultado_card_cyan {
    background-color: #ffffff;
    border: 1px solid #cfd8dc;
    border-left: 4px solid #0277bd;
    border-radius: 6px;
    padding: 10px 14px;
}

QFrame#resultado_card_amber {
    background-color: #ffffff;
    border: 1px solid #cfd8dc;
    border-left: 4px solid #e65100;
    border-radius: 6px;
    padding: 10px 14px;
}

QFrame#resultado_card_red {
    background-color: #ffffff;
    border: 1px solid #cfd8dc;
    border-left: 4px solid #c62828;
    border-radius: 6px;
    padding: 10px 14px;
}

/* === TYPOGRAPHY === */
QLabel#titulo {
    font-size: 24px;
    font-weight: 700;
    color: #263238;
    letter-spacing: -0.2px;
}

QLabel#subtitulo {
    font-size: 14px;
    color: #546e7a;
    margin-top: 2px;
}

QLabel#norma {
    font-size: 12px;
    color: #78909c;
    font-style: italic;
}

QLabel#label {
    font-size: 11px;
    color: #546e7a;
    font-weight: 600;
    margin-bottom: 4px;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}

QLabel#resultado_label {
    font-size: 13px;
    color: #546e7a;
    font-weight: 500;
}

QLabel#resultado_valor {
    font-size: 30px;
    font-weight: 700;
    color: #2e7d32;
    font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace;
    background: transparent;
}

QLabel#resultado_valor_cyan {
    font-size: 30px;
    font-weight: 700;
    color: #0277bd;
    font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace;
    background: transparent;
}

QLabel#resultado_valor_amber {
    font-size: 30px;
    font-weight: 700;
    color: #e65100;
    font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace;
    background: transparent;
}

QLabel#resultado_valor_red {
    font-size: 30px;
    font-weight: 700;
    color: #c62828;
    font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace;
    background: transparent;
}

QLabel#cumple {
    font-size: 14px;
    font-weight: 700;
    color: #2e7d32;
}

QLabel#no_cumple {
    font-size: 14px;
    font-weight: 700;
    color: #c62828;
}

QLabel#error_text {
    font-size: 13px;
    color: #c62828;
    background: rgba(198, 40, 40, 0.08);
    border: 1px solid rgba(198, 40, 40, 0.25);
    border-radius: 6px;
    padding: 10px 14px;
}

QLabel#hint_text {
    font-size: 11px;
    color: #78909c;
    margin-top: 2px;
    font-style: italic;
}

QLabel#info_box {
    background: rgba(30, 136, 229, 0.08);
    border: 1px solid rgba(30, 136, 229, 0.25);
    border-left: 4px solid #1e88e5;
    border-radius: 6px;
    padding: 12px 14px;
    color: #37474f;
    font-size: 12px;
}

QLabel#info_box_amber {
    background: rgba(230, 126, 0, 0.08);
    border: 1px solid rgba(230, 126, 0, 0.25);
    border-left: 4px solid #e67e00;
    border-radius: 6px;
    padding: 12px 14px;
    color: #37474f;
    font-size: 12px;
}

/* === INPUTS === */
QLineEdit {
    border: 1px solid #b0bec5;
    border-radius: 6px;
    padding: 10px 14px;
    background-color: #ffffff;
    color: #263238;
    font-size: 14px;
    min-height: 20px;
}

QLineEdit:focus {
    border: 1px solid #1e88e5;
    background-color: #ffffff;
}

QLineEdit:disabled {
    background-color: #f5f5f5;
    color: #90a4ae;
    border: 1px solid #cfd8dc;
}

QLineEdit[error="true"] {
    border: 1px solid #ef5350;
    background-color: rgba(239, 83, 80, 0.06);
}

QLineEdit[valid="valid"] {
    border: 2px solid #66bb6a;
    background-color: rgba(102, 187, 106, 0.06);
}

QLineEdit[valid="invalid"] {
    border: 2px solid #ef5350;
    background-color: rgba(239, 83, 80, 0.1);
}

QLineEdit[valid="empty"] {
    border: 1px solid #b0bec5;
}

QLineEdit::placeholder {
    color: #90a4ae;
}

QComboBox {
    border: 1px solid #b0bec5;
    border-radius: 6px;
    padding: 10px 14px;
    background-color: #ffffff;
    color: #263238;
    font-size: 14px;
    min-height: 20px;
}

QComboBox:focus {
    border: 1px solid #1e88e5;
    background-color: #ffffff;
}

QComboBox::drop-down {
    border: none;
    width: 28px;
    border-left: 1px solid #cfd8dc;
}

QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #78909c;
    margin-right: 7px;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    color: #263238;
    border: 1px solid #b0bec5;
    selection-background-color: rgba(30, 136, 229, 0.15);
    selection-color: #1565c0;
    padding: 4px;
}

/* === BUTTONS === */
QPushButton#btn_calcular {
    background-color: #1e88e5;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 12px 32px;
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

QPushButton#btn_calcular:hover {
    background-color: #1976d2;
}

QPushButton#btn_calcular:pressed {
    background-color: #1565c0;
}

QPushButton#btn_calcular:disabled {
    background-color: #cfd8dc;
    color: #90a4ae;
}

QPushButton#btn_limpiar {
    background-color: #78909c;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 12px 24px;
    font-size: 13px;
    font-weight: 600;
}

QPushButton#btn_limpiar:hover {
    background-color: #607d8b;
}

QPushButton#btn_limpiar:pressed {
    background-color: #546e7a;
}

QPushButton#btn_guardar {
    background-color: #2e7d32;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 10px 24px;
    font-size: 13px;
    font-weight: 600;
}

QPushButton#btn_guardar:hover {
    background-color: #1b5e20;
}

QPushButton#btn_secundario {
    background-color: transparent;
    color: #37474f;
    border: 1px solid #b0bec5;
    border-radius: 6px;
    padding: 8px 20px;
    font-size: 13px;
    font-weight: 500;
}

QPushButton#btn_secundario:hover {
    background-color: rgba(0, 0, 0, 0.04);
    border-color: #78909c;
}

QPushButton#btn_agregar {
    color: #1e88e5;
    border: none;
    background-color: transparent;
    font-size: 13px;
    font-weight: 500;
}

QPushButton#btn_agregar:hover {
    color: #1565c0;
}

QPushButton#btn_eliminar {
    color: #ef5350;
    border: none;
    background-color: transparent;
    font-size: 13px;
    padding: 4px 8px;
}

QPushButton#btn_darkmode {
    background-color: transparent;
    border: 1px solid #b0bec5;
    border-radius: 6px;
    font-size: 12px;
    padding: 6px 14px;
    color: #546e7a;
}

QPushButton#btn_darkmode:hover {
    background-color: rgba(0, 0, 0, 0.04);
    border-color: #78909c;
}

/* === RADIO BUTTONS (toggle pills) === */
QRadioButton {
    font-size: 13px;
    color: #37474f;
    padding: 8px 16px;
    background-color: #f5f5f5;
    border: 1px solid #cfd8dc;
    border-radius: 6px;
    margin: 2px;
}

QRadioButton::indicator {
    width: 0;
    height: 0;
}

QRadioButton:checked {
    background-color: #1e88e5;
    color: #ffffff;
    border-color: #1e88e5;
    font-weight: 600;
}

/* === LISTS (sidebar nav) === */
QListWidget {
    background-color: transparent;
    border: none;
    font-size: 14px;
    outline: none;
}

QListWidget::item {
    padding: 9px 14px;
    border-radius: 6px;
    color: #37474f;
    margin: 1px 6px;
}

QListWidget::item:selected {
    background-color: #1e88e5;
    color: #ffffff;
    font-weight: 600;
}

QListWidget::item:hover:!selected {
    background-color: rgba(0, 0, 0, 0.04);
}

/* === FRAMES & CARDS === */
QFrame#tarjeta {
    background-color: #ffffff;
    border: 1px solid #cfd8dc;
    border-radius: 8px;
    padding: 20px;
}

QFrame#resultado_frame {
    background: rgba(46, 125, 50, 0.06);
    border: 1px solid rgba(46, 125, 50, 0.25);
    border-left: 4px solid #2e7d32;
    border-radius: 8px;
    padding: 16px;
}

QFrame#resultado_frame_error {
    background: rgba(198, 40, 40, 0.06);
    border: 1px solid rgba(198, 40, 40, 0.25);
    border-left: 4px solid #c62828;
    border-radius: 8px;
    padding: 16px;
}

QFrame#resultado_frame_warning {
    background: rgba(230, 126, 0, 0.06);
    border: 1px solid rgba(230, 126, 0, 0.25);
    border-left: 4px solid #e67e00;
    border-radius: 8px;
    padding: 16px;
}

QFrame#separador {
    background: #cfd8dc;
    max-height: 1px;
}

/* === SCROLL BARS === */
QScrollArea {
    border: none;
    background-color: transparent;
}

QScrollBar:vertical {
    background-color: #f5f5f5;
    width: 7px;
    border-radius: 4px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background-color: #b0bec5;
    border-radius: 4px;
    min-height: 36px;
}

QScrollBar::handle:vertical:hover {
    background-color: #78909c;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* === TABLES === */
QTableWidget {
    border: 1px solid #cfd8dc;
    border-radius: 6px;
    font-size: 13px;
    background-color: #ffffff;
    gridline-color: #e0e0e0;
}

QTableWidget::item {
    padding: 8px;
    color: #263238;
}

QTableWidget::item:selected {
    background-color: rgba(30, 136, 229, 0.15);
    color: #1565c0;
}

QHeaderView::section {
    background-color: #f5f5f5;
    border: none;
    padding: 8px;
    font-weight: 600;
    color: #546e7a;
    border-bottom: 1px solid #cfd8dc;
}

/* === TOOLBAR === */
QToolBar {
    background-color: #f5f5f5;
    border-bottom: 1px solid #cfd8dc;
    spacing: 10px;
    padding: 6px 14px;
}
"""

# ═══════════════════════════════════════════════════════════════
# DARK MODE — The primary experience
# ═══════════════════════════════════════════════════════════════

DARK = """
/* ═══════════════════════════════════════════════════════════════
   THEME: Panel Técnico — Dark Mode
   Engineering workspace — panel gray, copper accent, precise
   ═══════════════════════════════════════════════════════════════ */

/* === BASE === */
QMainWindow, QWidget {
    background-color: #37474f;
    font-family: 'Inter', 'Segoe UI', 'Noto Sans', sans-serif;
    font-size: 14px;
    color: #eceff1;
}

/* === SIDEBAR === */
QWidget#sidebar {
    background-color: #37474f;
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}

QWidget#sidebar QFrame#sidebar_header {
    background-color: rgba(255, 255, 255, 0.03);
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    border: none;
}

QWidget#sidebar QLabel#logo {
    font-size: 18px;
    font-weight: 700;
    color: #eceff1;
    padding: 4px;
    letter-spacing: -0.3px;
}

QWidget#sidebar QLineEdit#search_box {
    background-color: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 6px;
    padding: 9px 12px;
    font-size: 13px;
    color: #eceff1;
}

QWidget#sidebar QLineEdit#search_box:focus {
    border: 1px solid #1e88e5;
    background-color: rgba(255, 255, 255, 0.06);
}

/* === CALCULATOR HEADER === */
QFrame#icon_box {
    background-color: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
}

QLabel#icon_label {
    font-size: 20px;
    font-weight: 600;
    color: #eceff1;
    background: transparent;
}

QLabel#compliance_icon {
    font-size: 16px;
    font-weight: 700;
    color: #66bb6a;
    background: transparent;
}

QLabel#resultado_titulo {
    font-size: 14px;
    font-weight: 600;
    color: #90a4ae;
    background: transparent;
}

/* === RESULT CARDS === */
QFrame#resultado_card_green {
    background-color: #455a64;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-left: 4px solid #66bb6a;
    border-radius: 6px;
    padding: 10px 14px;
}

QFrame#resultado_card_cyan {
    background-color: #455a64;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-left: 4px solid #42a5f5;
    border-radius: 6px;
    padding: 10px 14px;
}

QFrame#resultado_card_amber {
    background-color: #455a64;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-left: 4px solid #ffa726;
    border-radius: 6px;
    padding: 10px 14px;
}

QFrame#resultado_card_red {
    background-color: #455a64;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-left: 4px solid #ef5350;
    border-radius: 6px;
    padding: 10px 14px;
}

/* === TYPOGRAPHY === */
QLabel#titulo {
    font-size: 24px;
    font-weight: 700;
    color: #eceff1;
    letter-spacing: -0.2px;
}

QLabel#subtitulo {
    font-size: 14px;
    color: #90a4ae;
    margin-top: 2px;
}

QLabel#norma {
    font-size: 12px;
    color: #78909c;
    font-style: italic;
}

QLabel#label {
    font-size: 11px;
    color: #90a4ae;
    font-weight: 600;
    margin-bottom: 4px;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}

QLabel#resultado_label {
    font-size: 13px;
    color: #90a4ae;
    font-weight: 500;
}

QLabel#resultado_valor {
    font-size: 30px;
    font-weight: 700;
    color: #66bb6a;
    font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace;
    background: transparent;
}

QLabel#resultado_valor_cyan {
    font-size: 30px;
    font-weight: 700;
    color: #42a5f5;
    font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace;
    background: transparent;
}

QLabel#resultado_valor_amber {
    font-size: 30px;
    font-weight: 700;
    color: #ffa726;
    font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace;
    background: transparent;
}

QLabel#resultado_valor_red {
    font-size: 30px;
    font-weight: 700;
    color: #ef5350;
    font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace;
    background: transparent;
}

QLabel#cumple {
    font-size: 14px;
    font-weight: 700;
    color: #66bb6a;
}

QLabel#no_cumple {
    font-size: 14px;
    font-weight: 700;
    color: #ef5350;
}

QLabel#error_text {
    font-size: 13px;
    color: #ef5350;
    background: rgba(239, 83, 80, 0.08);
    border: 1px solid rgba(239, 83, 80, 0.3);
    border-radius: 6px;
    padding: 10px 14px;
}

QLabel#hint_text {
    font-size: 11px;
    color: #78909c;
    margin-top: 2px;
    font-style: italic;
}

QLabel#info_box {
    background: rgba(30, 136, 229, 0.08);
    border: 1px solid rgba(30, 136, 229, 0.25);
    border-left: 4px solid #42a5f5;
    border-radius: 6px;
    padding: 12px 14px;
    color: #b0bec5;
    font-size: 12px;
}

QLabel#info_box_amber {
    background: rgba(255, 167, 38, 0.08);
    border: 1px solid rgba(255, 167, 38, 0.25);
    border-left: 4px solid #ffa726;
    border-radius: 6px;
    padding: 12px 14px;
    color: #b0bec5;
    font-size: 12px;
}

/* === INPUTS === */
QLineEdit {
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 6px;
    padding: 10px 14px;
    background-color: #263238;
    color: #eceff1;
    font-size: 14px;
    min-height: 20px;
}

QLineEdit:focus {
    border: 1px solid #1e88e5;
    background-color: rgba(30, 136, 229, 0.08);
}

QLineEdit:disabled {
    background-color: rgba(255, 255, 255, 0.03);
    color: #546e7a;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

QLineEdit[error="true"] {
    border: 1px solid #ef5350;
    background-color: rgba(239, 83, 80, 0.08);
}

QLineEdit[valid="valid"] {
    border: 2px solid #66bb6a;
    background-color: rgba(102, 187, 106, 0.1);
}

QLineEdit[valid="invalid"] {
    border: 2px solid #ef5350;
    background-color: rgba(239, 83, 80, 0.15);
}

QLineEdit[valid="empty"] {
    border: 1px solid rgba(255, 255, 255, 0.18);
}

QLineEdit::placeholder {
    color: #546e7a;
}

QComboBox {
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 6px;
    padding: 10px 14px;
    background-color: #263238;
    color: #eceff1;
    font-size: 14px;
    min-height: 20px;
}

QComboBox:focus {
    border: 1px solid #1e88e5;
    background-color: rgba(30, 136, 229, 0.08);
}

QComboBox::drop-down {
    border: none;
    width: 28px;
    border-left: 1px solid rgba(255, 255, 255, 0.12);
}

QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #78909c;
    margin-right: 7px;
}

QComboBox QAbstractItemView {
    background-color: #263238;
    color: #eceff1;
    border: 1px solid rgba(255, 255, 255, 0.18);
    selection-background-color: rgba(30, 136, 229, 0.25);
    selection-color: #eceff1;
    padding: 4px;
}

/* === BUTTONS === */
QPushButton#btn_calcular {
    background-color: #1e88e5;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 12px 32px;
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

QPushButton#btn_calcular:hover {
    background-color: #1976d2;
}

QPushButton#btn_calcular:pressed {
    background-color: #1565c0;
}

QPushButton#btn_calcular:disabled {
    background-color: rgba(255, 255, 255, 0.08);
    color: #546e7a;
}

QPushButton#btn_limpiar {
    background-color: #546e7a;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 12px 24px;
    font-size: 13px;
    font-weight: 600;
}

QPushButton#btn_limpiar:hover {
    background-color: #607d8b;
}

QPushButton#btn_limpiar:pressed {
    background-color: #455a64;
}

QPushButton#btn_guardar {
    background-color: #2e7d32;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 10px 24px;
    font-size: 13px;
    font-weight: 600;
}

QPushButton#btn_guardar:hover {
    background-color: #1b5e20;
}

QPushButton#btn_secundario {
    background-color: transparent;
    color: #b0bec5;
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 6px;
    padding: 8px 20px;
    font-size: 13px;
    font-weight: 500;
}

QPushButton#btn_secundario:hover {
    background-color: rgba(255, 255, 255, 0.06);
    border-color: rgba(255, 255, 255, 0.25);
}

QPushButton#btn_agregar {
    color: #42a5f5;
    border: none;
    background-color: transparent;
    font-size: 13px;
    font-weight: 500;
}

QPushButton#btn_agregar:hover {
    color: #64b5f6;
}

QPushButton#btn_eliminar {
    color: #ef5350;
    border: none;
    background-color: transparent;
    font-size: 13px;
    padding: 4px 8px;
}

QPushButton#btn_darkmode {
    background-color: transparent;
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 6px;
    font-size: 12px;
    padding: 6px 14px;
    color: #78909c;
}

QPushButton#btn_darkmode:hover {
    background-color: rgba(255, 255, 255, 0.06);
    border-color: rgba(255, 255, 255, 0.25);
}

/* === RADIO BUTTONS (toggle pills) === */
QRadioButton {
    font-size: 13px;
    color: #b0bec5;
    padding: 8px 16px;
    background-color: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 6px;
    margin: 2px;
}

QRadioButton::indicator {
    width: 0;
    height: 0;
}

QRadioButton:checked {
    background-color: #1e88e5;
    color: #ffffff;
    border-color: #1e88e5;
    font-weight: 600;
}

/* === LISTS (sidebar nav) === */
QListWidget {
    background-color: transparent;
    border: none;
    font-size: 14px;
    outline: none;
}

QListWidget::item {
    padding: 9px 14px;
    border-radius: 6px;
    color: #b0bec5;
    margin: 1px 6px;
}

QListWidget::item:selected {
    background-color: #1e88e5;
    color: #ffffff;
    font-weight: 600;
}

QListWidget::item:hover:!selected {
    background-color: rgba(255, 255, 255, 0.06);
}

/* === FRAMES & CARDS === */
QFrame#tarjeta {
    background-color: #455a64;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    padding: 20px;
}

QFrame#resultado_frame {
    background: rgba(102, 187, 106, 0.06);
    border: 1px solid rgba(102, 187, 106, 0.25);
    border-left: 4px solid #66bb6a;
    border-radius: 8px;
    padding: 16px;
}

QFrame#resultado_frame_error {
    background: rgba(239, 83, 80, 0.06);
    border: 1px solid rgba(239, 83, 80, 0.25);
    border-left: 4px solid #ef5350;
    border-radius: 8px;
    padding: 16px;
}

QFrame#resultado_frame_warning {
    background: rgba(255, 167, 38, 0.06);
    border: 1px solid rgba(255, 167, 38, 0.25);
    border-left: 4px solid #ffa726;
    border-radius: 8px;
    padding: 16px;
}

QFrame#separador {
    background: rgba(255, 255, 255, 0.1);
    max-height: 1px;
}

/* === SCROLL BARS === */
QScrollArea {
    border: none;
    background-color: transparent;
}

QScrollBar:vertical {
    background-color: rgba(255, 255, 255, 0.04);
    width: 7px;
    border-radius: 4px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background-color: rgba(255, 255, 255, 0.18);
    border-radius: 4px;
    min-height: 36px;
}

QScrollBar::handle:vertical:hover {
    background-color: rgba(255, 255, 255, 0.28);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* === TABLES === */
QTableWidget {
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 6px;
    font-size: 13px;
    background-color: rgba(255, 255, 255, 0.03);
    gridline-color: rgba(255, 255, 255, 0.08);
}

QTableWidget::item {
    padding: 8px;
    color: #eceff1;
}

QTableWidget::item:selected {
    background-color: rgba(30, 136, 229, 0.25);
    color: #eceff1;
}

QHeaderView::section {
    background-color: rgba(255, 255, 255, 0.06);
    border: none;
    padding: 8px;
    font-weight: 600;
    color: #90a4ae;
    border-bottom: 1px solid rgba(255, 255, 255, 0.12);
}

/* === TOOLBAR === */
QToolBar {
    background-color: rgba(255, 255, 255, 0.03);
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    spacing: 10px;
    padding: 6px 14px;
}
"""
