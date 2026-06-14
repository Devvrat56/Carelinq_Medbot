"""
graph_builder.py

Build and manage the medical knowledge graph.
"""

import os
import pickle
import networkx as nx
from typing import List, Dict


class MedicalKnowledgeGraph:

    def __init__(
        self,
        graph_path: str = "knowledge_graph/knowledge_graph.pkl"
    ):

        self.graph_path = graph_path

        os.makedirs(
            os.path.dirname(graph_path),
            exist_ok=True
        )

        self.graph = nx.DiGraph()

    def add_entities(
        self,
        entities: List[Dict]
    ):

        for entity in entities:

            node_name = entity["entity"]

            node_type = entity["type"]

            if not self.graph.has_node(
                node_name
            ):

                self.graph.add_node(
                    node_name,
                    entity_type=node_type
                )

    def add_relationships(
        self,
        relationships: List[Dict]
    ):

        for relation in relationships:

            source = relation["source"]

            target = relation["target"]

            relationship = relation[
                "relationship"
            ]

            self.graph.add_edge(
                source,
                target,
                relationship=relationship
            )

    def build_graph(
        self,
        entities: List[Dict],
        relationships: List[Dict]
    ):

        self.add_entities(
            entities
        )

        self.add_relationships(
            relationships
        )

    def save_graph(self):

        with open(
            self.graph_path,
            "wb"
        ) as f:

            pickle.dump(
                self.graph,
                f
            )

        print(
            f"Graph saved to "
            f"{self.graph_path}"
        )

    def load_graph(self):

        if os.path.exists(
            self.graph_path
        ):

            with open(
                self.graph_path,
                "rb"
            ) as f:

                self.graph = pickle.load(
                    f
                )

            print(
                f"Graph loaded from "
                f"{self.graph_path}"
            )

        else:

            print(
                "No graph found."
            )

    def get_statistics(self):

        stats = {

            "nodes":
                self.graph.number_of_nodes(),

            "edges":
                self.graph.number_of_edges(),

            "node_types": {}
        }

        for node, data in (
            self.graph.nodes(
                data=True
            )
        ):

            entity_type = data.get(
                "entity_type",
                "Unknown"
            )

            stats["node_types"][
                entity_type
            ] = (

                stats["node_types"].get(
                    entity_type,
                    0
                ) + 1
            )

        return stats

    def print_graph_summary(
        self
    ):

        stats = (
            self.get_statistics()
        )

        print("\n=== GRAPH SUMMARY ===")

        print(
            f"Total Nodes: "
            f"{stats['nodes']}"
        )

        print(
            f"Total Relationships: "
            f"{stats['edges']}"
        )

        print(
            "\nEntity Types:"
        )

        for entity_type, count in (
            stats[
                "node_types"
            ].items()
        ):

            print(
                f"{entity_type}: "
                f"{count}"
            )

    def print_relationships(
        self
    ):

        print(
            "\n=== RELATIONSHIPS ==="
        )

        for source, target, data in (
            self.graph.edges(
                data=True
            )
        ):

            print(

                f"{source} "

                f"--"

                f"[{data['relationship']}]"

                f"--> "

                f"{target}"
            )


if __name__ == "__main__":

    from entity_extractor import (
        MedicalEntityExtractor
    )

    sample_text = """

    Prostate cancer is diagnosed
    using PSA test and biopsy.

    Hormone therapy treats
    advanced prostate cancer.

    Hormone therapy causes
    hot flashes.

    """

    extractor = (
        MedicalEntityExtractor()
    )

    entities = (
        extractor.extract_entities(
            sample_text
        )
    )

    relationships = (
        extractor.extract_relationships(
            sample_text,
            entities
        )
    )

    graph = (
        MedicalKnowledgeGraph()
    )

    graph.build_graph(
        entities,
        relationships
    )

    graph.print_graph_summary()

    graph.print_relationships()

    graph.save_graph()
