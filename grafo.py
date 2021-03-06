import json
import networkx as nx
from collections import defaultdict
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt
from networkx.algorithms.flow import maximum_flow
from networkx.algorithms.flow import edmonds_karp

# Funcion para mostrar el grafo mediante matplotlib
def show_graph(G):
    nx.nx_agraph.write_dot(G,'test.dot')
    layout = graphviz_layout(G, prog='dot')
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G,layout,edge_labels=labels)
    nx.draw(G, layout, with_labels=True, arrows=True, font_size=9, node_size=1000)
    plt.rcParams['figure.figsize'] = [10, 10]
    plt.show()

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

def analyze_b_graph(G):
    R = edmonds_karp(G, "s", "t", capacity='weight')
    flow_value = nx.maximum_flow_value(G, "s", "t", capacity='weight')
    print(flow_value == R.graph["flow_value"])

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

#implementaci??n de ford_fulkerson

class Graph:

    def __init__(self, graph):
        self.graph = graph
        self. ROW = len(graph)


    # Using BFS as a searching algorithm 
    def searching_algo_BFS(self, s, t, parent):

        visited = [False] * (self.ROW)
        queue = []

        queue.append(s)
        visited[s] = True

        while queue:

            u = queue.pop(0)

            for ind, val in enumerate(self.graph[u]):
                if visited[ind] == False and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u

        return True if visited[t] else False

    # Applying fordfulkerson algorithm
    def ford_fulkerson(self, source, sink):
        parent = [-1] * (self.ROW)
        max_flow = 0

        while self.searching_algo_BFS(source, sink, parent):

            path_flow = float("Inf")
            s = sink
            while(s != source):
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            # Adding the path flows
            max_flow += path_flow

            # Updating the residual values of edges
            v = sink
            while(v != source):
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

        return max_flow


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
            
            G.add_weighted_edges_from( [(match_node_name, one_win_node, 1) ] )
            G.add_weighted_edges_from( [(match_node_name, tie_node, 1)] )
            G.add_weighted_edges_from( [(match_node_name, two_win_node, 1) ] )
            
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
    print("??Qu?? desea analizar?")
    print()

    tipo = input("Introduzca F para f??tbol o B para B??squetbol: ")
    tipo = tipo.lower()

    while True:

        if tipo == "f":

            nombres = []
            puntos = []
            fechas = []

            with open('futbol.json') as file:
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

            equipo = input("INGRESE EQUIPO A EVALUAR: ")
            equipo = equipo.upper()

            #print(nombres.index(equipo))
            
            if(puntos[nombres.index(equipo)] + fechas[nombres.index(equipo)]*3 < puntos[0]):
            	print("No se puede salir primero")
            else:
            	print("Si se puede salir primero")
            	#llamar funcion ssp aqui
            
            Gf = create_f_graph(nombres, puntos, equipo)
            flow_value, flow_dict = nx.maximum_flow(Gf, "s", "t", capacity='weight')
            print(flow_value)
            #show_graph(Gf)

            break

        elif tipo == "b":
            nombres = []
            puntos = []
            #fechas = []

            with open('basquet.json') as file:
                data = json.load(file)

            for team in data['teams']:
                nombres.append((team['name']))

            for team in data['teams']:
                puntos.append((team['points']))
            
            #for team in data['teams']:
             #   fechas.append((team['rmatches']))

            print(nombres)
            print("####################")
            print(puntos)    
            print("####################")
            #print(fechas)    
            #print("####################")

            equipo = input("INGRESE EQUIPO A EVALUAR: ")
            equipo = equipo.upper()
            
            if(puntos[nombres.index(equipo)] + len(nombres)*2 < puntos[0]):
            	print("No se puede salir primero")
            else:
                Gb = create_b_graph(nombres, puntos, equipo)
             
                if(analyze_b_graph(Gb) == True):
            	    print("Si se puede salir primero")
            	    #llamar ford fulkerson aca

            
            #show_graph(Gb)

            break

        else:
            print("Entrada Incorrecta, Int??ntelo de nuevo")
            tipo = input("Introduzca F para f??tbol o B para B??squetbol: ")
            tipo = tipo.lower()

if(__name__ == '__main__'):
    main()
