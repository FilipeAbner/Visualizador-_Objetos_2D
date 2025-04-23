import copy
from poligonos import Ponto, Reta, Window, Orientacao
import math

"""
Função que realiza o clipping de uma reta utilizando o algoritmo de Liang-Barsky
Parametros: window (Window), linha (Reta)
"""
def LiangBarskyClipping(window: Window, linha: Reta):
    reta = copy.deepcopy(linha)
    u1 = 0.0
    u2 = 1.0

    deltaX = reta.ponto2.x_norm - reta.ponto1.x_norm
    deltaY = reta.ponto2.y_norm - reta.ponto1.y_norm

    p = [-deltaX, deltaX, -deltaY, deltaY]
    q = [
        reta.ponto1.x_norm - window.XminYmin.x_norm,
        window.XmaxYmin.x_norm - reta.ponto1.x_norm,
        reta.ponto1.y_norm - window.XminYmin.y_norm,
        window.XmaxYmax.y_norm - reta.ponto1.y_norm
    ]

    for i in range(4):
        if math.isclose(p[i], 0):
            if q[i] < 0:  # Linha fora da janela e paralela
                reta.visible = False
                return reta
        else:
            r = q[i] / p[i]
            if p[i] < 0:  # Linha entrando
                u1 = max(u1, r)
            else:  # Linha saindo
                u2 = min(u2, r)

    if u1 > u2:  # Linha completamente fora
        reta.visible = False
        return reta

    # Cálculo dos pontos de intersecção
    Q1 = copy.deepcopy(reta.ponto1)
    Q2 = copy.deepcopy(reta.ponto2)

    # Se a linha está entrando na janela
    if u1 > 0:
        Q1.x_norm = reta.ponto1.x_norm + deltaX * u1
        Q1.y_norm = reta.ponto1.y_norm + deltaY * u1
        Q1.intersecao = True
        Q1.orientacao = Orientacao.ENTRANDO

    # Se a linha está saindo da janela
    if u2 < 1:
        Q2.x_norm = reta.ponto1.x_norm + deltaX * u2
        Q2.y_norm = reta.ponto1.y_norm + deltaY * u2
        Q2.intersecao = True
        Q2.orientacao = Orientacao.SAINDO

    reta.ponto1 = Q1
    reta.ponto2 = Q2
    reta.visible = True
    
    # Evita erros devido a pontos coincidentes da window e do poligono
    epsilon = 0.00000000000001
    if Q1.compare_norm_coordinates(Q2): # Se os pontos de interseção são iguais
        reta.ponto2.x_norm = reta.ponto2.x_norm - epsilon
        reta.ponto2.y_norm = reta.ponto2.y_norm - epsilon
        reta.ponto1.orientacao = Orientacao.NAO_UTILIZADA
         
    return copy.deepcopy(reta)
