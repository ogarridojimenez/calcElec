"""
Tests unitarios para formulas.py
Cubre: Ley de Ohm, Potencia, Factor de Potencia, Caída de Tensión
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'calcElec'))

from formulas import (
    calcular_ohm,
    calcular_potencia_monofasica,
    calcular_potencia_trifasica,
    calcular_factor_potencia,
    calcular_caida_tension
)


class TestLeyDeOhm:
    """Tests para Ley de Ohm"""
    
    def test_calcular_voltaje(self):
        """V = I × R"""
        resultado = calcular_ohm('v', {'i': 10, 'r': 22})
        assert resultado['valor'] == 220.0
        assert resultado['unidad'] == 'V'
        assert resultado['formula'] == 'V = I x R'
    
    def test_calcular_corriente(self):
        """I = V / R"""
        resultado = calcular_ohm('i', {'v': 220, 'r': 22})
        assert resultado['valor'] == 10.0
        assert resultado['unidad'] == 'A'
        assert resultado['formula'] == 'I = V / R'
    
    def test_calcular_resistencia(self):
        """R = V / I"""
        resultado = calcular_ohm('r', {'v': 220, 'i': 10})
        assert resultado['valor'] == 22.0
        assert resultado['unidad'] == 'Ohm'
        assert resultado['formula'] == 'R = V / I'


class TestPotenciaMonofasica:
    """Tests para Potencia Monofásica"""
    
    def test_calcular_potencia(self):
        """P = V × I × cos(φ)"""
        resultado = calcular_potencia_monofasica('potencia', {
            'voltaje': 220,
            'corriente': 10,
            'fp': 0.9
        })
        assert abs(resultado['valor'] - 1980.0) < 0.1
        assert resultado['unidad'] == 'W'
    
    def test_calcular_voltaje(self):
        """V = P / (I × cos(φ))"""
        resultado = calcular_potencia_monofasica('voltaje', {
            'potencia': 1980,
            'corriente': 10,
            'fp': 0.9
        })
        assert abs(resultado['valor'] - 220.0) < 0.1
    
    def test_calcular_corriente(self):
        """I = P / (V × cos(φ))"""
        resultado = calcular_potencia_monofasica('corriente', {
            'potencia': 1980,
            'voltaje': 220,
            'fp': 0.9
        })
        assert abs(resultado['valor'] - 10.0) < 0.1


class TestPotenciaTrifasica:
    """Tests para Potencia Trifásica"""
    
    def test_calcular_potencia(self):
        """P = √3 × VL × I × cos(φ)"""
        resultado = calcular_potencia_trifasica('potencia', {
            'voltajeLinea': 380,
            'corriente': 10,
            'fp': 0.9
        })
        esperado = 1.732 * 380 * 10 * 0.9
        assert abs(resultado['valor'] - esperado) < 1.0


class TestFactorPotencia:
    """Tests para Corrección Factor de Potencia"""
    
    def test_calcular_capacitor(self):
        """Qc = P × (tan(φ₁) - tan(φ₂))"""
        resultado = calcular_factor_potencia(100, 0.7, 0.95)
        assert resultado['unidad'] == 'kVAR'
        # Debe ser positivo (mejora FP)
        assert resultado['valor'] > 0


class TestCaidaTension:
    """Tests para Caída de Tensión"""
    
    def test_caida_basica(self):
        """Prueba básica de caída de tensión"""
        resultado = calcular_caida_tension(
            voltaje=220,
            corriente=10,
            longitud=100,
            seccion=4,
            material='Cu',
            cosfi=0.9,
            fc=1
        )
        assert 'valor' in resultado
        assert resultado['valor'] > 0
