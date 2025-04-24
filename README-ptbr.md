# 🧭 Visualizador Interativo de Objetos 2D com Transformações, Clipping e Viewport

Este projeto é uma ferramenta gráfica interativa desenvolvida em Python, que permite visualizar, transformar e recortar objetos geométricos 2D em um sistema de coordenadas baseado em window e viewport. O sistema simula etapas importantes de um pipeline gráfico 2D, como transformação de coordenadas, recorte (clipping) e visualização.

## 🎯 Objetivo

O projeto visa oferecer um ambiente gráfico funcional para manipulação e exibição de objetos 2D com foco nos seguintes pontos:

- Transformação de coordenadas do sistema mundial para o sistema de viewport.
- Interação com a cena através da movimentação, rotação e escala da window.
- Aplicação de algoritmos clássicos de clipping para exibir apenas os objetos visíveis na viewport.

## 🛠️ Funcionalidades

### Parte 1
- 📂 Leitura de arquivos XML contendo objetos (pontos, retas e polígonos), window e viewport.
- 🖼️ Exibição gráfica dos objetos com `tkinter` utilizando canvas.
- 🎮 Movimentação da window com teclas direcionais.
- 🔁 Recalculo automático das coordenadas dos objetos na viewport.
- 💾 Exportação de arquivo XML com coordenadas transformadas.
- 🗺️ Minimapa para melhor percepção da posição da window.

### Parte 2
- ➕ Botões para movimentar, rotacionar e redimensionar a window.
- 🔄 Transformações da window em torno do centro: translação, rotação e escala.
- 🎯 Transformação para o Sistema de Coordenadas Normalizado (NCS).
- ✂️ Clipping de:
  - Pontos
  - Retas: Algoritmos de **Cohen-Sutherland** e **Liang-Barsky**
  - Polígonos: Algoritmo de **Weiler-Atherton**
- ✅ Apenas objetos visíveis após o clipping são renderizados.
- 🎨 Suporte a cores customizadas via atributo `cor` no XML.

## 📦 Estrutura dos Arquivos XML

O sistema utiliza arquivos XML com a seguinte estrutura:
- `Window` e `Viewport`: Definidas por suas extremidades.
- Objetos:
  - `Ponto2D`: Coordenadas (x, y)
  - `Reta2D`: Dois pontos distintos
  - `Polígono2D`: Lista de pontos conectados
- Saída contém também coordenadas transformadas para viewport.

## 📚 Tecnologias Utilizadas

- `Python 3`
- `tkinter` — interface gráfica
- `xml.etree.ElementTree` — leitura e escrita XML
- `numpy` — operações matemáticas
- Algoritmos de clipping clássicos implementados do zero

## 📸 Interface

A interface gráfica é composta por:
- Área principal de desenho (viewport)
- Minimapa com a visão geral do mundo
- Controles:
  - Teclas direcionais para mover a window
  - Botões para ampliar, reduzir e rotacionar a window
  - Caixa de seleção para escolher algoritmo de clipping de retas

## Dependencias
### Ubuntu/Debian
```sudo apt install python3-tk```

### Python
```pip install numpy ```<br> 
```pip install ipykernel```

## Utilizando
- Execute o arquivo ```interface.ipynb```


## Relatório

### 📌 Introdução

- O primeiro conceito relevante a ser abordado é a **viewport**, que é o espaço na tela do dispositivo onde as figuras serão desenhadas pelo programa. Associado a ela, existe também a **window**, que é o recorte do mundo que será desenhado na viewport. Apesar de ambas poderem ter tamanhos e proporções diferentes, é importante manter a proporção entre elas para evitar distorções na renderização.

- Para trazer as imagens da window para a viewport, não é recomendado que a
conversão das coordenadas seja feita de 1
para 1, pois a viewport pode ter diversos tamanhos, considerando que por exemplo,
dispositivos com tamanhos de tela diferentes sejam utilizados. Por isso é necessária a **transformada de viewport** que é um cálculo aplicado a todos os pontos para convertê-los das coordenadas da window para as coordenadas da viewport, ajustando automaticamente para dispositivos com diferentes tamanhos de tela.

A **window** pode sofrer três tipos principais de transformações:

- **Translação**: move a window pelos eixos x e y.
- **Rotação**: gira a window em seu próprio eixo.
- **Escala**: permite o zoom in e zoom out.

- Além disso, os pontos são normalizados para um **plano de coordenadas normalizado** (entre -1 e 1), o que facilita as transformações e a aplicação de algoritmos como o clipping, além de manter as coordenadas da window ao centro do mundo e fazendo o mesmo com as figuras para que a proporção seja mantida.

- A cada movimentacção feita à window,todos os cálculos desejados relacionados à renderização são aplicadas a todos os pontos do mundo, mesmo
que esses pontos não estejam dentro da window, o que gera uma grande quantidade de
cálculos desnecessários realizados pela GPU, para evitar isso, foram criados os algoritmos
de clipping. O **clipping** é aplicado para evitar que pontos fora da window passem pela transformada de viewport, otimizando o desempenho ao eliminar cálculos desnecessários.

### 🛠️ Implementação

A implementação foi realizada em Jupyter Notebooks. A maior parte do código está encapsulada na classe `Visualizacao`, com funcionalidades adicionais em arquivos externos.

#### Representações:
- **Window, viewport e NCS(Coordenadas Normalizadas)**: dicionários com `xmin`, `xmax`, `ymin`, `ymax`.
- **Formas geométricas (Ponto, Reta, Polígono)**: implementadas como classes.

