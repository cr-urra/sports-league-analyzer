import json


print("¿Qué desea analizar?")
print()
tipo = input("Introduzca F para fútbol o B para Básquetbol: ")

tipo = tipo.lower()

while True:


    if tipo == "f":

        nombres = []
        puntos = []

        with open('futbol.json') as file:
            data = json.load(file)

        for team in data['teams']:
            nombres.append((team['name']))

        for team in data['teams']:
            puntos.append((team['points']))  

        print(nombres)
        print("####################")
        print(puntos)    
        print("####################")

        equipo = input("INGRESE EQUIPO A EVALUAR: ")
        equipo = equipo.upper()

        print(nombres.index(equipo))
        break


    elif tipo == "b":
        nombres = []
        puntos = []

        with open('basquet.json') as file:
            data = json.load(file)

        for team in data['teams']:
            nombres.append((team['name']))

        for team in data['teams']:
            puntos.append((team['points']))  

        print(nombres)
        print("####################")
        print(puntos)    
        print("####################")

        equipo = input("INGRESE EQUIPO A EVALUAR: ")
        equipo = equipo.upper()

        print(nombres.index(equipo))
        break

    else:
        print("Entrada Incorrecta, Inténtelo de nuevo")
        tipo = input("Introduzca F para fútbol o B para Básquetbol: ")
        tipo = tipo.lower()