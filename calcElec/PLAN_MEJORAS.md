# Plan de Mejoras - CalcEléc

## Estado Actual (Actualizado)

Calculadora eléctrica profesional con:
- 18 calculadoras eléctricas (PyQt6)
- Temas claro/oscuro
- Historial con exportación PDF profesional
- Búsqueda de calculadoras
- Normas NC 800, IEC, NEC
- Botón "Limpiar" en cada calculadora
- Botón "Guardar en historial"

---

## 1. UX/UI (Alta prioridad)

| # | Estado | Problema | Mejora |
|---|--------|----------|--------|
| 1.1 | ✓ Listo | Atajos de teclado | Ctrl+B, Ctrl+D, Ctrl+H, Enter funcionan |
| 1.2 | ✓ Listo | Navegación sidebar | Flechas ↑↓ funcionan |
| 1.3 | ⚠️ Pendiente | Resultados no se ajustan automáticamente | Al calcular, los resultados deben appear debajo del botón sin maximizar ventana |
| 1.4 | ⚠️ Pendiente | Validación visual inputs | Borde rojo/verde al escribir valores |
| 1.5 | ✗ Pendiente | Sin tooltips | Agregar hints a campos |

---

## 2. Funcionalidad (Alta prioridad)

| # | Estado | Problema | Mejora |
|---|--------|----------|--------|
| 2.1 | ⚠️ Pendiente | Solo PDF para historial | **Agregar Exportar CSV** (prioridad alta) |
| 2.2 | ✗ Pendiente | Resultados no exportables desde calculadora | Agregar botón "Exportar" en cada calculadora |
| 2.3 | ✗ Pendiente | Sin detalles expands en historial | Click en card muestra detalles completos |
| 2.4 | ✗ Pendiente | Export individual por cálculo | Exportar cálculo actual a PDF/CSV |
| 2.5 | ✗ Pendiente | Modo inverso | calcular V dada P, o P dada I |
| 2.6 | ✗ Pendiente | Presets por proyecto | Guardar/cargar configuraciones |
| 2.7 | ✗ Pendiente | Calculadora capacitores | Banco capacitores para corrección FP |

---

## 3. Optimización (Alta prioridad) - NUEVO

| # | Problema | Mejora |
|---|----------|--------|
| 3.1 | Lentitud al iniciar | Lazy加载 calculadoras (solo importar al seleccionar) |
| 3.2 | Alto uso memoria | Lazy加载 UI, destruir widgets al cambiar de calculadora |
| 3.3 | Sin caché fórmulas | Cachear resultados si inputs no cambian |
| 3.4 | Sin perfilado | Medir tiempo de cálculo para optimizar |
| 3.5 | Animaciones pesadas | Reducir/eliminar animaciones (FadeAnimation, SlideAnimation) |

---

## 4. Arquitectura (Media prioridad)

| # | Estado | Problema | Mejora |
|---|--------|----------|--------|
| 4.1 | ⚠️ Pendiente | Duplicación código | Crear helpers: `add_number_field()`, `add_combo_field()` |
| 4.2 | ✗ Pendiente | Sin tests | **Agregar pytest** para fórmulas |
| 4.3 | ✗ Pendiente | Sin type hints | Agregar tipos a funciones clave |
| 4.4 | ✗ Pendiente | Strings hardcoded | Mover constantes a archivo dedicado |

---

## 5. Accesibilidad (Media prioridad)

| # | Problema | Mejora |
|---|----------|--------|
| 5.1 | Contraste bajo | Mejorar contraste en tema claro para datos críticos |
| 5.2 | Sin atajos por calculadora | `Alt+1`, `Alt+2`, etc. para cada calculadora |

---

## 6. Internacionalización (Baja prioridad)

- Estructura i18n para inglés/portugués (solo si hay demanda)

---

## 7. Nuevas Calculadoras (Opcional)

- Cálculo de transformador
- Coordinación de protecciones
- Cable en bandeja (NEC/NTC)

---

## Prioridades Recomendadas

### Fase 1 (Inmediato - Alto impacto)
1. ✓ ~~Atajos de teclado~~ - Listo
2. Exportar CSV desde historial
3. Exportar resultado individual desde calculadora
4. Click para expandir detalles en historial

### Fase 2 (Corto - Funcionalidad)  
5. Optimización: lazy loading calculadoras
6. Reducir animaciones si es necesario
7. Agregar pytests básicos

### Fase 3 (Medio - Arquitectura)
8. Refactorizar base class con helpers
9. Agregar type hints
10. Modo inverso en calculadoras

---

## Referencias

- Norma NC 800 (Cuba)
- IEC 60364-5-52
- NEC