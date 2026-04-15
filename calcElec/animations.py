"""
Animation utilities for CalcEléc Professional UI
Provides smooth transitions, fade effects, and animations
"""
from PyQt6.QtCore import (
    QPropertyAnimation, QEasingCurve, QPoint, QSize, 
    QVariantAnimation, QTimer, pyqtSignal
)
from PyQt6.QtWidgets import QWidget, QGraphicsOpacityEffect


class FadeAnimation:
    """Fade in/out animation using opacity"""
    
    @staticmethod
    def fade_in(widget, duration=300):
        """Fade in a widget"""
        opacity = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(opacity)
        opacity.setOpacity(0)
        
        anim = QPropertyAnimation(opacity, b"opacity")
        anim.setDuration(duration)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        anim.start()
        
        # Store animation object to prevent garbage collection
        widget._fade_anim = anim
        anim.finished.connect(lambda: widget.setGraphicsEffect(None))
        
        return anim
    
    @staticmethod
    def fade_out(widget, duration=300):
        """Fade out a widget"""
        opacity = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(opacity)
        opacity.setOpacity(1)
        
        anim = QPropertyAnimation(opacity, b"opacity")
        anim.setDuration(duration)
        anim.setStartValue(1)
        anim.setEndValue(0)
        anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        anim.start()
        
        widget._fade_anim = anim
        return anim


class SlideAnimation:
    """Slide animation for widgets"""
    
    @staticmethod
    def slide_in(widget, direction='left', duration=400):
        """Slide in a widget from a direction"""
        directions = {
            'left': (-20, 0),
            'right': (20, 0),
            'up': (0, -20),
            'down': (0, 20)
        }
        
        offset = directions.get(direction, (-20, 0))
        
        # Start position
        start_pos = widget.pos()
        widget.move(start_pos.x() + offset[0], start_pos.y() + offset[1])
        
        # Fade in
        FadeAnimation.fade_in(widget, duration)
        
        # Slide to final position
        anim = QPropertyAnimation(widget, b"pos")
        anim.setDuration(duration)
        anim.setStartValue(QPoint(start_pos.x() + offset[0], start_pos.y() + offset[1]))
        anim.setEndValue(start_pos)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.start()
        
        widget._slide_anim = anim
        return anim


class ResultFrameAnimation:
    """Specialized animations for result frames"""
    
    @staticmethod
    def show_with_animation(frame):
        """Show result frame with slide + fade animation"""
        frame.show()
        SlideAnimation.slide_in(frame, direction='up', duration=350)
    
    @staticmethod
    def pulse_effect(widget, duration=600):
        """Create a pulse/highlight effect"""
        anim = QPropertyAnimation(widget, b"minimumWidth")
        original_width = widget.width()
        
        anim.setDuration(duration)
        anim.setStartValue(original_width)
        anim.setKeyValueAt(0.3, original_width + 5)
        anim.setEndValue(original_width)
        anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        anim.start()
        
        widget._pulse_anim = anim
        return anim


class LoadingAnimation:
    """Loading/spinner animation for calculations"""
    
    @staticmethod
    def animate_button(btn, duration=800):
        """Animate button during loading state"""
        original_text = btn.text()
        btn.setText("⏳ Calculando...")
        btn.setEnabled(False)
        
        # Store original text for later
        btn._original_text = original_text
        
        return btn
    
    @staticmethod
    def restore_button(btn):
        """Restore button after loading"""
        if hasattr(btn, '_original_text'):
            btn.setText(btn._original_text)
        btn.setEnabled(True)


class HoverEffect:
    """Enhanced hover effects for various widgets"""
    
    @staticmethod
    def apply_hover_effect(widget, effect_type='lift'):
        """Apply hover effect to a widget"""
        if effect_type == 'lift':
            # Subtle lift effect on hover
            widget.installEventFilter(widget)
            widget._hover_effect = effect_type


class TransitionManager:
    """Manage transitions between calculator pages"""
    
    @staticmethod
    def smooth_transition(stack, old_index, new_index, duration=300):
        """Smooth transition between pages in a stack"""
        # Fade out old widget
        old_widget = stack.widget(old_index)
        if old_widget:
            FadeAnimation.fade_out(old_widget, duration // 2)
        
        # Fade in new widget
        new_widget = stack.widget(new_index)
        if new_widget:
            stack.setCurrentIndex(new_index)
            FadeAnimation.fade_in(new_widget, duration)
