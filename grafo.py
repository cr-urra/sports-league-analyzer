import json
import networkx as nx

# Algoritmo de flujo maximo con multiplicadores
def flow_multiplier_ssp(G):
    # Definicion de variables
    num_edges = len(G.edges)
    potentials = [0] * num_edges
    actual_flows = [0] * num_edges
    residual_cost = [0] * num_edges
    cost = [0] * num_edges
    E = {e: {0} for e in G.edges}       # Set de balances positivos
    D = {e: {0} for e in G.edges}       # Set de balances negativos

# Funcion para crear grafo de basketball
def create_b_graph(nombres, puntos=None, team_z=None):
    # Primero se debe eliminar del conjunto el grupo escogido
    # Y guardar su puntaje, y tambien los partidos por jugar
    z_points = 0
    for x in range(0, len(nombres)):
        if(nombres[x] == team_z):
            z_points = puntos.pop(x)
            break
    
    nombres.remove(team_z)
    matches_left = len(nombres) - 1

    # Se genera el grafo
    G = nx.DiGraph()
    second_layer_exist = False

    for i in range(0, len(nombres)):
        for x in range(i+1, len(nombres)):
            # Primera capa: Nodos de partidos
            match_node_name = nombres[i][0:3] + '\n' + nombres[x][0:3]
            G.add_weighted_edges_from( [('s', match_node_name, matches_left)] )
            
            # Segunda capa: Posibles resultados
            if (second_layer_exist == False):
                for team in nombres:
                    G.add_node(team)
                
                second_layer_exist = True
            
            G.add_weighted_edges_from( [(match_node_name, nombres[i], 1000) ] )
            G.add_weighted_edges_from( [(match_node_name, nombres[x], 1000) ] )
            
        # Cuarta capa: Condicion de victoria
        win_condition_capacity = z_points + matches_left + 1 - puntos[i]
        G.add_weighted_edges_from( [(nombres[i], 't', win_condition_capacity) ] )

    return G

# Funcion para crear grafo de futbol
def create_f_graph(nombres, puntos=None, team_z=None):
    # Primero se debe eliminar del conjunto el grupo escogido
    # Y guardar su puntaje, y tambien los partidos por jugar
    z_points = 0
    matches_left = len(nombres) - 1
    for x in range(0, len(nombres)):
        if(nombres[x] == team_z):
            z_points = puntos.pop(x)
    
    nombres.remove(team_z)
    
    # Se genera el grafo
    G = nx.DiGraph()  
    third_layer_exist = False
    
    for i in range(0, len(nombres)):
        for x in range(i+1, len(nombres)):
            # Primera capa: Nodos de partidos
            match_node_name = nombres[i][0:3] + '\n' + nombres[x][0:3]
            G.add_weighted_edges_from( [('s', match_node_name, 1)] )
            
            # Segunda capa: Posibles resultados
            one_win_node = match_node_name + '\n' + nombres[i] + ' Gana'
            tie_node = match_node_name + '\n' + 'empate'
            two_win_node = match_node_name + '\n' + nombres[x] + ' Gana'
            
            G.add_weighted_edges_from( [(match_node_name, one_win_node, 3) ] )
            G.add_weighted_edges_from( [(match_node_name, tie_node, 2)] )
            G.add_weighted_edges_from( [(match_node_name, two_win_node, 3) ] )
            
            # Tercera capa: Reparticion de puntos
            if (third_layer_exist == False):
                for team in nombres:
                    G.add_node(team)
                
                third_layer_exist = True
            
            G.add_weighted_edges_from( [(one_win_node, nombres[i], 3) ] )
            G.add_weighted_edges_from( [(tie_node, nombres[i], 1) ] )
            G.add_weighted_edges_from( [(tie_node, nombres[x], 1) ] )
            G.add_weighted_edges_from( [(two_win_node, nombres[x], 3) ] )
            
        # Cuarta capa: Condicion de victoria
        win_condition_capacity = z_points + matches_left*3 - puntos[i]
        G.add_weighted_edges_from( [(nombres[i], 't', win_condition_capacity) ] )

    return G

def main():
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
            
            for team in data['teams']:
                fechas.append((team['rmatches'])) 

            print(nombres)
            print("####################")
            print(puntos)    
            print("####################")
            print(fechas)    
            print("####################")

            equipo = input("INGRESE EQUIPO A EVALUAR: ")
            equipo = equipo.upper()

            print(nombres.index(equipo))
            if(puntos[nombres.index(equipo)] + fechas[nombres.index(equipo)]*3 < puntos[0]):
            	print("No se puede salir primero")
            else:
            	print("Si se puede salir primero")
            break

        else:
            print("Entrada Incorrecta, Inténtelo de nuevo")
            tipo = input("Introduzca F para fútbol o B para Básquetbol: ")
            tipo = tipo.lower()

if(__name__ == '__main__'):
    main()
