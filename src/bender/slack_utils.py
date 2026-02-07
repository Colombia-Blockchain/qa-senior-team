"""Shared Slack utilities — message splitting and formatting."""

# Slack message character limit
SLACK_MSG_LIMIT = 4000


def split_text(text: str, max_length: int = SLACK_MSG_LIMIT) -> list[str]:
    """Split text into chunks, preferring to break at newlines."""
    chunks: list[str] = []
    while len(text) > max_length:
        split_pos = text.rfind("\n", 0, max_length)
        if split_pos == -1:
            split_pos = max_length
        chunks.append(text[:split_pos])
        text = text[split_pos:].lstrip("\n")
    if text:
        chunks.append(text)
    return chunks
