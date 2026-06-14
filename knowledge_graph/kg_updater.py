import networkx as nx
import pickle
import os

class KnowledgeGraphUpdater:
    def __init__(self, graph_path="knowledge_graph/knowledge_graph.pkl"):
        self.graph_path = graph_path
        self.graph = self._load_graph()

    def _load_graph(self):
        if os.path.exists(self.graph_path):
            with open(self.graph_path, "rb") as f:
                return pickle.load(f)
        return nx.DiGraph()

    def save_graph(self):
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.graph_path), exist_ok=True)
        with open(self.graph_path, "wb") as f:
            pickle.dump(self.graph, f)

    def _add_triple(self, source, rel, target):
        if not source or not target:
            return
        # Ensure nodes exist
        if not self.graph.has_node(source):
            self.graph.add_node(source, entity_type="Condition")
        if not self.graph.has_node(target):
            self.graph.add_node(target, entity_type="Value")
            
        self.graph.add_edge(source, target, relationship=rel)

    def update_from_prostate_cancer(self, patient_id: str, data):
        """Updates universal knowledge graph based on Prostate Cancer findings."""
        root = "Prostate Cancer"
        if data.psa_level and data.psa_level.lower() != 'unknown':
            self._add_triple(root, "HAS_PSA", data.psa_level)
        if data.gleason_score and data.gleason_score.lower() != 'unknown':
            self._add_triple(root, "HAS_GLEASON", data.gleason_score)
        if data.current_treatment and data.current_treatment.lower() != 'unknown':
            self._add_triple(root, "TREATED_WITH", data.current_treatment)
        
        self.save_graph()
        print(f"Graph updated with Prostate Cancer data for Patient {patient_id}.")

    def update_from_breast_cancer(self, patient_id: str, data):
        """Updates universal knowledge graph based on Breast Cancer findings."""
        root = "Breast Cancer"
        if data.er_status and data.er_status.lower() != 'unknown':
            self._add_triple(root, "HAS_ER_STATUS", data.er_status)
        if data.pr_status and data.pr_status.lower() != 'unknown':
            self._add_triple(root, "HAS_PR_STATUS", data.pr_status)
        if data.her2_status and data.her2_status.lower() != 'unknown':
            self._add_triple(root, "HAS_HER2_STATUS", data.her2_status)
        if data.ki67 and data.ki67.lower() != 'unknown':
            self._add_triple(root, "HAS_KI67", data.ki67)
            
        self.save_graph()
        print(f"Graph updated with Breast Cancer data for Patient {patient_id}.")
