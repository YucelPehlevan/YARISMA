from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import gc
from concurrent.futures import ThreadPoolExecutor
import random

# Tasarım İçin Oluşturulan Sınıflar
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

# Performans için oluşturulan Sınıflar        
class AICache:
    """AI yanıtları için cache sistemi"""
    def __init__(self, max_size=100):
        self.cache = {}
        self.max_size = max_size
        self.access_count = {}
    
    def get_cache_key(self, user_input, filters):
        """Cache anahtarı oluştur"""
        filters_str = f"{filters.get('urun', '')}-{filters.get('butce', '')}-{filters.get('marka', '')}-{filters.get('kullanim', '')}"
        return f"{user_input.lower().strip()}-{filters_str}"
    
    def get(self, key):
        """Cache'den veri al"""
        if key in self.cache:
            self.access_count[key] = self.access_count.get(key, 0) + 1
            return self.cache[key]
        return None
    
    def set(self, key, value):
        """Cache'e veri ekle"""
        if len(self.cache) >= self.max_size:
            # En az kullanılan öğeyi sil
            least_used = min(self.access_count.items(), key=lambda x: x[1])[0]
            del self.cache[least_used]
            del self.access_count[least_used]
        
        self.cache[key] = value
        self.access_count[key] = 1
    
    def clear(self):
        """Cache'i temizle"""
        self.cache.clear()
        self.access_count.clear()

class MemoryManager:
    """Bellek yönetimi için sınıf"""
    def __init__(self, max_conversation_length=50):
        self.max_conversation_length = max_conversation_length
        self.cleanup_counter = 0
    
    def manage_conversation(self, conversation_history):
        """Konuşma geçmişini yönet"""
        if len(conversation_history) > self.max_conversation_length:
            # Eski mesajları sil, sadece son N tanesini tut
            conversation_history[:] = conversation_history[-self.max_conversation_length:]
        
        self.cleanup_counter += 1
        if self.cleanup_counter % 10 == 0:
            # Her 10 mesajda bir garbage collection çalıştır
            gc.collect()
    
    def cleanup_graphics(self, graphics_windows):
        """Kapalı grafik pencerelerini temizle"""
        return [window for window in graphics_windows if window and hasattr(window, 'isVisible') and window.isVisible()]

class AsyncAIHandler(QObject):
    """Async AI işlemleri için handler"""
    response_ready = pyqtSignal(str, str)  # user_input, ai_response
    error_occurred = pyqtSignal(str)
    
    def __init__(self, api_key, cache_system):
        super().__init__()
        self.api_key = api_key
        self.cache = cache_system
        self.model = None
        self.chat = None
        self.executor = ThreadPoolExecutor(max_workers=2)
    
    def initialize_model(self):
        """Model'i initialize et"""
        if not self.model:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel("models/gemini-2.0-flash")
                if not self.chat:
                    self.chat = self.model.start_chat(history=[])
            except Exception as e:
                self.error_occurred.emit(f"Gemini API hatası: {str(e)}")
                return False
        return True
    
    def send_message_async(self, prompt, user_input, cache_key):
        """Mesajı async olarak gönder"""
        future = self.executor.submit(self._send_message_sync, prompt, user_input, cache_key)
        return future
    
    def _send_message_sync(self, prompt, user_input, cache_key):
        """Senkron mesaj gönderim fonksiyonu"""
        try:
            # Cache kontrolü
            cached_response = self.cache.get(cache_key)
            if cached_response:
                self.response_ready.emit(user_input, cached_response)
                return
            
            if not self.initialize_model():
                return
            
            response = self.chat.send_message(prompt)
            ai_response = response.text
            
            # Cache'e kaydet
            self.cache.set(cache_key, ai_response)
            
            self.response_ready.emit(user_input, ai_response)
            
        except Exception as e:
            self.error_occurred.emit(f"AI yanıt hatası: {str(e)}")

class OptimizedTypingTimer(QObject):
    """Optimize edilmiş typing efekti"""
    character_typed = pyqtSignal(str)
    typing_finished = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self.type_next_char)
        self.typing_text = ""
        self.typing_index = 0
        self.chunk_size = 3  # Her seferinde 3 karakter ekle (performans için)
    
    def start_typing(self, text, speed=10):
        """Typing efektini başlat"""
        self.typing_text = text
        self.typing_index = 0
        self.timer.start(speed)
    
    def type_next_char(self):
        """Sonraki karakterleri ekle"""
        if self.typing_index < len(self.typing_text):
            # Chunk halinde karakterler ekle
            end_index = min(self.typing_index + self.chunk_size, len(self.typing_text))
            current_text = self.typing_text[:end_index]
            self.character_typed.emit(current_text)
            self.typing_index = end_index
        else:
            self.timer.stop()
            self.typing_finished.emit()
    
    def stop_typing(self):
        """Typing efektini durdur"""
        self.timer.stop()        
