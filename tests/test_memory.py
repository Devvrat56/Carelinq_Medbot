def test_memory_summarization():
    from memory.conversation_summarizer import ConversationSummarizer
    summarizer = ConversationSummarizer(max_history_length=2)
    history = ["Hello", "Hi", "How are you?"]
    summary = summarizer.summarize(history)
    assert len(summary) > 0