#### Interface:
- A interface possui botões para realizar translações, rotações e escalas. A cada ação:

1. Os pontos são normalizados para o NCS.
2. Os algoritmos de clipping são aplicados.
3. A transformada de viewport é usada para converter as coordenadas.
4. As figuras são renderizadas no `tkinter`.

- Um detalhe da implementação é que a matriz de transformação para o plano de
coordenadas normalizado é aplicado aos pontos da window apenas uma única vez durante
uma execução. Após isso ela é aplicada apenas aos pontos do mundo para que eles sejam
colocados de forma correta junto à window.

### ✂️ Clipping

O notebook principal (`interface.ipynb`) utiliza os arquivos auxiliares:
- `poligonos.py`: clipping de polígonos e definição das formas geométricas.
- `reta_liang.py`: clipping de retas via Liang-Barsky.
- `reta_cohen.py`: clipping de retas via Cohen-Sutherland.

### 🧮 Algoritmos de Clipping

#### 🔹 Cohen-Sutherland

- Usa **códigos regionais (region codes)** de 4 bits para indicar se um ponto está acima, abaixo, à esquerda ou à direita da window.
- Três casos:
  1. Totalmente visível (ambos os códigos = `0000`)
  2. Totalmente invisível (AND dos códigos ≠ `0000`)
  3. Parcialmente visível (AND = `0000`, mas algum código ≠ `0000`)

Se a linha precisar de recorte, buscamos o ponto de interseção da linha com a borda
da janela correspondente, substituímos o ponto fora da janela pelo ponto de interseção e
então repetimos o processo até que a linha esteja completamente dentro ou fora da janela.
Após o recorte, a linha resultante (se visível) será desenhada.

> Realiza interseções iterativamente até determinar visibilidade da reta.

#### 🔹 Liang-Barsky
- O algoritmo de Liang-Barsky utiliza **equações paramétricas** para detectar interseções, sendo uma técnica eficiente para detectar colisões ou
realizar recortes de segmentos de reta em relação a uma região retangular (janela de
recorte). Ele é uma melhoria sobre o algoritmo de Cohen-Sutherland, pois evita a
necessidade de calcular interseções para todas as arestas da janela, utilizando diretamente
as equações paramétricas da linha.
- Dessa forma, o algoritmo detecta as intersecções e então retorna a reta com os
pontos dentro da window, se assim houver.

#### 🔹 Weiler-Atherton

- O algoritmo começa identificando todos os pontos de interseção entre as arestas do
polígono e as arestas da janela (window). Durante este processo:
  - Cada ponto de interseção é marcado com uma orientação, indicando se é um ponto
de entrada (quando a aresta do polígono entra na janela) ou um ponto de saída
(quando a aresta do polígono sai da janela).
- Após determinar os pontos de interseção, o algoritmo constrói duas listas circulares que
organizam esses pontos:
  - Lista do Polígono: Contém todos os vértices originais do polígono,
complementados pelos pontos de interseção identificados. Esses pontos são
inseridos na ordem em que aparecem ao longo do polígono, preservando o sentido
horário.
  - Lista da Janela (Window): Contém os vértices da janela de recorte, também
complementados pelos pontos de interseção, ordenados no sentido horário.
Ambas as listas preservam a topologia original das formas, incluindo os pontos de
interseção.
-Com as listas circulares prontas, o algoritmo inicia o processo de construção do
polígono resultante, representando a porção do polígono que está contida na janela. O
processo é iterativo e segue os seguintes passos:

  **1. Busca por Pontos de Entrada: O algoritmo começa na lista do polígono, procurando o próximo ponto de entrada. <br>**
**2. Ao processar o ponto de entrada sua orientação é marcada como utilizada. <br>**
**3. Percorrer até o Ponto de Saída: A partir do ponto de entrada, percorre os pontos na lista do polígono até encontrar o próximo ponto de saída. <br>**
**4. Alternar para a Lista da Janela: No ponto de saída, o algoritmo alterna para a lista da janela, buscando o próximo ponto correspondente. <br>**
**5. Ao processar o ponto de saída sua orientação é marcada como utilizada. <br>**
**6. Percorrer até o Ponto de Entrada: A partir desse ponto de saída, o algoritmo percorre a lista da janela até encontrar o próximo ponto de entrada. <br>**
**7. Retornar à Lista do Polígono: Ao identificar o ponto de entrada na janela, oalgoritmo volta para a lista do polígono, conectando os pontos e continuando o processo. <br>**

Esse ciclo se repete até que todos os pontos de entrada do polígono tenham sido utilizados

---
### 📝 Observações

- O sistema é modular, com foco em flexibilidade e fácil manutenção.
- Arquivos XML de entrada e saída seguem o mesmo padrão, com adição de dados transformados.

### Contribuindo

```Contribuições são bem-vindas! ```
- Para mudanças maiores, abra uma issue primeiro para discutir o que você gostaria de mudar.

### Developers

|   | Name             | Github                         | 
| -------------------------------------------------------------------------------------------- | ---------------- | ------------------------------ |
| <img src="https://avatars.githubusercontent.com/u/60756521"  width="100px" heigth="100px" /> | Filipe Abner     | https://github.com/FilipeAbner |
| <img src="https://avatars.githubusercontent.com/u/70250416?v=4"  width="100px" heigth="100px" /> | Lucas Freitas     | https://github.com/LucasFreitaslpf1 |