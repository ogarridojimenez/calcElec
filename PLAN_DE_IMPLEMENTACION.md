# Plan de Mejoras CalcElec - Fases de Implementación

## Fase 1: Corrección Crítica y Tests (Semana 1)
**Objetivo:** Estabilidad y prevención de regresiones

### 1.1 Corregir Bug Cache Ley de Ohm
- **Archivo:** `formulas.py` línea 13
- **Problema:** `val = r / i` debería ser `val = v / r`
- **Impacto:** Cálculo incorrecto de corriente
- **Tiempo estimado:** 15 min

### 1.2 Crear Suite de Tests con pytest
- **Estructura:**
  ```
  tests/
  ├── __init__.py
  ├── test_formulas.py       # Tests unitarios fórmulas
  ├── test_calculadoras.py   # Tests UI básica
  └── conftest.py            # Fixtures compartidos
  ```
- **Cobertura objetivo:** 70% mínimo
- **Tests críticos:**
  - Ley de Ohm (V, I, R)
  - Potencia monofásica/trifásica
  - Caída de tensión
  - Factor de potencia
- **Tiempo estimado:** 4-6 horas

### 1.3 Agregar Logging Profesional
- **Reemplazar prints** por módulo `logging`
- **Configuración:**
  ```python
  logging.basicConfig(
      level=logging.INFO,
      format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
      handlers=[
          logging.FileHandler('calcelec.log'),
          logging.StreamHandler()
      ]
  )
  ```
- **Logs en:**
  - Inicio de app
  - Cálculos completados
  - Errores de validación
  - Exportaciones PDF/CSV
- **Tiempo estimado:** 2 horas

---

## Fase 2: Robustez y UX (Semana 2)
**Objetivo:** Mejorar experiencia de usuario y manejo de errores

### 2.1 Manejo de Errores en PDF Export
- **Validar ReportLab instalado** antes de exportar
- **Mensaje amigable** si falta dependencia
- **Log de errores** con stack trace
- **Tiempo estimado:** 1 hora

### 2.2 Internacionalización (i18n)
- **Estructura:**
  ```
  locales/
  ├── es/LC_MESSAGES/messages.po
  └── en/LC_MESSAGES/messages.po
  ```
- **Herramienta:** gettext o QTranslator
- **Textos a traducir:**
  - Labels de UI
  - Mensajes de error
  - Tooltips
  - Nombres de calculadoras
- **Tiempo estimado:** 3-4 horas

### 2.3 Validación Avanzada de Inputs
- **Rangos válidos** por campo (ej: FP entre 0-1)
- **Feedback visual inmediato** (ya implementado, extender)
- **Mensajes de error específicos** por campo
- **Tiempo estimado:** 2 horas

---

## Fase 3: Arquitectura y Escalabilidad (Semana 3)
**Objetivo:** Preparar para crecimiento futuro

### 3.1 Sistema de Plugins para Calculadoras
- **Carga dinámica** desde directorio `calculadoras/`
- **Decorador `@register_calculator`** para auto-registro
- **Eliminar imports hardcodeados** en main.py
- **Ejemplo:**
  ```python
  # calculadoras/__init__.py
  from importlib import import_module
  
  def load_all_calculators():
      calculators = []
      for filename in os.listdir('calculadoras'):
          if filename.endswith('.py') and filename != 'base.py':
              module = import_module(f'calculadoras.{filename[:-3]}')
              calculators.append(module.CalculatorClass)
      return calculators
  ```
- **Tiempo estimado:** 4 horas

### 3.2 Migrar a SQLite
- **Reemplazar JSON** por SQLite para:
  - Historial (`~/.calcElec_history.json`)
  - Presets (`~/.calcElec_presets.json`)
- **Ventajas:**
  - Consultas eficientes
  - Backup automático
  - Integridad de datos
