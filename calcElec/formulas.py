import math
from functools import lru_cache
from constants import *

# Cache simple para resultados de fórmulas (max 128 entries)
@lru_cache(maxsize=128)
def _cached_calcular_ohm(modo, v, i, r):
    """Versión cacheada de calcular_ohm"""
    if modo == "v":
        valor = i * r
        return (valor, "V", "V = I x R")
    elif modo == "i":
        valor = v / r
        return (valor, "A", "I = V / R")
    elif modo == "r":
        valor = v / i
        return (valor, "Ohm", "R = V / I")
    return (0, "V", "")

def calcular_ohm(modo, vals):
    """modo: 'v','i','r' — el que se calcula"""
    try:
        v = float(vals.get("v", 0))
        i = float(vals.get("i", 0))
        r = float(vals.get("r", 0))
        if v > 0 and i > 0 and r > 0:
            result = _cached_calcular_ohm(modo, v, i, r)
            return {"valor": result[0], "unidad": result[1], "formula": result[2]}
    except:
        pass
    
    # Fallback sin cache
    if modo == "v":
        v = vals["i"] * vals["r"]
        return {"valor": v, "unidad": "V", "formula": "V = I x R"}
    if modo == "i":
        i = vals["v"] / vals["r"]
        return {"valor": i, "unidad": "A", "formula": "I = V / R"}
    # r
    r = vals["v"] / vals["i"]
    return {"valor": r, "unidad": "Ohm", "formula": "R = V / I"}

def calcular_potencia_monofasica(modo, vals):
    fp = vals["fp"]
    if modo == "potencia":
        p = vals["voltaje"] * vals["corriente"] * fp
        q = vals["voltaje"] * vals["corriente"] * math.sin(math.acos(fp))
        s = vals["voltaje"] * vals["corriente"]
        return {"valor": p, "unidad": "W", "formula": "P = V × I × cos(φ)", "nota": f"P={p:.2f}W | Q={q:.2f}VAR | S={s:.2f}VA"}
    if modo == "voltaje":
        v = vals["potencia"] / (vals["corriente"] * fp)
        return {"valor": v, "unidad": "V", "formula": "V = P / (I × cos(φ))"}
    # corriente
    i = vals["potencia"] / (vals["voltaje"] * fp)
    return {"valor": i, "unidad": "A", "formula": "I = P / (V × cos(φ))"}

def calcular_potencia_trifasica(modo, vals):
    fp = vals["fp"]
    if modo == "potencia":
        p = math.sqrt(3) * vals["voltajeLinea"] * vals["corriente"] * fp
        return {"valor": p, "unidad": "W", "formula": "P = √3 × VL × I × cos(φ)"}
    if modo == "voltajeLinea":
        vl = vals["potencia"] / (math.sqrt(3) * vals["corriente"] * fp)
        return {"valor": vl, "unidad": "V", "formula": "VL = P / (√3 × I × cos(φ))"}
    # corriente
    i = vals["potencia"] / (math.sqrt(3) * vals["voltajeLinea"] * fp)
    return {"valor": i, "unidad": "A", "formula": "I = P / (√3 × VL × cos(φ))"}

def calcular_factor_potencia(p_kw, fp1, fp2, voltaje=220, f=60):
    phi1 = math.acos(fp1)
    phi2 = math.acos(fp2)
    Qc = p_kw * (math.tan(phi1) - math.tan(phi2))
    C = (Qc * 1000) / (2 * math.pi * f * voltaje ** 2) * 1e6
    return {"valor": Qc, "unidad": "kVAR", "formula": "Qc = P × (tan(φ₁) - tan(φ₂))",
            "nota": f"Qc = {Qc:.3f} kVAR\nC = {C:.2f} μF (a {voltaje}V, {f}Hz)\nφ₁={math.degrees(phi1):.1f}° → φ₂={math.degrees(phi2):.1f}°"}

