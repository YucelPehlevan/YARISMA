from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import random

class AnimatedChatBackground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_widget = parent
        self.particles = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_particles)
        self.timer.start(50)
        self.init_particles()
        
    def init_particles(self):
        for _ in range(40):
            particle = {
                'x': random.randint(0, 1800),
                'y': random.randint(0, 900),
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(-0.5, 0.5),
                'size': random.randint(1, 4),
                'opacity': random.uniform(0.2, 0.6),
                'color_shift': random.uniform(0, 360)
            }
            self.particles.append(particle)
    
    def update_particles(self):
        for particle in self.particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['color_shift'] += 1
            
            if particle['x'] < 0 or particle['x'] > 1800:
                particle['vx'] *= -1
            if particle['y'] < 0 or particle['y'] > 900:
                particle['vy'] *= -1
                
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Gradient background
        if hasattr(self.parent_widget, 'gece_modu') and self.parent_widget.gece_modu:
            gradient = QLinearGradient(0, 0, self.width(), self.height())
            gradient.setColorAt(0, QColor(15, 23, 42))
            gradient.setColorAt(0.3, QColor(30, 41, 59))
            gradient.setColorAt(0.7, QColor(51, 65, 85))
            gradient.setColorAt(1, QColor(15, 23, 42))
        else:
            gradient = QLinearGradient(0, 0, self.width(), self.height())
            gradient.setColorAt(0, QColor(67, 56, 202))
            gradient.setColorAt(0.3, QColor(79, 70, 229))
            gradient.setColorAt(0.7, QColor(99, 102, 241))
            gradient.setColorAt(1, QColor(67, 56, 202))
            
        painter.fillRect(self.rect(), gradient)
        
        # Draw animated particles
        for particle in self.particles:
            hue = (particle['color_shift'] % 360) / 360.0
            if hasattr(self.parent_widget, 'gece_modu') and self.parent_widget.gece_modu:
                color = QColor.fromHsvF(hue, 0.3, 0.8, particle['opacity'])
            else:
                color = QColor.fromHsvF(hue, 0.5, 1.0, particle['opacity'])
            
            painter.setPen(QPen(color, 1))
            painter.setBrush(QBrush(color))
            painter.drawEllipse(int(particle['x']), int(particle['y']), 
                              particle['size'], particle['size'])
            
class GlassmorphismFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.NoFrame)
        
        # Glow effect
        self.glow_effect = QGraphicsDropShadowEffect()
        self.glow_effect.setBlurRadius(30)
        self.glow_effect.setColor(QColor(99, 102, 241, 100))
        self.glow_effect.setOffset(0, 0)
        self.setGraphicsEffect(self.glow_effect)
        
        # Hover animation
        self.hover_animation = QPropertyAnimation(self, b"geometry")
        self.hover_animation.setDuration(200)
        self.hover_animation.setEasingCurve(QEasingCurve.OutCubic)
        
    def enterEvent(self, event):
        self.glow_effect.setBlurRadius(40)
        self.glow_effect.setColor(QColor(99, 102, 241, 150))
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self.glow_effect.setBlurRadius(30)
        self.glow_effect.setColor(QColor(99, 102, 241, 100))
        super().leaveEvent(event) 

class ModernButton(QPushButton):
    def __init__(self, text, parent=None, style_type="primary"):
        super().__init__(text, parent)
        self.style_type = style_type
        self.setup_effects()
        
    def setup_effects(self):
        # Glow effect
        self.glow_effect = QGraphicsDropShadowEffect()
        self.glow_effect.setBlurRadius(20)
        self.glow_effect.setColor(QColor(99, 102, 241, 80))
        self.glow_effect.setOffset(0, 5)
        self.setGraphicsEffect(self.glow_effect)
        
        # Scale animation
        self.scale_animation = QPropertyAnimation(self, b"geometry")
        self.scale_animation.setDuration(150)
        self.scale_animation.setEasingCurve(QEasingCurve.OutCubic)
        
    def enterEvent(self, event):
        self.glow_effect.setBlurRadius(30)
        self.glow_effect.setColor(QColor(99, 102, 241, 120))
        
        # Slight scale up
        current_rect = self.geometry()
        new_rect = QRect(current_rect.x() - 3, current_rect.y() - 1,
                        current_rect.width() + 6, current_rect.height() + 2)
        
        self.scale_animation.setStartValue(current_rect)
        self.scale_animation.setEndValue(new_rect)
        self.scale_animation.start()
        
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self.glow_effect.setBlurRadius(20)
        self.glow_effect.setColor(QColor(99, 102, 241, 80))
        
        # Scale back
        current_rect = self.geometry()
        new_rect = QRect(current_rect.x() + 3, current_rect.y() + 1,
                        current_rect.width() - 6, current_rect.height() - 2)
        
        self.scale_animation.setStartValue(current_rect)
        self.scale_animation.setEndValue(new_rect)
        self.scale_animation.start()
        
        super().leaveEvent(event) 

