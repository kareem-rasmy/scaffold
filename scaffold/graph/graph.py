import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
from scaffold.core.entity import MathematicalEntity
from scaffold.core.relation import Relation


class MathematicalGraph:

    def __init__(self):
        self._graph = nx.MultiDiGraph()

    def add_entity(self, entity: MathematicalEntity) -> None:
        self._graph.add_node(
            entity.id,
            entity=entity,
        )

    def add_relation(self, relation: Relation) -> None:

        self.add_entity(relation.source)
        self.add_entity(relation.target)

        self._graph.add_edge(
            relation.source.id,
            relation.target.id,
            relation_type=relation.relation_type,
        )

    def add_relations(self, relations) -> None:
        for relation in relations:
            self.add_relation(relation)

    def draw(self) -> None:
        graph = self._graph

        pos = graphviz_layout(graph, prog="dot")

        node_labels = {
            node_id: data["entity"].name
            for node_id, data in graph.nodes(data=True)
        }

        edge_labels = {
            (source, target, key): data["relation_type"].value
            for source, target, key, data
            in graph.edges(keys=True, data=True)
        }

        plt.figure(figsize=(14, 10))

        nx.draw_networkx_nodes(
            graph,
            pos,
            node_size=3000,
        )

        nx.draw_networkx_labels(
            graph,
            pos,
            labels=node_labels,
        )

        nx.draw_networkx_edges(
            graph,
            pos,
            arrows=True,
            arrowsize=20,
            node_size=3000,
            connectionstyle="arc3,rad=0.05",
        )

        nx.draw_networkx_edge_labels(
            graph,
            pos,
            edge_labels=edge_labels,
        )

        plt.axis("off")
        plt.show()
