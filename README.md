# INSTRUÇÕES DE EXECUÇÃO

## Pré-requisitos:
- Python 3.x instalado
- Biblioteca Tkinter (já inclusa na instalação padrão do Python)

## Execução:
Execute o arquivo gui_app.py usando o comando: python gui_app.py

## Funcionalidades
- Após a execução, a janela principal do simulador será aberta.
- No painel "Controles de Busca" à esquerda, configure os parâmetros da simulação:
  - Método de Busca: Selecione um dos algoritmos disponíveis (Amplitude, Profundidade, Profundidade Limitada, Aprofundamento Iterativo, Bidirecional, Custo Uniforme, Greedy, A-Estrela, AIA-Estrela).
  - Limite: Caso utilize "Profundidade Limitada" ou "Aprofundamento Iterativo", defina a profundidade máxima da busca.
  - Estado Inicial e Objetivo: Informe as coordenadas (X, Y) e a orientação de partida e chegada do veículo.
  - Prioridade de Expansão: Reordene a lista de orientações para definir a ordem de exploração dos nós sucessores.
- Clique em "Iniciar Busca" para executar o algoritmo com os parâmetros definidos.
- Acompanhe os resultados que serão exibidos no painel de controle:
  - Custo do Caminho: O custo total acumulado da rota encontrada.
  - Caminho Encontrado: A sequência de estados (posição e orientação) da rota.
- Visualize o resultado graficamente no painel à direita:
  - O grid da fábrica é exibido com obstáculos em cinza.
  - A rota encontrada é desenhada, destacando o ponto inicial (verde) e o final (vermelho).

## Desenvolvido por: Izaque Nogueira e Vinicius Cardoso
