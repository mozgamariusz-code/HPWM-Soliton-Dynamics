# HPWM: High-Precision Wave Mechanics

![Build Status](https://github.com/MariuszMozga/HPWM/actions/workflows/verify.yml/badge.svg)
![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

**HPWM** (High-Precision Wave Mechanics) to autorskie, nieszewolucyjne środowisko obliczeniowe do badania dynamiki, spektroskopii oraz nieliniowych przejść fazowych w topologicznych solitonach Hopfa ($B=1$). 

Projekt stanowi fundament obliczeniowy dla monografii naukowych analizujących załamanie teorii perturbacyjnej w reżimie ekstremalnego sprzężenia.

## 🔬 Architektura i Możliwości

Oprogramowanie implementuje 5-polowy operator Mozga-Diraca (piony $a, b, c$ oraz skalary $x, y$) i rozwiązuje dynamikę kwazicząstek przy użyciu trzech niezależnych, wzajemnie weryfikujących się filarów numerycznych:
1. **Macierz Rozpraszania S (Jost Determinant):** Całkowanie ODE do strefy asymptotycznej.
2. **Exterior Complex Scaling (ECS FEM):** Nieszewolucyjna metoda rotacji współrzędnych na płaszczyźnie zespolonej do mapowania biegunów rezonansowych.
3. **Deep Space Time-Domain:** Rygorystyczna symulacja pakietów falowych w dziedzinie czasu z wykorzystaniem siatek pochłaniających i schematu Crank-Nicolson.

## 🚀 Kluczowe Odkrycia Fizyczne (Zaimplementowane w testach)
- Weryfikacja rezonansu radialnego $K=0$ z precyzją rzędu $10^{-16}$.
- Udowodnienie opóźnień kinematycznych ($v_g \ll c$) przyprogowych stanów wysokiego spinu ($K=1$).
- Dowód istnienia **niestabilności tachionowej (Vacuum Decay)** dla $\kappa_H > 2.0$.
- Odkrycie topologicznego kolapsu rdzenia solitonu dla sprzężenia $\zeta > 1.2$.
- Żelazna ochrona symetrii parzystości przestrzennej $\mathbb{Z}_2^P$ z zachowaniem wycieków poniżej progu numerycznego ($10^{-26}$).

## ⚙️ Instalacja i Wymagania

Wymagany jest Python w wersji 3.12+ oraz pakiety naukowe.

```bash
git clone https://github.com/TwojLogin/HPWM.git
cd HPWM
python -m venv .venv
source .venv/bin/activate  # (Dla Windows: .venv\Scripts\activate)
pip install -r requirements.txt
```

## 🧪 Niezależny Protokół Weryfikacji (Independent Audit)
Głównym punktem wejścia do kodu jest skrypt automatycznego audytu. Odtwarza on 5-etapowy proces walidacji wszystkich twierdzeń fizycznych zawartych w badaniach.

Aby uruchomić pełen test warunków skrajnych dla modelu, wywołaj:
```bash
python run_independent_verification.py
```
*(lub w strukturze pakietu: `python scripts/run_verification.py`)*

## 👤 Autor
**Mariusz Mozga** – Inżynier, Architekt oprogramowania HPWM.