def calcular_caida_tension(voltaje, corriente, longitud, seccion, material, cosfi, fc=1):
    rho = RHO_CU if material == "cobre" else RHO_AL
    dv = (2 * rho * corriente * longitud) / seccion
    dv_pct = (dv / voltaje) * 100 * fc
    return {"valor": dv_pct, "unidad": "%", "formula": "ΔV% = (2×ρ×I×L×FC)/(S×V)×100",
            "nota": f"ΔV = {dv:.2f}V ({dv_pct:.2f}%)\nFC={fc}\nρ={'Cu' if material=='cobre' else 'Al'}={rho}"}

def calcular_caida_tension_rx(seccion, longitud, corriente, voltaje, cosfi, sistema):
    # Tabla de impedancias Ω/km (NC 800)
    R_TABLE = {1.5:12.10,2.5:7.41,4:4.61,6:3.08,10:1.83,16:1.15,25:0.727,35:0.524,50:0.387,70:0.268,95:0.193,120:0.153,150:0.124,185:0.0991,240:0.0754}
    X_TABLE = {1.5:0.177,2.5:0.166,4:0.157,6:0.149,10:0.143,16:0.138,25:0.127,35:0.119,50:0.119,70:0.114,95:0.110,120:0.107,150:0.107,185:0.106,240:0.100}
    r = R_TABLE.get(seccion, 1.0)
    x = X_TABLE.get(seccion, 0.1)
    sinfi = math.sin(math.acos(cosfi))
    factor = 2 if sistema == "monofasico" else math.sqrt(3)
    dv = (factor / 1000) * longitud * corriente * (r * cosfi + x * sinfi)
    dv_pct = (dv / voltaje) * 100
    return {"valor": round(dv_pct, 3), "unidad": "%", "formula": "ΔV = (factor/1000)×L×I×(R×cosφ+X×sinφ)",
            "nota": f"ΔV={dv:.3f}V | R={r}Ω/km | X={x}Ω/km\nNorma Ref:: NC 800"}

def calcular_seccion_conductor(corriente, material):
    K = K_CU if material == "cobre" else K_AL
    s = corriente / K
    return {"valor": seccion_norm(s), "unidad": "mm²", "formula": f"S = I/K = {corriente}/{K}",
            "nota": f"S calc={s:.3f}mm² → S norm={seccion_norm(s)}mm²"}

def calcular_proteccion(corriente, tipo_carga):
    # NC 801: multiplicadores según tipo de carga
    mult = {"general":1.25, "motores":1.25, "transformador":1.50}[tipo_carga]
    i_adj = corriente * mult
    i_prot = in_norm(i_adj)
    # NC 801: curva C para motores (inductivo), curva B para otros
    curva = "C" if tipo_carga == "motores" else "B"
    return {"valor": i_prot, "unidad": "A", "formula": f"In = {corriente}×{mult} → {i_adj:.2f}A → {i_prot}A normalizado",
            "nota": f"Corriente ajustada: {i_adj:.2f}A\nInterruptor: {i_prot}A Curva {curva}\nNorma NC 801"}

def calcular_puesta_tierra(rho, L, d_mm, n_varillas):
    # NC 802: Fórmula de Dwight
    d = d_mm / 1000.0  # convertir mm a m
    R_una = (rho / (2 * math.pi * L)) * math.log(4 * L / d)
    # Factor de reducción para múltiples varillas
    factor_n = n_varillas if n_varillas <= 3 else n_varillas * 0.9
    R_total = R_una / factor_n
    return {"valor": round(R_total, 2), "unidad": "Ω", "formula": "R = (ρ/2πL)×ln(4L/d) / n",
            "nota": f"R una varilla = {R_una:.2f}Ω\nR total ({n_varillas} varillas) = {R_total:.2f}Ω\n{'✓ CUMPLE NC 802 (≤25Ω)' if R_total<=25 else '✗ NO CUMPLE NC 802 (>25Ω)'}\nNorma Ref:: NC 802"}

