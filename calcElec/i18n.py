"""Módulo de internacionalización para CalcElec"""
import configparser
import os

DEFAULT_LANG = 'es'
LOCALES_DIR = os.path.join(os.path.dirname(__file__), 'locales')

class Translator:
    def __init__(self, lang=None):
        self.lang = lang or DEFAULT_LANG
        self.strings = {}
        self._load_language()
    
    def _load_language(self):
        """Carga el archivo de idioma"""
        lang_file = os.path.join(LOCALES_DIR, f'{self.lang}.ini')
        if not os.path.exists(lang_file):
            lang_file = os.path.join(LOCALES_DIR, f'{DEFAULT_LANG}.ini')
        
        config = configparser.ConfigParser()
        config.read(lang_file, encoding='utf-8')
        
        # Aplanar secciones a diccionario único
        for section in config.sections():
            for key, value in config.items(section):
                self.strings[f'{section}.{key}'] = value
    
    def get(self, key, default=None):
        """Obtiene una cadena traducida"""
        return self.strings.get(key, default or key)
    
    def set_language(self, lang):
        """Cambia el idioma activo"""
        self.lang = lang
        self.strings.clear()
        self._load_language()

# Instancia global
translator = Translator()

def tr(key):
    """Función de traducción rápida"""
    return translator.get(key)
