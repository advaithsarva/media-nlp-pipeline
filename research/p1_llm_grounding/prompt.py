"""The fixed prompt template every model tier gets, verbatim. Changing wording between
models would confound the comparison -- this is the one thing that must not vary."""

PROMPT_TEMPLATE = """You will be given a passage of news text. Identify up to 5 phrases that show \
bias, loaded language, or a propaganda technique (e.g. name-calling, appeal to fear, \
glittering generalities, bandwagon, unsupported quantifiers).

For each phrase:
- Quote it EXACTLY as it appears in the passage, character for character. Do not paraphrase, \
summarize, or correct spelling/punctuation.
- Give the character offset (start_char, end_char) of that exact quote within the passage \
text below, counting from 0.

Return ONLY a JSON array, no other text, in this exact shape:
[{{"quote": "...", "start_char": 0, "end_char": 10}}, ...]

If you find nothing, return [].

PASSAGE (index characters from 0 at the very first character):
{passage}
"""


def build_prompt(passage_text: str) -> str:
    return PROMPT_TEMPLATE.format(passage=passage_text)
