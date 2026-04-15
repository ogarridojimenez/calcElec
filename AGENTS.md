# CalcElec - Developer Notes

## Quick Start

```bash
cd E:\Mis proyectos\openclaude-main\Calculadora-Python\calcElec
python main.py
```

## Architecture

- **Framework**: PyQt6 (desktop GUI)
- **Entry**: `main.py` → `MainWindow`
- **Calculators**: 18 calculators in `calculadoras/` (inherit from `CalculadoraBase`)
- **Formulas**: `formulas.py` - all calculation logic with caching
- **Constants**: `constants.py` - tables (FLA, ampacidad, conduit areas, resistividades)
- **Theme**: `theme.py` - light/dark QSS styles
- **Export**: `pdf_export.py` - uses `reportlab` for professional PDF
- **History**: `history_manager.py` - saves to `~/.calcElec_history.json`
- **Presets**: `calculadoras/base.py` - save/load configs to `~/.calcElec_presets.json`

## New Features (v2.0)

### Validation Visual
- Inputs show green border when valid, red when invalid
- Real-time validation as user types
- Works for all QLineEdit fields

### Toooltips
- Added tooltips to all form fields
- Helpful hints displayed on hover

### Presets System
- Save current calculator configuration with a name
- Load saved presets from dialog
- Stored in `~/.calcElec_presets.json`

### Export Individual
- Each calculator has "Exportar" button
- Export current calculation to PDF or CSV
- Includes both input values and results

### PDF Professional Design
- Header with CalcElec branding
- INPUTS section (white table)
- RESULTS section (green table)
- Professional styling with ReportLab

### Mode Inverso
- Calculators with multiple modes (Ohm, Potencia) use radio buttons
- Select which value to calculate

## Key Formulas & Norms (matched to GitHub reference)

| Calculator | Key Values |
|------------|-----------|
| Resistividad Cu | 0.0178 Ω·mm²/m (NC 800) |
| Resistividad Al | 0.0282 Ω·mm²/m |
| Motor K_arr DOL | 6 (NC 804) |
| Motor K_arr E-T | 2.15 |
| Motor K_arr VFD | 1.25 |
| Protección motor | 1.15×In (NC 804) |
| Protección general | 1.25×In (NC 801) |
| Conductor PE | S≤16→S, S≤35→16, S>35→S/2 (NC 802) |
| Conduit fill | 1 cond=53%, 2=31%, 3+=40% (NEC 358) |
| Caída tensión | Uses factor FC (1=3%, 1.67=5%) |
| Conductor areas | Real NEC diameters (not internal) |

## Testing

```bash
# Test all imports
python -c "from calculadoras.ohm import CalculoOhm; print(CalculoOhm.NOMBRE)"

# Test formulas
python -c "import formulas; print(formulas.calcular_ohm('v', {'i':10,'r':20}))"

# Test history
python -c "from history_manager import HistoryManager; h = HistoryManager(); print(h.obtener())"

# Test presets
python -c "from calculadoras.base import save_preset, load_all_presets; print(load_all_presets())"

# Test PDF export
python -c "from pdf_export import export_history_pdf; export_history_pdf([], 'test.pdf')"
```

## Common Issues

1. **Cache corruption**: Delete `__pycache__` and `*.pyc` if import errors
   ```powershell
   Get-ChildItem -Path "calcElec" -Recurse -Filter "__pycache__" -Directory | Remove-Item -Recurse -Force
   ```

2. **Encoding errors**: Use `encoding='utf-8'` when reading/writing JSON files

3. **PDF export**: Requires `reportlab` (`pip install reportlab`)

4. **Table alignment errors**: In pdf_export.py use string alignment ('LEFT', 'CENTER') not TA_ constants

## File Structure

```
calcElec/
├── main.py                 # Application entry point
├── formulas.py             # Calculation logic with @lru_cache
├── constants.py            # Electrical tables and constants
├── theme.py                # Light/Dark QSS styles
├── pdf_export.py           # PDF generation with ReportLab
├── history_manager.py      # History dialog with CSV/PDF export
├── toast.py                # Toast notifications
├── animations.py           # UI animations
├── PLAN_MEJORAS.md         # Improvement plan (completed)
├── calculadoras/
│   ├── base.py             # CalculadoraBase with presets, validation
│   ├── ohm.py              # Ley de Ohm
│   ├── potencia_mono.py    # Potencia Monofásica
│   ├── potencia_tri.py     # Potencia Trifásica
│   ├── factor_potencia.py  # Corrección FP (capacitores)
│   ├── motor.py            # Motor Eléctrico
│   ├── motor_fla.py        # Motor por FLA
│   ├── caida_tension.py    # Caída de Tensión
│   ├── caida_tension_avanzada.py
│   ├── seccion_conductor.py
│   ├── iluminacion.py     # Iluminación
│   ├── demanda.py          # Demanda Máxima
│   ├── canalizacion.py    # Canalización
│   ├── ampacidad.py        # Ampacidad (aire)
│   ├── ampacidad_d.py      # Ampacidad (ducto)
│   ├── conduit.py         # Conduit
│   ├── proteccion.py      # Protección
│   ├── puesta_tierra.py   # Puesta a Tierra
│   └── cortocircuito.py   # Cortocircuito
```

## Dependencies

```
PyQt6>=6.0
reportlab>=4.0
pyinstaller>=6.0
```

## Build .exe

```bash
cd calcElec
pip install pyinstaller
pyinstaller main.py --name CalcElec --onefile --windowed --clean
# Output: dist/CalcElec.exe (~46MB)
```

## Reference

- GitHub: https://github.com/ogarridojimenez/calcElec
- Reference: https://github.com/ogarridojimenez/calculadora-electrica
- Norma NC 800 (Cuba) for electrical calculations