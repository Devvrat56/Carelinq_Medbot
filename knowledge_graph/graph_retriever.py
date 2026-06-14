"""
graph_retriever.py

Retrieve medical knowledge from the
Knowledge Graph for KAG.
"""

import pickle
import os
import networkx as nx

from knowledge_graph.entity_extractor import (
    MedicalEntityExtractor
)


class GraphRetriever:

    def __init__(
        self,
        graph_path="knowledge_graph/knowledge_graph.pkl"
    ):

        self.graph_path = graph_path

        self.extractor = (
            MedicalEntityExtractor()
        )

        self.graph = self.load_graph()

    def load_graph(self):

        if not os.path.exists(
            self.graph_path
        ):

            raise FileNotFoundError(
                f"Knowledge Graph not found at "
                f"{self.graph_path}"
            )

        with open(
            self.graph_path,
            "rb"
        ) as f:

            graph = pickle.load(f)

        print(
            f"Loaded graph with "
            f"{graph.number_of_nodes()} nodes "
            f"and "
            f"{graph.number_of_edges()} edges"
        )

        return graph

    def extract_query_entities(
        self,
        query
    ):

        entities = (
            self.extractor.extract_entities(
                query
            )
        )

        return entities

    def retrieve_knowledge(
        self,
        query
    ):

        entities = (
            self.extract_query_entities(
                query
            )
        )

        if not entities:

            return []

        knowledge = []

        for entity in entities:

            entity_name = entity[
                "entity"
            ]

            if self.graph.has_node(
                entity_name
            ):

                # Outgoing relationships
                for neighbor in (
                    self.graph.successors(
                        entity_name
                    )
                ):

                    edge = (
                        self.graph[
                            entity_name
                        ][neighbor]
                    )

                    knowledge.append(

                        {
                            "source":
                                entity_name,

                            "relationship":
                                edge[
                                    "relationship"
                                ],

                            "target":
                                neighbor
                        }
                    )

                # Incoming relationships
                for predecessor in (
                    self.graph.predecessors(
                        entity_name
                    )
                ):

                    edge = (
                        self.graph[
                            predecessor
                        ][entity_name]
                    )

                    knowledge.append(

                        {
                            "source":
                                predecessor,

                            "relationship":
                                edge[
                                    "relationship"
                                ],

                            "target":
                                entity_name
                        }
                    )

        return knowledge

    def format_knowledge(
        self,
        knowledge
    ):

        if not knowledge:

            return (
                "No graph knowledge found."
            )

        formatted = []

        for item in knowledge:

            formatted.append(

                f"{item['source']} "

                f"{item['relationship']} "

                f"{item['target']}"
            )

        return "\n".join(
            formatted
        )


if __name__ == "__main__":

    retriever = (
        GraphRetriever()
    )

    while True:

        query = input(
            "\nEnter Query "
            "(exit to stop): "
        )

        if query.lower() == "exit":
            break

        knowledge = (
            retriever.retrieve_knowledge(
                query
            )
        )

        print(
            "\nRetrieved Knowledge:"
        )

        print(
            retriever.format_knowledge(
                knowledge
            )
        )