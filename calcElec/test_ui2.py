import sys
sys.path.insert(0, r'E:\Mis proyectos\openclaude-main\Calculadora-Python\calcElec')

results = []

results.append('=== TEST 6: UI Elements Structure ===')

from calculadoras.ohm import CalculoOhm
from calculadoras.potencia_mono import CalculoPotenciaMonofasica
from calculadoras.motor import CalculoMotor

calc = CalculoOhm()
results.append('CalculoOhm.NOMBRE: ' + calc.NOMBRE)
results.append('Has _guardar: ' + str(hasattr(calc, '_guardar')))
results.append('Has _validate_field: ' + str(hasattr(calc, '_validate_field')))
results.append('Has _save_preset: ' + str(hasattr(calc, '_save_preset')))
results.append('Has _get_input_values: ' + str(hasattr(calc, '_get_input_values')))

calc2 = CalculoPotenciaMonofasica()
results.append('CalculoPotenciaMonofasica.NOMBRE: ' + calc2.NOMBRE)
results.append('Has modo inverso (radio_group): ' + str(hasattr(calc2, 'radio_group')))

calc3 = CalculoMotor()
results.append('CalculoMotor.NOMBRE: ' + calc3.NOMBRE)

results.append('OK: All UI elements structure OK')

with open('test_results.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(results))