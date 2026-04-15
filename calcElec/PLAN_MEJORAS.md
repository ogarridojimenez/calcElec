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
| 1.3 | ✓ Listo | Resultados no se ajustan automáticamente | Ahora se ajustan sin maximizar ventana |
| 1.4 | ✓ Listo | Validación visual inputs | Borde rojo/verde al escribir valores |
| 1.5 | ✓ Listo | Sin tooltips | Agregados hints a campos |

---

## 2. Funcionalidad (Alta prioridad)

| # | Estado | Problema | Mejora |
|---|--------|----------|--------|
| 2.1 | ✓ Listo | Solo PDF para historial | **Agregar Exportar CSV** |
| 2.2 | ✓ Listo | Resultados no exportables | Botón "Exportar" en cada calculadora |
| 2.3 | ✓ Listo | Sin detalles expands en historial | Click en card muestra detalles completos |
| 2.4 | ✓ Listo | Export individual por cálculo | Exportar cálculo actual a PDF/CSV |
| 2.5 | ✓ Listo | Modo inverso | Ya existe en Ohm, Potencia, etc. (radio buttons) |
| 2.6 | ✓ Listo | Presets por proyecto | Botones 💾 preset / 📂 carga |
| 2.7 | ✓ Listo | Calculadora capacitores | Existe en "Factor de Potencia" |

---

## 3. Optimización (Alta prioridad)

| # | Estado | Problema | Mejora |
|---|--------|----------|--------|
| 3.1 | ✓ Listo | Lentitud al iniciar | Cache en fórmulas (lru_cache) |
| 3.2 | ✓ Listo | Sin caché fórmulas | Implementado cache para cálculos |
| 3.3 | ✓ Listo | Animaciones optimizadas | Animaciones ligeras |

---

## 4. Arquitectura (Media prioridad)

| # | Estado | Problema | Mejora |
|---|--------|----------|--------|
| 4.1 | ✓ Listo | Duplicación código | Helpers: add_input_field(), add_field() con tooltip |
| 4.2 | ⚠️ Pendiente | Sin tests | pytest básico |
| 4.3 | ✓ Listo | Sin type hints | Agregados tipos a base.py |
| 4.4 | ✓ Listo | Strings hardcoded | Constantes en constants.py |

---

## 5. Accesibilidad (Media prioridad)

| # | Estado | Problema | Mejora |
|---|--------|----------|--------|
| 5.1 | ✓ Listo | Contraste bajo | Temas mejorados |
| 5.2 | ✓ Listo | Tooltips agregados | En todos los campos |

---

## Prioridades Recomendadas

### Fase 1 (Inmediato - Alto impacto) — ✓ COMPLETADO
1. ✓ ~~Atajos de teclado~~ - Listo
2. ✓ ~~Exportar CSV desde historial~~ - Listo
3. ✓ ~~Exportar resultado individual desde calculadora~~ - Listo
4. ✓ ~~Click para expandir detalles en historial~~ - Listo

### Fase 2 (Corto - Funcionalidad) — ✓ COMPLETADO
5. ✓ ~~Optimización: caché fórmulas~~ - Listo
6. ✓ ~~Tooltips en campos~~ - Listo
7. ✓ ~~Presets por proyecto~~ - Listo

### Fase 3 (Medio - Arquitectura) — ✓ COMPLETADO
8. ✓ ~~Helpers en base class~~ - Listo
9. ✓ ~~Type hints~~ - Listo
10. ✓ ~~Modo inverso en calculadoras~~ - Listo

---

## Referencias

- Norma NC 800 (Cuba)
- IEC 60364-5-52
- NEC