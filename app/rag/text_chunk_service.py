import re
def split_text_into_chunks(text, max_size=1000):
    """
    Splits a large text chunk into smaller chunks based on sentences, ensuring each chunk
    does not exceed the specified maximum size.

    Args:
        chunk (str): The large text chunk to split.
        max_size (int): The maximum size of each chunk in characters.

    Returns:
        list: A list of sentence-based chunks, each with a size up to `max_size`.
    """

    if not isinstance (text, str):
        raise ValueError("Input `text` must be a string.")
    if not isinstance(max_size, int) or max_size <=0:
        raise ValueError("Input `max_size` must be a positive integer.")
    if len(text.strip()) == 0:
        return []
    
    # split the text into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    
    chunks = []
    current_chunk = ''
    
    # Iterate over sentences
    for sentence in sentences:
        # If adding the sentence exceeds max_size, finalize the current chunk
        if len(current_chunk) + len(sentence) + 1 > max_size:  # +1 for a space
            chunks.append(current_chunk.strip())  # append the completed chunk
            current_chunk = sentence  # Start a new chunk with the current sentence
        else:
            # add the sentence to the current chunk
            current_chunk += " " + sentence

    # Add the last chunk if it is not empty
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks
    