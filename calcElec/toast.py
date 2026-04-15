from PyQt6.QtWidgets import QLabel, QGraphicsOpacityEffect, QFrame, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt, QEasingCurve, QTimer, QPropertyAnimation, QPoint

class ToastManager:
    def __init__(self, parent):
        self.parent = parent
        self.current_toast = None
        self.toast_timer = None
    
    def show_toast(self, text: str, level: str = "info", duration: int = 2500):
        """Show a toast notification with animations and colors"""
        # Hide existing toast if any
        self._hide_immediate()
        
        # Create new toast
        self.current_toast = QLabel(self.parent)
        self.current_toast.setWordWrap(True)
        self.current_toast.setMaximumWidth(400)
        
        # Style based on level — Panel Técnico
        styles = {
            "success": """
                QLabel {
                    background: #263238;
                    color: #66bb6a;
                    border-radius: 6px;
                    padding: 10px 16px;
                    font-size: 12px;
                    font-family: 'Inter', 'Segoe UI', sans-serif;
                    border: 1px solid rgba(255, 255, 255, 0.12);
                    border-left: 3px solid #66bb6a;
                }
            """,
            "error": """
                QLabel {
                    background: #263238;
                    color: #ef5350;
                    border-radius: 6px;
                    padding: 10px 16px;
                    font-size: 12px;
                    font-family: 'Inter', 'Segoe UI', sans-serif;
                    border: 1px solid rgba(255, 255, 255, 0.12);
                    border-left: 3px solid #ef5350;
                }
            """,
            "warning": """
                QLabel {
                    background: #263238;
                    color: #ffa726;
                    border-radius: 6px;
                    padding: 10px 16px;
                    font-size: 12px;
                    font-family: 'Inter', 'Segoe UI', sans-serif;
                    border: 1px solid rgba(255, 255, 255, 0.12);
                    border-left: 3px solid #ffa726;
                }
            """,
            "info": """
                QLabel {
                    background: #263238;
                    color: #42a5f5;
                    border-radius: 6px;
                    padding: 10px 16px;
                    font-size: 12px;
                    font-family: 'Inter', 'Segoe UI', sans-serif;
                    border: 1px solid rgba(255, 255, 255, 0.12);
                    border-left: 3px solid #42a5f5;
                }
            """
        }
        
        self.current_toast.setStyleSheet(styles.get(level, styles["info"]))
        
        # Prefix text
        prefixes = {
            "success": "OK: ",
            "error": "Error: ",
            "warning": "Atención: ",
            "info": ""
        }
        prefix = prefixes.get(level, "")
        self.current_toast.setText(f"{prefix}{text}")
        self.current_toast.adjustSize()
        
        # Position at bottom center of parent
        parent_rect = self.parent.geometry()
        w, h = self.current_toast.width(), self.current_toast.height()
        x = parent_rect.x() + (parent_rect.width() - w) // 2
        y = parent_rect.y() + parent_rect.height() - h - 40
        self.current_toast.move(x, y + 20)  # Start 20px below
        
        # Set window flags
        self.current_toast.setWindowFlags(
            self.current_toast.windowFlags() | 
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.Tool |
            Qt.WindowType.WindowStaysOnTopHint
        )
        
        # Fade in animation
        self.effect = QGraphicsOpacityEffect(self.current_toast)
        self.current_toast.setGraphicsEffect(self.effect)
        self.effect.setOpacity(0)
        
        # Slide + fade in animation
        self.current_toast.show()
        self.anim_in = QPropertyAnimation(self.effect, b"opacity")
        self.anim_slide = QPropertyAnimation(self.current_toast, b"pos")
        
        self.anim_in.setDuration(300)
        self.anim_in.setStartValue(0)
        self.anim_in.setEndValue(1)
        self.anim_in.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        self.anim_slide.setDuration(300)
        self.anim_slide.setStartValue(QPoint(x, y + 20))
        self.anim_slide.setEndValue(QPoint(x, y))
        self.anim_slide.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        self.anim_in.start()
        self.anim_slide.start()
        
        # Auto-hide timer
        self.toast_timer = QTimer()
        self.toast_timer.setSingleShot(True)
        self.toast_timer.timeout.connect(self._hide_toast)
        self.toast_timer.start(duration)
    
    def _hide_toast(self):
        """Hide toast with fade out animation"""
        if self.current_toast:
            self.anim_out = QPropertyAnimation(self.effect, b"opacity")
            self.anim_out.setDuration(250)
            self.anim_out.setStartValue(1)
            self.anim_out.setEndValue(0)
            self.anim_out.setEasingCurve(QEasingCurve.Type.InCubic)
            self.anim_out.start()
            
            # Delete after animation
            QTimer.singleShot(250, self._hide_immediate)
    
    def _hide_immediate(self):
        """Immediately hide and cleanup toast"""
        if self.current_toast:
            self.current_toast.hide()
            self.current_toast.deleteLater()
            self.current_toast = None
        if self.toast_timer and self.toast_timer.isActive():
            self.toast_timer.stop()
