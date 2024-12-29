import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def procesar_resultados(datos_respuestas):
    # Definir variables de entrada para cada área vocacional
    areas_vocacionales = set()
    for tipo_test in datos_respuestas.values():
        areas_vocacionales.update(tipo_test.keys())
    
    variables_entrada = {}
    for area in areas_vocacionales:
        variables_entrada[area] = ctrl.Antecedent(np.arange(0, 101, 1), area)
        variables_entrada[area]['bajo'] = fuzz.trimf(variables_entrada[area].universe, [0, 0, 50])
        variables_entrada[area]['medio'] = fuzz.trimf(variables_entrada[area].universe, [0, 50, 100])
        variables_entrada[area]['alto'] = fuzz.trimf(variables_entrada[area].universe, [50, 100, 100])

    # Definir variable de salida
    afinidad = ctrl.Consequent(np.arange(0, 101, 1), 'afinidad')
    afinidad['baja'] = fuzz.trimf(afinidad.universe, [0, 0, 50])
    afinidad['media'] = fuzz.trimf(afinidad.universe, [0, 50, 100])
    afinidad['alta'] = fuzz.trimf(afinidad.universe, [50, 100, 100])

    # Definir reglas
    reglas = []
    for area in areas_vocacionales:
        reglas.append(ctrl.Rule(variables_entrada[area]['alto'], afinidad['alta']))
        reglas.append(ctrl.Rule(variables_entrada[area]['medio'], afinidad['media']))
        reglas.append(ctrl.Rule(variables_entrada[area]['bajo'], afinidad['baja']))

    # Crear sistema de control
    sistema_ctrl = ctrl.ControlSystem(reglas)

    # Crear simulación
    simulacion = ctrl.ControlSystemSimulation(sistema_ctrl)

    # Procesar respuestas
    resultados = {}
    for area in areas_vocacionales:
        puntajes = []
        for tipo_test, areas in datos_respuestas.items():
            if area in areas:
                puntajes.extend(areas[area])
        
        if puntajes:
            puntaje_promedio = sum(puntajes) / len(puntajes)
            simulacion.input[area] = puntaje_promedio
    
    simulacion.compute()
    
    for area in areas_vocacionales:
        resultados[area] = simulacion.output['afinidad']

    return resultados