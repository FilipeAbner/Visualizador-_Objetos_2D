from itertools import cycle
from enum import Enum
from math import atan2
import copy
from copy import deepcopy
import numpy as np

"""
Classe Ponto -> Representa um ponto com coordenadas x e y
Atributos:
    x (float): Coordenada x do ponto
    y (float): Coordenada y do ponto
    x_norm (float): Coordenada x normalizada do ponto
    y_norm (float): Coordenada y normalizada do ponto
    visible (bool): Visibilidade do ponto
    orientacao (Orientacao): Orientação do ponto
    intersecao (bool): Indica se o ponto é uma interseção para o algoritmo de clipping de poligonos
"""
class Ponto:
    def __init__(self, x: float = 0, y: float = 0, orientacao=None, cor='black'):
        self.cor = cor
        self.x = x
        self.y = y
        self.x_norm = x
        self.y_norm = y
        self.visible = True
        self.orientacao = orientacao if orientacao else Orientacao.NAO_UTILIZADA
        self.intersecao = False

    def __str__(self):
        return f"Ponto({self.x_norm},{self.y_norm},{self.orientacao})"

    """
    Normaliza o ponto com base na matriz de normalização
    Parâmetros:
        matriz_normalizada (numpy.ndarray): Matriz de normalização
    """
    def normalizar(self, matriz_normalizada):
        ponto = [[self.x],[self.y], [1]]
        ponto = np.dot(matriz_normalizada, ponto)

        self.x_norm = float(ponto[0,0])
        self.y_norm = float(ponto[1,0])

    def str_normalizado(self):
        return f"PontoNorm({self.x_norm},{self.y_norm})"

    """
    Criterios de igualdade para o ponto:
    - Coordenadas x e y
    - Coordenadas x_norm e y_norm
    - Visibilidade
    """
    def __eq__(self, other):
        if not isinstance(other, Ponto):
            return False
        casas_decimais = 8
        return round(self.x,casas_decimais) == round(other.x,casas_decimais) and\
            round(self.y,casas_decimais) == round(other.y,casas_decimais) and\
            self.visible == other.visible and\
            round(self.x_norm,casas_decimais) == round(other.x_norm,casas_decimais) and\
            round(self.y_norm,casas_decimais) == round(other.y_norm,casas_decimais)

    """
    Comparação de coordenadas normalizadas
    Criterios de igualdade para o ponto normalizado:
    - Coordenadas x_norm e y_norm
    - Visibilidade
    """
    def compare_norm_coordinates(self, other):
        if not isinstance(other, Ponto):
            return False
        casas_decimais = 8
        return round(self.x_norm,casas_decimais) == round(other.x_norm,casas_decimais) and\
            round(self.y_norm,casas_decimais) == round(other.y_norm,casas_decimais) and\
            self.visible == other.visible

"""
Classe Reta -> Representa uma reta com dois pontos
"""
class Reta:
    def __init__(self, ponto1: Ponto, ponto2: Ponto, cor = 'black'):
        self.cor = cor
        self.ponto1 = ponto1
        self.ponto2 = ponto2
        self.visible = True

    """
    Normaliza os pontos da reta com base na matriz de normalização
    """
    def normalizar(self, matriz_normalizada):
        self.ponto1.normalizar(matriz_normalizada)
        self.ponto2.normalizar(matriz_normalizada)

    def __str__(self):
        return f"Reta({self.ponto1}, {self.ponto2})"

"""
Classe Poligono -> Representa um poligono com uma lista de pontos
"""
class Poligono:
    def __init__(self, pontos : list = None, cor='black'):
        self.cor = cor
        self.visible = True
        self.pontos = pontos if pontos is not None else []

    def __str__(self):
        string = f'Poligono com os pontos '
        for i in range(len(self.pontos)):
            string = string + f" {self.pontos[i]} "
        return string

    """
    Normaliza todos os pontos do polígono com base na matriz de normalização
    """
    def normalizar(self, matriz_normalizada):
        for ponto in self.pontos:
            ponto.normalizar(matriz_normalizada)

    # Retorna uma string com os pontos normalizados
    def str_normalizado(self):
        string = f'Poligono com os pontos normalizados '
        for i in range(len(self.pontos)):
            string = string + f" {self.pontos[i].str_normalizado()} "
        return string

    """
    Ordena os pontos do polígono no sentido horário com base no centroide
    Parâmetros:
        centro_poligono (Ponto): Centroide do polígono
    """
    def ordenar_pontos(self, centro_poligono):

        cx = centro_poligono.x_norm
        cy = centro_poligono.y_norm

        self.pontos = sorted(self.pontos, key=lambda ponto: -atan2(ponto.y_norm - cy, ponto.x_norm - cx))

    def __iter__(self):
        return iter(self.pontos)

