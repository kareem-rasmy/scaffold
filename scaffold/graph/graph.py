import matplotlib.pyplot as plt
import networkx as nx
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

        pos = nx.spring_layout(graph)

        node_labels = {
            node_id: data["entity"].name
            for node_id, data in graph.nodes(data=True)
        }

        edge_labels = {
            (source, target, key): data["relation_type"].name
            for source, target, key, data
            in graph.edges(keys=True, data=True)
        }

        nx.draw(
            graph,
            pos,
            labels=node_labels,
            with_labels=True,
            node_size=3000,
            arrows=True,
        )

        nx.draw_networkx_edge_labels(
            graph,
            pos,
            edge_labels=edge_labels,
        )

        plt.show()
