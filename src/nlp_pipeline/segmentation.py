"""Splits the document text into sentences, keeping exact character offsets.

The offsets are the load-bearing part. Every piece of evidence the pipeline reports is a
(start_char, end_char) pair into the original text, built by adding an offset inside a
sentence to the sentence's own start. If a sentence start is wrong by one character,
every quote in the report is wrong by one character.

pysbd does the sentence splitting. It is rule-based, so it gives the same answer every
time, which a statistical model would not guarantee. Two things are handled around it:

  * a blank line is always a boundary -- a headline with no full stop must not be glued
    to the paragraph beneath it;
  * a single line break inside a paragraph is never a boundary -- plain-text files wrap
    at a fixed width, and pysbd would otherwise report each line as its own sentence.

Only boundaries move. The text itself is never touched, so offsets stay true.
"""

import re

import pysbd

from nlp_pipeline.shared_types import Sentence, NormalizedDocument

# A blank line, i.e. a line break followed by another with only whitespace between.
PARAGRAPH_BREAK = re.compile(r"\n[ \t]*\n\s*")

SENTENCE_ENDINGS = (".", "!", "?", '."', '?"', '!"', ".'", "?'", "!'", ".)", "?)", "!)")


class SentenceSegmenter:
    def __init__(self, segmentation_config=None):
        config = segmentation_config or {}
        # clean=False is not optional: cleaning rewrites the text, and the offsets pysbd
        # hands back would then refer to a string we no longer have.
        self.segmenter = pysbd.Segmenter(
            language=config.get("language", "en"),
            clean=False,
            char_span=True,
        )

    def _paragraphs(self, text):
        """(start, end) of each block of text between blank lines."""
        blocks = []
        position = 0
        for gap in PARAGRAPH_BREAK.finditer(text):
            if gap.start() > position:
                blocks.append((position, gap.start()))
            position = gap.end()
        if position < len(text):
            blocks.append((position, len(text)))
        return blocks

    def _merge_wrapped_lines(self, paragraph, spans):
        """Join back together the pieces pysbd split at a mid-sentence line break.

        A split is a real sentence end only if the part before it ends in sentence
        punctuation. If it does not, the two pieces belong to one sentence.
        """
        merged = []
        for span in spans:
            start, end = span.start, span.end
            if merged:
                previous_start, previous_end = merged[-1]
                if not paragraph[:previous_end].rstrip().endswith(SENTENCE_ENDINGS):
                    merged[-1] = (previous_start, end)
                    continue
            merged.append((start, end))
        return merged

    def segment(self, doc: NormalizedDocument) -> NormalizedDocument:
        text = doc.text
        sentences = []

        for block_start, block_end in self._paragraphs(text):
            paragraph = text[block_start:block_end]
            spans = self._merge_wrapped_lines(paragraph, self.segmenter.segment(paragraph))

            for start, end in spans:
                # pysbd keeps the whitespace that follows a sentence; pull the boundaries
                # in so a quoted sentence carries no stray spaces
                while start < end and paragraph[start].isspace():
                    start += 1
                while end > start and paragraph[end - 1].isspace():
                    end -= 1
                if start >= end:
                    continue

                absolute_start = block_start + start
                absolute_end = block_start + end
                sentence_text = text[absolute_start:absolute_end]

                sentences.append(Sentence(
                    sentence_id=len(sentences),
                    text=sentence_text,
                    start_char=absolute_start,
                    end_char=absolute_end,
                ))

        doc.sentences = sentences
        return doc