"""
Classe que representa a window de recorte
"""
class Window:
    def __init__(self, xmin: float, ymin: float, xmax: float, ymax: float):
        self.XminYmin = Ponto(xmin,ymin)
        self.XminYmax = Ponto(xmin,ymax)
        self.XmaxYmax = Ponto(xmax,ymax)
        self.XmaxYmin = Ponto(xmax,ymin)

    def __iter__(self):
        # Retorna um iterador sobre os pontos na ordem desejada
        return iter([self.XminYmin, self.XminYmax, self.XmaxYmax, self.XmaxYmin])

    def __str__(self):
        return (f"Window(XminYmin={self.XminYmin}, XminYmax={self.XminYmax}, "
                f"XmaxYmax={self.XmaxYmax}, XmaxYmin={self.XmaxYmin})")

"""
Classe destinada a definir a Orientacao dos pontos para utilização no algoritmo de clipping de poligonos
Nao utilizada -> (Padrao) Ponto ainda nao foi utilizado pelo algoritmo de clipping
Entrando -> Ponto esta entrando na window
Saindo -> Ponto esta saindo da window
Utilizada -> Ponto ja foi utilizado pelo algoritmo de clipping
"""
class Orientacao(Enum):
    NAO_UTILIZADA = 1
    ENTRANDO = 2
    SAINDO = 3
    UTILIZADA = 4

"""
Classe que define uma lista circular de pontos de um polígono.
"""
class CircularListPoligono:
    class Node:
        def __init__(self, ponto: Ponto):
            self.ponto = ponto
            self.next = None
            self.prev = None

    def __init__(self, poligono: Poligono):
        self.current = None
        self.size = 0
        self.initialize_from_poligono(poligono)

    """
    Cria uma lista circular a partir de um polígono.
    Parâmetros:
        poligono (Poligono): Polígono a ser utilizado
    """
    def initialize_from_poligono(self, poligono: Poligono):
        for ponto in poligono.pontos:
            self.append(ponto)

    """
    Adiciona um novo ponto à lista circular.
    """
    def append(self, ponto: Ponto):
        new_node = self.Node(ponto)
        if not self.current:
            # Primeiro nó da lista
            new_node.next = new_node
            new_node.prev = new_node
            self.current = new_node
        else:
            # Inserção no final
            tail = self.current.prev
            tail.next = new_node
            new_node.prev = tail
            new_node.next = self.current
            self.current.prev = new_node
        self.size += 1

    """
    Move para o próximo ponto na lista circular.
    """
    def move_forward(self):
        if self.current:
            self.current = self.current.next

    """
    Move para o ponto anterior na lista circular.
    """
    def move_backward(self):
        if self.current:
            self.current = self.current.prev

    """
    Retorna o ponto atual da lista circular.
    """
    def get_current(self):
        if self.current:
            return self.current.ponto
        return None

    """
    Permite iterar pelos pontos da lista circular.
    """
    def __iter__(self):
        if not self.current:
            return
        start = self.current
        yield start.ponto
        node = start.next
        while node != start:
            yield node.ponto
            node = node.next

    def __str__(self):
        if not self.current:
            return "[]"
        return "[" + " <-> ".join(map(str, self)) + "]"

"""
Verifica se o ponto está dentro da window através das coordenadas x e y do ponto e da window
Atribui True para visibilidade do ponto se ele estiver dentro da window
Atribui False para visibilidade do ponto se ele estiver fora da window
Parâmetros:
    window (Window): Window de recorte
    ponto (Ponto): Ponto a ser verificado
"""
def PointClipping(window : Window, ponto : Ponto):

    if not((ponto.x_norm <= window.XmaxYmax.x and ponto.x_norm >= window.XminYmax.x) and (ponto.y_norm <= window.XminYmax.y and ponto.y_norm >= window.XminYmin.y)):
        ponto.visible = False
    else:
        ponto.visible = True
    return ponto

