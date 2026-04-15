## Qwen Added Memories
- Proyecto CalcEléc (Calculadora Eléctrica Python + PyQt6) en e:\Mis proyectos\openclaude-main\Calculadora-Python\calcElec\

**Estado actual:**
- 18 calculadoras implementadas y funcionando
- Historial de cálculos con guardado en JSON y exportación a PDF
- Tema claro/oscuro funcional
- Toast notifications funcionando
- Archivos principales: main.py, theme.py, constants.py, formulas.py, history_manager.py, toast.py, pdf_export.py
- Calculadoras en: calculadoras/ (18 archivos .py)

**Bugs conocidos pendientes:**
1. motor_fla.py - Falta resultado contactor; inputs arranque/metodo/temp/circuitos no se usan
2. demanda.py - Método _eliminar_carga buggy
3. ampacidad.py - lbl_max_circ hint nunca se pobla
4. caida_tension.py - Mismatch rho: UI dice 0.0178/0.0282 pero fórmula usa 0.01724/0.02817
5. cortocircuito.py - Icono debería ser rojo pero es cyan
6. canalizacion.py - Al eliminar conductor queda layout huérfano

**Última acción:** Se arregló exportación PDF (error de estilos reportlab). Cache limpiado.
