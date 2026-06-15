def test_escalation_manager():
    from retriever.escalation_manager import EscalationManager
    manager = EscalationManager(confidence_threshold=0.5, hallucination_threshold=0.6)
    
    assert manager.should_escalate("I am having a heart attack", 0.9, 0.9)
    assert manager.should_escalate("Normal query", 0.4, 0.9)
    assert not manager.should_escalate("What is diabetes?", 0.8, 0.8)
