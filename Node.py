class Node(object):
    """
    Representa um nó na árvore de busca.

    Atributos:
        pai (Node): O nó pai na árvore de busca.
        estado (any): O estado que o nó representa no espaço de estados do problema.
        v1 (float): O custo acumulado desde o nó inicial até este nó (g(n)).
        anterior (Node): Ponteiro para o nó anterior (não utilizado nesta implementação).
        proximo (Node): Ponteiro para o próximo nó (não utilizado nesta implementação).
    """
    def __init__(self, pai=None, estado=None, v1=None,
                 anterior=None,  proximo=None):
        self.pai       = pai
        self.estado    = estado
        self.v1        = v1
        self.anterior  = anterior
        self.proximo   = proximo