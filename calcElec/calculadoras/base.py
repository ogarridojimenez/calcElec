from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QLineEdit, QComboBox,
    QButtonGroup, QRadioButton, QSizePolicy
)
from PyQt6.QtCore import Qt
from datetime import datetime
from animations import FadeAnimation, SlideAnimation, ResultFrameAnimation, LoadingAnimation
import os
from typing import Dict, List, Optional, Any

class CalculadoraBase(QWidget):
    NOMBRE = ""
    SUBTITULO = ""
    NORMA = ""
    ICONO = "⚡"

    def __init__(self):
        super().__init__()
        self.toast = None
        self.history = None
        self.resultado_data = {}
        self._build_ui()

    def _build_ui(self):
        # Main scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        # Container widget inside scroll
        container = QWidget()
        self.layout_main = QVBoxLayout(container)
        self.layout_main.setContentsMargins(40, 32, 40, 40)
        self.layout_main.setSpacing(20)
        self.layout_main.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMinAndMaxSize)
        
        # Header with icon
        header = QHBoxLayout()
        header.setSpacing(16)

        # Icon box — panel style, no hard-coded colors
        icon_box = QFrame()
        icon_box.setFixedSize(48, 48)
        icon_box.setObjectName("icon_box")
        icon_lbl = QLabel(self.ICONO)
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setObjectName("icon_label")
        icon_box_layout = QVBoxLayout(icon_box)
        icon_box_layout.setContentsMargins(0, 0, 0, 0)
        icon_box_layout.addWidget(icon_lbl)
        header.addWidget(icon_box)
        
        # Titles
        titles = QVBoxLayout()
        titles.setSpacing(4)
        t = QLabel(self.NOMBRE)
        t.setObjectName("titulo")
        titles.addWidget(t)
        if self.SUBTITULO:
            s = QLabel(self.SUBTITULO)
            s.setObjectName("subtitulo")
            titles.addWidget(s)
        if self.NORMA:
            n = QLabel(self.NORMA)
            n.setObjectName("norma")
            titles.addWidget(n)
        header.addLayout(titles)
        header.addStretch()
        self.layout_main.addLayout(header)
        
        # Info box
        self.build_info_box()
        
        # Separator
        sep = QFrame()
        sep.setObjectName("separador")
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFixedHeight(1)
        self.layout_main.addWidget(sep)
        
        # Input card
        self.frame_inputs = QFrame()
        self.frame_inputs.setObjectName("tarjeta")
        self.layout_inputs = QVBoxLayout(self.frame_inputs)
        self.layout_inputs.setSpacing(16)
        self.layout_inputs.setContentsMargins(24, 24, 24, 24)
        self.build_inputs()
        self.layout_main.addWidget(self.frame_inputs)
        
        # Error label
        self.lbl_error = QLabel("")
        self.lbl_error.setObjectName("error_text")
        self.lbl_error.setWordWrap(True)
        self.lbl_error.hide()
        self.layout_main.addWidget(self.lbl_error)
        
        # Buttons row
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)
        
        self.btn_calcular = QPushButton("[ Calcular ]")
        self.btn_calcular.setObjectName("btn_calcular")
        self.btn_calcular.setFixedHeight(40)
        self.btn_calcular.clicked.connect(self._on_calcular)
        btn_row.addWidget(self.btn_calcular)
        
        self.btn_limpiar = QPushButton("[ Limpiar ]")
        self.btn_limpiar.setObjectName("btn_limpiar")
        self.btn_limpiar.setFixedHeight(40)
        self.btn_limpiar.clicked.connect(self._on_limpiar)
        btn_row.addWidget(self.btn_limpiar)
        btn_row.addStretch()
        self.layout_main.addLayout(btn_row)
        
        # Result frame with animation
        self.frame_resultado = QFrame()
        self.frame_resultado.setObjectName("resultado_frame")
        # Make it expand to fill available space
        self.frame_resultado.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum
        )
        self.layout_resultado = QVBoxLayout(self.frame_resultado)
        self.layout_resultado.setSpacing(10)
        self.layout_resultado.setContentsMargins(16, 16, 16, 16)
        self.layout_resultado.setStretch(0, 1)
        
        # Result header — compliance badge area
        result_header = QHBoxLayout()
        result_header.setSpacing(10)

        # Compliance icon (will be colored dynamically)
        check_icon = QLabel("✓")
        check_icon.setObjectName("compliance_icon")
        result_header.addWidget(check_icon)

        result_title = QLabel("Resultado")
        result_title.setObjectName("resultado_titulo")
        result_header.addWidget(result_title)
        result_header.addStretch()
        self.layout_resultado.addLayout(result_header)

        # Separator
        result_sep = QFrame()
        result_sep.setObjectName("resultado_sep")
        result_sep.setFrameShape(QFrame.Shape.HLine)
        result_sep.setFixedHeight(1)
        self.layout_resultado.addWidget(result_sep)
        
        self.frame_resultado.hide()
        self.layout_main.addWidget(self.frame_resultado)
        
        # Buttons row: Guardar | Exportar | Presets
        btn_save_row = QHBoxLayout()
        self.btn_guardar = QPushButton("[ guardar ]")
        self.btn_guardar.setObjectName("btn_guardar")
        self.btn_guardar.setFixedHeight(36)
        self.btn_guardar.clicked.connect(self._guardar)
        self.btn_guardar.hide()
        btn_save_row.addWidget(self.btn_guardar)
        
        self.btn_export = QPushButton("[ exportar ]")
        self.btn_export.setObjectName("btn_export")
        self.btn_export.setFixedHeight(36)
        self.btn_export.clicked.connect(self._export_single)
        self.btn_export.hide()
        btn_save_row.addWidget(self.btn_export)
        
        # Preset buttons
        self.btn_save_preset = QPushButton("[ 💾 preset ]")
        self.btn_save_preset.setObjectName("btn_preset")
        self.btn_save_preset.setFixedHeight(36)
        self.btn_save_preset.clicked.connect(self._save_preset)
        self.btn_save_preset.hide()
        btn_save_row.addWidget(self.btn_save_preset)
        
        self.btn_load_preset = QPushButton("[ 📂 carga ]")
        self.btn_load_preset.setObjectName("btn_preset")
        self.btn_load_preset.setFixedHeight(36)
        self.btn_load_preset.clicked.connect(self._load_preset_dialog)
        self.btn_load_preset.hide()
        btn_save_row.addWidget(self.btn_load_preset)
        
        btn_save_row.addStretch()
        self.layout_main.addLayout(btn_save_row)
        
        # Allow flexible height for results
        self.layout_main.setStretch(0, 0)
        
        scroll.setWidget(container)
        container.setMinimumWidth(scroll.viewport().width())
        
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0,0,0,0)
        outer.addWidget(scroll, 1)

    def add_field(self, label_text, widget, hint="", required=True, tooltip=""):
        row = QVBoxLayout()
        row.setSpacing(6)
        lbl = QLabel(label_text + (" *" if required else ""))
        lbl.setObjectName("label")
        if tooltip:
            lbl.setToolTip(tooltip)
        row.addWidget(lbl)
        if hint:
            h = QLabel("💡 " + hint)
            h.setObjectName("hint_text")
            row.addWidget(h)
        
        if isinstance(widget, QLineEdit):
            widget.setPlaceholderText(hint or "Valor")
            widget.setObjectName("input_field")
            if tooltip:
                widget.setToolTip(tooltip)
            widget.textChanged.connect(lambda: self._validate_field(widget))
        
        row.addWidget(widget)
        self.layout_inputs.addLayout(row)
    
    def _validate_field(self, widget):
        """Valida visualmente un campo - borde rojo/verde"""
        text = widget.text().strip()
        if not text:
            widget.setProperty("valid", "empty")
        else:
            try:
                float(text)
                widget.setProperty("valid", "valid")
            except ValueError:
                widget.setProperty("valid", "invalid")
        widget.style().unpolish(widget)
        widget.style().polish(widget)
    
    def add_input_field(self, name, placeholder="", hint="", tooltip="", min_val=None, max_val=None):
        """Helper para crear campo de entrada con validación automática
        
        Args:
            name: Nombre del campo
            placeholder: Texto de ayuda
            hint: Pista adicional
            tooltip: Tooltip al pasar mouse
            min_val: Valor mínimo permitido (None = sin límite)
            max_val: Valor máximo permitido (None = sin límite)
        """
        inp = QLineEdit()
        inp.setPlaceholderText(placeholder or hint)
        inp.setObjectName("input_field")
        if tooltip:
            inp.setToolTip(tooltip)
        
        # Guardar rangos como atributo dinámico
        inp.setProperty('min_val', min_val)
        inp.setProperty('max_val', max_val)
        
        inp.textChanged.connect(lambda: self._validate_advanced(inp))
        return inp
    
    def _validate_advanced(self, widget):
        """Validación avanzada con rangos y feedback visual"""
        text = widget.text().strip()
        
        if not text:
            widget.setProperty("valid", "empty")
            widget.setToolTip("")
        else:
            try:
                value = float(text)
                min_val = widget.property('min_val')
                max_val = widget.property('max_val')
                
                # Validar rango si existe
                if min_val is not None and value < min_val:
                    widget.setProperty("valid", "invalid")
                    widget.setToolTip(f"Valor mínimo: {min_val}")
                elif max_val is not None and value > max_val:
                    widget.setProperty("valid", "invalid")
                    widget.setToolTip(f"Valor máximo: {max_val}")
                else:
                    widget.setProperty("valid", "valid")
                    widget.setToolTip("✓ Valor válido")
            except ValueError:
                widget.setProperty("valid", "invalid")
                widget.setToolTip("✗ Valor numérico requerido")
        
        widget.style().unpolish(widget)
        widget.style().polish(widget)
    
    def _validate_advanced(self, widget):
        """Validación avanzada con rangos y feedback visual"""
        text = widget.text().strip()
        
        if not text:
            widget.setProperty("valid", "empty")
            widget.setToolTip("")
        else:
            try:
                value = float(text)
                min_val = widget.property('min_val')
                max_val = widget.property('max_val')
                
                # Validar rango si existe
                if min_val is not None and value < min_val:
                    widget.setProperty("valid", "invalid")
                    widget.setToolTip(f"Valor mínimo: {min_val}")
                elif max_val is not None and value > max_val:
                    widget.setProperty("valid", "invalid")
                    widget.setToolTip(f"Valor máximo: {max_val}")
                else:
                    widget.setProperty("valid", "valid")
                    widget.setToolTip("✓ Valor válido")
            except ValueError:
                widget.setProperty("valid", "invalid")
                widget.setToolTip("✗ Valor numérico requerido")
        
        widget.style().unpolish(widget)
        widget.style().polish(widget)
    
    def add_field_inline(self, label_text, widget, hint="", tooltip=""):
        row = QHBoxLayout()
        row.setSpacing(12)
        lbl = QLabel(label_text)
        lbl.setObjectName("label")
        lbl.setFixedWidth(250)
        if tooltip:
            lbl.setToolTip(tooltip)
        row.addWidget(lbl)
        row.addWidget(widget)
        if hint:
            h = QLabel(hint)
            h.setObjectName("hint_text")
            h.setFixedWidth(60)
            row.addWidget(h)
        if isinstance(widget, QLineEdit):
            widget.setObjectName("input_field")
            widget.textChanged.connect(lambda: self._validate_field(widget))
        self.layout_inputs.addLayout(row)
        row = QHBoxLayout()
        row.setSpacing(12)
        lbl = QLabel(label_text)
        lbl.setObjectName("label")
        lbl.setFixedWidth(250)
        if tooltip:
            lbl.setToolTip(tooltip)
        row.addWidget(lbl)
        row.addWidget(widget)
        if hint:
            h = QLabel(hint)
            h.setObjectName("hint_text")
            h.setFixedWidth(60)
            row.addWidget(h)
        if isinstance(widget, QLineEdit):
            widget.setObjectName("input_field")
            widget.textChanged.connect(lambda: self._validate_field(widget))
        self.layout_inputs.addLayout(row)

    def add_resultado_item(self, label, valor_str, color="green"):
        row = QHBoxLayout()
        row.setSpacing(8)

        # Result card — themed with compliance accent
        accent_map = {
            "green": "#66bb6a",
            "cyan": "#42a5f5",
            "amber": "#ffa726",
            "red": "#ef5350"
        }
        accent = accent_map.get(color, "#66bb6a")

        result_card = QFrame()
        result_card.setObjectName(f"resultado_card_{color}")

        card_layout = QHBoxLayout(result_card)
        card_layout.setSpacing(12)

        lbl = QLabel(f"{label}")
        lbl.setObjectName("resultado_label")
        card_layout.addWidget(lbl)

        val = QLabel(valor_str)
        obj_name = {
            "green": "resultado_valor",
            "cyan": "resultado_valor_cyan",
            "amber": "resultado_valor_amber",
            "red": "resultado_valor_red",
        }.get(color, "resultado_valor")
        val.setObjectName(obj_name)
        card_layout.addWidget(val)

        card_layout.addStretch()
        row.addWidget(result_card)
        row.addStretch()
        self.layout_resultado.addLayout(row)

    def add_resultado_grid(self, items):
        """Add results in a 2-column grid layout"""
        grid = QHBoxLayout()
        grid.setSpacing(16)

        for i, (label, valor_str, color) in enumerate(items):
            col = QVBoxLayout()
            col.setSpacing(6)

            lbl = QLabel(label)
            lbl.setObjectName("resultado_label")
            col.addWidget(lbl)

            val = QLabel(valor_str)
            obj_name = {
                "green": "resultado_valor",
                "cyan": "resultado_valor_cyan",
                "amber": "resultado_valor_amber",
                "red": "resultado_valor_red",
            }.get(color, "resultado_valor")
            val.setObjectName(obj_name)
            col.addWidget(val)

            # Card — uses theme-defined tarjeta style
            card = QFrame()
            card.setObjectName("tarjeta")
            card.setLayout(col)
            grid.addWidget(card)

            # Start new row every 2 items
            if i % 2 == 1 and i < len(items) - 1:
                self.layout_resultado.addLayout(grid)
                grid = QHBoxLayout()
                grid.setSpacing(16)

        # Add remaining items
        if len(items) % 2 == 1:
            grid.addStretch()

        self.layout_resultado.addLayout(grid)

    def limpiar_resultados(self):
        while self.layout_resultado.count():
            itm = self.layout_resultado.takeAt(0)
            if itm.layout():
                while itm.layout().count():
                    w = itm.layout().takeAt(0).widget()
                    if w:
                        w.deleteLater()
            elif itm.widget():
                # Don't delete header and separator
                if itm.widget().objectName() not in ["resultado_header", "resultado_sep"]:
                    itm.widget().deleteLater()

    def _on_limpiar(self):
        # Hide results
        self.frame_resultado.hide()
        self.limpiar_resultados()
        self.btn_guardar.hide()
        self.btn_export.hide()
        self.lbl_error.hide()
        # Clear input fields - call virtual method
        self.limpiar_inputs()
        if self.toast:
            self.toast.show_toast("> datos limpiados", "info")

    def limpiar_inputs(self):
        """Clear all input widgets in the input frame"""
        from PyQt6.QtWidgets import QLineEdit, QComboBox, QStackedWidget, QTableWidget
        import functools
        
        def clear_widget(w):
            if isinstance(w, QLineEdit):
                w.setText("")
            elif isinstance(w, QComboBox):
                w.setCurrentIndex(0)
            elif isinstance(w, QStackedWidget):
                # Clear all pages
                for p in range(w.count()):
                    page = w.widget(p)
                    if page:
                        clear_widget_page(page)
            elif isinstance(w, QTableWidget):
                # Clear table rows except first one, set values to empty
                for row in range(w.rowCount()):
                    for col in range(w.columnCount()):
                        item = w.item(row, col)
                        if item:
                            item.setText("")
        
        def clear_widget_page(page):
            if hasattr(page, 'layout') and page.layout():
                for i in range(page.layout().count()):
                    item = page.layout().itemAt(i)
                    if item:
                        if item.widget():
                            clear_widget(item.widget())
                        elif item.layout():
                            for j in range(item.layout().count()):
                                nested = item.layout().itemAt(j)
                                if nested and nested.widget():
                                    clear_widget(nested.widget())
        
        # Clear main input layout
        for i in range(self.layout_inputs.count()):
            item = self.layout_inputs.itemAt(i)
            if item:
                if item.widget():
                    clear_widget(item.widget())
                elif item.layout():
                    for j in range(item.layout().count()):
                        nested = item.layout().itemAt(j)
                        if nested and nested.widget():
                            clear_widget(nested.widget())

    def _on_calcular(self):
        self.lbl_error.hide()
        self.limpiar_resultados()
        
        # Loading animation
        LoadingAnimation.animate_button(self.btn_calcular)
        
        try:
            self.calcular()
            self.build_resultados()
            
            # Show with animation
            ResultFrameAnimation.show_with_animation(self.frame_resultado)
            self.btn_guardar.show()
            self.btn_export.show()
            self.btn_save_preset.show()
            self.btn_load_preset.show()
            FadeAnimation.fade_in(self.btn_guardar, 300)
            FadeAnimation.fade_in(self.btn_export, 300)
            FadeAnimation.fade_in(self.btn_save_preset, 300)
            FadeAnimation.fade_in(self.btn_load_preset, 300)
            
            # Force immediate layout recalculation
            from PyQt6.QtCore import QTimer
            self.frame_resultado.setVisible(True)
            self.frame_resultado.setMinimumHeight(0)
            self.layout_main.activate()
            # Process events to update layout
            from PyQt6.QtWidgets import QApplication
            QApplication.processEvents()
            
            # Restore button
            LoadingAnimation.restore_button(self.btn_calcular)
            
            if self.toast:
                self.toast.show_toast("> calculo completado", "success")
        except ValueError as e:
            self.lbl_error.setText(f"> error: {str(e)}")
            self.lbl_error.show()
            FadeAnimation.fade_in(self.lbl_error, 300)
            self.frame_resultado.hide()
            
            # Restore button
            LoadingAnimation.restore_button(self.btn_calcular)
            
            if self.toast:
                self.toast.show_toast(f"> {e}", "error")

    def _guardar(self):
        """Guarda inputs + resultado en historial."""
        from PyQt6.QtWidgets import QLineEdit, QComboBox
        import logging
        
        datos_guardar = {}
        
        # 1. Capturar TODOS los campos de entrada del formulario
        def get_all_widgets(layout):
            """Recursively get all widgets from a layout"""
            widgets = []
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item.widget():
                    widgets.append(item.widget())
                elif item.layout():
                    widgets.extend(get_all_widgets(item.layout()))
            return widgets
        
        # Get all widgets from layout_inputs
        all_widgets = get_all_widgets(self.layout_inputs)
        
        for widget in all_widgets:
            # QLineEdit - campos de entrada
            if isinstance(widget, QLineEdit):
                texto = widget.text().strip()
                placeholder = widget.placeholderText().strip()
                # Skip "Resultado" and "0.0" placeholders - those are disabled fields
                if texto and placeholder not in ('Resultado', '0.0', ''):
                    datos_guardar[placeholder] = texto
                elif texto and not placeholder:
                    datos_guardar[f"campo_{len(datos_guardar)}"] = texto
            
            # QComboBox - selections
            elif isinstance(widget, QComboBox):
                if widget.currentIndex() >= 0:
                    datos_guardar[widget.objectName() or "seleccion"] = widget.currentText()
            
            # QRadioButton / QButtonGroup
            elif isinstance(widget, QRadioButton) and widget.isChecked():
                datos_guardar["tipo_calculo"] = widget.text()
        
        # 2. Agregar resultado del cálculo
        resultado = getattr(self, '_resultado', None)
        if not resultado:
            resultado = getattr(self, 'resultado_data', None)
        if resultado:
            for key, value in resultado.items():
                datos_guardar[f"RESULT_{key}"] = value
        
        # 3. También guardar en resultado_data para otras funciones
        if resultado:
            self.resultado_data = resultado
        
        if self.history and datos_guardar:
            self.history.agregar(self.NOMBRE, datos_guardar)
            if self.toast:
                self.toast.show_toast("> guardado en historial", "success")
            LoadingAnimation.restore_button(self.btn_guardar)
    
    def _export_single(self):
        # Export current calculation result + inputs to file
        from PyQt6.QtWidgets import QLineEdit, QComboBox, QRadioButton
        
        # 1. Get input values (same logic as _guardar)
        datos = {}
        
        def get_all_widgets(layout):
            widgets = []
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item.widget():
                    widgets.append(item.widget())
                elif item.layout():
                    widgets.extend(get_all_widgets(item.layout()))
            return widgets
        
        all_widgets = get_all_widgets(self.layout_inputs)
        
        for widget in all_widgets:
            if isinstance(widget, QLineEdit):
                texto = widget.text().strip()
                placeholder = widget.placeholderText().strip()
                if texto and placeholder not in ('Resultado', '0.0', ''):
                    datos[placeholder] = texto
                elif texto and not placeholder:
                    datos[f"campo_{len([k for k in datos if k.startswith('campo_')])}"] = texto
            elif isinstance(widget, QComboBox):
                if widget.currentIndex() >= 0:
                    datos[widget.objectName() or "seleccion"] = widget.currentText()
            elif isinstance(widget, QRadioButton) and widget.isChecked():
                datos["tipo_calculo"] = widget.text()
        
        # 2. Add result values with RESULT_ prefix
        resultado = getattr(self, '_resultado', None)
        if not resultado:
            resultado = getattr(self, 'resultado_data', None)
        if resultado:
            for key, value in resultado.items():
                datos[f"RESULT_{key}"] = value
        
        if not resultado:
            if self.toast:
                self.toast.show_toast("> no hay resultado para exportar", "error")
            return
        
        # Show save dialog
        from PyQt6.QtWidgets import QFileDialog, QMessageBox
        default_name = f"{self.NOMBRE}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Exportar Resultado", default_name, 
            "CSV (*.csv);;PDF (*.pdf)"
        )
        
        if not filepath:
            return
        
        try:
            if filepath.endswith('.pdf'):
                from pdf_export import export_history_pdf
                export_history_pdf([{
                    'nombre': self.NOMBRE,
                    'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'datos': datos
                }], filepath)
            else:
                import csv
                with open(filepath, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Campo', 'Valor'])
                    for key, value in datos.items():
                        writer.writerow([key, value])
            
            if self.toast:
                self.toast.show_toast("> exportado OK", "success")
        except Exception as e:
            if self.toast:
                self.toast.show_toast(f"> error: {e}", "error")
    
    def _get_input_values(self):
        """Get current input values as dictionary"""
        from PyQt6.QtWidgets import QLineEdit, QComboBox, QRadioButton
        
        datos = {}
        
        def get_all_widgets(layout):
            widgets = []
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item.widget():
                    widgets.append(item.widget())
                elif item.layout():
                    widgets.extend(get_all_widgets(item.layout()))
            return widgets
        
        all_widgets = get_all_widgets(self.layout_inputs)
        
        for widget in all_widgets:
            if isinstance(widget, QLineEdit):
                texto = widget.text().strip()
                placeholder = widget.placeholderText().strip()
                if texto and placeholder not in ('Resultado', '0.0', ''):
                    datos[placeholder] = texto
                elif texto and not placeholder:
                    datos[f"campo_{len([k for k in datos if k.startswith('campo_')])}"] = texto
            elif isinstance(widget, QComboBox):
                if widget.currentIndex() >= 0:
                    datos[widget.objectName() or "seleccion"] = widget.currentText()
            elif isinstance(widget, QRadioButton) and widget.isChecked():
                datos["tipo_calculo"] = widget.text()
        
        return datos
    
    def _set_input_values(self, datos):
        """Set input values from dictionary"""
        from PyQt6.QtWidgets import QLineEdit, QComboBox, QRadioButton
        
        def get_all_widgets(layout):
            widgets = []
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item.widget():
                    widgets.append(item.widget())
                elif item.layout():
                    widgets.extend(get_all_widgets(item.layout()))
            return widgets
        
        all_widgets = get_all_widgets(self.layout_inputs)
        
        for widget in all_widgets:
            if isinstance(widget, QLineEdit):
                placeholder = widget.placeholderText().strip()
                if placeholder in datos:
                    widget.setText(datos[placeholder])
            elif isinstance(widget, QComboBox):
                name = widget.objectName()
                if name and name in datos:
                    idx = widget.findText(datos[name])
                    if idx >= 0:
                        widget.setCurrentIndex(idx)
    
    def _save_preset(self):
        """Save current inputs as a preset"""
        from PyQt6.QtWidgets import QInputDialog, QMessageBox
        
        datos = self._get_input_values()
        if not datos:
            if self.toast:
                self.toast.show_toast("> no hay datos para guardar", "error")
            return
        
        nombre, ok = QInputDialog.getText(self, "Guardar Preset", "Nombre del preset:")
        if ok and nombre.strip():
            nombre = nombre.strip()
            save_preset(self.NOMBRE, nombre, datos)
            if self.toast:
                self.toast.show_toast(f"> preset '{nombre}' guardado", "success")
    
    def _load_preset_dialog(self):
        """Show dialog to load a preset"""
        from PyQt6.QtWidgets import QInputDialog, QMessageBox
        
        presets = get_preset_names(self.NOMBRE)
        if not presets:
            if self.toast:
                self.toast.show_toast("> no hay presets guardados", "error")
            return
        
        preset, ok = QInputDialog.getItem(self, "Cargar Preset", "Seleccione un preset:", presets, 0, False)
        if ok and preset:
            presets_all = load_all_presets()
            datos = presets_all.get(self.NOMBRE, {}).get(preset, {})
            if datos:
                self._set_input_values(datos)
                if self.toast:
                    self.toast.show_toast(f"> preset '{preset}' cargado", "success")

    def build_info_box(self):
        pass
    def build_inputs(self):
        pass
    def build_resultados(self):
        pass
    def calcular(self):
        pass

# ═══════════════════════════════════════════════════════════════════
# PRESET SYSTEM - Save/Load configurations per calculator
# ═══════════════════════════════════════════════════════════════════

PRESETS_FILE = os.path.join(os.path.expanduser("~"), ".calcElec_presets.json")

def save_preset(nombre_calc, preset_name, datos):
    """Save a preset configuration for a calculator"""
    import json
    presets = load_all_presets()
    if nombre_calc not in presets:
        presets[nombre_calc] = {}
    presets[nombre_calc][preset_name] = datos
    with open(PRESETS_FILE, 'w', encoding='utf-8') as f:
        json.dump(presets, f, ensure_ascii=False, indent=2)
    return True

def load_all_presets():
    """Load all presets from file"""
    import json
    if os.path.exists(PRESETS_FILE):
        try:
            with open(PRESETS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def get_preset_names(nombre_calc):
    """Get list of preset names for a calculator"""
    presets = load_all_presets()
    return list(presets.get(nombre_calc, {}).keys())

def delete_preset(nombre_calc, preset_name):
    """Delete a preset"""
    import json
    presets = load_all_presets()
    if nombre_calc in presets and preset_name in presets[nombre_calc]:
        del presets[nombre_calc][preset_name]
        with open(PRESETS_FILE, 'w', encoding='utf-8') as f:
            json.dump(presets, f, ensure_ascii=False, indent=2)
        return True
    return False
