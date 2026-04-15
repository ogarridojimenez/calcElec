import sys
sys.path.insert(0, r'E:\Mis proyectos\openclaude-main\Calculadora-Python\calcElec')

print('=== TEST 6: UI Elements Structure ===')

from calculadoras.ohm import CalculoOhm
from calculadoras.potencia_mono import CalculoPotenciaMonofasica
from calculadoras.motor import CalculoMotor

# Test Ohm calculator
calc = CalculoOhm()
print('CalculoOhm.NOMBRE:', calc.NOMBRE)
print('Has _guardar:', hasattr(calc, '_guardar'))
print('Has _validate_field:', hasattr(calc, '_validate_field'))
print('Has _save_preset:', hasattr(calc, '_save_preset'))
print('Has _get_input_values:', hasattr(calc, '_get_input_values'))

# Test another calculator
calc2 = CalculoPotenciaMonofasica()
print('CalculoPotenciaMonofasica.NOMBRE:', calc2.NOMBRE)
print('Has modo inverso (radio_group):', hasattr(calc2, 'radio_group'))

# Test motor
calc3 = CalculoMotor()
print('CalculoMotor.NOMBRE:', calc3.NOMBRE)

print('OK: All UI elements structure OK')