def calcular_iluminacion(E, area, eta, fm, flujo_lum=None, largo=None, ancho=None, h=None):
    flujo_total = (E * area) / (eta * fm)
    res = {"flujo_total": flujo_total}
    if flujo_lum:
        N = flujo_total / flujo_lum
        res["N_calc"] = N
        res["N_ceil"] = math.ceil(N)
    if largo and ancho and h:
        k = (largo * ancho) / (h * (largo + ancho))
        res["k"] = k
    return res

def calcular_motor(potencia_kw, vl, eta, fp, tipo_arranque):
    In = potencia_kw * 1000 / (math.sqrt(3) * vl * eta * fp)
    # NC 804 - Factores de arranque
    KIN = {"directo":6, "estrella-triangulo":2.15, "variador":1.25}
    kin = KIN.get(tipo_arranque, 6)
    I_arr = kin * In
    # NC 804: protección = 1.15 x In (diferente a NC 801)
    prot = in_norm(1.15 * In)
    conductor = seccion_norm(In * 1.25 / 4)
    contactor_base = 1.15 * In
    contactor = next((x for x in [9,12,16,18,25,32,38,40,50,63,75,80,95,115,125,150,185,225,265,300,400,500] if x >= contactor_base), 500)
    return {"In": In, "I_arr": I_arr, "prot": prot, "conductor": conductor, "contactor": contactor, "kin": kin}

def calcular_motor_fla(hp, tension):
    from constants import FLA_TABLE
    fla = FLA_TABLE.get(hp, {}).get(tension, 0)
    conductor = seccion_norm(fla * 1.25 / 4)
    itm = in_norm(1.25 * fla)
    return {"fla": fla, "conductor": conductor, "itm": itm}

def calcular_conductor_pe(seccion_fase):
    """NC 802: Conductor PE según sección de fase"""
    if seccion_fase <= 16:
        # S_fase ≤ 16mm² → S_PE = S_fase
        pe = seccion_fase
    elif seccion_fase <= 35:
        # 16 < S_fase ≤ 35mm² → S_PE = 16mm²
        pe = 16
    else:
        # S_fase > 35mm² → S_PE = S_fase/2
        pe = seccion_fase / 2
    return {"valor": pe, "unidad": "mm²", "formula": f"S_PE = {pe}mm² (NC 802)"}

def calcular_cortocircuito(vl, vf, longitud, seccion, material):
    # NC 801: Usar Z total (R + jX)
    rho = RHO_CU if material == "cobre" else RHO_AL
    reactancia = 0.08  # Ω/km (asumido)
    r_total = (rho * longitud * 2) / seccion  # Ω
    z_total = math.sqrt(r_total**2 + reactancia**2)
    Icc_3f = vl / (math.sqrt(3) * z_total) / 1000  # kA
    Icc_1f = vf / (2 * z_total)  # kA
    return {
        "Icc_3f": round(Icc_3f, 2), 
        "Icc_1f": round(Icc_1f, 2),
        "r_total": round(r_total, 4),
        "z_total": round(z_total, 4)
    }

def calcular_demanda_detallada(cargas_array, fp, sistema, tension):
    fd_map = {t["tipo"]: t["fd"] for t in TIPOS_CARGA_DEMANDA}
    D = sum(c["potencia"] * fd_map.get(c["tipo"], 1.0) for c in cargas_array)
    S = D / fp
    if sistema == "trifasico":
        I = S / (math.sqrt(3) * tension)
    else:
        I = S / tension
    return {"D_W": D, "D_kW": D/1000, "S_kVA": S/1000, "I": I}

def calcular_demanda_residencial(p_total_w):
    if p_total_w <= 1500:
        D = p_total_w
    else:
        D = 1500 + 0.4 * (p_total_w - 1500)
    return {"D_W": D, "D_kW": D/1000}