"""
Calcul o centroide do polígono (ponto médio)
"""
def calcula_centroide_poligono(poligono : Poligono) -> Ponto:
    c = Ponto()

    c.x_norm = sum(ponto.x_norm for ponto in poligono.pontos) / len(poligono.pontos)
    c.y_norm = sum(ponto.y_norm for ponto in poligono.pontos) / len(poligono.pontos)

    return c

"""
Returna True se o poligono esta totalmente dentro da window
Returna False se o poligono esta totalmente fora da window
incluida margem de erro para evitar pontos coincidentes com a window
"""
def checa_poligono_totalmente_dentro_window(window : Window, poligono : Poligono):
    # Margem de erro para o arredondamento
    epsilon = 0.00000000000001

    for i in range(len(poligono.pontos)):
        p1 = poligono.pontos[i]
        p2 = poligono.pontos[(i + 1) % len(poligono.pontos)]

        if not ((((p1.x_norm + epsilon) >= window.XminYmin.x_norm) and (p1.x_norm <= (window.XmaxYmin.x_norm + epsilon))) and
                (((p2.x_norm + epsilon) >= window.XminYmin.x_norm) and (p2.x_norm <= (window.XmaxYmin.x_norm + epsilon))) and
                (((p1.y_norm + epsilon) >= window.XminYmin.y_norm) and (p1.y_norm <= (window.XminYmax.y_norm + epsilon))) and
                (((p2.y_norm + epsilon) >= window.XminYmin.y_norm) and (p2.y_norm <= (window.XminYmax.y_norm + epsilon)))
        ): #if not DENTRO
            return False

    return True

"""
Calcula as listas de recorte do polígono e da window para serem utilizadas no algoritmo de Weiler-Atherton
Parâmetros:
    window (Window): Window de recorte
    poligono (Poligono): Polígono a ser recortado
Retorna:
    list: Lista com as 2 listas de recorte, respectivamente, do polígono e da window
"""
def calcula_listas_recorte(window : Window, poligono : Poligono) -> list: 
    from algoritmos.reta_liang import LiangBarskyClipping
    pontosIntersecaoPoligono = []

    #lista que se tornara a lista circular dos pontos do poligono
    list1 = Poligono()
    #lista que se tornara a lista circular dos pontos da window
    list2 = Poligono()

    for i in range(len(poligono.pontos)):
        # Ponto atual e próximo ponto (o último conecta ao primeiro)
        ponto1 = Ponto(poligono.pontos[i].x_norm, poligono.pontos[i].y_norm)
        ponto2 = Ponto(poligono.pontos[(i + 1) % len(poligono.pontos)].x_norm,
                   poligono.pontos[(i + 1) % len(poligono.pontos)].y_norm)

        list1.pontos.append(ponto1)

        # Recebe as retas com pontos de interseção ou não
        pontosIntersecaoReta = LiangBarskyClipping(window, Reta(ponto1, ponto2))

        # Checa se houve pontos de interseção
        if pontosIntersecaoReta.ponto1.intersecao:
            list1.pontos.append(pontosIntersecaoReta.ponto1)
            pontosIntersecaoPoligono.append(pontosIntersecaoReta.ponto1)
        if isinstance(pontosIntersecaoReta.ponto2,Ponto) and pontosIntersecaoReta.ponto2.intersecao:
            list1.pontos.append(pontosIntersecaoReta.ponto2)
            pontosIntersecaoPoligono.append(pontosIntersecaoReta.ponto2)

    #Se nao houve intersecao com a window checa se o poligono esta totalmente dentro ou fora da window
    if not pontosIntersecaoPoligono:
        dentro = checa_poligono_totalmente_dentro_window(window,poligono)
        return [dentro]

    # Adiciona os pontos da window na lista 2
    for atr, value in vars(window).items():
        if isinstance(value, Ponto):
            list2.pontos.append(value)

    # Adiciona os pontos de interseção na lista 2
    for point in pontosIntersecaoPoligono:
        list2.pontos.append(point)

    #Ordena os pontos da lista2
    centro_poligono_list2 = calcula_centroide_poligono(list2)
    list2.ordenar_pontos(centro_poligono_list2)

    return [list1,list2]

