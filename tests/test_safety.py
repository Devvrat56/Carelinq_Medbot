def test_safety_guardrails():
    from Data_safety.guardrails import ClinicalGuardrails
    guardrails = ClinicalGuardrails()
    
    assert not guardrails.is_safe("What dosage of ibuprofen should I take?")
    assert not guardrails.is_safe("Can you diagnose my rash?")
    assert guardrails.is_safe("What are the side effects of ibuprofen?")
