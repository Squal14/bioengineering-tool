import numpy as np
from scipy.integrate import solve_ivp

def monod_kinetics(t, y, mu_max, Ks, Yxs):
    """Define el sistema de ecuaciones diferenciales para el modelo de monod"""
    X, S = y #DEsempaquetamos los valores acutales de biomasa y sustrato

    #Ecuación de Monod para la tasa específica de crecimiento
    mu = mu_max*(S/(Ks+S))

    #Balances de materia
    dXdt = mu*X
    dSdt = -(1/Yxs)*dXdt

    return [dXdt, dSdt]

def resolver_biorreactor(datos_ui, t_final=5.0):
    """toma el diccionario de la UI y resuelve la cinética en el tiempo"""

    #Extraemos los datos que envió la interfaz.
    X0 = datos_ui["X0"]
    S0 = datos_ui["S0"]
    mu_max = datos_ui["mu_max"]
    Ks = datos_ui["Ks"]

    #Asumimos un rendimiento fijo por ahora
    Yxs = 0.5
    
    #Vector de condiciones iniciales
    y0 = [X0, S0]

    #Rango de tiempo a simular (de 0 al t_final)
    t_span = (0, t_final)

    #Le pedimos a SciPy que nos devuelva 500 puntos para que la gráfica salga muy suave.
    t_eval = np.linspace(0, t_final, 500)

    #Resolvemos el sistema
    solucion = solve_ivp(
        fun=monod_kinetics,
        t_span=t_span,
        y0=y0,
        args=(mu_max, Ks, Yxs),
        t_eval=t_eval,
        method='RK45' #Método de Runge-Kutta de 4to/5to orden.
    )

    #Retornamos los arreglos de tiempo, biomasa y sustrato
    return solucion.t, solucion.y[0], solucion.y[1]