def calcular_ampacidad(seccion, material, metodo, aislamiento, temp, n_circ, disposicion):
    tabla = AMPACIDAD_BASE.get(metodo, {}).get(aislamiento, {})
    Ia = tabla.get(seccion, 0)
    if material == "Aluminio":
        Ia = Ia * 0.78
    is_xlpe = "XLPE" in aislamiento
    ft_table = FT_XLPE if is_xlpe else FT_PVC
    t = min(ft_table.keys(), key=lambda x: abs(x - temp))
    Ft = ft_table[t]
    max_circ = {"Empotrados o encerrados":20}.get(disposicion, 9)
    n = min(n_circ, max_circ)
    n_key = min(FG.keys(), key=lambda x: abs(x - n))
    Fg = FG[n_key]
    Iz = Ia * Ft * Fg
    return {"Ia": Ia, "Ft": Ft, "Fg": Fg, "Iz": round(Iz,1), "formula": f"Iz={Ia}×{Ft}×{Fg}={Iz:.1f}A"}

def calcular_ampacidad_d(seccion, material, aislamiento, temp, resistividad, n_circ):
    tabla = AMPACIDAD_D.get(aislamiento, {})
    Ia = tabla.get(seccion, 0)
    if material == "Aluminio":
        Ia = Ia * 0.78
    t = min(FT_SUELO.keys(), key=lambda x: abs(x - temp))
    Ft = FT_SUELO[t]
    r_key = min(FR_SUELO.keys(), key=lambda x: abs(x - resistividad))
    Fr = FR_SUELO[r_key]
    n = min(n_circ, 6)
    Fg = FG_D.get(n, 0.60)
    Iz = Ia * Ft * Fr * Fg
    return {"Ia": Ia, "Ft": Ft, "Fr": Fr, "Fg": Fg, "Iz": round(Iz,1),
            "formula": f"Iz={Ia}×{Ft}×{Fr}×{Fg}={Iz:.1f}A"}

def calcular_canalizacion(conductores_dict, d_tubo_mm):
    # Áreas reales de conductores (NEC Tabla 5-A)
    AREAS = {1.5:8.11,2.5:13.48,4:20.43,6:28.89,10:51.87,16:81.07,25:126.7,35:166.3,50:229.7,70:352.0,95:483.1,120:616.8}
    # Área interior del tubo
    area_tubo = math.pi * (d_tubo_mm/2)**2
    area_total = sum(AREAS.get(c["seccion"],10) * c["cantidad"] for c in conductores_dict)
    pct = (area_total / area_tubo) * 100
    return {"pct": round(pct,1), "area_total": area_total, "area_tubo": area_tubo,
            "cumple": pct <= 40}

def calcular_conduit(conductores_dict):
    from constants import TABLA_TUBERIAS, AREAS_CONDUCTORES_MM2
    area_total = sum(AREAS_CONDUCTORES_MM2.get(c["seccion"],10) * c["cantidad"] for c in conductores_dict)
    n_total = sum(c["cantidad"] for c in conductores_dict)
    # Factor de llenado según NEC: 1 conductor=0.53, 2=0.31, 3+=0.40
    fl = 0.53 if n_total == 1 else 0.31 if n_total == 2 else 0.40
    # Buscar conduit que cumpla: area_total_mm2 * fl >= area_total
    recomendado = None
    for t in TABLA_TUBERIAS:
        if t["area_total_mm2"] * fl >= area_total:
            recomendado = t
            break
    if not recomendado:
        raise ValueError("Conductores exceden conduit 2\". Dividir en varios tubos.")
    # % ocupación real = (areaTotal / areaTotalConduit) * 100, redondeado a 1 decimal
    ocupacion = round((area_total / recomendado["area_total_mm2"]) * 10) / 10
    return {
        "valor": ocupacion,
        "unidad": "%",
        "formula": "Ocupación = (Área conductores / Área conduit) × 100",
        "nota": f"Área total: {area_total:.1f}mm² | Factor: {int(fl*100)}% | Conduit: {recomendado['nombre']} ({recomendado['area_total_mm2']}mm²)",
        "area_conductores": area_total,
        "n_conductores": n_total,
        "recomendado": recomendado
    }
