import json, os
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QPushButton, QFileDialog, QMessageBox,
    QFrame, QScrollArea, QWidget
)
from PyQt6.QtCore import Qt, QSize
from datetime import datetime

HIST_FILE = os.path.join(os.path.expanduser('~'), '.calcElec_history.json')

class HistoryManager:
    def __init__(self):
        self.entries = []
        self._load()
    def _load(self):
        if os.path.exists(HIST_FILE):
            try:
                with open(HIST_FILE, 'r', encoding='utf-8') as f:
                    self.entries = json.load(f)
            except Exception:
                self.entries = []
    def _save(self):
        with open(HIST_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.entries, f, ensure_ascii=False, indent=2)
    def agregar(self, nombre, datos):
        self.entries.append({
            "nombre": nombre, 
            "datos": datos,
            "fecha": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        self._save()
    def obtener(self):
        return self.entries
    def limpiar(self):
        self.entries = []
        self._save()

class HistoryDialog(QDialog):
    def __init__(self, manager: HistoryManager, dark_mode: bool, parent=None):
        super().__init__(parent)
        self.manager = manager
        self.dark_mode = dark_mode
        self.setWindowTitle("Historial de Cálculos")
        self.setMinimumSize(800, 550)
        
        # Initialize expand tracking
        self.expand_icons = {}
        self._card_frames = {}
        
        self._setup_ui()
        self._populate(manager.obtener())
    
    def _setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        header = QFrame()
        header.setObjectName("header")
        header.setFixedHeight(70)
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(24, 16, 24, 16)
        
        title = QLabel("Historial de Cálculos")
        title.setObjectName("title")
        header_layout.addWidget(title)
        
        subtitle = QLabel(f"{len(self.manager.obtener())} cálculo(s) guardado(s)")
        subtitle.setObjectName("subtitle")
        header_layout.addWidget(subtitle)
        
        main_layout.addWidget(header)
        
        # Content area with cards
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setObjectName("content")
        
        container = QWidget()
        self.content_layout = QVBoxLayout(container)
        self.content_layout.setContentsMargins(24, 16, 24, 16)
        self.content_layout.setSpacing(12)
        
        scroll.setWidget(container)
        main_layout.addWidget(scroll, 1)
        
        # Buttons
        btn_frame = QFrame()
        btn_frame.setObjectName("btn_frame")
        btn_frame.setFixedHeight(70)
        btn_layout = QHBoxLayout(btn_frame)
        btn_layout.setContentsMargins(24, 12, 24, 12)
        
        self.btn_pdf = QPushButton("📄 PDF")
        self.btn_pdf.setObjectName("btn_primary")
        self.btn_pdf.setFixedSize(100, 44)
        self.btn_pdf.clicked.connect(self._export_pdf)
        btn_layout.addWidget(self.btn_pdf)
        
        self.btn_csv = QPushButton("📊 CSV")
        self.btn_csv.setObjectName("btn_csv")
        self.btn_csv.setFixedSize(100, 44)
        self.btn_csv.clicked.connect(self._export_csv)
        btn_layout.addWidget(self.btn_csv)
        
        btn_clear = QPushButton("🗑 Limpiar Todo")
        btn_clear.setObjectName("btn_danger")
        btn_clear.setFixedSize(140, 44)
        btn_clear.clicked.connect(self._clear)
        btn_layout.addWidget(btn_clear)
        
        btn_layout.addStretch()
        
        btn_close = QPushButton("✕ Cerrar")
        btn_close.setObjectName("btn_secondary")
        btn_close.setFixedSize(100, 44)
        btn_close.clicked.connect(self.accept)
        btn_layout.addWidget(btn_close)
        
        main_layout.addWidget(btn_frame)
        
        # Apply theme
        self._apply_theme()
    
    def _apply_theme(self):
        if self.dark_mode:
            self.setStyleSheet("""
                QDialog { background: #0f172a; }
                QFrame#header { background: linear-gradient(135deg, #0891b2 0%, #0e7490 100%); }
                QLabel#title { color: #ffffff; font-size: 20px; font-weight: bold; }
                QLabel#subtitle { color: #bae6fd; font-size: 13px; }
                QFrame#content { background: #0f172a; border: none; }
                QFrame#btn_frame { background: #1e293b; border-top: 1px solid #334155; }
                QPushButton#btn_primary { 
                    background: #0891b2; color: #ffffff; border: none; 
                    border-radius: 8px; font-size: 14px; font-weight: 600; 
                }
                QPushButton#btn_primary:hover { background: #0e7490; }
                QPushButton#btn_danger { 
                    background: transparent; color: #ef4444; border: 1px solid #ef4444; 
                    border-radius: 8px; font-size: 13px; 
                }
                QPushButton#btn_danger:hover { background: #fef2f2; }
                QPushButton#btn_secondary { 
                    background: #334155; color: #cbd5e1; border: none; 
                    border-radius: 8px; font-size: 13px; 
                }
                QPushButton#btn_secondary:hover { background: #475569; }
                QPushButton#btn_csv {
                    background: #059669; color: #ffffff; border: none;
                    border-radius: 8px; font-size: 14px; font-weight: 600;
                }
                QPushButton#btn_csv:hover { background: #047857; }
            """)
        else:
            self.setStyleSheet("""
                QDialog { background: #f8fafc; }
                QFrame#header { background: linear-gradient(135deg, #0891b2 0%, #0e7490 100%); }
                QLabel#title { color: #ffffff; font-size: 20px; font-weight: bold; }
                QLabel#subtitle { color: #bae6fd; font-size: 13px; }
                QFrame#content { background: #f1f5f9; border: none; }
                QFrame#btn_frame { background: #ffffff; border-top: 1px solid #e2e8f0; }
                QPushButton#btn_primary { 
                    background: #0891b2; color: #ffffff; border: none; 
                    border-radius: 8px; font-size: 14px; font-weight: 600; 
                }
                QPushButton#btn_primary:hover { background: #0e7490; }
                QPushButton#btn_danger { 
                    background: transparent; color: #dc2626; border: 1px solid #dc2626; 
                    border-radius: 8px; font-size: 13px; 
                }
                QPushButton#btn_danger:hover { background: #fef2f2; }
                QPushButton#btn_secondary { 
                    background: #e2e8f0; color: #475569; border: none; 
                    border-radius: 8px; font-size: 13px; 
                }
                QPushButton#btn_secondary:hover { background: #cbd5e1; }
                QPushButton#btn_csv {
                    background: #059669; color: #ffffff; border: none;
                    border-radius: 8px; font-size: 14px; font-weight: 600;
                }
                QPushButton#btn_csv:hover { background: #047857; }
            """)
    
    def _create_card(self, index, entry):
        """Create a clickable card for each calculation entry."""
        datos = entry.get('datos', {})
        
        # Main card (clickable header + collapsed preview)
        card = QFrame()
        card.setObjectName("calc_card")
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(6)
        
        # Header row (always visible) - click to expand
        header_row = QHBoxLayout()
        
        idx_label = QLabel(f"#{index + 1}")
        idx_label.setObjectName("idx")
        header_row.addWidget(idx_label)
        
        nombre = QLabel(entry.get('nombre', 'Desconocido'))
        nombre.setObjectName("calc_name")
        header_row.addWidget(nombre, 1)
        
        self.expand_icons = self.expand_icons or {}
        self.expand_icons[index] = QLabel("▶")  # expand icon
        self.expand_icons[index].setObjectName("expand_icon")
        header_row.addWidget(self.expand_icons[index])
        
        fecha = QLabel(entry.get('fecha', ''))
        fecha.setObjectName("fecha")
        header_row.addWidget(fecha)
        
        layout.addLayout(header_row)
        
        # Divider
        divider = QFrame()
        divider.setObjectName("divider")
        divider.setFixedHeight(1)
        layout.addWidget(divider)
        
        # Preview: first 3 key:value pairs (collapsed by default)
        preview_frame = QFrame()
        preview_layout = QVBoxLayout(preview_frame)
        preview_layout.setSpacing(3)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        
        if not datos:
            no_data = QLabel("Sin datos - click para expandir")
            no_data.setObjectName("no_data")
            preview_layout.addWidget(no_data)
        else:
            # Show first 3 items as preview
            items = list(datos.items())[:3]
            for key, value in items:
                row = QHBoxLayout()
                row.setSpacing(6)
                k_label = QLabel(str(key) + ":")
                k_label.setObjectName("field_key")
                k_label.setFixedWidth(100)
                row.addWidget(k_label)
                v_label = QLabel(str(value)[:25])
                v_label.setObjectName("field_value")
                v_label.setWordWrap(True)
                row.addWidget(v_label, 1)
                preview_layout.addLayout(row)
            
            # Show "more" indicator if there are more items
            if len(datos.items()) > 3:
                more = QLabel(f"+{len(datos.items()) - 3} más... (click)")
                more.setObjectName("more_hint")
                preview_layout.addWidget(more)
        
        layout.addWidget(preview_frame)
        
        # Details frame (initially hidden) - expanded view
        details_frame = QFrame()
        details_frame.setObjectName("details_frame")
        details_frame.setVisible(False)  # Initially collapsed
        details_layout = QVBoxLayout(details_frame)
        details_layout.setSpacing(4)
        details_layout.setContentsMargins(0, 8, 0, 0)
        
        # Show all items in detail
        for key, value in datos.items():
            row = QHBoxLayout()
            row.setSpacing(8)
            k_label = QLabel(str(key))
            k_label.setObjectName("field_key")
            k_label.setFixedWidth(120)
            row.addWidget(k_label)
            v_label = QLabel(str(value))
            v_label.setObjectName("field_value")
            v_label.setWordWrap(True)
            row.addWidget(v_label, 1)
            details_layout.addLayout(row)
        
        layout.addWidget(details_frame)
        
        # Make card clickable to toggle expansion
        def toggle_expand():
            is_visible = details_frame.isVisible()
            details_frame.setVisible(not is_visible)
            # Update icon
            self.expand_icons[index].setText("▶" if is_visible else "▼")
            # Update card height
            card.setFixedHeight(180 if not is_visible else 95)  # approximate expanded/collapsed
        
        # Install event filter for click
        card.mousePressEvent = lambda event: toggle_expand()
        
        # Store reference for toggling
        self._card_frames = getattr(self, '_card_frames', {})
        self._card_frames[index] = (details_frame, self.expand_icons[index])
        
        # Card style
        if self.dark_mode:
            card.setStyleSheet("""
                QFrame#calc_card { 
                    background: #1e293b; border-radius: 10px; 
                    border: 1px solid #334155; 
                }
                QFrame#calc_card:hover {
                    border-color: #475569;
                }
                QLabel#idx { color: #64748b; font-size: 12px; font-weight: bold; }
                QLabel#calc_name { color: #22d3ee; font-size: 16px; font-weight: bold; }
                QLabel#expand_icon { color: #94a3b8; font-size: 14px; }
                QLabel#fecha { color: #64748b; font-size: 12px; }
                QFrame#divider { background: #334155; }
                QLabel#field_key { color: #94a3b8; font-size: 11px; font-weight: bold; }
                QLabel#field_value { color: #e2e8f0; font-size: 12px; }
                QLabel#no_data { color: #64748b; font-style: italic; }
                QLabel#more_hint { color: #0891b2; font-size: 11px; font-style: italic; }
            """)
        else:
            card.setStyleSheet("""
                QFrame#calc_card { 
                    background: #ffffff; border-radius: 10px; 
                    border: 1px solid #e2e8f0; 
                }
                QFrame#calc_card:hover {
                    border-color: #0891b2;
                }
                QLabel#idx { color: #94a3b8; font-size: 12px; font-weight: bold; }
                QLabel#calc_name { color: #0891b2; font-size: 16px; font-weight: bold; }
                QLabel#expand_icon { color: #64748b; font-size: 14px; }
                QLabel#fecha { color: #94a3b8; font-size: 12px; }
                QFrame#divider { background: #e2e8f0; }
                QLabel#field_key { color: #64748b; font-size: 11px; font-weight: bold; }
                QLabel#field_value { color: #0f172a; font-size: 12px; }
                QLabel#no_data { color: #94a3b8; font-style: italic; }
                QLabel#more_hint { color: #0891b2; font-size: 11px; font-style: italic; }
            """)
        
        return card
    
    def _populate(self, entries):
        # Clear existing cards
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()
        
        if not entries:
            # Empty state
            empty = QLabel("No hay cálculos guardados.\nGuarda uno desde cualquier calculadora.")
            empty.setObjectName("empty")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            if self.dark_mode:
                empty.setStyleSheet("color: #64748b; font-size: 16px; padding: 40px;")
            else:
                empty.setStyleSheet("color: #94a3b8; font-size: 16px; padding: 40px;")
            self.content_layout.addWidget(empty)
        else:
            # Create cards for each entry
            for i, entry in enumerate(entries):
                card = self._create_card(i, entry)
                self.content_layout.addWidget(card)
            
            # Update subtitle
            self.findChild(QLabel, "subtitle").setText(
                f"{len(entries)} cálculo(s) guardado(s)"
            )
    
    def _export_pdf(self):
        entries = list(self.manager.obtener())
        if not entries:
            QMessageBox.information(self, "Sin datos", "No hay cálculos en el historial.")
            return
        
        reply = QMessageBox.question(
            self, "Exportar PDF",
            f"Se exportarán {len(entries)} cálculo(s) a PDF.\n¿Continuar?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        default_name = f"CalcElec_Historial_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Exportar PDF", default_name, "PDF (*.pdf)"
        )
        if filepath:
            try:
                from pdf_export import export_history_pdf
                export_history_pdf(entries, filepath)
                QMessageBox.information(self, "Éxito", f"PDF exportado:\n{filepath}\n\n¿Desea abrir el PDF?")
                
                # Abrir PDF automáticamente para vista previa
                import os
                respuesta = QMessageBox.question(
                    self, "Abrir PDF", "¿Desea abrir el PDF?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.Yes
                )
                if respuesta == QMessageBox.StandardButton.Yes:
                    os.startfile(filepath)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error:\n{e}")
    
    def _export_csv(self):
        entries = list(self.manager.obtener())
        if not entries:
            QMessageBox.information(self, "Sin datos", "No hay cálculos en el historial.")
            return
        
        reply = QMessageBox.question(
            self, "Exportar CSV",
            f"Se exportarán {len(entries)} cálculo(s) a CSV.\n¿Continuar?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        default_name = f"CalcElec_Historial_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Exportar CSV", default_name, "CSV (*.csv)"
        )
        if filepath:
            try:
                import csv
                with open(filepath, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['#', 'Calculadora', 'Fecha', 'Campo', 'Valor'])
                    
                    for i, entry in enumerate(entries, 1):
                        nombre = entry.get('nombre', '')
                        fecha = entry.get('fecha', '')
                        datos = entry.get('datos', {})
                        
                        if isinstance(datos, dict):
                            for key, value in datos.items():
                                writer.writerow([i, nombre, fecha, key, value])
                        else:
                            writer.writerow([i, nombre, fecha, 'datos', str(datos)])
                    
                QMessageBox.information(self, "Éxito", f"CSV exportado:\n{filepath}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error:\n{e}")
    
    def _clear(self):
        reply = QMessageBox.question(
            self, "Limpiar Historial",
            "¿Eliminar todo el historial?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.manager.limpiar()
            self._populate([])