import numpy as np


def calc_es(t: np.ndarray) -> np.ndarray:
    """
    絶対温度[K]に対応する飽和水蒸気圧[hPa]を求めます
    @param t: 絶対温度 [K]
    @return: 飽和水蒸気圧 [hPa]
    @reference: Bolton, MWR, 1980, EQ.9
    """
    g0 = -2.9912729e3
    g1 = -6.0170128e3
    g2 =  1.887643854e1
    g3 = -2.8354721e-2
    g4 =  1.7838301e-5
    g5 = -8.4150417e-10
    g6 =  4.4412543e-13
    g7 =  2.858487e0

    return np.exp( g0*np.power(t, -2) + \
                   g1*np.power(t, -1) + \
                   g2*np.power(t,  0) + \
                   g3*np.power(t,  1) + \
                   g4*np.power(t,  2) + \
                   g5*np.power(t,  3) + \
                   g6*np.power(t,  4) + \
                   g7*np.log(t) ) / 100.0


def calc_qs(t: np.ndarray, p: np.ndarray) -> np.ndarray:
    """
    絶対温度t[K]と気圧p[hPa]に対応する飽和混合比qs(t,p)[g/kg]を求めます
    @param t: 絶対温度 [K]
    @param p: 気圧[hPa]
    @return qs: 飽和混合比[g/kg]
    @reference: 二宮, 気象がわかる数と式, p.64, EQ.1
    """
    return 0.622*calc_es(t) / (p - calc_es(t))


def calc_theta_es(t: np.ndarray, p: np.ndarray) -> np.ndarray:
    """
    絶対温度t[K]と気圧p[hPa]に対応する飽和相当温位θe*(t,p)[K]を求めます
    @param t: 絶対温度 [K]
    @param p: 気圧[hPa]
    @return θe*: 飽和相当温位[K]
    @reference: 二宮, 気象がわかる数と式, p.109, EQ.1
    """
    p0    = 1000.0  # 基準気圧 [hPa]
    kappa = 0.286   # rd/cpd
    cpd   = 1004.0  # 乾燥空気の定圧比熱 [J/kg/K]
    lv    = 2.50e6  # 蒸発の潜熱 [J/kg]
    return t*np.power(p0/p, kappa) * np.exp((lv/cpd)*(calc_qs(t, p)/t))