"""
Busca um ponto de entrada na lista circular de pontos do polígono
Parâmetros:
    circular_list (CircularListPoligono): Lista circular de pontos do polígono
    max_iteracoes (int): Número máximo de iterações
Retorna:
    Ponto: Ponto de entrada
"""
def busca_ponto_entrada(circular_list, max_iteracoes) ->Ponto:

    p = circular_list.get_current()
    iteracoes = 0
    while p.orientacao != Orientacao.ENTRANDO and iteracoes < max_iteracoes:
        iteracoes = iteracoes + 1
        circular_list.move_forward()
        p = circular_list.get_current()

    return p

"""
Itera sobre a lista circular de pontos do polígono ou da window buscando por um ponto com base em suas coordenadas normalizadas e orientação
Parâmetros:
    ponto (Ponto): Ponto a ser buscado
    lista (CircularListPoligono): Lista circular de pontos
Retorna:
    Ponto: Ponto buscado
"""
def busca_ponto_lista(ponto: Ponto, lista : CircularListPoligono):
    ponto_buscado_poligono = lista.get_current()

    while (((ponto.x_norm != ponto_buscado_poligono.x_norm) or
            (ponto.y_norm != ponto_buscado_poligono.y_norm)) or
            ponto.orientacao != ponto_buscado_poligono.orientacao):

        lista.move_forward()
        ponto_buscado_poligono = lista.get_current()

    return ponto_buscado_poligono


"""
Algoritmo de clipping de polígonos de Weiler-Atherton
Permite recortar um polígono com base na window
Parâmetros:
    window (Window): Window de recorte
    poligono (Poligono): Polígono a ser recortado
Retorna:
    Poligono: Polígono recortado
"""
def WeilerAthertonPolygonClipping(window : Window, poligono: Poligono) -> Poligono:
    poligonoRecortado = Poligono()

    listas = calcula_listas_recorte(window,poligono)
    existe_ponto_entrada = True

    if listas and isinstance(listas[0], bool):
        if listas[0] == True:
            return poligono
        else:
            poligonoRecortado.visible = False
            # print("Poligono totalmente recortado")
            return poligonoRecortado

    circular_list_poligono = CircularListPoligono(Poligono(deepcopy(listas[0].pontos)))
    circular_list_window = CircularListPoligono(Poligono(deepcopy(listas[1].pontos)))

    p = busca_ponto_entrada(circular_list_poligono,len(listas[0].pontos))

    while existe_ponto_entrada:
        existe_ponto_entrada = False

        for _ in range(len(listas[0].pontos)):
            point = circular_list_poligono.get_current()
            circular_list_poligono.move_forward()

            if point.orientacao == Orientacao.ENTRANDO:
                existe_ponto_entrada = True

        if not existe_ponto_entrada:
            break

        p = busca_ponto_lista(Ponto(p.x_norm,p.y_norm,Orientacao.ENTRANDO),circular_list_poligono)

        while p.orientacao != Orientacao.SAINDO:
            p.orientacao = Orientacao.UTILIZADA
            poligonoRecortado.pontos.append(p)
            circular_list_poligono.move_forward()
            antigo = p
            p = circular_list_poligono.get_current()


        p = busca_ponto_lista(Ponto(p.x_norm,p.y_norm,Orientacao.SAINDO),circular_list_window)

        while (p.orientacao != Orientacao.ENTRANDO):
            p.orientacao = Orientacao.UTILIZADA
            poligonoRecortado.pontos.append(p)
            circular_list_window.move_forward()
            p = circular_list_window.get_current()

    # Caso limitrofe em que apenas um ponto do poligono esta dentro da window e o mesmo é coincidente com um ponto da window
    # Neste caso o poligono recortado é formado apenas pelo ponto de insersecao
    if not poligonoRecortado.pontos:
        for ponto_intersecao in listas[1].pontos:
            if ponto_intersecao.intersecao:
                ponto_intersecao.visible = True
                poligonoRecortado.pontos.append(ponto_intersecao)
    poligonoRecortado.cor = poligono.cor
    return poligonoRecortado