class AnimatedBackground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_widget = parent
        self.particles = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_particles)
        self.timer.start(50)  # 20 FPS
        self.init_particles()
        
    def init_particles(self):
        for _ in range(30):
            particle = {
                'x': random.randint(0, 1600),
                'y': random.randint(0, 900),
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(-1, 1),
                'size': random.randint(2, 6),
                'opacity': random.uniform(0.3, 0.8)
            }
            self.particles.append(particle)
    
    def update_particles(self):
        for particle in self.particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            
            if particle['x'] < 0 or particle['x'] > 1600:
                particle['vx'] *= -1
            if particle['y'] < 0 or particle['y'] > 900:
                particle['vy'] *= -1
                
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Gradient background
        if hasattr(self.parent_widget, 'gece_modu') and self.parent_widget.gece_modu:
            gradient = QLinearGradient(0, 0, self.width(), self.height())
            gradient.setColorAt(0, QColor(26, 32, 44))
            gradient.setColorAt(0.5, QColor(45, 55, 72))
            gradient.setColorAt(1, QColor(26, 32, 44))
        else:
            gradient = QLinearGradient(0, 0, self.width(), self.height())
            gradient.setColorAt(0, QColor(79, 172, 254))
            gradient.setColorAt(0.5, QColor(0, 242, 254))
            gradient.setColorAt(1, QColor(79, 172, 254))
            
        painter.fillRect(self.rect(), gradient)
        
        # Draw particles
        for particle in self.particles:
            color = QColor(255, 255, 255, int(particle['opacity'] * 255))
            painter.setPen(QPen(color, 1))
            painter.setBrush(QBrush(color))
            painter.drawEllipse(int(particle['x']), int(particle['y']), 
                              particle['size'], particle['size'])

class GlowButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.glow_effect = QGraphicsDropShadowEffect()
        self.glow_effect.setBlurRadius(20)
        self.glow_effect.setColor(QColor(0, 150, 255, 100))
        self.glow_effect.setOffset(0, 0)
        self.setGraphicsEffect(self.glow_effect)
        
        self.scale_animation = QPropertyAnimation(self, b"geometry")
        self.scale_animation.setDuration(150)
        self.scale_animation.setEasingCurve(QEasingCurve.OutCubic)
        
    def enterEvent(self, event):
        self.glow_effect.setBlurRadius(30)
        self.glow_effect.setColor(QColor(0, 150, 255, 150))
        
        # Scale animation
        current_rect = self.geometry()
        new_rect = QRect(current_rect.x() - 5, current_rect.y() - 2,
                        current_rect.width() + 10, current_rect.height() + 4)
        
        self.scale_animation.setStartValue(current_rect)
        self.scale_animation.setEndValue(new_rect)
        self.scale_animation.start()
        
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self.glow_effect.setBlurRadius(20)
        self.glow_effect.setColor(QColor(0, 150, 255, 100))
        
        # Scale back
        current_rect = self.geometry()
        new_rect = QRect(current_rect.x() + 5, current_rect.y() + 2,
                        current_rect.width() - 10, current_rect.height() - 4)
        
        self.scale_animation.setStartValue(current_rect)
        self.scale_animation.setEndValue(new_rect)
        self.scale_animation.start()
        
        super().leaveEvent(event)

class FloatingCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.NoFrame)
        
        # Drop shadow effect
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(25)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.shadow.setOffset(0, 10)
        self.setGraphicsEffect(self.shadow)
        
        # Float animation
        self.float_animation = QPropertyAnimation(self, b"pos")
        self.float_animation.setDuration(3000)
        self.float_animation.setEasingCurve(QEasingCurve.InOutSine)
        self.float_animation.setLoopCount(-1)  # Infinite loop
        
    def start_floating(self):
        start_pos = self.pos()
        end_pos = QPoint(start_pos.x(), start_pos.y() - 10)
        
        self.float_animation.setStartValue(start_pos)
        self.float_animation.setEndValue(end_pos)
        self.float_animation.start()
