from app.ingestion.chunking import fixed_chunk, recursive_chunk, semantic_chunk, structural_chunk


def test_chunkers_return_content():
    text = "# Policy\nRetail customers have a maximum limit. Late penalties apply after a grace period."
    assert fixed_chunk(text)
    assert recursive_chunk(text)
    assert semantic_chunk(text)
    assert structural_chunk(text)
