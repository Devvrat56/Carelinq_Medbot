import time

class Tracer:
    def __init__(self):
        self.spans = []

    def start_span(self, name: str):
        span = {
            "name": name,
            "start_time": time.time()
        }
        self.spans.append(span)
        return len(self.spans) - 1

    def end_span(self, span_index: int):
        if 0 <= span_index < len(self.spans):
            span = self.spans[span_index]
            span["end_time"] = time.time()
            span["duration"] = span["end_time"] - span["start_time"]
            
    def get_traces(self):
        return self.spans
