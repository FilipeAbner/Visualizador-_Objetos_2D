import copy
from poligonos import Ponto, Reta, Window

"""
Retorna o código da região de um ponto em relação a window
Parametros: ponto (Ponto), window (Window)
Codigos de Regiao:
ACIMA = 8
ABAIXO = 4
DIREITA = 2
ESQUERDA = 1
"""
def RegionCode(ponto, window) -> int:
    c=0 # ponto dentro da window

    if( ponto.y_norm > window.XminYmax.y_norm ):      # ponto ACIMA da window
        c = 8
    elif( ponto.y_norm < window.XminYmin.y_norm ):   # ponto ABAIXO da window
        c = 4
    
    if ( ponto.x_norm > window.XmaxYmin.x_norm ):     # ponto à DIREITA da window
        c += 2
    elif ( ponto.x_norm < window.XminYmin.x_norm ): # ponto à ESQUERDA da window
        c += 1
        
    return c

"""
Função que realiza o clipping de uma reta utilizando o algoritmo de Cohen-Sutherland
"""
def CohenSutherlandClipping(window: Window, r: Reta)-> Reta:

    reta = copy.deepcopy(r)
    done=False
    codA = RegionCode(reta.ponto1, window)
    codB = RegionCode(reta.ponto2, window)
    p = Ponto()

    while not done:
        if ( (codA | codB) == 0 ): # pelo menos um ponto esta dentro da window
            done = True
            reta.visible = True 
        elif ( (codA & codB) != 0 ):
            reta.visible = False  # ambos fora da window
            return copy.deepcopy(reta)
        else:
            # pegar o codigo de um ponto externo à window (A ou B)
            if ( codA != 0):
                codOut = codA
            else:
                codOut = codB
            
            # caso especial: a reta é vertical ou horizontal...
            if ( reta.ponto1.x_norm == reta.ponto2.x_norm ):
                if ( codOut & 0x08 ): 
                    p.y_norm = window.XminYmax.y_norm   # intersecção com o TOPO
                else:
                    p.y_norm = window.XminYmin.y_norm   # intersecção com a BASE
                p.x_norm = reta.ponto1.x_norm
            
            elif ( reta.ponto1.y_norm == reta.ponto2.y_norm ):
                if ( codOut & 0x01 ):
                    p.x_norm = window.XminYmin.x_norm   # intersecção com o lado ESQUERDO
                else:
                    p.x_norm = window.XmaxYmin.x_norm   # intersecção com o lado DIREITO
                p.y_norm = reta.ponto1.y_norm

            # reta com inclinação para dentro da window
            else:
                #Inclinação da reta
                m = float(reta.ponto2.y_norm - reta.ponto1.y_norm)/(reta.ponto2.x_norm - reta.ponto1.x_norm)
                #ponto de intersecção:
                # y_norm = y0 + inclinacao * (x_norm-x0) 
                # x_norm = x0 + ( 1/inclinacao ) * (y_norm-y0)    
                if ( codOut & 0x08 ): # intersecção com o TOPO
                    p.y_norm = window.XminYmax.y_norm
                    p.x_norm = reta.ponto1.x_norm + (window.XminYmax.y_norm - reta.ponto1.y_norm)/m
                elif ( codOut & 0x04 ): #intersecção com a BASE
                    p.y_norm = window.XminYmin.y_norm
                    p.x_norm = reta.ponto1.x_norm + (window.XminYmin.y_norm - reta.ponto1.y_norm)/m
                elif ( codOut & 0x02 ): # intersecçao com o lado DIREITO
                    p.x_norm = window.XmaxYmin.x_norm
                    p.y_norm = reta.ponto1.y_norm + m*(window.XmaxYmin.x_norm - reta.ponto1.x_norm)
                elif ( codOut & 0x01 ): # intersecção com o lado ESQUERDO
                    p.x_norm = window.XminYmin.x_norm
                    p.y_norm = reta.ponto1.y_norm + m*(window.XminYmin.x_norm - reta.ponto1.x_norm)
                
         # atualizar o Ponto da reta AB e seu respectivo "region code"
            if ( codOut == codA ): # o ponto A é que estava fora da window
                reta.ponto1 = p
                codA = RegionCode(reta.ponto1, window)
            else: # o ponto B é que estava fora da window
                reta.ponto2 = p
                codB = RegionCode(reta.ponto2, window)
            
    return copy.deepcopy(reta)