- **Esquema:**
  ```sql
  CREATE TABLE history (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      calculator TEXT,
      timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
      inputs TEXT,  -- JSON
      results TEXT  -- JSON
  );
  
  CREATE TABLE presets (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      calculator TEXT,
      name TEXT,
      data TEXT,  -- JSON
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );
  ```
- **Tiempo estimado:** 5-6 horas

### 3.3 Base de Datos de Constantes
- **Externalizar tablas** a archivo YAML/JSON
- **Cargar dinámicamente** en runtime
- **Facilitar actualización** de normas NC/NEC
- **Tiempo estimado:** 2 horas

---

## Fase 4: Documentación y CI/CD (Semana 4)
**Objetivo:** Profesionalizar proyecto para distribución

### 4.1 Documentación Técnica con Sphinx
- **Estructura:**
  ```
  docs/
  ├── index.rst
  ├── installation.rst
  ├── usage.rst
  ├── api_reference.rst
  └── contributing.rst
  ```
- **Generar automáticamente** desde docstrings
- **Publicar en ReadTheDocs**
- **Tiempo estimado:** 4 horas

### 4.2 CI/CD con GitHub Actions
- **Workflow:**
  ```yaml
  name: Tests & Build
  on: [push, pull_request]
  jobs:
    test:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - run: pip install pytest
        - run: pytest tests/
    build:
      needs: test
      runs-on: windows-latest
      steps:
        - run: pyinstaller main.py --onefile --windowed
        - upload: dist/CalcElec.exe
  ```
- **Build automático** del .exe en releases
- **Tiempo estimado:** 3 horas

### 4.3 Code Quality Tools
- **Agregar:**
  - `black` para formateo automático
  - `flake8` para linting
  - `mypy` para type checking estricto
- **Pre-commit hooks** para validar antes de commit
- **Tiempo estimado:** 2 horas

---

## Fase 5: Features Opcionales (Post-v2.0)
**Objetivo:** Expandir funcionalidad

### 5.1 Nuevas Calculadoras
- Cálculo de transformadores
- Coordinación de protecciones
- Cable en bandeja (NEC 392)
- Análisis de armónicos
- **Tiempo estimado:** 2-3 horas cada una

### 5.2 Gráficos Interactivos
- **Matplotlib integrado** para:
  - Curva de caída de tensión vs longitud
  - Diagrama fasorial de potencia
  - Curvas de disparo de protecciones
- **Tiempo estimado:** 6-8 horas

### 5.3 Modo Proyecto
- **Guardar múltiples cálculos** relacionados
- **Exportar reporte completo** de proyecto
- **Incluir diagramas unifilares** básicos
- **Tiempo estimado:** 8-10 horas

### 5.4 Actualización Automática
- **Check de versión** en GitHub al iniciar
- **Descargar nueva versión** automáticamente
- **Backup de configuración** antes de actualizar
- **Tiempo estimado:** 4 horas

---

## Cronograma Estimado

| Fase | Duración | Dependencias |
|------|----------|--------------|
| Fase 1 | 1 semana | Ninguna |
| Fase 2 | 1 semana | Fase 1 |
| Fase 3 | 1 semana | Fase 2 |
| Fase 4 | 1 semana | Fase 3 |
| Fase 5 | Opcional | Fase 4 |

**Total estimado:** 4 semanas para versión profesional completa

---

## Métricas de Éxito

- ✅ **Tests:** >70% cobertura
- ✅ **Bug-free:** 0 bugs críticos en release
- ✅ **UX:** <3 clicks para cálculo típico
- ✅ **Performance:** <2s inicio de app
- ✅ **Docs:** 100% funciones documentadas

---

## Próximos Pasos Inmediatos

1. **Corregir bug cache Ohm** (15 min)
2. **Crear estructura tests/** (30 min)
3. **Escribir tests para Ley de Ohm** (1 hora)
4. **Commit y push** de cambios

¿Comenzamos con la Fase 1?