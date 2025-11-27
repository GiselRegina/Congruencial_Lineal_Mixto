import streamlit as st
import pandas as pd

class GeneradorCongruencialLineal:
    def __init__(self, a, c, m, x0):
        self.a = a
        self.c = c
        self.m = m
        self.x0 = x0

    def siguiente(self):
        self.x0 = (self.a * self.x0 + self.c) % self.m
        return self.x0

    def uniforme(self):
        return self.siguiente() / self.m

    def series(self, n):
        return [self.uniforme() for _ in range(n)]


def comparacion(gen, n):
    filas = []
    for i in range(1, n + 1):
        entero = gen.siguiente()
        uniforme = entero / gen.m
        filas.append([i, entero, uniforme])
    return pd.DataFrame(filas, columns=["Iteración", "Entero Xn", "Uniforme Un"])


def convergencia(a, c, m, x0, max_iter=500):
    filas = []
    xn = x0
    vistos = {x0: 0}

    for n in range(max_iter):
        axc = a * xn + c
        mod = axc % m
        filas.append([n, xn, axc, mod])

        if n > 0 and mod in vistos:
            ciclo_inicio = vistos[mod]
            ciclo_fin = n + 1
            periodo = ciclo_fin - ciclo_inicio
            df = pd.DataFrame(filas, columns=["n", "X(n)", "aX+c", "(aX+c) mod m"])
            return df, ciclo_inicio, ciclo_fin, periodo

        vistos[mod] = n + 1
        xn = mod

    df = pd.DataFrame(filas, columns=["n", "X(n)", "aX+c", "(aX+c) mod m"])
    return df, None, None, None


# INTERFAZ STREAMLIT
st.title("Generador Congruencial Lineal Mixto (MCL)")
st.write("Autores: José Alejandro, Gisel Regina, Luis Eduardo, Daniel Emilio")

st.sidebar.header("Parámetros del Generador")

a = st.sidebar.number_input("a (multiplicador)", min_value=1, value=37)
c = st.sidebar.number_input("c (constante)", min_value=0, value=3)
m = st.sidebar.number_input("m (módulo)", min_value=2, value=107)
x0 = st.sidebar.number_input("Semilla (X0)", min_value=0, value=2)
n = st.sidebar.number_input("Cantidad de números a generar (n)", min_value=1, value=80)

if st.sidebar.button("Ejecutar Generador"):

    st.subheader("Tabla comparativa: Entero vs Uniforme")
    gen = GeneradorCongruencialLineal(a, c, m, x0)
    df_comp = comparacion(gen, n)
    st.dataframe(df_comp)

    st.subheader("Tabla de convergencia (hasta repetir valor)")
    df_conv, inicio, fin, periodo = convergencia(a, c, m, x0)
    st.dataframe(df_conv)

    if inicio is not None:
        st.success(
            f"Convergencia detectada:\n"
            f"- Primer aparición: iteración {inicio}\n"
            f"- Repetición: iteración {fin}\n"
            f"- ➝ Período del ciclo: **{periodo}**"
        )
    else:
        st.warning("No se encontró ciclo en el número máximo de iteraciones.")
