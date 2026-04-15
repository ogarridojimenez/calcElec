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
- **Formulas**: `formulas.py` - all calculation logic
- **Constants**: `constants.py` - tables (FLA, ampacidad, conduit areas, resistividades)
- **Theme**: `theme.py` - light/dark QSS styles
- **Export**: `pdf_export.py` - uses `reportlab`
- **History**: `history_manager.py` - saves to `~/.calcElec_history.json`

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
# Run all formula tests
python -c "import formulas; print(formulas.calcular_ohm('v', {'i':10,'r':20}))"

# Test specific calculator
python main.py
```

## Common Issues

1. **Cache corruption**: Delete `__pycache__` and `*.pyc` if import errors
   ```powershell
   Get-ChildItem -Path "calcElec" -Recurse -Filter "__pycache__" -Directory | Remove-Item -Recurse -Force
   ```

2. **Encoding errors**: Use `encoding='utf-8'` when reading/writing JSON files

3. **PDF export**: Requires `reportlab` (`pip install reportlab`)

4. **Table alignment errors**: In pdf_export.py use string alignment ('LEFT', 'CENTER') not TA_ constants

## Reference

- Reference GitHub: https://github.com/ogarridojimenez/calculadora-electrica
- Norma NC 800 (Cuba) for electrical calculations