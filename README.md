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
- Atributo adicional `cor="nome_cor"` (conforme nomes do X11)
- Saída contém também coordenadas transformadas para viewport.

## 📚 Tecnologias Utilizadas

- Python 3
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

# Dependencias
## Ubuntu/Debian Dependencias
```sudo apt install python3-tk```

## Python Dependencias
```pip install numpy ```<br> 
```pip install ipykernel```


# Relatório

# 📝 Observações

- O sistema é modular, com foco em flexibilidade e fácil manutenção.
- Arquivos XML de entrada e saída seguem o mesmo padrão, com adição de dados transformados.

