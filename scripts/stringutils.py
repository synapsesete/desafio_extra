def get_string_between_chars(text, char1, char2):
    """
    Extracts the substring between two specified characters.

    Args:
        text (str): The input string.
        char1 (str): The first character.
        char2 (str): The second character.

    Returns:
        str: The substring between char1 and char2, or an empty string if
             either character is not found or not in the correct order.
    """
    start_index = text.find(char1)
    if start_index == -1:
        return ""  # First character not found

    end_index = text.find(char2, start_index + 1)
    if end_index == -1:
        return ""  # Second character not found after the first

    return text[start_index + 1 : end_index]