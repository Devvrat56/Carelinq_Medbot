class MetricsTracker:
    def __init__(self):
        self.metrics = {
            "token_usage": 0,
            "safety_triggers": 0,
            "queries_processed": 0
        }

    def record_token_usage(self, tokens: int):
        self.metrics["token_usage"] += tokens

    def record_safety_trigger(self):
        self.metrics["safety_triggers"] += 1

    def record_query(self):
        self.metrics["queries_processed"] += 1

    def get_metrics(self):
        return self.metrics
