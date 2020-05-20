from datetime import datetime
from copy import deepcopy


class Grafo:
    """
    Classe para implementação da representação e algorítmos de grafos.
    """

    def __init__(self, digrafo, valorado, vertices, arestas):
        """
        Construtor da Classe
        :param digrafo: True se o grafo for direcionado, False se não.
        :param valorado: True se o grafo for valorado, False se não.
        :param vertices: Lista de Vértices do grafo.
        :param arestas: Lista de Arestas do grafo.
        """
        self._id_grafo = f"{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self._digrafo = digrafo
        self._valorado = valorado
        self._vertices = vertices
        self._arestas = arestas
        self._max_peso = 1

    def estrutura_adjacencia(self):
        """
        Método que retorna um dicionário correspondente à estrutura de
        adjacencia que representa o grafo.
        """
        estrutura_adjacencia = {}
        for i in range(len(self._vertices)):
            estrutura_adjacencia.update({self._vertices[i]: []})
        arestas = self._arestas
        if self._valorado:
            for trio in arestas:
                i, j, p = trio.strip().split("-")
                p = float(p)
                estrutura_adjacencia[i].append({'vertice_id': j, 'peso': p})
                if not self._digrafo:
                    estrutura_adjacencia[j].append({'vertice_id': i,
                                                    'peso': p})
                if p > self._max_peso:
                    self._max_peso = p
        else:
            for par in arestas:
                i, j = par.strip().split("-")
                estrutura_adjacencia[i].append({'vertice_id': j, 'peso': 1})
                if not self._digrafo:
                    estrutura_adjacencia[j].append({'vertice_id': i,
                                                    'peso': 1})
        return estrutura_adjacencia

    def get_adjacentes(self, vertice):
        """
        Método que recebe um vértice do grafo e retorna uma lista
        contendo os vértices adjacentes a ele.
        """
        grafo = self.estrutura_adjacencia()
        adjacentes = []
        for i in grafo[vertice]:
            adjacentes.append(i['vertice_id'])
        return adjacentes

    def _get_adjacentes_e_pesos(self, vertice):
        """
        Método privado que recebe um vértice do grafo e retorna uma
        lista contendo os vértices adjacentes a ele e uma outra lista
        contendo seus respectivos pesos.
        """
        grafo = self.estrutura_adjacencia()
        adjacentes = []
        pesos = []
        for i in grafo[vertice]:
            adjacentes.append(i['vertice_id'])
            pesos.append(i['peso'])
        return adjacentes, pesos

    def dijkstra_com_parada(self, v_origem, k=10):
        """
        Adaptação do algoritmo de djikstra para retornar os 'k' vértices
        mais próximos.
        """
        dist = [float('inf') for i in range(len(self._vertices))]
        path = ['-' for i in range(len(self._vertices))]
        s = [v_origem]
        not_s = deepcopy(self._vertices)
        not_s.remove(v_origem)
        dist[self._vertices.index(v_origem)] = 0

        v_atual = v_origem

        while not_s:
            _adj, _p = self._get_adjacentes_e_pesos(v_atual)
            adjacentes, pesos = [], []
            for idx, vertice in enumerate(_adj):
                if vertice in not_s:
                    adjacentes.append(_adj[idx])
                    pesos.append(_p[idx])

            for idx, vertice in enumerate(adjacentes):
                if dist[self._vertices.index(vertice)] > \
                        dist[self._vertices.index(v_atual)] + pesos[idx]:
                    dist[self._vertices.index(vertice)] = \
                        dist[self._vertices.index(v_atual)] + pesos[idx]
                    path[self._vertices.index(vertice)] = v_atual

            min_dist = float('inf')
            for vertice in not_s:
                if dist[self._vertices.index(vertice)] < min_dist:
                    min_dist = dist[self._vertices.index(vertice)]
                    v_atual = vertice

            s.append(v_atual)
            if len(s) > k:
                s.pop(0)
                return s
            not_s.remove(v_atual)

        s.pop(0)
        return s
