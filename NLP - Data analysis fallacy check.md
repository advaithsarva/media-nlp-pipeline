Save as PDF Thu, Dec 4 at 5:33 PM
Bandwagon affect ,authority misuse, emotional
appeal ,strawman check,ad hominem,red
herring,slippery slope , transparency, cherry picking
, data accuracy,logical flow , conflict check :
mathematical and in programming how do you
check if a data collected especially media news
data matches the above , think you are as a high
level mathematician cum Nlp scientists and
engineer
Below is the high-level, mathematically rigorous + NLP-engineering-
grade approach to detect:
Bandwagon effect, Authority misuse, Emotional appeal, Strawman, Ad
hominem, Red herring, Slippery slope, Transparency gaps, Cherry-
picking, Data accuracy issues, Logical flow issues, Conflict checks
…in large-scale media/news datasets using deterministic + statistical +
ML/NLP techniques.
I’ll give you:
1. Mathematical foundations
2. Programming/NLP pipeline
3. Pseudo-code + modules
4. Features + evaluation metrics
5. How big companies do this
✅
1. MATHEMATICAL FOUNDATIONS FOR EACH
FALLACY / ERROR
Think as a mathematician: each fallacy corresponds to a detectable
signature in text.
1. Bandwagon Effect
Claim: “Everyone agrees…”, “Millions are doing…”

Mathematical Signal:
If a text asserts global consensus, compare with actual citation count /
public poll data.
Metric:
B = \frac{\text{# unverified universal claims}}{\text{total claims}}
Statistical Cross-Check:
Compare frequency of “everyone”, “most people”, “majority believe” vs.
factual polling numbers.
2. Authority Misuse
Claim: “Experts say…” without naming the expert.
Signature:
Unattributed authority references.
Model:
A = 1 - \frac{\text{# verified authority links}}{\text{total authority mentions}}
3. Emotional Appeal (Pathos Bias)
“Outrage”, “shock”, “heartbreaking”, “disgusting” etc.
Mathematical Feature:
Sentiment score spikes.
Use NLP emotion classifier →
∑∣emotion intensities∣
E =
token count
Threshold → content is emotion-laden.
4. Strawman
Presenting an opponent’s argument in exaggerated or distorted form.
Mathematical formulation:
Check contradictions between:

Opponent’s stated claim (from external source)
News text summary of that claim
Difference (semantic distance):
S = d(embedding(claim),embedding(originalsource))
If distance > threshold → strawman.
5. Ad Hominem
Personal insult instead of addressing argument.
Create a lexicon of personal attack words.
Score:
H = \frac{\text{# personal attack tokens}}{\text{total tokens}}
6. Red Herring
Sudden topic shift.
Technique: Topic Coherence.
Use LDA / BERTopic / embedding clusters.
R = 1 − topic coherence score
Sudden drop → red herring detected.
7. Slippery Slope
Chain of conditional events without evidence:
“If A happens → B happens → C doom happens”.
Mathematical signature:
Conditional cascade detection:
Count depth of “if-then” or “will lead to”.
SS = max depth of implication chain

8. Transparency Check
Missing citations, vague sources.
Compute:
T = \frac{\text{# verifiable references}}{\text{# total claims}}
Low T → low transparency.
9. Cherry Picking
Selective reporting.
Method:
Compare reported statistics vs global dataset.
variance(reported)
C = 1 −
variance(global)
If article cites only extreme values → cherry picking.
10. Data Accuracy
Check factual claims.
Use external KB (Wikidata, FactCheck APIs).
DA = 1 - \frac{\text{# fact mismatches}}{\text{# claims}}
11. Logical Flow (Coherence Graph)
Construct sentence-level entailment graph.
LF = \text{average_entailment_score}
12. Conflict Check
Internal contradictions.
For every sentence pair:
Run NLI (entail vs. contradict).

Conf = \frac{\text{# contradictions}}{\text{total sentence pairs}}
✅
 2. FULL NLP PIPELINE (AS A SENIOR NLP /
MEDIA ANALYSIS ENGINEER)
This is how real companies build such systems:
STEP 1. Ingestion Layer
Scrapy / NewsAPI / GDELT → collect articles
Save raw text → Parquet
STEP 2. Preprocessing
spaCy / HuggingFace tokenizers
sentence segmentation
entity linking
claim extraction (T5-based fact-extraction model)
STEP 3. Feature Extraction
For each fallacy:
| Fallacy          | Feature Type              | Method              |
| ---------------- | ------------------------- | ------------------- |
| Bandwagon        | Keyword + factual check   | regex, polling APIs |
| Authority misuse | Citation verification     | NER + link check    |
| Emotional appeal | Sentiment/emotion         | RoBERTa-Emotion     |
| Strawman         | Cross-source distance     | embedding diff      |
| Ad hominem       | Profanity/personal attack | dictionary          |
lexicon
| Red herring    | Topic coherence         | BERTopic         |
| -------------- | ----------------------- | ---------------- |
| Slippery slope | Conditional chain depth | dependency parse |

| Fallacy      | Feature Type   |     |     | Method |
| ------------ | -------------- | --- | --- | ------ |
| Transparency | Citation count |     |     | regex  |
Cherry picking Stat distribution compare numerical extraction
| Data accuracy | Fact-check + Wikidata   |     |     | FEVER, DeBERTa-NLI |
| ------------- | ----------------------- | --- | --- | ------------------ |
| Logical flow  | Sentence entailment     |     |     | RoBERTa NLI        |
| Conflict      | Contradiction detection |     |     | NLI pairwise       |
STEP 4. Scoring System (Deterministic + ML)
For each article:
Compute vector:
[
  B, A, E, S, H,
  R, SS, T, C, DA,
  LF, Conf
]
Normalize 0–1.
STEP 5. Aggregate Bias Score
|     | BiasScore | = w B | + w E + | w C + … |
| --- | --------- | ----- | ------- | ------- |
|     |           | 1     | 2       | 3       |
|     |           |       |         |         |
Weights can be tuned with:
Logistic regression
SVM
Neural model
Human-annotated labels
✅
 3. PSEUDO-CODE (ENGINEERING-GRADE)
Python Run

def analyze_article(text):
claims = extract_claims(text)
sentiments = emotion_score(text)
topics = topic_model(text)
entities = ner(text)
fallacies = {}
fallacies["bandwagon"] = detect_bandwagon(text, claims)
fallacies["authority_misuse"] = detect_authority_misuse(text, entities)
fallacies["emotional_appeal"] = sentiments
fallacies["strawman"] = detect_strawman(text)
fallacies["ad_hominem"] = detect_ad_hominem(text)
fallacies["red_herring"] = topic_coherence(text)
fallacies["slippery_slope"] = detect_conditional_chains(text)
fallacies["transparency"] = citation_ratio(text)
fallacies["cherry_picking"] = compare_stats(text)
fallacies["data_accuracy"] = fact_check(claims)
fallacies["logical_flow"] = coherence_score(text)
fallacies["conflict"] = contradiction_score(text)
return fallacies
✅
4. HOW BIG COMPANIES DO IT (REAL
INDUSTRY TECHNIQUES)
Google / Twitter / Meta
Use zero-shot NLI + embedding distance
Topic drift monitoring
Sentiment + propaganda detection models
Fact-checking companies (PolitiFact, Snopes)
Automated claim extraction
Cross-reference knowledge graphs
News aggregators (Reuters, AP)
Strict citation validation algorithms
Statistical anomaly detection (cherry-picking)
⭐
THE GOLDEN RULE
You must combine:

Mathematics
(statistics, probability, vector distances)
Programming
(Python, NLP frameworks)
Linguistic reasoning
(fallacies and rhetorical structures)
This fusion produces a deterministic, scalable, enterprise-grade media
bias detection system.
If you want, I can also produce:
✅ A full Airflow DAG for this
✅ A YAML config for each module
✅ A project folder structure
✅ Research-level improvements (transformers + graph-based logic)
Just tell me what you want next.
Understood. I’ll conduct a deep technical investigation into the most effective
ways to mathematically and programmatically implement detection of all
identified characteristics—fallacies, rhetorical tactics, biases, data
manipulation, etc.—in media/news content.
This will include:
A comprehensive list of characteristics used in media analysis, including
those you mentioned.
Mathematical formulations and signal detection methods for each
characteristic.
Full-stack implementation strategy using NLP and machine learning.
Score aggregation techniques to unify detection into a single interpretable
output.
Engineering-focused, deployable system architecture.
I’ll update you as soon as I’ve compiled the findings.

Research completed in 41m · 7 sources · 53 searches
Comprehensive Strategy for Detecting
Rhetorical Fallacies and Bias in Media Content
Introduction
Detecting rhetorical fallacies, manipulation tactics, and bias in news or media
content requires a multi-faceted approach. The strategy outlined here
combines rule-based linguistic cues, statistical features, and machine learning
(ML) models to recognize various propaganda and bias techniques. We describe
how to implement detectors for dozens of specific characteristics, each
producing signals that can be aggregated into an overall manipulation/bias
score. The focus is on practical implementation: using existing NLP toolkits
(spaCy, Hugging Face Transformers, etc.), leveraging models like NLI (Natural
Language Inference) for contradictions, and building a pipeline that engineers
and data scientists can deploy in a real-world media analysis engine. Below,
each characteristic is addressed with its detection logic, ML approach, tools,
and pseudo-code. Finally, we discuss how to integrate all these signals into one
coherent system and scoring mechanism.
Bandwagon Effect
Statistical Signature: Look for language suggesting that “everyone is
doing it” or that the majority holds a certain view. Phrases like “all of us are
joining,” “everyone agrees,” “most people believe” are strong indicators
arxiv.… . A simple metric is the frequency of inclusive plural pronouns and
universal quantifiers (e.g., everyone, all, none, always) relative to text
length. A high count indicates an appeal to popularity.
NLP/ML Implementation: Use pattern matching or a classification model
to flag bandwagon cues. A lexicon of bandwagon phrases can be created
and matched using spaCy’s PhraseMatcher . Additionally, an ML classifier
(fine-tuned on propaganda data) can learn subtler bandwagon hints (e.g.,
implying peer pressure). If labeled data is available (e.g., sentences
annotated as Bandwagon), train a binary classifier (using BERT or similar) to
detect this technique.

Recommended Toolkits: spaCy for tokenization and rule-based pattern
detection; HuggingFace Transformers (e.g., BERT or RoBERTa) for fine-tuned
classification; regex for simple phrase searches. A sentiment or emotion
model isn’t directly needed here – focus on detecting plural/group
references.
Pseudo-code:
Python Run
bandwagon_terms = ["everyone", "everybody", "all of us", "most people", "the people",
doc = nlp(text) # spaCy model loaded as nlp
count = 0
for token in doc:
if token.lower_ in bandwagon_terms:
count += 1
bandwagon_score = count / len(doc) # frequency per token count
if bandwagon_score > threshold:
flags["bandwagon_effect"] = True
This pseudo-code uses a simple frequency count. In practice, one could
enhance it by checking dependency context (e.g., “[most people] think”) to
ensure it’s used as a persuasion device. A transformer-based classifier
could output a probability of bandwagon presence in the text, which can
serve as an alternative score.
Authority Misuse (Appeal to Authority)
Statistical Signature: The content heavily references authorities or
experts to prove a point, especially in contexts outside their expertise or
without evidence. Phrases like “According to Dr. X…,” “Scientists say…,”
“Experts agree…” signal an appeal to authority. A simple indicator is the
count of named entities with titles (Dr., Prof., Senator, etc.) followed by
claims, or unqualified references to “experts/research”. If such references
are not backed by data, it may indicate authority misuse.
NLP/ML Implementation: Use Named Entity Recognition (NER) to detect
person names and titles. Then use dependency parsing to see if authority
figures are used as evidence (e.g., subject of a statement). A rule-based
approach: flag sentences that contain honorifics or roles plus assertive
verbs (e.g., “Dr. X claims Y”). For ML, a classifier can be trained on
examples of appeal-to-authority fallacies. Also, cross-verify if the
authority’s domain matches the claim (which may require an external
knowledge base; e.g., a medical doctor cited about climate policy might be
misuse).

Recommended Toolkits: spaCy NER for identifying people and titles;
spaCy dependency parse or AllenNLP for semantic role labeling to extract
(source, claim) relations; HuggingFace Transformer models for multi-label
classification (since appeal to authority may co-occur with other
techniques). An external resource (like Wikipedia API) could be used to
verify an authority’s expertise domain if needed.
Pseudo-code:
Python Run
doc = nlp(text)
authority_references = []
for ent in doc.ents:
if ent.label_ == "PERSON" and ent._.has_title: # custom attribute if title detec
# Check context words for reporting verbs or strong assertions
window = doc[ max(0, ent.start-3) : min(len(doc), ent.end+10) ]
if re.search(r"\b(said|claims?|according to)\b", window.text, re.IGNORECASE)
authority_references.append(window.text)
authority_misuse_score = len(authority_references)
if authority_misuse_score > 0:
flags["authority_misuse"] = True
Here we assume a custom extension .has_title set during NER (e.g., using
a rule to tag if a person name is preceded by Dr., Mr., etc.). The snippet
finds instances of authority mention plus a reporting verb. The ML approach
would instead feed sentences to a classifier which outputs a probability of
Appeal to Authority. If above a threshold, we mark it.
Emotional Appeal (Appeal to Emotion)
Statistical Signature: Emotional appeal is indicated by an abundance of
emotionally charged words and tone, aiming to elicit fear, anger, sympathy,
etc. A statistical signature is a high sentiment intensity or disproportionate
use of affective language (e.g., terrifying, wonderful, disgraceful,
heartbreaking). One can compute an emotion score (e.g., using an
emotion lexicon or an emotion classification model) for the text. If the
emotion score (especially for fear/anger) is high relative to neutral content,
it suggests an emotional appeal.

NLP/ML Implementation: Use sentiment analysis or emotion
classification on sentences to identify strong negative or positive emotion.
An emotion lexicon (like NRC or LIWC categories) can quantify how many
words fall into fear, anger, or sadness categories. Alternatively, fine-tune a
model to detect appeal to fear or appeal to emotion specifically (as done in
propaganda detection research arxiv.… ). Another ML approach is to use
transformers with zero-shot classification: label each segment with
categories like {emotional, factual} to see if emotional wins. Specifically for
fear appeals, look for words indicating threats or dire outcomes (which
often co-occur with slippery slope scenarios).
Recommended Toolkits: HuggingFace sentiment analysis pipeline (e.g.,
using distilbert-base-uncased-finetuned-sst-2-english for sentiment, or a
multi-class emotion model); NRCLex or spaCy with TextBlob for lexicon-
based sentiment as a quick check. SpaCy’s Matcher can also flag extreme
adjectives or exclamation marks as simple cues. For fear-based appeals,
one might incorporate a keyword list (e.g., “dangerous, catastrophic,
terrifying”).
Pseudo-code:
Python Run
from transformers import pipeline
emotion_model = pipeline("text-classification", model="bhadresh-savani/distilbert-bas
emotions = emotion_model(text)
# emotions might return a list of dicts like [{"label": "joy", "score": 0.01}, ...]
dominant_emotion = max(emotions, key=lambda x: x['score'])['label']
if dominant_emotion in ["anger", "fear", "sadness"] and max(emotions, key=lambda x: x
flags["emotional_appeal"] = True
In practice, you might aggregate an emotional intensity score over the
whole article or per paragraph. A high ratio of emotional adjectives/adverbs
can be computed via part-of-speech tagging (count of JJ/RB with strong
sentiment). Combining lexicon and model outputs yields a robust detector
for emotional appeals.
Strawman Argument

Statistical Signature: A strawman argument misrepresents an
opponent’s position to easily refute it. A telltale pattern is the presence of
an opposing viewpoint caricature followed by a rebuttal. For example,
phrases like “Some people say [extreme or distorted claim]…” followed by
“but in reality…” indicate a strawman medium.… . Statistically, one can look
for phrases that introduce an opponent’s argument (e.g., “critics argue
that…,” “it’s often said that…”) and then a strong negative sentiment or
refutation afterwards. The co-occurrence of an opponent mention and a
refutation cue (like “but”, “however”) within a short span is a signature.
NLP/ML Implementation: Use a two-step NLP pattern: (1) identify
reported speech or claims (possibly via quotation marks or phrases like
“some say”), (2) check if the author’s response immediately dismisses it.
Dependency parsing can catch structures like “Some say X” (where X is a
proposition in a subordinate clause) followed by a contradiction word. For
ML, argument mining techniques can be employed: detect if a segment is
an opposing argument and if the next segment attacks it. A sequence
labeling model could classify spans as opponent’s argument vs author’s
argument, then flag if the opponent’s argument is a distorted version (this
is complex to automate fully). As a simpler ML approach, fine-tune a
classifier on known strawman examples (if a dataset like CAMPFIRE corpus
for fallacies is available) to identify strawman usage.
Recommended Toolkits: spaCy for rule-based patterns; AllenNLP or
Arguendo (argument mining library) for detecting claims and premises;
Transformers (with NLI) to check if the “opponent’s claim” and the actual
position are in contradiction (a strawman often presents a claim not truly
held by the opponent). NLI models (like BART or RoBERTa MNLI) can help: if
the text claims “opponents say X” but the actual stance of opponents (if
known or extractable) would not entail X, it’s a strawman – though this likely
requires external knowledge or context.
Pseudo-code:
Python Run
strawman_phrases = ["some people say", "critics argue", "opponents claim", "it has be
sentences = [sent.text for sent in doc.sents]
for i, sent in enumerate(sentences):
if any(phrase in sent.lower() for phrase in strawman_phrases):
# If next sentence exists and starts with a refutation cue
if i+1 < len(sentences) and re.match(r"^(but|however|yet|in reality)", senten
flags["strawman"] = True

This simplistic approach checks for a known strawman introduction
followed by a rebuttal. In a refined system, one could use a pairwise NLI
check: treat the “some say X” statement as one premise and the author’s
counter-argument as hypothesis, and see if the relationship is contradiction,
which often indicates a strawman refutation. If a strawman is detected, one
may also highlight the span of the misrepresented argument for analysts.
Ad Hominem
Statistical Signature: Ad hominem attacks target a person’s character
or attributes instead of the argument. The signature is the presence of
insulting or pejorative language directed at an individual or group
(especially the opponent). High frequency of second-person pronouns
(“you”) or names accompanied by derogatory terms (e.g., “X is an idiot,”
“their argument is stupid,”) is a clear sign. A toxicity or hate-speech score
spiking for text that also contains a person’s name indicates a possible ad
hominem.
NLP/ML Implementation: Leverage toxicity detection models (like
Perspective API or a fine-tuned BERT on insult/hate data) to flag personal
attacks. Use NER to find person names or pronouns and check nearby
sentiment. A rule-based approach: maintain a list of negative adjectives
(idiotic, lazy, corrupt, etc.) and see if they are applied to a person (using
dependency parse to find [Person] + copula + [insult] structures, e.g.,
“He is a fraud”). ML approach: fine-tune a classifier for ad hominem vs
neutral on debate transcripts or comments labeled for personal attacks. In
addition, detect name-calling, which overlaps with ad hominem: labeling
someone with negative terms arxiv.… . The output could be a binary flag
and a score (e.g., severity based on toxicity probability).
Recommended Toolkits: spaCy for NER and dependency (to link insults to
targets); HuggingFace Transformers (e.g., a RoBERTa model fine-tuned on
Jigsaw Toxic Comments for toxicity detection); Perspective API as an
external service (provides a toxicity score). Also, use lists from hate speech
lexicons for quick checks.
Pseudo-code:
Python Run
insults = ["idiot", "stupid", "liar", "fool", "corrupt", "ignorant", "crazy"]
doc = nlp(text)
for ent in doc.ents:
if ent.label_ == "PERSON":
# Check words around the person entity for insults

window = doc[max(0, ent.start-3): min(ent.end+3, len(doc))]
if any(token.lower_ in insults for token in window):
flags["ad_hominem"] = True
# Additionally, use a toxicity classifier on sentences
toxic_model = pipeline("text-classification", model="unitary/toxic-bert")
for sent in doc.sents:
score = toxic_model(sent.text)[0]['score']
if score > 0.9 and 'PERSON' in [ent.label_ for ent in sent.ents]:
flags["ad_hominem"] = True
This pseudo-code checks for insults near person names and also runs a
toxicity model on each sentence containing a person. The combination
reduces false positives. An advanced system might separate direct insults
at opponent from generic name-calling propaganda, but both are captured
here as ad hominem tactics.
Red Herring
Statistical Signature: A red herring is a diversion — introducing
irrelevant information or tangents to distract from the main issue.
Statistically, the text will contain a segment that is off-topic relative to the
rest of the content. One measurable sign is a topic shift: e.g., using LDA
(Latent Dirichlet Allocation) or another topic model, one might find an
outlier topic in one paragraph that doesn’t match the overall theme.
Another clue is abrupt change in named entities or keywords (e.g., an
article about healthcare suddenly discusses an unrelated scandal mid-way).
Cohesion metrics drop when a red herring is present (the coherence
between consecutive sentences is lower than average).
NLP/ML Implementation: Use a topic modeling or embedding-based
similarity: split the article into segments (paragraphs), compute
embeddings (using sentence transformers or TF-IDF vectors). If one
segment’s similarity to the main topic (e.g., first paragraph or title) is very
low, flag it as a potential red herring. Additionally, use keyword overlap – if
a section has many new entities not seen elsewhere, it might be off-topic.
On the ML side, you can train a classifier to detect known red-herring
patterns (the SemEval propaganda task combined Red Herring with Straw
Man mdpi.… , which suggests treating it similarly to strawman by pattern).
Another approach: check if a question is posed and then the answer drifts
away (common in interviews or political Q&A where a tangential answer is a
red herring). An NLI model can also help: if the segment does not logically
follow from the previous context (it neither entails nor contradicts – just
irrelevant), that irrelevance might be flagged.

Recommended Toolkits: Gensim or sklearn LDA for topic detection;
Sentence-BERT for embedding similarity between segments (to detect
outlier content); spaCy for text segmentation and entity extraction. For
logical irrelevance, HuggingFace NLI models can classify pairs of sentences
as entailment/neutral/contradiction – a red herring would often come up as
neutral (unrelated) when comparing a suspect sentence with the article’s
thesis.
Pseudo-code:
Python Run
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
sentences = [sent.text for sent in doc.sents]
embeddings = model.encode(sentences)
# Compute similarity of each sentence to the first sentence (assumed main topic)
main_emb = embeddings[0]
for i, emb in enumerate(embeddings[1:], start=1):
sim = util.cos_sim(main_emb, emb)
if sim < 0.2: # very low similarity
flags["red_herring"] = True
break
This example marks a red herring if any sentence is very dissimilar to the
introduction. In practice, you might compare each section to the overall
article vector (e.g., average embedding) or use clustering to find an odd
cluster. A more explicit check: if a segment contains entities/keywords not
elsewhere in the piece, and isn’t elaborated upon, it could be a diversion.
Combining these methods gives a robust detection of red herrings.
Slippery Slope
Statistical Signature: A slippery slope argument claims that a relatively
small first step will inevitably lead to a chain of related events culminating
in a significant (usually negative) effect. The signature is a causal chain
expressed in the text, often using conditional language (“if we allow A, then
B will happen, then ultimately Z”). We can detect an unusual frequency of
conditional connectors (if, then, leads to, results in) and extreme outcome
words (disaster, chaos, etc.) in close proximity. Another statistical cue:
future-tense or modal verbs (will, would, could) tied to escalating scenarios.
If a single sentence or consecutive sentences have multiple cause-effect
relations or events in sequence, that’s a hallmark of a slippery slope
sigann.gith… sigann.gith… .

NLP/ML Implementation: Use dependency parsing or semantic role
labeling to identify cause-effect statements. Check if the text contains a
cascade: e.g., “If X, then Y” and within Y clause mention another
consequence. A rule-based detector can look for “if/when X, then Y”
patterns and flag if Y is an extreme scenario not necessarily warranted by
X. We can also use frame semantics: the CAMPFIRE project used a frame
for slippery slope requiring identifying the initial trigger and the final
outcome sigann.gith… . On the ML side, train a classifier on examples of
slippery slope arguments (which often contain keywords like “spiral into,”
“chain reaction,” etc.). An alternative is to use generative ML: prompt a
large language model to identify if an argument is assuming an
unwarranted chain reaction. However, a reliable approach is a rule/ML
hybrid: find conditional statements and then use a classifier to judge if it’s a
slippery slope or a reasonable prediction.
Recommended Toolkits: spaCy or Stanza for dependency parsing (to
extract conditional clauses and their consequences); AllenNLP for semantic
role labeling (to identify cause and effect phrases); HuggingFace
Transformers (a fine-tuned model on logical fallacy data for slippery slope
detection if available). Even without a specific model, an NLI approach can
check if X truly entails Y – a slippery slope often has Y that does not logically
follow from X (so an NLI model might classify it as neutral or low-
confidence entailment, hinting at a logical leap).
Pseudo-code:
Python Run
import re
slippery_phrases = ["if", "then", "would lead to", "sooner or later", "inevitably"]
text_lower = text.lower()
if "if" in text_lower and re.search(r"\bwill happen\b|\bwould result\b|\blead to\b",
# Check for multiple sequential conditional markers
if text_lower.count("if") > 1 or text_lower.count("then") > 1:
flags["slippery_slope"] = True
# Or use dependency parse:
for sent in doc.sents:
if any(tok.lower_ == "if" for tok in sent) and any(tok.lower_ in ["will", "would"
# A crude check: conditional + strong modal
flags["slippery_slope"] = True

The above is a heuristic: it flags text that contains an “if… then … will …”
structure, especially if chained. In a more refined system, we would extract
the condition and outcome, then possibly query a knowledge base or use
logical reasoning to see if the outcome is indeed far-fetched. If the leap is
large (e.g., “allowing cats -> everyone will own an alligator” sigann.gith… ),
that’s a slippery slope. The system can highlight the chain of events
detected.
Transparency Gaps
Statistical Signature: Transparency gaps occur when important details
about sources, data, or methods are omitted. Quantitatively, this might
manifest as a high number of claims or allegations with no attribution. For
example, many sentences might use passive voice or vague subjects (“It is
known that…”, “Experts believe…”) without stating who knows or believes
it. A simple metric is the attribution ratio: the fraction of factual
statements that contain an explicit source or evidence. If this ratio is low
(many facts stated, few sources given), there’s a transparency gap.
Another clue: usage of passive constructions (e.g., “[Something] was done”
with no agent mentioned) can be counted via grammatical analysis.
NLP/ML Implementation: Use part-of-speech and dependency analysis to
find claims (sentences with factual assertions) and check if they contain a
citation, a quote, or a named source. SpaCy can identify reporting verbs
and whether they have a subject (e.g., “[source] reported that…” vs just “It
is reported that…”). Implement a rule: flag sentences with patterns like “It
is said that…”, “Some people claim…”, “Studies show…” that do not cite
which study or person arxiv.… . For ML, one could train a model to classify
sentences as well-sourced vs lacking source. Additionally, a question
generation + search approach: for each claim, attempt to find a source
(like a reference or footnote or known fact). If the system consistently fails
to find sources for claims, that indicates opacity.
Recommended Toolkits: spaCy for parsing and pronoun/reference
detection; prose.io or textstat for reading voice detection (to find passive
voice frequency); HuggingFace Transformers for a question-answering or
fact-checking model (like a FEVER fact-check system) to verify if a
statement is supported by an external source. If a fact-check model often
responds with “citation needed”, that’s a sign of missing transparency.
Pseudo-code:
Python Run

import textstat
passive_count = textstat.passive_voice_count(text)
sentences = [sent.text for sent in doc.sents]
unattributed = 0
for sent in sentences:
# simple check: contains a fact-indicator but no source
if re.search(r"\b(study|experts?|research|report)\b", sent.lower()) and not re.se
unattributed += 1
transparency_gap_score = unattributed / len(sentences)
if transparency_gap_score > 0.2 or passive_count > X: # X = passive threshold
flags["transparency_gaps"] = True
The code counts sentences that refer to studies/experts or use quotes
without attribution. If more than 20% of sentences have such issues
(threshold adjustable), we mark transparency gaps. The passive voice
count is also considered (if content heavily uses passive voice to hide the
actor, e.g., “was decided” instead of who decided it). Combined, these
metrics catch lack of transparency in how information is obtained.
Cherry Picking
Statistical Signature: Cherry picking is selecting only favorable evidence
while ignoring counter-evidence. Statistically, the text may cite data points
all aligning to one conclusion with no mention of contrary data. This is hard
to quantify internally without external knowledge, but some cues include:
repeated use of one type of evidence (e.g., only anecdotes or only statistics
that support X), or citing multiple facts all on one side of an issue. An
imbalance score can be computed: if an article presents N supporting
facts for its thesis and 0 opposing facts when opposing evidence is known
to exist (which might be inferred from general knowledge or other
sources), that’s cherry-picking. Internally, one might measure diversity of
sources or viewpoints: low diversity (e.g., all quotes from one side) is a hint.

NLP/ML Implementation: This likely requires comparing the content to an
external baseline (like other reports on the same topic) to see what’s
omitted. One approach: use a knowledge graph or database to see if key
facts are missing. For instance, if an article praises a policy citing only
successful cases, a fact-check module could query if there were failures not
mentioned. If the answer is yes, likely cherry-picking. In absence of external
data, use stance detection: if the article is strongly one-sided (all
sentences have the same stance toward a topic, with no acknowledgement
of alternative views), flag it. Implementation: classify each sentence’s
sentiment or stance on the main issue; if 100% are positive (or negative)
with zero counterpoints, the article may be cherry-picking evidence.
Another heuristic: look for words like “only” or “no mention of” in a meta-
sense (though the latter is tricky). ML approach: a classifier could be trained
on pairs of articles – one balanced, one cherry-picked – to identify patterns
(balanced ones might use contrastives like “however” and present both
sides). Lacking direct training data, rule-based and external checks are
primary.
Recommended Toolkits: HuggingFace for stance detection models (e.g.,
classify each sentence as pro, con, or neutral regarding the topic); Google
Knowledge Graph or WikiBrowser for retrieving known facts on the topic;
OpenAI GPT (if allowed) to summarize what’s missing compared to general
knowledge. Tools like the FEVER fact-checking dataset could help
identify if claims ignore contradictory evidence.
Pseudo-code:
Python Run
# Pseudo-approach: count distinct sources or perspectives
perspectives = {"pro": 0, "con": 0}
topic = determine_main_topic(doc) # e.g., by keywords or title
for sent in doc.sents:
stance = stance_classifier.predict(sent.text, topic) # returns "pro", "con", or
if stance in ["pro", "con"]:
perspectives[stance] += 1
# If one side is heavily represented and the other is zero, likely cherry-picking
if perspectives["pro"] > 0 and perspectives["con"] == 0:
flags["cherry_picking"] = True
if perspectives["con"] > 0 and perspectives["pro"] == 0:
flags["cherry_picking"] = True

This assumes a function to get the main topic and a stance classifier per
sentence. For example, if the article is about a drug’s effectiveness and
every fact is pro-drug with no mention of any study that showed issues, the
detector flags it. In a full system, we might integrate a database of known
counter-evidence: e.g., if the content claims “Studies A, B show positive
results” but does not mention Study C which had negative results (and the
system knows about Study C from elsewhere), that’s cherry-picking. Such
integration requires a knowledge base and is complex, but even a within-
text stance uniformity check is a useful indicator.
Data Accuracy
Statistical Signature: Data accuracy issues manifest as incorrect or
implausible statistics, dates, names, etc. A straightforward approach is to
attempt to verify every factual claim. The “signature” is not internal to the
text but comes from cross-checking with trusted data sources. However,
internally, signs of inaccurate data can include contradictory numbers
within the text or extreme values with no source. Another metric:
numerical consistency – if the text contains multiple numbers referring to
the same thing but they don’t match (e.g., “the budget was $5 million” in
one place and “the budget was $7 million” later), that indicates inaccuracy
or inconsistency.
NLP/ML Implementation: Use an automated fact-checking pipeline. For
each factual claim (extract using a tool like AllenNLP’s IE or regex for
numbers/dates), query an external knowledge base (Wikipedia API,
DBpedia, or a fact-check model) to see if the claim is supported or refuted.
For example, if the text says “Crime rose by 50% in 2022”, the system can
query reliable statistics; if the result doesn’t match, flag potential
inaccuracy. There are pre-trained models (e.g., based on the FEVER
dataset) that classify a claim and evidence as
Supported/Refuted/NotEnoughInfo. Use those: feed claim, get a score for
refuted. Additionally, use internal consistency checks: run NLI on pairs of
statements within the article to catch any contradiction involving data (e.g.,
one sentence says X happened in 1990, another says 1992 – an NLI model
might catch that as contradiction).

Recommended Toolkits: HuggingFace Transformers – models like
facebook/bart-large-mnli for NLI (to detect internal contradictions about
facts) and models like uclnlp/bert-tiny-fever or ynie/roberta-large-
snli_mnli_fever_anli_R1_R2_R3-nli for fact verification against Wikipedia.
The Google Fact Check Tool API or the Wikidata Query Service can also
retrieve known facts. Diffbot Knowledge Graph or OpenAI GPT with
browsing can be used if external calls are allowed. Implementing a custom
module that uses search (via Bing API or similar) to find the claim and see if
authoritative sites confirm it is also viable.
Pseudo-code:
Python Run
import requests
from transformers import pipeline
nli_model = pipeline("text-classification", model="facebook/bart-large-mnli")
claims = extract_factual_claims(doc) # e.g., find sentences with numbers or assertiv
for claim in claims:
# Try simple Wikipedia API check
res = requests.get(f"https://api.duckduckgo.com/?q={claim}&format=json").json()
summary = res.get("AbstractText", "")
if summary:
# Compare claim with summary using NLI
premise = claim
hypothesis = summary[:1000] # take a portion of summary (limit length)
result = nli_model(premise + " </s></s> " + hypothesis)
if result[0]['label'] == 'CONTRADICTION':
flags["data_accuracy"] = True
This simplified approach uses a search (here DuckDuckGo’s API for brevity)
to get an abstract, then checks for contradiction. In a real system, a more
rigorous approach is needed: possibly use a specialized fact-check model or
integrate with known datasets (e.g., if the claim matches an item in a
verified database, mark correct; if not, flag). The pseudo-code above just
illustrates an automated cross-check. For speed, one might maintain a
cache of common facts or use an offline knowledge graph.
Logical Flow

Statistical Signature: Logical flow refers to the orderly progression of
ideas. Poor logical flow may indicate manipulation (the author is jumping
around or evading a coherent line of reasoning). A way to quantify flow is
via discourse coherence metrics. For example, one can measure how
well each sentence transitions to the next using cosine similarity of
sentence embeddings or using coherence models (like an entity grid). A
sudden drop in similarity or an unexpected discourse marker (e.g.,
“Nonetheless” used inappropriately) can signal a break in logical flow.
Another measure: count of discourse markers and whether they align (if
“however” appears but the content following doesn’t actually contrast
anything, that’s a logical inconsistency).
NLP/ML Implementation: Use a coherence model: e.g., train a model on
well-written vs disjoint texts to score coherence. A simpler implementation
is pairwise similarity: generate embeddings for consecutive sentences and
compute their cosine similarity. Calculate the average or minimum
similarity; very low values indicate a potential gap in logic. Additionally,
check for contradiction or irrelevance with NLI between adjacent sentences
– if one doesn’t follow from the other (either neutral or contradiction), the
logical flow might be broken. One can also parse for discourse relations
using a library like pyRST (Rhetorical Structure Theory parser) to see if
relations like Elaboration, Cause, Contrast are properly used. If the
structure is chaotic (e.g., random shifts without proper discourse relation),
flag it.
Recommended Toolkits: spaCy or transformers (sentence-transformers)
for sentence embeddings; NLTK or Coherence Models for entity-grid
(though that’s older tech, it’s still insightful); AllenNLP’s discourse parser or
rstlite for RST parsing. For implementation ease, the embedding approach
using Sentence-BERT is effective to catch logical jumps. Also, HuggingFace’s
Cohere or other coherence evaluators if available.
Pseudo-code:
Python Run
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L12-v2')
sens = [sent.text for sent in doc.sents]
cos_sims = []
for i in range(len(sens)-1):
u = model.encode(sens[i])
v = model.encode(sens[i+1])
sim = util.cos_sim(u, v)
cos_sims.append(float(sim))

avg_sim = sum(cos_sims) / len(cos_sims) if cos_sims else 1.0
if avg_sim < 0.1 or min(cos_sims) < some_low_threshold:
flags["logical_flow"] = False # indicate logical flow is broken
else:
flags["logical_flow"] = True
In this pseudo-code, extremely low similarity between some adjacent
sentences triggers a warning. For example, if most similarities are ~0.8 but
one pair is 0.0, there’s likely a logical disconnect there. This can be
augmented by checking the text around that point for known non sequiturs
or red herrings. We might also incorporate a check for proper use of logical
connectors: e.g., if a sentence starts with “Therefore” but no clear premise
before it, that’s a logical flow error.
Conflict/Contradiction Detection
Statistical Signature: A text containing contradictory statements is a
strong indicator of poor credibility or bias (the narrative is not consistent
with itself). The signature is the presence of two or more statements that
logically cannot all be true. This can be measured by scanning all pairs (or
semantically related pairs) of claims for mutual contradiction. A practical
metric: count how many pairs of sentences are flagged as contradictions by
an NLI model. If any non-trivial contradictions exist, set a contradiction flag.
The percentage of contradictory statements vs total statements could be a
measure (though usually even one contradiction is significant).
NLP/ML Implementation: Use an NLI (Natural Language Inference)
model to evaluate sentence pairs. Specifically, take each declarative
sentence (or each claim extracted) and compare with others on the same
topic (you can filter by shared entities or subjects to reduce pairwise
comparisons). If the NLI model outputs “contradiction” with high confidence
for any pair sigann.gith… , you’ve found an internal conflict. Another
approach: use a knowledge-based reasoner for specific contradictions (like
temporal ones: if one sentence says “X happened in 2020” and another
says “X happened in 2021” – a simple date check can catch that).
Implement both semantic (NLI) and heuristic (keyword-based) contradiction
checks.
Recommended Toolkits: HuggingFace NLI pipeline (e.g., using roberta-
large-mnli or facebook/bart-large-mnli ); spaCy or Diffbot for knowledge
extraction (to catch contradictions like two different values for the same
property). Tools like DeCLUTR or Sentence-BERT can cluster similar
sentences, then you only run NLI within clusters of related content (more
efficient than all pairs).

Pseudo-code:
Python Run
from transformers import AutoModelForSequenceClassification, AutoTokenizer
model = AutoModelForSequenceClassification.from_pretrained("roberta-large-mnli")
tokenizer = AutoTokenizer.from_pretrained("roberta-large-mnli")
sentences = [s.text for s in doc.sents]
contradictions = 0
for i in range(len(sentences)):
for j in range(i+1, len(sentences)):
# Only compare if the sentences share a subject or named entity, for efficien
if any(ent in sentences[j] for ent in re.findall(r"[A-Z]\w+", sentences[i]))
pair_input = tokenizer(sentences[i], sentences[j], return_tensors='pt', t
logits = model(**pair_input).logits
# logits index: 0=entailment,1=neutral,2=contradiction for roberta-mnli
if logits.argmax().item() == 2: # contradiction
contradictions += 1
if contradictions > 0:
flags["contradiction"] = True
This brute-force approach checks each pair containing a common named
entity or capitalized term (a heuristic to catch related statements). If any
contradiction is found, we mark it. In a production system, we would refine
by focusing on key claims (maybe extracted with an IE tool) rather than all
sentences. Still, NLI is a powerful method to catch conflicts where humans
might miss them. This helps ensure the content isn’t internally inconsistent.
False Dilemma (Black-and-White Fallacy)
Statistical Signature: A false dilemma presents only two extreme options
when more possibilities exist (black-and-white thinking). The linguistic
signature is the use of either/or constructions or language that implies
“there are only two choices”. For instance: “We either ban technology X or
face catastrophe” is a false dichotomy if alternatives exist. Count the
occurrences of “either X or Y” and look for absence of nuance words (such
as “maybe, sometimes, partial” which would indicate recognition of middle
ground). Another metric: measure modality diversity – if only absolute
modals (must, never, always) are present and no hedging, the argument
might be framing a binary choice.

NLP/ML Implementation: Use regex or parsing to detect either…or
patterns and no other option phrases (“no choice but to”, “the only way”). A
rule-based check: if “either” or “neither” appears, ensure it’s in the context
of a choice; if yes, likely a dilemma is being posed. Also flag “if not X then
Y” type constructions that ignore alternatives. For ML, classify sentences for
black-and-white thinking vs nuanced. A dataset like the propaganda one
has Black-and-White Fallacy labeled mdpi.… . A fine-tuned classifier on
those examples (if available) can detect more implicit dichotomies. Another
tip: search for extreme antonyms used (good/evil, with us/against us) – that
polarizing language often accompanies false dilemmas.
Recommended Toolkits: spaCy for dependency (to identify “either” as a
conjunction); HuggingFace for a model fine-tuned on fallacy detection (if
you train one or use something like roberta-large-mnli in a creative way by
checking if combining the two half statements yields neutral – not directly
applicable, better to just classify). Even without training, a list of phrases is
effective. For example, the presence of “only if” or “cannot have it both
ways” might be explicitly coded.
Pseudo-code:
Python Run
dilemma_phrases = ["either", "no other", "only if", "the only way", "with us or again
text_low = text.lower()
false_dilemma_flag = False
if " either " in text_low and " or " in text_low:
false_dilemma_flag = True
for phrase in ["no other choice", "no alternative", "either way", "only option"]:
if phrase in text_low:
false_dilemma_flag = True
if false_dilemma_flag:
flags["false_dilemma"] = True
This catches explicit either/or and “no alternative” wording. We would refine
by making sure it’s genuinely presenting a limited choice (the context often
makes it clear). If a transformer model is used, you’d feed the sentence
into it and get a probability of Black-and-White Fallacy. As noted in
research, Black-and-White Fallacy (false dilemma) is a recognized category
mdpi.… that one can detect similarly to other propaganda techniques.
Circular Reasoning

Statistical Signature: Circular reasoning occurs when the conclusion of
an argument is also used as a premise with no real support (A because A).
This is tricky to catch statistically because it involves semantic equivalence
between statements. A possible signature is repetition of key phrases or
ideas as justification. If the text’s claim and evidence are essentially the
same (perhaps reworded), then it’s circular. One can measure similarity
between statements that are connected by causal or explanatory
connectors (because, therefore). If the similarity is above a threshold, it
might be the conclusion restating the premise. Also, the presence of
tautological phrases (“it is what it is”, or defining something by itself) could
be flagged.
NLP/ML Implementation: Identify argument structures: for example, use
an argument parser to identify conclusion and supporting statement. Then
use semantic similarity (embedding or lexical overlap) to see if they mirror
each other. A rule: if a sentence contains “because” or “since” and the
parts on both sides share many words or synonyms, suspect circular
reasoning. For ML, a specialized model might be needed – few datasets
explicitly label circular reasoning. One could create a heuristic training set:
e.g., generate sentences like “X is true because X is true” variations and
train a classifier. Alternatively, use a language model to detect if an
explanation is essentially repeating the claim (LLMs sometimes can detect
tautologies). Another approach: check if the argument has zero external
evidence – if claim and justification have high overlap and no new
information introduced, flag it.
Recommended Toolkits: spaCy for dependency (to break on “because”
clauses); WordNet or embeddings to detect if two clauses are semantically
equivalent. HuggingFace Transformers: possibly use a question-answering
approach – ask the model “Why does the author claim X?” and see if the
answer is basically X, which indicates circular logic. This is experimental but
could reveal lack of real evidence.
Pseudo-code:
Python Run
import difflib
circular_flag = False
for sent in doc.sents:
if 'because' in sent.text.lower():
parts = sent.text.split('because')
if len(parts) >= 2:
premise = parts[1]
conclusion = parts[0]

# simple similarity check
sim = difflib.SequenceMatcher(None, premise.strip().lower(), conclusion.s
if sim > 0.7:
circular_flag = True
if circular_flag:
flags["circular_reasoning"] = True
This checks if content after “because” is very similar to content before it. A
more advanced check would account for synonyms (using WordNet or
embedding similarity rather than raw string similarity). For example, “We
must trust the leader because he is trustworthy” – premise and conclusion
share the root trust. That would be caught by a high similarity or by
explicitly noticing the premise uses the claim’s key concept (trust). The
system can also track the main claim of an article and see if any supporting
point simply repeats it in different words.
Overgeneralization (Hasty Generalization)
Statistical Signature: Overgeneralization happens when a broad
conclusion is drawn from limited examples (e.g., “My two neighbors are
loud, so all people in this town are loud”). The signature is the presence of
absolute language (all, every, never) used to generalize, often following a
specific anecdote or small sample. Counting universal quantifiers (all,
everyone, no one, none, always, never) gives a clue sigann.gith… . If such
words appear immediately after a narrow evidence (like one example or
one data point), it suggests a hasty generalization. Another metric:
measure the ratio of sample size mentioned to the population described – if
the text mentions one instance but concludes about "everyone", that ratio
is essentially 1:N (with N large), a red flag.
NLP/ML Implementation: Use regex to detect sweeping statements (e.g.,
“all plural are something”, “X always Y”). Use dependency/constituency
parse to identify subject quantifiers. If an absolute quantifier is used and
there was no prior broad evidence, flag it. We might combine this with an
earlier unsupported quantifiers check (coming later) since both involve
detecting quantifiers without backup. ML approach: train a classifier for
hasty generalization on fallacy-labeled data (CAMPFIRE corpus includes
Hasty Generalization sigann.gith… ). The model would likely learn patterns like
presence of universals and singular evidence. Additionally, an argument
mining approach: identify if the argument jumps from specific to general
with no intermediate logic (which could be done by checking if any general
evidence was provided – e.g., other data points or statistics).

Recommended Toolkits: spaCy for token analysis (to find quantifiers and
nouns following them); NLTK or regex for pattern matching common
overgeneralization forms. If using ML, a fine-tuned transformer on logical
fallacies (if available) or zero-shot classification with a prompt like “Is this
statement an overgeneralization?” could be attempted with GPT-based
models (with caution).
Pseudo-code:
Python Run
overgeneral_flag = False
generalizers = ["all ", "everyone", "no one", "never", "always", "none of"]
for sent in doc.sents:
text = sent.text.lower()
if any(text.startswith(gen) or f" {gen}" in text for gen in generalizers):
# Check if previous sentence or same sentence provided multiple examples; if
if not re.search(r'\bfor example\b|\bsuch as\b|\bdata\b|\bstudy\b', text):
overgeneral_flag = True
if overgeneral_flag:
flags["overgeneralization"] = True
This flags sentences that contain universal quantifiers without nearby
phrases indicating evidence or examples. For instance, “Everyone knows
that product X is a failure” with no supporting data would trigger this. The
logic could be expanded: track if earlier sentences gave a basis (like if one
sentence mentions two cases, and next says “therefore all cases are like
that” – that transition can be caught by connecting sentences with
coreference or causal connectives). The CAMPFIRE example “My cat is
black, so all cats are black.” sigann.gith… clearly matches this pattern.
False Causality (Correlation vs Causation)

Statistical Signature: False causality (or causal oversimplification) is
concluding that A causes B just because A and B correlate or occurred
sequentially. The signature is use of causal language (“because”, “leads to”,
“as a result”) linking things that might not have a proven causal relation.
Statistically, count the number of causal connectors (because, therefore,
hence, due to, consequently). Then evaluate if evidence for causation is
provided (like an experiment or scientific explanation). If causal terms are
high but sources are lacking or the relationship is dubious (for example, an
unrelated temporal link: “After X happened, Y happened, so X caused Y”),
flag it. Also, oversimplification often involves singular causes for complex
issues (e.g., “The economy fell because of that one policy”), ignoring other
factors. So detecting phrases like “the sole reason” or “nothing else but” is
another clue.
NLP/ML Implementation: Use dependency parsing or semantic role
labeling to extract causal relations (subject, verb, object in cause-effect
context). Then apply knowledge or logical checks: for instance, if the
relation is “A causes B” but known domain knowledge or data would say it’s
more complex, mark it. In practice, implement a rule: if a sentence uses a
causal connector and either (a) it’s just a temporal sequence (“after”) or
(b) it’s a stretch (we might need to rely on external knowledge or at least
the improbability of the link, which is hard algorithmically). Another
approach: use an NLI model as a causal consistency check – for example,
ask the model if “A causes B” is entailed by known facts or by a larger
context. If not, and no evidence given, it’s likely false causality. ML
classification: the propaganda taxonomy has Causal Oversimplification as a
category mdpi.… , so a classifier can be trained to detect it. It might pick up
on keywords plus context (lack of nuance or multiple causes).
Recommended Toolkits: spaCy or AllenNLP for event and cause
extraction (AllenNLP’s OpenIE might label causal relations); HuggingFace
Transformers to fine-tune on causal fallacy detection. Also, Cause-effect
pairs dataset if available can help train or validate. For external verification,
Google Scholar or knowledge base to see if a claimed cause is established
by experts (though that’s advanced).
Pseudo-code:
Python Run
causal_markers = ["because", "due to", "as a result", "resulted in", "led to"]
false_cause_flag = False
for sent in doc.sents:
text = sent.text.lower()

if any(marker in text for marker in causal_markers):
# If "because" is used, check if it's simply linking two events that might ju
# Simple heuristic: if "because" connects two clauses both containing past te
if " because " in text:
clauses = text.split(" because ")
if len(clauses) >= 2:
clause1, clause2 = clauses[0], clauses[1]
if re.search(r"\b(VBD|VBN)\b", " ".join(token.tag_ for token in nlp(c
re.search(r"\b(VBD|VBN)\b", " ".join(token.tag_ for token in nlp(c
false_cause_flag = True
# Also flag oversimplification phrases
if re.search(r"\bsole reason\b|\bnothing else\b", text):
false_cause_flag = True
if false_cause_flag:
flags["false_causality"] = True
This pseudo-code flags sentences where “because” connects two past-
tense events (which often is just chronological correlation being misused as
causation) and phrases that imply a single cause. In a refined system, we’d
also integrate domain knowledge: e.g., if someone writes “Vaccines caused
the stock market crash,” the system alone can’t know it’s false without
external info, but it can flag that such a causal claim is suspicious if no
evidence is given. Hence coupling this with the data accuracy/fact-check
module is wise: check if authoritative sources support the causal claim; if
not, mark it as misleading causality.
Equivocation
Statistical Signature: Equivocation is using an ambiguous term in
multiple senses, making an argument misleading. The signature is a term
that appears multiple times with different meanings or contexts.
Statistically, one approach is to detect polysemous words (words with
multiple meanings) that are key to the argument and see if the contexts
differ. If a keyword’s embedding in one part of the text is very different
from its embedding in another part, the term might be used equivocally.
Another possible metric: high word sense diversity – using Word Sense
Disambiguation (WSD) on repeated keywords. If the WSD yields different
senses for the same word in different places, that’s equivocation.

NLP/ML Implementation: Identify important terms (nouns or noun
phrases central to the argument). Use a WSD tool or context embedding to
determine the sense each time the term is used. If a term’s sense changes
in the course of argument (e.g., “public interest” used first as curiosity and
later as benefit of the public), the system flags it. A simpler method: use
WordNet: for each occurrence of the word, get synonyms from context; if
sets of synonyms differ significantly between occurrences, suspect
equivocation. ML approach: not many off-the-shelf classifiers for
equivocation, but one could attempt a custom approach: e.g., train a model
to detect if a word is being redefined or used inconsistently. In practice,
focusing on the lexicon and semantic similarity differences is more
straightforward.
Recommended Toolkits: NLTK or spaCy WordNet integration for sense
disambiguation; BERT embeddings – since BERT embeddings for the same
word in different sentences will differ if senses differ. We can cluster
embeddings of the same word from different parts of the text: if they fall
into two distinct clusters, that suggests two senses. There are also libraries
like pyWSD or AlanNLP WSD for explicit sense identification.
Pseudo-code:
Python Run
from nltk.corpus import wordnet as wn
equivocate_terms = []
# Find top N frequent content words
words = [token.lemma_.lower() for token in doc if token.pos_ in ("NOUN","VERB","ADJ"
freq = Counter(words)
for term, count in freq.items():
if count > 1:
contexts = []
for sent in doc.sents:
if term in sent.text.lower():
contexts.append(sent.text)
# Attempt to get distinct synsets for the term in each context
synsets_used = set()
for ctx in contexts:
# naive: take first sense that fits at least one word from context
for syn in wn.synsets(term):
if any(word in syn.definition() for word in ctx.split()):
synsets_used.add(syn.name())
break
if len(synsets_used) > 1:
equivocate_terms.append(term)
if equivocate_terms:

flags["equivocation"] = True
This is a heuristic attempt: it collects contexts for each frequent term and
tries to guess synsets being invoked. If more than one synset is found, the
term might be used equivocally. In reality, a better way is to use contextual
embeddings: compute the embedding of the term in each context (say
using BERT), then cluster them. If two clusters form, that indicates two
meanings. Regardless, if flagged, the system can report which terms might
be ambiguous. The analyst or an AI could then further inspect if it’s
deliberate equivocation or just normal language use.
Anecdotal Evidence
Statistical Signature: Anecdotal evidence is using personal stories or
isolated examples as proof of a general claim. The signature includes first-
person references (“I”, “we”) or specific case descriptions, often with vivid
detail, followed by a general statement. We can quantify the presence of
personal pronouns and narrative style (past tense verbs, descriptive
language) preceding or following a broad claim. Also, if a paragraph starts
with a story (e.g., a single incident) and later the article concludes
something general without additional data, that’s largely anecdotal support.
Count of anecdotes: we might detect quotation marks or named individuals
(non-public figures) which often indicate a personal example.
NLP/ML Implementation: Identify segments that likely contain anecdotes:
use regex for story-like patterns (“One time, …”, “A [person] from [place]
experienced …”) or check for presence of personal pronouns and past
tense. Tag these segments. Then see if those segments are used as
evidence: e.g., followed by language like “this shows that [generalization]”.
A rule: if a singular example is directly followed by a universal claim, flag
anecdotal evidence misuse. ML approach: fine-tune a classifier to detect
anecdotal vs empirical evidence sentences. Or use a sequence labeling to
mark sentences as anecdote, claim, evidence. The presence of anecdote
without other evidence yields a flag. Also, an NLI approach: treat the
anecdote as premise and the general claim as hypothesis – obviously an
anecdote cannot fully entail a generalization, so an NLI model might label
that as neutral, indicating that the general claim isn’t logically proven by
the anecdote.

Recommended Toolkits: spaCy for part-of-speech (to find personal
pronouns, past tense verbs), HuggingFace for a model like GPT-3 fine-tuned
on identifying narrative vs analytic text, or use OpenAI’s GPT-4 with a
prompt to identify if something is an anecdote (if that were allowed in the
pipeline). For a simpler route, maintain a list of anecdotal introduction
phrases (“In my experience,” “I remember when,” “A friend of mine…”).
Also, quote extraction can help: news often include an anecdotal quote
from a person – if the conclusion relies on that quote alone, it’s anecdotal
evidence.
Pseudo-code:
Python Run
anecdotal_flag = False
anecdote_markers = ["I remember", "we once", "one time", "a story", "a case where", "
for sent in doc.sents:
text = sent.text.lower()
# Check if sentence looks like first-person or specific story
if text.startswith("i ") or any(marker in text for marker in anecdote_markers):
anecdotal_flag = True
anecdote_sent_index = sent.i
# Check the next sentence for a broad claim (universal quantifier or conclusi
if anecdote_sent_index + 1 < len(doc.sents):
next_sent = doc.sents[anecdote_sent_index + 1].text.lower()
if re.search(r"\btherefore\b|\bthis shows\b|\bthus\b|\ball\b|\beveryone\b
flags["anecdotal_evidence"] = True
This code flags if a sentence appears to be personal/anecdotal and the
following sentence generalizes (thus, … or uses “all/everyone”). We set an
anecdotal_flag in general if any anecdote is present, but only raise the final
flag if it’s used to draw a general conclusion. In a full system, even
anecdotal stories not followed by overt generalizations might be noted as a
bias technique (because anecdotes sway emotions), but the most
concerning is when they are used in lieu of data.
Appeal to Tradition/Appeal to Novelty

Statistical Signature: An appeal to tradition argues something is good
because it’s traditional (“we’ve always done it this way”), while an appeal to
novelty argues something is good because it’s new (“the latest = the best”).
The signature is the presence of keywords relating to age or novelty in a
value-laden way. For tradition: words like “time-honored, classic, traditional,
longstanding” near positive evaluations. For novelty: “new, innovative,
cutting-edge” near positive evaluations. We can count occurrences of such
keywords and check context: e.g., “has been used for centuries” as a
justification, or “the newest model is automatically better”. A spike in such
terms could indicate these fallacies.
NLP/ML Implementation: Use lexicons for tradition and novelty appeals.
Create two small dictionaries: one for tradition (old, traditional, classical,
etc.) and one for novelty (new, modern, revolutionary, latest). Scan the text
for these. If found, see if they are part of argumentative statements (for
example, followed by a claim of superiority or used as reasoning: “since it’s
traditional, it must be good”). One can also use sentiment analysis: these
appeals often couple the word with a positive sentiment. If “traditional X” or
“modern X” correlates with a positive tone without other justification, flag it.
ML approach: classify sentences as appeal to tradition, appeal to novelty, or
neither, using a fine-tuned model (training data would be needed, possibly
from argumentation mining or fallacy datasets). Zero-shot classification
could also be attempted by prompting a model with labels "tradition,
novelty, none".
Recommended Toolkits: spaCy or regex for keyword spotting;
HuggingFace zero-shot classifier (e.g., facebook/bart-large-mnli treating
"appeal to tradition" as a label, though that’s not foolproof). Possibly
fastText with manually labeled examples if doing a quick custom classifier.
But likely simple pattern matching suffices for many cases.
Pseudo-code:
Python Run
tradition_markers = ["tradition", "traditional", "time-honored", "long-standing", "ag
novelty_markers = ["new", "innovative", "cutting-edge", "latest", "modern"]
for sent in doc.sents:
text = sent.text.lower()
for t in tradition_markers:
if t in text:
if re.search(r"\b(good|better|best|superior|must)\b", text):
flags["appeal_to_tradition"] = True
for n in novelty_markers:
if n in text:

if re.search(r"\b(good|better|best|improved|excellent)\b", text):
flags["appeal_to_novelty"] = True
This flags a sentence if, say, "traditional" and a positive adjective appear,
suggesting the argument "traditional = good". Similarly for "new". We also
might look for comparative language like “as we always have, and it
worked” or “the old ways are the best ways”. Those could be added
patterns. This simplistic check might overflag some cases (e.g., "traditional
dish" in a neutral context), so in production you’d refine by focusing on
usage in argumentation (maybe only consider if “because it’s traditional”
explicitly appears). Nonetheless, pattern-based detection for these appeals
is usually effective since the keywords are distinctive.
False Attribution
Statistical Signature: False attribution involves citing an authority or
source that is either misquoted, out of context, or not actually supporting
the claim. This is hard to see from text alone, but clues include: quotes with
no clear source, or famous names cited for things they never said.
Statistically, one could count quotes and references and see if they have an
associated source mention (e.g., a name or publication). If a quote is in
quotes but no speaker is given (e.g., “Blah blah,” but no “said [name]”),
that’s suspicious. Another signature: authoritative names used oddly (like
referencing a known person in a context that doesn’t fit their known
expertise or timeline).
NLP/ML Implementation: Use NER to find person names around
quotation marks or statements of the form “According to X”. If X is cited,
verify if X is a known authority in that field (which could require a
knowledge base lookup). Also, verify quotes via external search: e.g., if the
text says Einstein said something, check via an API if that quote is
documented. If not found, mark potential false attribution. Another
approach: maintain a database of misattributed quotes (there are known
ones) to catch those. ML approach: fact-checking models on quotes – feed
the quote and supposed source to a model that can retrieve if that source
indeed said it. This overlaps with fact-checking tools (like those used in
rumor detection). Additionally, style cues: if many claims are attributed to
vague entities (“a scientist said that…”) without naming, that’s more of a
transparency issue, but also a form of weak attribution. Flagging those
instances can be part of this.

Recommended Toolkits: spaCy NER to get quotes and entities; Wikiquote
API or Google to verify known quotes; HuggingFace retrieval QA models
(like ktrapeznikov/albert-xlarge-v2-squad-v2 etc.) to see if the quote can be
found. If building an internal system, integrate a quote verification service.
For mis-attributed data (like claiming a study says X when it doesn’t), one
could incorporate a document retrieval to find the study by title and check
content. That’s complex, so initial implementation might just flag suspicious
patterns (no source given, or source context mismatch).
Pseudo-code:
Python Run
import re
quotes = re.findall(r'“([^”]+)”', text) # extract content inside quotation marks
for quote in quotes:
# Check if quote is followed by attribution like - Name or Name said
if re.search(r'”\s*(?:-|—)?\s*\w', text):
# crude check: if a dash or said isn't present after quote
continue
else:
flags["false_attribution"] = True
# Additionally, if specific attributions exist, verify via search (pseudo):
for ent in doc.ents:
if ent.label_ == "PERSON" and "said" in ent.sent.text.lower():
# e.g., "Einstein said that ...";
claim = ent.sent.text
# pseudo external check, e.g., call a search API (not implemented here)
if not verify_claim_with_source(ent.text, claim):
flags["false_attribution"] = True
The above first loop flags quotes with no attribution. The second part
sketches verifying an attributed claim with an external function (which
could search a database to see if that person actually said that or supports
that claim). Implementing verify_claim_with_source would involve hitting an
external knowledge service. For demonstration, one might simply flag if the
person is famous and the statement sounds out-of-character (which could
be too advanced). In real deployment, hooking into a fact-check knowledge
base is ideal to truly catch false attributions.
Motive Fallacy (Questioning Motives)

Statistical Signature: A motive fallacy dismisses an argument by
attacking the motive of the arguer rather than the argument’s content
(e.g., “You only say that because you would benefit”). The signature
phrases include “just because” (implying an ulterior motive), “only
because,” “they have an agenda,” etc. It often appears as accusations of
bias: “The study concludes X, but the researchers are funded by Y”. While
pointing out conflict of interest can be valid, in fallacy form it ignores the
actual evidence. We look for language that attributes intent or bias as a
counter-argument. Statistically, count occurrences of “because you…” or
“because they…” where it’s not giving factual cause but implying self-
interest. Also, terms like “agenda,” “vested interest,” “for your own gain.”
These indicate motive attacks.
NLP/ML Implementation: Use pattern matching for common
constructions: “only saying that because…,” “just want to…,” “trying to
[benefit]”. Use dependency: find “because” clauses where the subject is
“you” or a group and the clause contains a motive (money, power, etc.). A
sentiment approach: such statements often have a negative or accusatory
tone directed at a person or group (overlap with ad hominem but
specifically focusing on intent). For ML, train a classifier to detect motive
attacks using argumentation datasets if available. Alternatively, a two-step
approach: identify when a statement is used as a rebuttal (maybe track
that it comes after someone else’s claim) and contains a motive keyword.
Another approach: use NLI to test if the rebuttal actually addresses the
claim or just the person – if the rebuttal does not logically refute the
content of the claim (but instead is about the person), it could be flagged.
Recommended Toolkits: spaCy for pronoun resolution (to know “you”
refers to the arguer possibly) and dependency for cause clauses;
HuggingFace for sentiment or classification (there might not be a pre-
trained for motive fallacy, but one could fine-tune or zero-shot it). Possibly
transformers pipeline for emotion could detect a tone of
suspicion/accusation. But more direct is lexicon+pattern.
Pseudo-code:
Python Run
motive_markers = ["only because", "just because", "only want", "agenda", "vested inte
for sent in doc.sents:
text = sent.text.lower()
if any(marker in text for marker in motive_markers):
if "you " in text or "they " in text or "he " in text or "she " in text:
flags["motive_fallacy"] = True

This looks for typical motive attributions. Example it would catch: “He
supports the policy only because he’s paid to.” If needed, refine to ensure
it's actually dismissing an argument (maybe check if previous sentence was
that person’s argument, but in a single article context, often the author is
asserting someone’s motive to discredit them). So context could be
considered. Another hint: presence of financial or personal gain terms in
argument (money, fame) near a person or group reference. Combining all
such cues should effectively detect motive-based fallacies.
Loaded Language
Statistical Signature: Loaded language involves using words with strong
emotional connotation (positive or negative) to influence the audience
arxiv.… . The signature is a high density of adjectives or adverbs that carry
subjective or extreme sentiment (e.g., “disastrous failure,” “glorious
triumph,” “ridiculous policy”). A metric is the Loaded Language Score:
e.g., the percentage of words that are in a loaded lexicon. Also, the
variance in sentiment might be high (some extremely positive sections,
extremely negative others). If nearly every noun has an attached
emotionally charged adjective, that’s a clear sign.
NLP/ML Implementation: Create a lexicon of loaded terms or use an
existing one (e.g., the Connotation Lexicon or subjective lexicon). Count
their occurrences. Additionally, use sentiment analysis: a neutral factual
piece should have moderate sentiment, while propaganda with loaded
language will have very high magnitude sentiment (either direction). Thus,
compute sentiment polarity and intensity for each sentence; if many
sentences are very positive or very negative in tone, mark loaded
language. ML approach: The propaganda detection models (like BERT fine-
tuned) have Loaded Language as one of the easiest classes to detect
sigann.gith… because it correlates with obvious lexical features. You can
fine-tune a classifier to identify spans of loaded language (as done in
SemEval 2020 Task 11). Even simpler: use a pre-trained model’s output if
available (some systems output which words are propaganda-loaded
words). If you prefer ML directly, a logistic regression on TF-IDF could even
catch this, since it’s largely about specific words.
Recommended Toolkits: spaCy for part-of-speech tagging (to isolate
adjectives/adverbs), NRCLex or VADER for sentiment scores; HuggingFace
Transformers (fine-tuned on propaganda spans or use a model like
sknfer/propaganda-techniques if it exists) for classification. The Propaganda
Detection Project released data for loaded language identification
arxiv.… which could be used to train a model.

Pseudo-code:
Python Run
loaded_count = 0
loaded_lexicon = {"disaster", "outrageous", "shameful", "triumphant", "so-called", "r
for token in doc:
if token.text.lower() in loaded_lexicon:
loaded_count += 1
loaded_ratio = loaded_count / len(doc)
if loaded_ratio > SOME_THRESHOLD:
flags["loaded_language"] = True
# Alternatively, using sentiment intensity
from textblob import TextBlob
polarities = [TextBlob(sent.text).sentiment.polarity for sent in doc.sents]
if sum(1 for p in polarities if abs(p) > 0.5) > X:
flags["loaded_language"] = True
The lexicon method flags if more than, say, 3-5% of words are highly
connotative. The sentiment method flags if more than X sentences have
strong sentiment. The values of threshold can be tuned (perhaps based on
reference corpora). In practice, combining both is good: lexicon for known
strong terms plus a model to catch context-dependent ones. For instance,
“This brutal policy is an assault on our rights” would light up via lexicon
(brutal, assault) and sentiment (very negative). Loaded language is one of
the most straightforward to detect due to its “clear linguistic signature”
sigann.gith… .
Glittering Generalities
Statistical Signature: Glittering generalities are vague, positive terms or
slogans used to evoke approval without specifics fiveabl… propagandac… .
The signature is the use of abstract virtue words (e.g., freedom, justice,
honor, innovation, prosperity) without concrete detail. These often appear
in slogans or campaign phrases. Statistically, detect the presence of such
words and check if they are not backed by specifics. A high count of
abstract nouns with positive connotations in the absence of explanatory
context yields a high glittering generality score. For example, “We stand for
freedom, progress, and unity” – all feel-good words, little substance.

NLP/ML Implementation: Use a predefined list of “virtue words”. For
each occurrence, see if the text around them contains concrete
information or just uses them standalone. If a virtue word is in the same
sentence as another vague term or just linked by “and” in a list, that’s a
clue (like the example with freedom, progress, unity). Implement a rule: if a
sentence is composed mostly of abstract positive words and lacks any
specific policy or fact, flag it. Also, detect slogans (short sentences that
read like taglines). ML approach: a classifier can be trained on propaganda
text to identify “glittering generality or slogan” usage – indeed Slogans was
a category in propaganda datasets mdpi.… . A model could differentiate
between meaningful statements vs platitudes by context (likely the
presence of data vs none). But simpler is lexicon + check for lack of
content words (like numbers, proper nouns etc.).
Recommended Toolkits: spaCy for POS tagging (to identify abstract
nouns, though distinguishing abstract vs concrete nouns might need a list
or WordNet check); WordNet to see if a noun is an intangible concept;
regex for uppercase slogans (sometimes slogans have title case or
exclamation). Possibly transformers fine-tuned on propaganda can directly
output a label for glittering generalities if trained on that category.
Pseudo-code:
Python Run
virtue_words = {"freedom", "liberty", "justice", "honor", "integrity", "prosperity",
for sent in doc.sents:
text = sent.text
vw_count = sum(1 for w in virtue_words if re.search(rf"\b{w}\b", text, re.IGNOREC
# If sentence is short (slogan-like) or just a string of virtue words, flag
if vw_count >= 2 and len(text.split()) < 15:
flags["glittering_generalities"] = True
elif vw_count >= 1:
# check if those words are explained or just presented
if not re.search(r"\bbecause\b|\bfor example\b|\bsuch as\b", text):
# no explanation present
flags["glittering_generalities"] = True

This flags if a sentence has multiple virtue words and is short (likely a
slogan), or even one virtue word that is not elaborated (no “because/for
example” indicating detail). For example, “Fighting for Freedom and
Justice!” would trigger easily (2 virtue words, short). Meanwhile, “We need
economic justice because current disparities...” might not be flagged due to
the because (indicating elaboration). This approach may overflag a bit, but
it’s a starting point. Fine-tuning with actual examples of glittering
generalities from a corpus (maybe political speeches) could refine the
lexicon and thresholds.
Name Calling (Labeling)
Statistical Signature: Name calling is applying a negative label to a
person or group, often a simplistic one (e.g., “traitor,” “radical,” “loser”). It
overlaps with ad hominem, but name-calling is more about tagging
someone with a loaded label to discredit them arxiv.… . The signature is the
presence of derogatory or pejorative nouns (or short noun phrases)
directed at a target. Statistically, count occurrences of known epithets or
negative labels, especially capitalized ones used as nicknames (e.g., calling
a politician “Crooked X” as a label). Also, check if a person’s name or group
is directly followed by a disparaging noun/adjective.
NLP/ML Implementation: Use a lexicon of common insults and slurs
(similar to ad hominem detection). Additionally, use context: if Name +
appositive comma + negative label appears (e.g., “Pelosi, a liar, …”), that’s
name-calling. Or the [derogatory label] [group] (e.g., “the idiots in
congress”). Use dependency: find noun compounds or subj–pred
complement structures like “[Person] is a [slur]”. The implementation is
largely rule/lexicon-based. ML can help by classifying whether a phrase is a
name-calling instance (there are data in propaganda detection for Name
Calling/Labeling). A fine-tuned model on those could identify more subtle
cases (like sarcastic ones or where the label is not a traditional “insult” but
still negative context). Combine with toxicity detection as used in ad
hominem.
Recommended Toolkits: spaCy for dependency and NER (to find persons
and link adjectives/nouns describing them); HuggingFace for any pre-
trained propaganda classifier covering name-calling; lexicon resources like
Hatebase for slurs, or just compile from common usage. The earlier ad
hominem approach covers personal insults; here we ensure to cover also
political labeling (e.g., calling someone a “socialist” or “elitist” in a
pejorative sense). That might require context to see if it’s derogatory or just
factual. But often tone or pairing with negative adjectives clarifies it.

Pseudo-code:
Python Run
name_calling_labels = {"liar", "hypocrite", "idiot", "buffoon", "criminal", "crook",
for ent in doc.ents:
if ent.label_ in ["PERSON", "ORG", "NORP"]: # person, organization, or group
# check token immediately after entity for "is a X" pattern
span_end = ent.end
if span_end < len(doc) and doc[span_end].lemma_ == "be": # e.g., is/was
if span_end+1 < len(doc) and doc[span_end+1].lemma_.lower() in name_calli
flags["name_calling"] = True
# check if entity is followed by a comma and a label
if span_end < len(doc) and doc[span_end].text == ",":
# e.g., "Senator Y, a traitor, ...", look two after comma
if span_end+2 < len(doc) and doc[span_end+1].lemma_ in ["a","an","the"] a
flags["name_calling"] = True
This checks two common forms: “[Entity] is a [label]” and “[Entity], a
[label],”. It uses a small list of labels which can be expanded. For group
labels (NORP stands for nationalities, religious or political groups in spaCy),
if we see something like “All [group] are [negative term]”, that overlaps with
hate speech detection – but that is name-calling toward a group (and also
overgeneralization). We could reuse the overgeneralization detection to
catch “All <group> are traitors” as both. In practice, one might unify these
detectors, but we keep them separate for clarity. The result is any flagged
instance marks the text as using name-calling.
Card Stacking
Statistical Signature: Card stacking is a propaganda technique of
presenting only information positive to your side and omitting contrary
information (similar to cherry-picking, but often refers to stacking a one-
sided argument high with supporting data). Statistical signs: one-sided use
of facts, possibly indicated by an imbalance in sentiment or slant when
describing two sides of an issue. For example, if an article describes one
party with all positive descriptors and the opposing party with all negative
descriptors, that’s card stacking via tone. A metric: sentiment or adjective
bias by entity. If you track each named entity (person, org) and score the
sentiment of sentences about them, card stacking would show one entity
consistently described positively, another consistently negatively. Another
indicator: lack of balance in sources (all sources from one side). If for an
issue you expect two sides, but only one side’s quotes or data are present,
that’s card stacking. This overlaps with cherry-picking and omission bias.

NLP/ML Implementation: Implement an entity sentiment analysis: for
each major entity or viewpoint, compute sentiment score of surrounding
text. If all mentions of Entity A are positive and all of Entity B are negative,
that’s suspicious. Or if only Entity A is mentioned with data and Entity B’s
perspective is never mentioned (omission). Another approach: classify the
article’s stance and see if it acknowledges counter-arguments – if not, likely
card stacking. One can also simply measure if multiple data points are
given on one side vs none on the other. ML approach: multi-label
classification for propaganda often doesn’t have a separate label “card
stacking,” but we can combine signals from cherry-picking, omission, and
loaded language to infer it. Possibly train a model on synthetic data where
one side’s info is systematically removed. But likely better to use feature-
based logic.
Recommended Toolkits: spaCy for NER and coreference (to gather all
mentions of an entity), HuggingFace sentiment models to get polarity of
sentences referencing that entity. Also, Cross-document analysis if needed
(though for a single document, we can still check balance within that doc).
Possibly Graph analysis: build a bipartite graph of {entities mentioned} vs
{positive/negative words around them}, see if distributions differ strongly
for different entities.
Pseudo-code:
Python Run
entity_sentiment = {} # e.g., {"EntityName": [list of sentiment scores]}
for ent in doc.ents:
if ent.label_ in ["PERSON","ORG","NORP"]:
# find the sentence or phrase describing this entity
sent = ent.sent
# get sentiment (simple: TextBlob or a HF model)
polarity = TextBlob(sent.text).sentiment.polarity
entity = ent.text
entity_sentiment.setdefault(entity, []).append(polarity)
# Now analyze distribution
if entity_sentiment:
# Compute average sentiment per entity
avg_sent = {e: sum(scores)/len(scores) for e,scores in entity_sentiment.items()}
if len(avg_sent) >= 2:
# check if one entity has avg >0.5 and another < -0.5 for example
vals = list(avg_sent.values())
if max(vals) > 0.5 and min(vals) < -0.5:
flags["card_stacking"] = True
# Also, count number of distinct sources/quotes for different sides (if known side af

This code looks at sentiment by entity. For example, if “Policy A” or the
government is consistently described with negative words (polarity -0.8
avg) and the opposition not mentioned or if mentioned, maybe positive, it
flags. The threshold and logic can be refined, but the idea is to catch strong
disparity. Additionally, if the context allows identifying two camps (e.g., pro
vs con), we’d check evidence distribution (like all facts support one camp).
That could be done by topic modeling each paragraph to see if only one
viewpoint is present. The simpler approach shown combined with cherry-
picking detection covers much of card stacking detection.
Guilt by Association
Statistical Signature: Guilt by association smears someone by linking
them to an unpopular person/group/idea, rather than addressing their own
actions. The signature pattern is “X is connected to Y (bad thing), therefore
X is tainted.” Linguistically, look for mentions of a subject together with a
negative entity in a context implying similarity or connection. Phrases like
“ties to,” “in the same camp as,” “associated with,” combined with known
negative labels or individuals. Also comparisons: “He’s the next Hitler”
(Reductio ad Hitlerum is a form of this, explicitly listed with Bandwagon in
propaganda categories mdpi.… ). So, presence of very negative
comparisons (especially to universally reviled figures or groups) is a strong
signal.
NLP/ML Implementation: Use NER to catch named entities in the same
sentence or phrase, especially if connected by words like “with, ally of,
friend of, linked to.” If one of the entities has a generally negative
connotation (could use a list of known negative entities like terrorist groups,
or check if the entity is described negatively elsewhere in text), then flag
guilt by association. Another approach: sentiment towards the second
entity is strongly negative, and they are mentioned in context of the first
entity, implying negativity rubs off. ML classification: the concept is niche,
but one could label training examples of guilt by association statements
(like “The candidate has been seen with members of the extremist group
X”) to train a model. Alternatively, treat it as a combination of entity linking
and sentiment analysis. Possibly use a knowledge base to see if that
association is irrelevant (like if the link is tenuous historically). But simpler:
rely on phrase patterns and known demonized groups.

Recommended Toolkits: spaCy for entity parsing and dependency
(subject-object relations); Hate groups lists or similar to identify if an entity
is a commonly vilified one. HuggingFace could be used with zero-shot
classification by labeling a statement as “association fallacy” (though not
guaranteed to be robust). Patterns might suffice for many cases.
Pseudo-code:
Python Run
guilt_association_terms = ["ally of", "associated with", "linked to", "connected to",
bad_entities = {"Hitler", "Nazis", "terrorist", "criminal", "mafia", ...} # expand w
for sent in doc.sents:
text = sent.text
for term in guilt_association_terms:
if term in text:
# If sentence contains "X [term] Y"
# Identify entities around the term
before, after = text.split(term, 1)
# Take last word of before, first word of after as entity names (simplist
ent1 = before.split()[-1]
ent2 = after.split()[0]
if ent2.rstrip('.,?!') in bad_entities or ent1.rstrip('.,?!') in bad_enti
flags["guilt_by_association"] = True
This simplistic snippet splits on association terms to find entities. A more
robust method: use spaCy’s dependency to find if a proper noun is subject
and another is object of “associate/link” verb or connected via a prep like
“with X”. If one of the entities is recognized as negative (either by list or by
context sentiment), then flag. For example, “He hangs out with terrorists” –
ent1=He , term="with" , ent2=terrorists (which is in bad_entities list). That
flags guilt by association. Note: Reductio ad Hitlerum (“X is like Hitler”)
specifically can be caught if “Hitler” or “Nazi” is mentioned; that’s
practically always a guilt-by-association or extreme smear, so we could
explicitly flag any comparison to Hitler/Nazi as a form of association fallacy
mdpi.… .
Scapegoating

Statistical Signature: Scapegoating is blaming a person or group for
problems they did not solely cause. The signature is frequent mention of a
particular group in contexts of blame or negative outcomes. A quantitative
marker: high co-occurrence of a group name with negative verbs (caused,
ruined, responsible for) and problems. Also, one group being singularly
identified as the cause across multiple issues. For example, an article
repeatedly saying “Immigrants are to blame for X,” “Immigrants caused Y,”
etc. If the same target is blamed in multiple sentences or contexts, that’s
scapegoating. We can measure how often a particular entity is the subject
of sentences that have negative sentiment or problem keywords.
NLP/ML Implementation: Identify target groups (common scapegoated
groups could be immigrants, minorities, etc., but any entity could be
scapegoated). Then check context: is that entity often syntactically the
subject of negative actions or the object of blame phrases (like “blamed
for”, “the reason for our troubles”)? Use dependency: look for constructs
[Entity] + (aux) + blame/cause/ responsible + [problem]. Alternatively,
check if an entity is near words indicating problems (crime, unemployment,
etc.) in multiple sentences. ML approach: content that scapegoats often has
a distinctive tone – one could fine-tune a model on examples of
scapegoating statements vs neutral statements about a group. But a rule-
based approach using sentiment and frequency might suffice. If a group is
mentioned with significantly negative sentiment consistently, and especially
if language implies causation of woes, flag scapegoating.
Recommended Toolkits: spaCy for dependency and NER (especially to
differentiate if the entity is plural group vs individual, scapegoating often
targets groups); HuggingFace sentiment or a hate-speech classifier
(scapegoating often overlaps with targeted hate speech). Possibly Targeted
Sentiment Analysis tools which give sentiment towards a specific entity in
text (there are research models for that). If the targeted sentiment towards
group X is very negative in many instances, then scapegoating is
happening.
Pseudo-code:
Python Run
problem_words = ["crime", "unemployment", "crisis", "problem", "fault", "job loss", "
scapegoat_targets = {}
for sent in doc.sents:
# Find if any group entity is in sentence
targets = [ent.text for ent in sent.ents if ent.label_ in ["ORG","NORP","GPE"]]
if not targets:

continue
text = sent.text.lower()
if any(word in text for word in ["blame", "responsible for", "cause of", "fault o
for tgt in targets:
scapegoat_targets[tgt] = scapegoat_targets.get(tgt, 0) + 1
else:
# Also if target is subject of a negative verb or problem context
for tgt in targets:
if any(p in text for p in problem_words):
# crude: if a problem word is present with target
scapegoat_targets[tgt] = scapegoat_targets.get(tgt, 0) + 1
# If any target has multiple attributions of blame
for tgt, count in scapegoat_targets.items():
if count >= 2: # appears in blame context multiple times
flags["scapegoating"] = True
metadata["scapegoat_target"] = tgt
This code maps entities to how many times they are blamed or in problem
contexts. If an entity (especially a group) is blamed multiple times, we flag
scapegoating. Threshold 2 means at least two instances, which is a sign of
a pattern. In application, you might filter out if that entity is indeed
responsible (which requires external knowledge), but scapegoating often
has exaggerated breadth (blaming one group for many issues). The system
could output that "Group X appears to be scapegoated for various
problems" using this info.
Whataboutism
Statistical Signature: Whataboutism deflects criticism by bringing up a
different issue as a distraction or comparison (“What about Y?” when X is
under discussion). The hallmark signature is a direct question or statement
starting with “What about [something unrelated]?”. Also phrases like “How
about…?” used as a retort. It can also appear as tu quoque (you too)
arguments: “You criticize X, but you do Y”. Statistically, count occurrences
of the phrase “what about”. If found in a context where it shifts topic, that’s
a direct catch. Also, look for sentences that start with “What about” or “And
[other subject]?” in contexts of debate. Another signal: a question that
doesn’t actually get answered or tied back, indicating it was just thrown out
to derail.

NLP/ML Implementation: Use straightforward pattern detection for
"what about". If found, likely it's whataboutism, as that phrase is not often
used except in that rhetorical way. Also detect tu quoque structure: e.g.,
“How can you complain about X when Y (that you did)?”. That might not
always have "what about" literally, but could be “you did Y as well”. For ML,
classify sentences or exchanges as whataboutism if they contain those
patterns – could fine-tune on debate transcripts or online discussions known
for that. A rule combined with a bit of semantic check: see if the question
topic is different from current topic. That could be done by comparing the
nouns in the "What about Y" question to the nouns in previous context. If
largely disjoint, definitely a change of topic.
Recommended Toolkits: Regex for "what about"; spaCy for topic
modeling or noun extraction to compare topics; maybe HuggingFace for an
NLI or similarity check to confirm the introduced topic is off-course. But
honestly, simply catching "what about [noun]" covers many cases. We
should also cover phrasing like "And [other issue]?". If building a robust
system, include variations ("what of", "how about").
Pseudo-code:
Python Run
whatabout_flag = False
sentences = [s.text for s in doc.sents]
for i, sent in enumerate(sentences):
low = sent.lower().strip()
if low.startswith("what about") or low.startswith("and what about"):
whatabout_flag = True
# also check for direct counter-accusation
if re.match(r"^you (also )?did", low):
whatabout_flag = True
if whatabout_flag:
flags["whataboutism"] = True
This flags any sentence beginning with "What about". For example, “What
about the other side of this issue?” would match. The second check is a
simple tu quoque catch: "you did ..." at start of a sentence (like "You do it
too"). In a single article context, direct "you" might not appear unless
quoting, but if analyzing a dialogue or op-ed addressing someone, it could.
The main hallmark is the literal phrase “What about”, which is usually
enough to identify whataboutism in text.
Gaslighting

Statistical Signature: Gaslighting is making someone doubt their own
perception or sanity, often through persistent denial, misdirection,
contradiction, or lying. In text, look for phrases that directly invalidate or
belittle the audience’s or another’s experiences (e.g., “That never
happened,” “you’re just imagining things,” “don’t be so sensitive,” etc.). The
signature is second-person statements that dismiss the other’s viewpoint or
memory. Also general denial phrases in response to an accusation. Another
metric: high frequency of phrases implying the other party is confused or
overreacting. Gaslighting often occurs in dialogue; in media content, it
might appear as quotes or a narrative that suggests critics are crazy or
events widely reported didn’t happen as reported.
NLP/ML Implementation: Use a set of known gaslighting phrases (there
are lists from psychology literature, e.g., “you’re crazy,” “no one will believe
you,” “I never said that,” etc.). Scan the text for these. Also look for a
pattern: someone makes a claim and the response is an absolute denial
plus an attack on their perception (this requires dialogue context, which a
news article might not have unless quoting someone). If analyzing opinion
pieces or interviews, you can split speaker segments and apply it. ML
approach: possibly treat it as a form of abusive language detection
specifically targeting credibility. A classifier could be trained on
conversational data labeled for gaslighting (if such exists, or synthetic
generation). But a lexicon-based approach catches blatant instances.
Recommended Toolkits: Regex or keyword search for classic gaslighting
lines; Perspective API for attributes like flippant or dismissive, though not
sure if that exists. HuggingFace Transformers: one could attempt a zero-
shot classification with a label "gaslighting" for suspicious sentences, but
better to rely on direct phrases. Also, context analysis: if a sentence
contradicts known facts (like widely known truth) while calling the opponent
crazy, that’s a sign, but identifying that automatically is tough. Focus on
direct linguistic cues.
Pseudo-code:
Python Run
gaslighting_phrases = [
"you're being paranoid", "you're crazy", "that never happened",
"you're imagining things", "don't be so sensitive", "no one will believe you",
"you're overreacting", "it's all in your head"
]
for sent in doc.sents:
low = sent.text.lower()
for phrase in gaslighting_phrases:

if phrase in low:
flags["gaslighting"] = True
This straightforward approach flags any sentence that contains a known
gaslighting phrase. If the content is an article describing someone
gaslighting (e.g., The official responded, "You're just imagining that"), it
would trigger. There is a risk that an article might report someone
gaslighting (which still might be worth flagging, as it highlights manipulative
behavior being quoted). We assume we flag anyway, since the engine’s
goal is to detect presence of such tactics in the content, whether it’s the
author or a quoted source using them. The flagged segments can then be
reviewed by analysts or further logic to see context.
Source Opaqueness
Statistical Signature: Source opaqueness is when sources of information
are not clearly disclosed. It overlaps with transparency gaps, but specifically
focuses on citations and references. A signature metric is the Unnamed
Source Count: count how many times sources are referenced vaguely
(e.g., “experts say,” “a source close to X,” “it has been reported”) versus
named. If the count of vague references is high relative to concrete
attributions, the content is source-opaque. Another statistic: the ratio of
direct quotes to attributions – if many quotes lack a named speaker, that’s
opaqueness. Also, usage of phrases like “reportedly,” “sources say,” etc.,
which allow the writer to assert things without accountability.
NLP/ML Implementation: Use regex to find common anonymous source
phrases: “experts say”, “scientists claim”, “analysts believe” without
naming who. Also “according to a study” without giving which study. Check
for the presence of at least a partial detail (like an institution or author)
after “according to”. If not, flag. Similarly, find “reportedly” or “it is
reported” which are passive references. Implement a rule counting these.
Another angle: if the article has many claims but few citations (footnotes,
hyperlinks, or references), measure that. In news articles, citations might
not be explicit, but quotes from named people count as sources. So count
quotes with “said [Name]” vs quotes with no attribution. ML approach:
classify the article on a scale of sourcing quality – a model could be trained
on known high-quality journalism vs dubious ones to learn if sources are
properly named (features might include presence of proper nouns after key
verbs). But pattern-based is reliable here.

Recommended Toolkits: Regex/spaCy for pattern matching (looking for
“say/said/report” etc. in passive or anonymous form). Possibly use
newspaper3k or similar libraries for extracting links or references if any
(some articles link sources; if none are present, that’s one hint of
opaqueness). But not all media content has explicit links even if well-
sourced (they might just mention the source in text).
Pseudo-code:
Python Run
opaque_count = 0
opaque_patterns = [
r"\bexperts say\b", r"\bobservers say\b", r"\banalysts believe\b",
r"\bits (is|was) reported\b", r"\bsources say\b", r"\breportedly\b",
r"\baccording to a (study|report|source)\b"
]
for pattern in opaque_patterns:
matches = re.findall(pattern, text, flags=re.IGNORECASE)
opaque_count += len(matches)
# Also count total number of "said [Name]" attributions for comparison
named_sources = len(re.findall(r"said\s+[A-Z][a-z]+", text))
if opaque_count > 0 and named_sources == 0:
flags["source_opaqueness"] = True
elif opaque_count > named_sources:
flags["source_opaqueness"] = True
This counts some typical phrases. If opaque references outnumber clear
ones, flag it. For example, if we see multiple “experts say” and not a single
name of an expert or study, definitely opaque. If there’s a mix, one could
still flag but maybe consider a threshold. We combine both absolute and
relative signals here. This might mark content that heavily relies on
unnamed authority, which is a transparency red flag.
Conflict of Interest Indicators

Statistical Signature: Conflict of interest (COI) indicators are often meta-
data or context, not always explicit in text. But textual signs: the piece may
not disclose relationships (no disclosure statement present when there
should be), or it might have unusual positivity toward something the author
is tied to. One hint: if the author or outlet is known (from external data) to
be affiliated with a subject of the article, and that article is biased, that’s a
COI. Internally, look for first-person plural referencing an organization (“we
at Company X”) in what purports to be a neutral article – that’s a sign of
vested interest. If an article uses overly promotional language about an
entity without stating it’s sponsored or authored by that entity, that’s
suspicious. This is hard to detect from text alone without external
metadata. But one thing we can do: integrate a knowledge base of known
ownerships or political ties. E.g., if an article about Tobacco has the author
in a tobacco lobby group, or the outlet is funded by tobacco companies,
that’s a COI – but we need external data. So an indicator would be lack of
expected disclosure: e.g., if it’s an opinion piece about a company but no
“Disclosure: I work for that company” appears, might be missing. Not
straightforward to quantify, but maybe check if article has a section or note
like “Disclosure” or “Disclaimer”. If not and the topic suggests it should (like
heavy promotion of a product by someone likely related), flag possibility.
NLP/ML Implementation: This likely requires connecting the article’s
metadata (author name, publication) to external info. A practical
implementation: maintain a database of known media biases or affiliations
(e.g., outlet X is owned by Y). If the article is praising Y or attacking Y’s
competitor, that’s a potential COI. Another: parse the author bio or byline
for clues (if provided). If the text is an opinion piece (detect by style or
byline saying "Opinion"), check if author’s background matches the content
and if not disclosed. Without external data, we might look for internal clues
like unnatural promotion. Possibly treat it as part of bias: if extremely one-
sided praise, consider COI or undisclosed sponsorship. But that overlaps
with propaganda detection. Because COI is more about who is writing and
why, which text analysis alone can’t fully reveal. We can just note that
integration with external data (author profiles, ownership info) is
recommended. For now, maybe implement a placeholder: e.g., if the article
heavily praises or defends a single entity beyond normal, and uses first
person or insider tone, mark COI.

Recommended Toolkits: Media Bias/Fact Check databases for outlet bias;
Wikidata for ownership of media. Spacy for author extraction from HTML
(some scraping needed possibly). If building a full system, incorporate a
module that checks the source (which might be done outside text analysis
but part of pipeline).
Pseudo-code:
Python Run
# Pseudo: if we have metadata
if article.author and article.topic_entity:
if knowledge_base.is_affiliated(article.author, article.topic_entity):
flags["conflict_of_interest"] = True
# Without metadata, use textual heuristic:
if "we" in text.lower()[:200] and article.title and article.title.lower().strip().sta
# If it's an opinion and uses 'we' referring to an organization or project, possi
flags["conflict_of_interest"] = True
This is mostly pseudo since we assume a knowledge_base with affiliation
info. For example, if John Doe wrote it and John Doe works for Company A,
and the article praises Company A, we flag. Achieving that automatically
requires integration with external data. The second part checks if the piece
is explicitly opinion and uses 'we' (implying the author is part of the group
being written about). Not foolproof but an heuristic. Ultimately, COI
detection is more of a meta-analysis task. In our system architecture, this
might be a separate component that uses metadata (see System
Architecture below).
Omission Bias

Statistical Signature: Omission bias is presenting information in a way
that omits crucial facts that would change the interpretation. It’s hard to
“see” what’s omitted in one article alone, but statistical hints include:
extremely unbalanced coverage of an issue (e.g., covering only events
favorable to one narrative, none of the opposing events). One measure
could be comparing the content to a checklist of expected points. For
example, for a known story, if a key element appears in most sources but
not in this one, that’s an omission. This again often needs cross-source
analysis. Internally, one might guess omission if the article is suspiciously
silent on obvious counterpoints (like a scandal piece that never mentions
the defendant’s rebuttal). If we have a database of important facts for a
topic, we can see if any are missing. Another approach: if the article’s
Claim-to-Evidence ratio is high (lots of claims, little evidence), it implies
omission of supporting evidence or context – though that also fits other
categories.
NLP/ML Implementation: A realistic implementation uses multi-
document analysis: gather several articles on the same event (via search or
news API) and do a comparison to identify what this article did not mention.
That’s complex but doable: use named entity and event extraction from
multiple sources, and highlight entities/events present in others but not in
this one. Those might be omissions. For within-article detection, you can
incorporate general knowledge: e.g., if article is about a study’s result and
doesn’t mention limitations that are typically mentioned, that could be
omission bias. But detecting that requires knowing the domain. An
alternative: measure how thoroughly the piece answers the basic
journalistic questions (who, what, where, when, why, how). If some are
missing where expected, maybe something’s omitted. That’s an indirect
guess.
Recommended Toolkits: News API + Python difflib or set operations to
compare content of multiple articles. HuggingFace summarization or QA to
see if a known question about the event can be answered by the article – if
not, maybe that info was omitted. This is advanced and not purely NLP on
one text. Perhaps mention that an aggregation layer in the system could
handle this. For single-document analysis, we might skip a concrete
implementation beyond noting lack of contrary info (which we did in cherry-
picking and card stacking).
Pseudo-code (Cross-Doc idea):
Python Run

# Given article text and assuming we have a function to get related docs
related_docs = get_similar_articles(article.title)
key_ents = set(ent.text for ent in doc.ents if ent.label_ in ["PERSON","ORG","GPE","E
for other in related_docs:
other_doc = nlp(other.text)
other_ents = set(ent.text for ent in other_doc.ents if ent.label_ in ["PERSON","O
missing = other_ents - key_ents
# If other article mentions something (person/event) not in this one that seems c
if missing:
omission_cues.update(missing)
if omission_cues:
flags["omission_bias"] = True
metadata["omitted_points"] = list(omission_cues)
This approach fetches related docs (maybe by searching the title or a
summary) and compares named entities/events. If many other sources
mention "Investigation" or "opposition response" and our article does not,
that's a clue. One has to filter trivial differences. But if a person like the
main opponent or a key location is missing, it might be biased omission.
This requires external data; our final system architecture will mention a
Cross-Document Analysis module for such features.
Statistical Manipulation
Statistical Signature: Statistical manipulation includes using figures in a
misleading way (e.g., cherry-picked stats, improper comparisons, graphs
with misleading axes if visual, etc.). In text, signs include presenting
statistics without context (like a percentage without absolute numbers),
using comparisons that are not apples-to-apples, or using big numbers
without baseline. A metric: count how many statistics (numbers, %) are
present and check for context around them (like “out of [total]”). If
numbers are given without denominators or time frames, that might be
manipulative. Also, extreme precision or overly broad stats (like "up 300%!"
with no baseline – that is a known trick). Another clue: mismatched
statistics (one part uses percentage, another uses absolute in an
inconsistent manner to emphasize a point).

NLP/ML Implementation: Use regex to extract all numbers and % signs.
For each, see if context contains baseline indicators (like “from last year” or
“of the population”). If not, possibly misleading. Also look for cherry-picked
time frames: words like “record-breaking” but not specifying the window
can mislead. A rule could identify if a percentage is used without an
absolute reference (like “crime rose 50%” should mention from what to
what, if not, suspicious). ML approach: a trained model on text that is
known to distort statistics vs properly contextualize might learn patterns
(like presence/absence of contextual info around numbers). But that’s
niche. Possibly leverage a knowledge base: if a statistic is known, check if
context matches known correct interpretation. Example: if widely known
data says something, but the text presents it differently (like focusing on a
subset to inflate figure), an algorithm might catch it by cross-checking
official stats. That’s similar to fact-checking but specifically numeric.
Recommended Toolkits: regex/numeral parser for extracting numbers;
knowledge base (WDI/Wikidata, etc.) for known stats if relevant;
HuggingFace QA – e.g., ask a QA model “what is the context for [statistic]?”
and see if the article provides it. Also Unit conversion or consistency checks
if applicable (e.g., mixing metrics to confuse, but that’s more in technical
data). Possibly pandas/NumPy if doing analysis on series of numbers given
(like verifying if a trend claim matches the numbers).
Pseudo-code:
Python Run
import re
stats = re.findall(r"\b\d+(\.\d+)?%?\b", text)
stat_manip_flag = False
for stat in stats:
if stat.endswith('%'):
# If percentage, check if context has "of" or baseline
match = re.search(rf"{stat}[^.,;]*(?:of|out of|in|from|than)", text)
if not match:
stat_manip_flag = True
else:
# If a raw number, see if it's labeled (e.g., dollars, people, etc.). If just
# simplistic: no unit or descriptor within 3 words after or before
idx = text.index(stat)
window = text[max(0, idx-10): idx+len(stat)+10]
if not re.search(r"\b(year|people|dollar|vote|cases|students|km|years|men|wom
stat_manip_flag = True
if stat_manip_flag:
flags["statistical_manipulation"] = True

The logic here: any percentage with no context around (e.g., "50% of
respondents" has 'of', which is good; "50% increase from last year" has
'from', good; just "50% increase!" alone, flag). For absolute numbers, if a
number is given without any unit or descriptor near it, possibly a
meaningless big number (like "He wasted 5 million" vs "5 million dollars",
the latter is at least a unit). This is heuristic but highlights numbers that
might be thrown without clarity. More advanced: track if multiple stats are
combined illogically (like using one stat for population A and another for B
as if they are comparable). That requires deeper semantic analysis or
domain knowledge. But basic context absence is a red flag for statistical
misleading.
Framing Bias
Statistical Signature: Framing bias is presenting information with a
selective focus or angle to influence interpretation. It can be detected by
analyzing tone and perspective. A signature metric could be how different
the language is when describing two sides of an issue (similar to sentiment
bias measured earlier). Another measure: which aspects are emphasized
(for example, describing an event either highlighting losses vs highlighting
gains – classic framing difference). If we had a way to represent the
narrative frame, we might compare it to a neutral frame. For instance, an
article about a protest could frame it as “chaos and violence” vs “massive
turnout for justice” – checking word choices like “rioters” vs “protesters”. So
a technique: check for loaded synonyms that indicate a particular frame.
Also measure if certain expected keywords (that would appear in a neutral
account) are replaced by more connotative ones. For quantification: maybe
a framing vocabulary score – count words that belong to a certain frame
lexicon. E.g., in immigration: calling individuals “illegal aliens” vs
“undocumented immigrants” indicates a frame. If we define lexicons for
different framing of common issues, we can spot bias.

NLP/ML Implementation: Identify the topic and then apply known
framing variations. If topic is known (e.g., climate change can be framed as
“climate crisis” vs “climate alarmism” depending on bias), detect which
frame words are used. Another approach: use topic-specific sentiment or
connotation analysis. Alternatively, use ML to compare to a reference:
generate a summary of the article and compare it to a Wikipedia or neutral
summary of the event. Differences in word choice or focus can reveal
framing. This is advanced but feasible: e.g., feed article to a summarizer,
feed a neutral source to a summarizer, then use an NLI or embedding
comparison to see differences in emphasis. Simpler: maintain lists of loaded
terms for certain contentious topics (like gun control: “gun safety” vs “gun
control” vs “Second Amendment rights”). If the article consistently uses one
set, that indicates a particular frame.
Recommended Toolkits: Domain-specific lexicons for framing (some
research has lexicons for political framing); HuggingFace Transformers for
summarization (to get the gist and compare to others); embedding models
to detect differences in what aspects are mentioned (embedding of this
article vs an aggregated embedding of multiple sources on same topic – if
angle is different, perhaps cluster analysis would show it’s an outlier in
content focus). Also LIWC (Linguistic Inquiry and Word Count) categories
can show if the article is high in anxiety, anger, etc., hinting at a fear frame
for instance.
Pseudo-code:
Python Run
# Example for a specific known framing: say topic is Economy, frame could be "booming
economy_positive_frame = ["booming", "record highs", "job growth"]
economy_negative_frame = ["recession", "inflation", "crisis", "unemployment"]
pos_count = sum(text.lower().count(term) for term in economy_positive_frame)
neg_count = sum(text.lower().count(term) for term in economy_negative_frame)
if pos_count > 0 and neg_count == 0:
flags["framing_bias"] = True
metadata["frame"] = "positive_only"
elif neg_count > 0 and pos_count == 0:
flags["framing_bias"] = True
metadata["frame"] = "negative_only"

This simplistic snippet tries to see if only one frame (positive vs negative in
economic terms) is present. Real framing bias detection would require a
broader approach and knowledge of what frames are possible. For
example, crime stories can frame by focusing on individual responsibility vs
societal factors. Because generic implementation is hard, many systems
rely on pre-defined issue-specific cues or a training approach. We can
mention that our system can be extended with custom modules per topic to
check framing biases using curated lexicons or models.
Narrative Inconsistency
Statistical Signature: Narrative inconsistency means the story told
doesn’t add up – perhaps timeline issues, character behavior issues, or
illogical plot. In news context, this could mean the sequence of events or
causal relations described conflict or change inexplicably. A sign might be if
the article’s timeline jumps around or if an entity’s story changes within the
article (maybe quoting them contradictorily, which is also contradiction
detection). Another metric: Temporal consistency – use a temporal
parser to extract dates/times mentioned and see if they make sense
chronologically. Or if the narrative says X happened then Y, but date
mentions or logic imply the opposite. Also, check coherence of who did
what: coreference and entity tracking can spot if someone who was in one
location is suddenly somewhere else without explanation. These are subtle
and often require deep reading.
NLP/ML Implementation: Use a temporal information extraction tool to
build a timeline of events in the article. If events are out-of-order in a
confusing way or overlap impossibly, flag inconsistency. Also use
coreference to follow entities – if John is said to do something that
contradicts earlier info about John (like earlier: John was not present, later:
John did it), that’s an inconsistency (or a contradiction, which we covered).
Could also treat narrative inconsistency as a type of low coherence, which
we measured under logical flow and contradiction. Possibly measure by
dividing the article into beginning/middle/end summary (with a summarizer
or key point extraction) and see if the key points are logically consistent. ML
approach: maybe sequence models like LSTMs or GPT can be asked to
detect if a story is internally consistent (some research in story
understanding tries to do that with perplexity – if the language model is
very surprised by later parts given earlier, maybe inconsistency). Another
approach: NLI on earlier part vs later part to see if later part contradicts
earlier, which we did in contradiction detection.

Recommended Toolkits: HeidelTime or spaCy’s time extraction for
timeline; AllenNLP Coreference resolver to track characters; and NLI as
above. Possibly Temporal reasoning models from AllenAI or others if
available. Our earlier contradiction detection likely catches many narrative
inconsistencies of factual kind. For subtle ones (like motivations not lining
up, or unanswered questions in narrative), those might not be caught by
automation easily. We might lean on the coherence metrics and
contradiction already done.
Pseudo-code:
Python Run
# Using timeline approach
import sutime # SUTime, Stanford time tagger (just conceptual, assume available)
times = sutime.parse(text) # returns structured times and events if it existed
# times might give list of events with start/end if described
# We could then sort events by described time and see if order in text differs or ove
sequence_order = [event['text'] for event in times] # as they appear
chronological_order = sorted(times, key=lambda x: x.get('start')) # if start times
if sequence_order != [e['text'] for e in chronological_order]:
flags["narrative_inconsistency"] = True
This pseudo assumes we get events and times, which might be unrealistic
without manual annotation. It highlights the concept: if text narrates events
out of logical order (without clear reason like flashbacks, which news
typically wouldn’t do without explanation), flag it. Another simple check: if
the text mentions something like “After X, earlier, Y happened” –
contradictory temporal adverbs, but that’s likely just contradiction. We
might rely on contradiction detection and coherence measures largely for
this.
Coherence Drop

Statistical Signature: Coherence drop means the text suddenly becomes
harder to follow or loses clarity at some point – possibly where propaganda
or filler is inserted. A metric is perplexity or language model score over
sections: if a segment yields a much higher perplexity (meaning it’s less
predictable given prior text) that could signal a jarring, incoherent insertion.
Also, we can measure the flow of topics: if at one paragraph boundary,
semantic similarity dips sharply (which we did in logical flow), that’s a
coherence drop. Another approach: readability metrics per section – if an
article is mostly well-structured but a certain part is confusing (maybe
deliberately), the readability score might worsen (long convoluted
sentences, etc.). So compute readability (like Flesch reading ease) in a
sliding window; a sudden drop suggests a section that’s harder to parse,
possibly intentionally obfuscating.
NLP/ML Implementation: Use a pre-trained language model to compute
perplexity of the text sentence by sentence. Identify if there’s a sentence or
section with perplexity way above average (meaning it doesn’t fit well with
context). Alternatively, check coherence by splitting text and using a model
to predict next sentence probability – if actual next sentence is very unlikely
given previous, coherence issue. Readability: use textstat or similar to get
reading score of first half vs second half or per paragraph. If there's a
significant difference (one part is far more complex or vague), that’s
suspicious. ML approach: one could train a model on known high-quality
news vs manipulated news and find that manipulated content often has
disjointed or clunky transitions. That model might implicitly learn coherence
differences. But explicit metrics are easier to implement.
Recommended Toolkits: GPT-2 or GPT-Neo language model to measure
perplexity; NLTK or textstat for readability; BERT Next Sentence Prediction
(NSP) mode (though NSP is deprecated, but it can still be used to see if
sentence B is likely after A). Also our earlier Sentence-BERT similarity
covers structural coherence. So coherence drop can piggyback on that
analysis (looking for a local minimum in similarity or perplexity curve across
the text).
Pseudo-code:
Python Run
from transformers import GPT2LMHeadModel, GPT2TokenizerFast
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
sents = [sent.text for sent in doc.sents]
perp_scores = []

for sent in sents:
inputs = tokenizer(sent, return_tensors='pt')
loss = model(**inputs, labels=inputs["input_ids"]).loss
perp = float(torch.exp(loss))
perp_scores.append(perp)
# find if any perp is much larger than preceding
for i in range(1, len(perp_scores)):
if perp_scores[i] > 2 * perp_scores[i-1] and perp_scores[i] > some_threshold:
flags["coherence_drop"] = True
break
This calculates perplexity for each sentence in isolation (for a more
accurate coherence, one might condition on previous context, but GPT-2
might not handle super long context easily without careful batching). If a
sentence has perplexity double the previous (and high in absolute terms), it
indicates the sentence is unexpectedly incoherent given style/language
learned. For example, if suddenly the article spouts word salad or a very
different style, perplexity would spike. We also ensure it's above some
absolute threshold to avoid minor style changes triggering it. This is a
heuristic way to catch an unusual segment. Combining with similarity
checks from before gives a robust detection of coherence issues.
Claim-to-Evidence Ratio
Statistical Signature: The claim-to-evidence ratio is how many claims or
assertions are made relative to how many are backed by evidence (data,
quotes, references). A high ratio means lots of claims with little supporting
evidence – indicating a possibly biased or sloppy piece. To quantify: count
the number of sentences that contain factual claims vs the number of
sentences that provide evidence (e.g., citing a source, providing a statistic
or quote). For example, an article with many declarative statements and
only a couple of citations has a high claim/evidence ratio. We can
approximate: treat sentences with proper nouns, numbers, or assertive
verbs as claims, and sentences with quotes, citations, or references as
evidence. The ratio = count_claims / max(1, count_evidence). If this is >>
1, it’s problematic.

NLP/ML Implementation: Use NER and part-of-speech: any sentence
stating a fact about an entity or containing a number could be considered a
claim. Use patterns to identify evidence: sentences that contain quotation
marks, cite a source (according to X), contain a hyperlink (if HTML, but in
plain text not applicable unless markup is present), or mention study/data.
Count those. Then compute ratio. ML approach: could train a classifier to
label each sentence as claim, evidence, opinion, etc. (like argument mining
classification). If such a classifier is available, it would yield counts of claims
vs evidence segments. But a simpler heuristic works in many cases.
Recommended Toolkits: spaCy for NER (entities and numbers detection),
regex for quotes and citations; possibly BeautifulSoup if we had HTML to
identify links (but probably working with text only). If using ML, maybe a
model from fact-checking literature that identifies check-worthy claims. But
those might be overkill.
Pseudo-code:
Python Run
claim_count = 0
evidence_count = 0
for sent in doc.sents:
text = sent.text
# Heuristic: if sentence has a factual statement structure
if re.search(r"\b(is|are|was|were|has|have|numbers?|percent|million)\b", text):
claim_count += 1
# If sentence has evidence indicators
if '"' in text or 'according to' in text.lower() or re.search(r'\bdata\b|\bstudy\
evidence_count += 1
ratio = claim_count / (evidence_count if evidence_count>0 else 1)
if ratio > 3: # say more than 3 claims per evidence piece is high
flags["high_claim_to_evidence"] = True
metadata["claim_evidence_ratio"] = ratio
This counts a sentence as a claim if it has a linking verb or numeric or
something that suggests a statement of fact (rough heuristic). Evidence if it
has a quote or “according to” or mentions of data/study. Then if we have,
say, 10 claims and 2 pieces of evidence (ratio 5), we flag. The threshold can
be tuned; a value above, e.g., 3 or 4 might indicate an article that states
many things but barely supports them. This gives a single numeric feature
that we can also incorporate in the final scoring.
Unsupported Quantifiers

Statistical Signature: Unsupported quantifiers are words like “many”,
“few”, “most”, “countless” used without evidence. The signature is simply
the presence of those quantifiers not followed by specifics. For example,
“Many people are saying X” with no source or number. We can detect
quantifier words and check if the sentence also contains a number or
reference; if not, it’s unsupported. Metric: count of such occurrences. If any
unsupported quantifier exists, flag, or if more than a certain number.
NLP/ML Implementation: Use a list of quantifier terms (many, numerous,
some, a lot, several, etc.). For each occurrence, see if the sentence
contains either a specific number or a reference class like “according to
poll” or “survey” that would support it. If not, that quantifier is unsupported.
We can implement this with simple rules. ML approach: could be part of a
larger fact-check classifier, but likely overkill. This is straightforward with
pattern checking.
Recommended Toolkits: spaCy or regex for finding quantifier words; also
we might use dependency to ensure it's quantifying something (though
usually in text, “many” as determiner or “many people” can be caught just
by word). Possibly incorporate it into the bandwagon detection as well (as
bandwagon often uses quantifiers like “everyone”). But here it’s general –
even “some experts” is unsupported quantifier plus authority misuse.
Overlap is fine, we can double-flag in multiple categories if needed.
Pseudo-code:
Python Run
quantifiers = ["many", "most", "numerous", "several", "a lot of", "countless", "few"]
for sent in doc.sents:
text = sent.text.lower()
for quant in quantifiers:
if re.search(rf"\b{quant}\b", text):
# if the sentence doesn't have a number or cite, flag it
if not re.search(r'\b\d+|\b%|\baccording to|\bstudy\b|\breport\b', text)
flags["unsupported_quantifiers"] = True

This will flag sentences like “Many people think this is true.” (contains
'many' and no numbers or source). It won’t flag “Many (37%) of
respondents ...” because there's a number/percent. It also won't flag if it
says "many studies show" because 'studies' triggers a partial exception
(though even "many studies" without references could be flagged by
transparency gap anyway). We might add something: if "many studies" but
no actual citation, still an issue, but that might be caught by transparency
gap earlier. This simple check covers the core pattern of vague
quantification.
Hedging Signals
Statistical Signature: Hedging signals are words that indicate uncertainty
or caution (e.g., “might,” “maybe,” “likely,” “suggests,” “could,”
“somewhat,” etc.). These are not malicious; in fact, hedging can be a sign
of honest journalism. However, in analysis, tracking hedging is useful to see
how definitive vs speculative the content is. A high amount of hedging
might indicate the source is not confident or is trying to avoid commitment
to facts. The signature metric is the proportion of hedging words relative to
statements. Another measure: Hedge Density (e.g., hedges per 100 words).
NLP/ML Implementation: Use a list of hedge words/phrases. There are
known lists from academic writing analysis (e.g., “weasel words”). Count
them. Optionally classify sentences as hedged vs not (there is research on
hedge detection, often in scientific text). In media, phrases like “up to,” “as
much as,” “could mean,” “it is possible that” are hedges. We implement by
simple substring checks. ML approach: sequence labeling can mark hedge
cues, but likely unnecessary if lexicon is comprehensive. Tools exist
specifically for hedge detection (some in PyPI or academic code). We can
integrate one if needed. But a straightforward approach should suffice.
Recommended Toolkits: Lexicons from e.g., Wikipedia “weasel word” list
or a hedge detection dataset; or libraries like Clinical Hedging Detector (if
any open-source) since they do speculation detection in biomedical papers.
But likely fine to custom code.
Pseudo-code:
Python Run
hedges = ["may", "might", "could", "perhaps", "possibly", "suggests", "it is possible
hedge_count = 0
for token in doc:
if token.lower_ in hedges:
hedge_count += 1

hedge_density = hedge_count / len(doc) # hedges per token
if hedge_density > 0.02: # e.g., more than 2 hedging words per 100 words
flags["hedging_signals"] = True
metadata["hedge_density"] = hedge_density
This counts single-word hedges. Multi-word ones like "it is possible" would
need a phrase check (we can include "it is possible" in hedges list as one
string and search in text, or do n-gram search). The threshold 0.02 (2%) is
arbitrary; adjust depending on how common hedging normally is. The
outcome is not necessarily a "manipulation" but it's an indicator we track. A
high hedge density could mean the piece is cautious (or evasive, depending
on context). The system might use this in scoring differently (maybe not
penalize like a fallacy, but note style).
With all individual detectors defined, the system can produce a profile of the
article: which fallacies or bias signals were detected and to what extent. Next,
we discuss combining these signals and the overall architecture.
Combining into a Manipulation/Bias Score
After detecting all these characteristics, we need to aggregate them into a
single composite score that indicates the level of manipulation or bias in the
content. This can be done through a weighted scoring system or a machine
learning meta-model that takes all feature outputs as input.
Approach to Scoring:
1. Feature Normalization: First, convert each detected characteristic into a
numerical feature. For example, bandwagon_effect could be binary (0/1 for
presence) or a frequency count; loaded_language could be the
loaded_ratio; contradiction could be number of contradictions found, etc.
We normalize these to a common scale (e.g., 0-1).
2. Weighting: Assign weights to each feature based on perceived impact on
overall bias. For instance, factual issues like data_accuracy or contradiction
might weigh more than style issues like hedging. One could give higher
weight to things like cherry_picking, false_causality, loaded_language as
these strongly indicate manipulation. The weights can be set by experts or
learned by training a model on a labeled dataset of articles with known
“bias scores.”

3. Aggregation Formula: Compute a weighted sum or average:
\text{bias_score} = \frac{\sum_i w_i \cdot \text{feature}_i}{\sum_i w_i}
where feature_i are the normalized signals (e.g., 1 if a particular fallacy was
detected, or a value between 0 and 1 indicating degree) and w_i are
weights. This yields a score between 0 and 1 (or 0-100 scale) representing
how manipulative the content is.
4. Calibration: Calibrate the score by testing on examples of neutral vs highly
biased content to ensure it correlates correctly. Possibly, map the score into
categories (e.g., 0-0.3 = low bias, 0.3-0.7 = moderate, 0.7-1 = high
manipulation).
Using a Meta-Classifier: An alternative is to train a classifier that takes all
the features and outputs a binary or multi-class label (e.g., unbiased, somewhat
biased, very biased). For regression, train to predict a bias severity score. This
would require a training set of articles labeled by bias level. The features each
characteristic produces (counts, flags, ratios) are input to a model (like a
Random Forest, SVM, or even a simple logistic regression). The model can learn
non-linear combinations (maybe certain combinations of fallacies are
particularly indicative of disinformation). The advantage is it can automatically
tune weights. The disadvantage is needing labeled data.
In practice, a combined approach might be used: define an initial formula by
expert knowledge and then refine it with machine learning.
Example:
If loaded_language, name_calling, ad_hominem are present, those each
add say 0.1 to bias score.
If fact issues like false_causality or contradiction are present, add 0.2 each.
If omission/cherry_picking detected, add 0.15.
Minor signals like hedging_signals might add only 0.05 (if at all, since
hedging could even be a sign of caution rather than manipulation).
Then clip the score at 1.0 maximum.
These weights can be adjusted. For transparency, the system can output the
breakdown (e.g., "Score contributed by loaded language: 0.1, by contradictions:
0.2, ... total = 0.7").
Additionally, one might implement a rule that if certain severe issues occur (like
outright contradictions or provably false info), the score is automatically high
regardless of other factors.

The combination should also consider interactions: e.g., if both bandwagon and
unsupported_quantifiers are triggered, they’re related (both about vague
majority appeals) – but that likely just reinforces the signal rather than over-
counting, which a well-chosen weight covers.
In summary, combining is either via a weighted rule-based score or an ML
meta-model. Both aim to produce a single score that correlates with how
manipulative or biased the text is.
Recommended System Architecture
Implementing this as a real-world media analysis engine involves multiple
components in a pipeline. Here’s a high-level architecture with layers and tool
integrations:
1. Data Ingestion:
Input can be raw text of an article or transcript. The system may include a
web scraper or API client to fetch content. This feeds into a preprocessing
stage.
2. Preprocessing Layer:
Cleaning: Remove irrelevant parts (HTML tags, scripts) if any. Normalize
text (handle Unicode, etc.). Possibly split the article into title, body,
paragraphs.
NLP Annotation: Use spaCy (or similar) to tokenize, tag POS, perform
dependency parsing, and NER on the text. This yields a Doc object with
sentences, tokens, entities, etc., which many detectors will use.
Optionally, perform coreference resolution if needed for certain analyses
(like narrative tracking, though spaCy or HuggingFace has coref models to
integrate).
3. Feature Extraction Modules: (These can run in parallel since they are
mostly independent analyses of the text.)
Lexical Scanning Module: Looks for specific keywords/phrases for various
fallacies. This covers bandwagon terms, authority phrases, emotional
language, hedging words, quantifiers, etc. Implemented with pattern
matching (regex or spaCy’s Matcher). Outputs a dictionary of flags/counts
(e.g., {bandwagon: count, hedges: count, ...} ).

Sentiment & Emotion Module: Uses a sentiment analyzer or emotion
classifier on sentences/paragraphs. Outputs metrics like overall sentiment,
emotional appeal score, loaded language score (could be part of lexical
too).
Logic & Consistency Module: Uses NLI models to detect contradictions
and possibly check entailment of claims vs evidence internally. Also checks
logical fallacies:
It might run specialized classifiers or rules for strawman, red herring,
circular reasoning, etc., using the patterns described.
It can incorporate a Natural Language Inference step for consecutive
sentences or important claim pairs (as in contradiction detection).
This module might be further split into sub-modules per fallacy type in
code, but conceptually it handles coherence and logical consistency
signals.
Evidence & Fact-Checking Module:
Performs claim extraction (identify sentences that appear to be factual
claims, especially ones with numbers or proper nouns).
For each claim, optionally calls an external API or uses a local
knowledge base to verify (if available). This is the part that checks data
accuracy, false attribution (by verifying quotes), etc.
It also computes claim-to-evidence ratio by counting how many claims
vs sources as described.
Could integrate a tool like the FEVER fact-check model or just mark
unverifiable claims.
Propaganda Technique Classifier: Optionally, a multi-label classifier pre-
trained on propaganda techniques (like SemEval Task 11 data) can be used
to predict spans or presence of techniques such as Name Calling, Loaded
Language, Whataboutism, etc. arxiv.… . This provides another layer of
detection to complement rules. For instance, a fine-tuned BERT might
output a probability for each of the 14 propaganda categories given each
sentence. Those probabilities can be thresholded to decide flags (e.g., if
sentence gets high score for Name Calling, set that flag). This classifier
essentially overlaps with many of our rule-based detectors but can catch
subtle instances our rules might miss.

Topic & Framing Module: Identify the main topics or entities in the article
(could use spaCy NER + a topic model or just the most frequent entities).
Then apply framing analysis (if we have lexicons for certain topics as
discussed). Also, gather if multiple perspectives are present or only one (for
omission bias / card stacking detection).
Readability & Coherence Module: Calculates readability scores and
coherence metrics (like the similarity between sentences, perplexity with a
language model). It flags if it finds anomalies (big drops or very difficult
passages). This covers transparency of narrative and potential deliberate
complexity injection.
4. Feature Integration Layer:
All modules output their findings (could be booleans for each technique
flag, counts, or scores). For example:
{bandwagon: True, authority_misuse: False, emotional_score: 0.8, strawman:
True, ... loaded_language_score: 0.5, contradictions: 2,
claim_evidence_ratio: 5.0, hedging_density: 0.03, ...} .
This layer assembles a feature vector from these outputs. It may also
attach meta-info like which specific phrases or sentences triggered a flag
(useful for explanation, though not needed for the numeric score itself).
5. Scoring Engine:
This component takes the feature vector and computes the overall
manipulation/bias score as discussed. This could be a simple weighted sum
implemented as code (configurable weights), or a machine-learned model
(in which case this component loads the trained model and applies it to the
feature vector).
The output is a score and possibly a classification (e.g., “Bias Score: 0.75 –
High Manipulation”). It can also produce a summary of top contributing
factors (e.g., "Loaded language and cherry-picked data primarily contribute
to the high bias").
6. Report Generation:
Finally, the system can generate a report or data structure combining the
score and the individual indicators for transparency. This could be a JSON
with all flags and score, or a human-readable summary highlighting which
fallacies were detected. For UI, one might highlight spans of the text that
correspond to each issue.
7. (Optional) Feedback Loop:

If this system is used interactively, engineers might incorporate a feedback
loop where editors/analysts can correct false positives/negatives, and the
system learns from it (updating thresholds or retraining the meta-model).
This would refine the performance over time.
Architectural Considerations:
Use a modular design: each detection module can be developed and tested
independently, then integrated. This makes maintenance easier (e.g.,
update the propaganda classifier model without touching others).
Ensure efficiency: Some modules (like pairwise NLI for contradictions) are
computationally expensive for long articles. To optimize, first identify key
sentences or use clustering as mentioned to cut down comparisons.
Running everything in parallel using asynchronous calls or multi-threading
(if on CPU) or batching (if on GPU for ML models) will speed up processing.
Use caching for external lookups: fact-check queries can be slow or rate-
limited, so cache results for repeated claims or for articles that are re-
processed.
Scalability: If analyzing many articles, the pipeline could be deployed in a
distributed fashion. For example, one service for NLI tasks (contradiction,
etc.), one for sentiment and lexicon checks, etc., orchestrated by a central
coordinator.
Diagram – System Pipeline:
While we can't draw here, envision a flow like:
[Input Article] → [Preprocessing] → [
Lexical Module | Sentiment Module | Logic Module | Fact-check Module |
Propaganda Classifier | Framing Module | Coherence Module ] (parallel)
→ [Integration of Features] → [Scoring Engine] → [Output Results].
Each module in the parallel section feeds into the feature integration. The
arrows indicate data flow. The diagram would show how the text goes into
multiple analysis components and all their outputs go into the scorer.
This architecture ensures the system is implementation-focused: each part
corresponds to concrete NLP tasks or existing libraries:
spaCy NLP pipeline in Preprocessing,
custom code or regex for lexical and patterns,
HuggingFace transformers for classifiers (sentiment, NLI, etc.),

possibly a small database or external API usage in fact-checking,
a final combination logic.
Usability for Engineers: Engineers can implement each module with readily
available tools (as cited above) and tune parameters as needed. Data scientists
can train/fine-tune models for specific detectors (like propaganda classification
or stance detection) to improve accuracy on their domain. The modular design
allows updating one component (say, a better coreference model or an
updated hedge words list) without rewriting the whole system.
By following this comprehensive strategy, the team can detect and quantify a
wide array of manipulative techniques in text, ultimately producing a score and
explanation that helps end-users or analysts understand how and where an
article might be trying to mislead or bias readers arxiv.… sigann.gith… . This
combination of rule-based and ML-based methods covers everything from
blatant propaganda to subtle bias, providing a robust, implementation-ready
solution for media analysis.
Sources
Sat, Dec 6 at 7:14 AM
YYoouu aarree aa sseenniioorr NNLLPP rreesseeaarrcchh eennggiinneeeerr aanndd aapppplliieedd
mmaatthheemmaattiicciiaann ssppeecciiaalliizziinngg iinn ccoommppuuttaattiioonnaall
lliinngguuiissttiiccss,, mmeeddiiaa bbiiaass ddeetteeccttiioonn,, aanndd llaarrggee--ssccaallee
tteexxtt aannaallyyttiiccss.. YYoouu hhaavvee 1100++ yyeeaarrss ooff eexxppeerriieennccee
bbuuiillddiinngg pprroodduuccttiioonn--ggrraaddee NNLLPP ssyysstteemmss ffoorr
mmiissiinnffoorrmmaattiioonn ddeetteeccttiioonn,, pprrooppaaggaannddaa aannaallyyssiiss,, aanndd
aauuttoommaatteedd ffaacctt--cchheecckkiinngg aatt oorrggaanniizzaattiioonnss lliikkee RRAANNDD
CCoorrppoorraattiioonn,, MMIITT MMeeddiiaa LLaabb,, aanndd lleeaaddiinngg ffaacctt--
cchheecckkiinngg ccoonnssoorrttiiuummss.. YYoouurr eexxppeerrttiissee ssppaannss
ccllaassssiiccaall NNLLPP,, ddeeeepp lleeaarrnniinngg aarrcchhiitteeccttuurreess
((TTrraannssffoorrmmeerrss,, BBEERRTT vvaarriiaannttss)),, ssttaattiissttiiccaall mmooddeelliinngg,,
Show more
Thanks for this comprehensive and detailed blueprint. Just to confirm before I
proceed with the full deep-dive implementation plan:
1. Do you already have a preferred tech stack for deployment? (e.g., Python-
only, PySpark for scaling, cloud platforms like AWS/GCP, database like

PostgreSQL or MongoDB?)
2. Do you want code examples and modules written for batch processing,
real-time APIs, or both?
3. Will this system operate independently, or will it need to integrate into
existing tools (like fact-checking UIs, dashboards, etc.)?
Let me know so I can tailor every component accordingly — from architecture
to validation and scoring layers.
i want best psedo code, python,spark,
ray,python,couple of api and other ingestion tools
code is prefferd, SQl, vector db search like Fiass, for
2 i want psedocode( the code must include libarry(
maintained ones preferabbly), 3 one honestly idk,
you know my media analysis nlp pipline, this owuld
be integrated into that pipline
Great, I’ll create an advanced implementation plan focused on large-scale
media analysis NLP systems. The plan will include:
Best practices in pseudo-code and Python using scalable frameworks like
Spark and Ray.
Batch and real-time components.
Integration-ready API-level modules.
Ingestion with robust tools (e.g., NewsAPI, Scrapy).
SQL + vector DB storage (e.g., PostgreSQL + FAISS).
All components will be tailored for seamless integration into your existing media
analysis pipeline. I’ll update you once the full implementation blueprint is ready.
Research completed in 58m · 4 sources · 28 searches
Media Bias and Propaganda Detection System
Design
Token, Sentence & Document-Level Feature
Infrastructure

Mathematical Foundation
At the core, each document is modeled as a sequence of sentences, and each
sentence is a sequence of tokens. Formally, let a document $D$ be a sequence
of sentences $S_1, S_2, \dots, S_m$, and each sentence $S_i$ is a sequence of
tokens $t_{i1}, t_{i2}, \dots, t_{in_i}$. Each token carries linguistic features
such as part-of-speech (POS), lemma, named entity type, etc. We define
functions to compute various base features:
Token features: For each token $t$, we gather attributes like $\text{POS}
(t)$, $\text{lemma}(t)$, $\text{is_stopword}(t)$ (boolean for common stop
words), $\text{NER}(t)$ (named entity label or None), etc. These are basic
deterministic mappings from the token text.
Sentence features: For each sentence $S$, we compute properties such
as length $|S|$ (number of tokens), average word length, and placeholders
for advanced scores like sentiment or factual density (to be filled by later
modules).
Document features: For each document $D$, we can aggregate
sentence-level features (e.g., average sentence length, vocabulary
richness, count of quotes, etc.) and initialize vectors for bias, fallacy,
propaganda scores (which will be populated by specialized modules).

Aggregation functions: To build document-level metrics from token/sentence
features, we often use means or sums. For example, the document’s average
POS distribution is $\frac{1}{N_t}\sum_{t \in D} \mathbf{1}{\text{POS}
(t)=X}$ for each POS tag $X$ (where $N_t$ is total tokens in $D$). Sentence-
level scores can be aggregated upward by mean or max: e.g., overall
document sentiment = $\frac{1}{m}\sum{i=1}^m \text{sentiment}(S_i)$, or
overall fallacy presence might be the max severity of any fallacy in the
document (since one strong fallacy can taint the piece). We ensure
vectorization by representing features in arrays: for instance, we maintain a
vector of token lengths for a document to quickly compute mean and variance
in one pass.
Normalization: Many raw counts are normalized to comparable scales.
Frequencies (e.g., number of quotes) are divided by total sentences or tokens
to yield rates in [0,1]. For example, if $N_{\text{passive}}$ is the count of
passive-voice sentences and $m$ is total sentences, the passive voice ratio =
$N_{\text{passive}}/m \in [0,1]$. We apply min-max normalization at the
corpus level for features with unbounded ranges (e.g., document length) so
that extreme outliers are capped. Z-score normalization may be used for
certain features during combination to ensure each contributes comparably
(mean 0, std 1), though final user-facing scores will be scaled to [0,1] or [-1,1]
as required. We will also use logistic/sigmoid scaling for metrics like fallacy
frequency, to compress heavy-tailed distributions (e.g., using $f(x)=1 - e^{-
\lambda x}$ to convert a count $x$ to 0-1 severity).

Sparse/Missing Data: If a document lacks certain elements (e.g., no quotes
or no detected entities), the corresponding features default to 0 or a neutral
score. All formulas handle zero-denominator cases safely (e.g., if no claims
were found, the verified-claim ratio can be defined as 1 or 0 by convention – we
will define it as 0 in output, meaning no verified claims present). We ensure
robust handling so that missing data doesn’t propagate as errors: for instance,
if no sentences have discourse connectives, the discourse connective
frequency is simply 0.
Statistical Validation: The distribution of each base feature will be examined
across a large corpus to verify it aligns with expectations (e.g., average
sentence length ~15-20 words, etc.). We will perform sanity checks using
known readability baselines and simple test documents. For example, we can
validate that our syllable counter and sentence splitter produce the correct
Flesch-Kincaid reading grade on a sample text with known readability. Likewise,
ensuring that tokenization and POS tagging yield expected counts (e.g., number
of nouns or verbs in a simple sentence matches manual count) helps verify the
correctness of the pipeline's foundation.
Implementation Strategy
Approach: Use a hybrid rule-based and ML approach for base feature
extraction. Deterministic rules handle tokenization, POS tagging, parsing
(via proven libraries), ensuring consistency. No learning is needed at this
stage – it’s about reliable linguistic analysis.
Primary Library: Use spaCy 3.x for fast tokenization, POS, NER, and
dependency parsing. spaCy provides pre-trained models for English that
are robust and production-ready. For scalability, consider SparkNLP 4.x
(built on Apache Spark) or spaCy’s multiprocessing support to distribute
parsing across cores/nodes.
Pretrained Model: spaCy’s en_core_web_lg (or xx_ent_wiki_sm for multi-
language) model for linguistic annotations. This model includes word
vectors for semantic similarity tasks. Alternatively, Stanza (StanfordNLP)
can be used if needed for languages spaCy doesn’t cover, albeit with
possibly lower speed.
Computational Complexity: Linear in document length, $O(N_t)$ per
document for tokenization and tagging. spaCy processes around 1M tokens
per CPU core per second, so it scales linearly with text size. Parsing (for
dependency and NER) is also linear-ish per sentence, with a small constant
factor.

Scalability: Yes, it can handle 1M documents. Use batch processing and
parallelization – e.g., spaCy’s nlp.pipe(docs, n_process=8) to use 8 cores, or
distribute documents across a Ray cluster or Spark RDD/DataFrame. In
Spark, one could use mapPartitions with a spaCy model loaded per
executor. The design ensures we stream through documents without
holding everything in memory, enabling large-scale processing.
Code Template
Python Run
import spacy
# Load spaCy model (large model for better accuracy in NER, POS)
nlp = spacy.load("en_core_web_lg")
def process_document(doc_id, text):
doc = nlp(text)
# Token-level features
token_features = []
for token in doc:
token_features.append({
"token": token.text,
"lemma": token.lemma_,
"pos": token.pos_,
"is_stopword": token.is_stop,
"ner_type": token.ent_type_ if token.ent_type_ else None,
"sentiment": 0.0, # placeholder, will fill later
"toxicity": 0.0, # placeholder for later toxic terms
"fallacy_signal": 0.0, # placeholder for later fallacy flag
"bias_signal": 0.0, # placeholder for later bias flag
"propaganda_signal": 0.0 # placeholder for later propaganda flag
})
# Sentence-level features
sentence_features = []
for i, sent in enumerate(doc.sents):
sent_text = sent.text
sentence_features.append({
"sentence_id": i,
"text": sent_text,
"sentiment": 0.0, # to be computed by sentiment module
"subjectivity": 0.0, # to be computed (e.g., via TextBlob or model)
"stance": None, # to be determined by stance module
"factual_density": 0.0, # e.g., number of claims in this sentence (compute
"fallacy_present": False, # mark True if fallacy detection flags this senten
"propaganda_present": False, # mark True if propaganda detected
"logical_flow_score": 1.0, # placeholder for coherence (1.0 = fully coherent)
"complexity": 0.0 # e.g., parse tree depth or reading ease for this
})
# Document-level features

doc_features = {
"doc_id": doc_id,
"topic_distribution": {}, # placeholder (to fill via topic modeling if needed)
"overall_bias_vector": [], # to be filled by bias analysis (multiple bias score
"fallacy_vector": [], # to be filled with fallacy counts/severity per type
"propaganda_vector": [], # filled with propaganda technique frequencies
"stance_distribution": {}, # e.g., counts of support/oppose/neutral
"factuality_score": 0.0,
"transparency_score": 0.0,
"data_accuracy_score": 0.0,
"conflict_score": 0.0, # e.g., internal contradiction presence
"aggregate_quality_score": 0.0
}
return {"tokens": token_features, "sentences": sentence_features, "document": doc_fea
# Example usage:
doc_data = process_document("doc123", example_text)
Pseudocode: In a production setting, wrap the above in a distributed map. For
instance, using Ray you could do:
Python Run
import ray
ray.init()
@ray.remote
def process_batch(batch):
return [process_document(doc_id, text) for doc_id, text in batch]
# Suppose docs is a list of (id, text) pairs
batches = [docs[i:i+1000] for i in range(0, len(docs), 1000)]
results = ray.get([process_batch.remote(batch) for batch in batches])
This would distribute the workload across workers. Similarly, with Spark, you
could parallelize using sc.parallelize(docs).map(lambda doc:
process_document(doc_id, text)) . Each worker would need to load the spaCy
model (consider using a broadcast variable or initializer in Spark to avoid re-
loading for every record).
Scoring & Calibration
At this stage, most features are raw or frequency-based. Calibration mainly
occurs in later modules when combining signals. However, we ensure
consistent scaling:
Length normalization: Features like counts of specific words (e.g.,
number of loaded language terms) will be normalized by document length
or sentence length to avoid bias toward longer texts.

Global normalization: After processing a large sample, we may adjust
some metrics so that 0.5 represents an average value. For instance, if
average document sentiment comes out around 0.6 on a [0,1] scale, we
might re-center or re-scale the sentiment scoring function so that an
unbiased neutral document scores ~0.5.
Thresholds: Some binary flags (like fallacy_present ) are initially False/True
based on detection rules or model outputs; these thresholds will be tuned in
their respective modules and reflected here. E.g., if a fallacy model gives
confidence 0.8, above a threshold 0.7, we mark fallacy_present=True for
that sentence.
All numeric outputs are finally constrained to the specified range [0,1] or [-1,1].
For example, sentiment raw scores from a model (often in [-1,1]) might be
linearly scaled to that range if needed or left as is if already conforming.
Validation
We validate the foundational processing by unit tests and visual inspection:
Tokenization/POS/NER: Run the pipeline on sample texts and verify
tokens and entities against manual annotation. For example, feed a known
sentence like "Barack Obama was born in Hawaii." and check that Barack
Obama is one entity (PERSON) and that the tokens are correctly split, POS
tags ( Barack/PROPN , etc.) are sensible.
Feature correctness: Calculate a simple metric (like average word length
or sentence length) manually for a test document and compare with the
pipeline’s output. Any discrepancy indicates a bug in aggregation.
Speed tests: Process a large batch (e.g., 100k documents) on a single
machine and measure throughput. This ensures that scaling out to 1M docs
linearly is feasible. If performance per document is too slow, we might
simplify the pipeline (e.g., disable very expensive parsing features or use a
faster model).
We will also use benchmark datasets for sub-tasks once those modules
are in place. For now, verifying base features might involve comparing our
POS tag distribution against known distributions from linguistic corpora to
ensure no major biases (e.g., ~40% nouns, etc., depending on text
domain).
Integration Notes
The token/sentence/document feature extraction is the foundation upon which
all other analysis builds. It produces a structured representation that
subsequent modules (fallacy detection, bias scoring, etc.) will enrich:

Other modules will take sentence_features and update fields like sentiment ,
stance , fallacy_present , etc., rather than creating new structures from
scratch. This ensures all data remains linked by indices (e.g., we know
exactly which sentence a fallacy was found in via the sentence_id ).
This stage requires language-specific models. For multilingual support,
we would replicate this pipeline with models for each language or use a
multilingual model. The rest of the system is largely language-agnostic
once features are extracted.
Dependencies: Downstream, the fallacy detector might depend on
dependency parse (to identify argument structures) or NER (to see if an
attack is ad-hominem on a person). Thus, high-quality parsing here
improves later precision.
Storage: Consider storage implications — token-level details for 1M docs
could be huge. We likely won’t store every token’s features in a database
permanently (perhaps just keep in memory for processing or serialize to
compressed form if needed). Instead, we store key aggregate signals and
only keep detailed features for troubleshooting or examples. A possible
strategy: store sentence-level and document-level features in a database,
and optionally store token features as JSON blobs or in a search index if
needed for query (or not at all to save space).
The data structures can be easily converted to JSON for storage or to
Pandas DataFrames for analysis. This foundation will feed into the
composite scoring later by providing all the counts and indicators needed
to compute final scores.
Logical Fallacy Detection & Scoring
Mathematical Foundation
Logical fallacies are detected at the sentence or argument level and quantified
in terms of type, confidence, and impact. Let $F = {$*strawman, ad_hominem,
slippery_slope, red_herring, circular_reasoning, false_dilemma,
burden_of_proof, cherry_picking, hasty_generalization, false_cause,
appeal_to_authority, equivocation, no_true_scotsman, appeal_to_emotion,
bandwagon$}$ be the set of fallacy types to identify (as defined in the feature
list). We produce for each detected fallacy instance a tuple
$(\text{fallacy_type}, \text{text_span}, s, c, \ell)$, where:
$\text{text_span}$ is the exact excerpt of text containing the fallacious
reasoning.

$c$ is a confidence score $c \in [0,1]$ indicating the system’s certainty
that this span is indeed that fallacy.
$s$ is a severity score $s \in [0,1]$ indicating how severely this fallacy
attempts to mislead or manipulate.
$\ell$ is the logical flow disruption score $\ell \in [0,1]$ estimating how
much this fallacy breaks the coherent logical flow of the argument.
Detection formulation: We treat this as a sequence classification or tagging
problem. For each sentence (or clause) $S_i$, we aim to assign a label from $F
\cup {\text{no_fallacy}}$. A classifier $M$ produces probabilities $P(f \mid
S_i)$ for each fallacy type $f$. The confidence $c$ for a predicted type is the
model’s probability for that type: e.g., if $M(S_i)$ outputs 0.85 for
slippery_slope, then $c=0.85$ for that span. (If multiple fallacies might co-occur
in one sentence, a multi-label approach can be used, giving a confidence for
each $f$.) We define:
$\text{fallacy_present}(S_i) = \mathbf{1}{\max_{f \in F} P(f|S_i) > \tau}$
as an indicator if any fallacy is present above threshold $\tau$.
If present, $\text{fallacy_type}(S_i) = \arg\max_{f \in F} P(f|S_i)$ (the
highest scoring fallacy type).

Severity: Not all fallacy instances are equal. We derive a severity $s$ based on
the fallacy type and context intensity. For example, an appeal to emotion can
be mild or extreme. We quantify severity as:
s = c× I × I × ⋯ ,
emotional repetition
where $I_{\text{emotional}}$ might be an intensity factor computed from
emotional language (e.g., proportion of fear/anger words in the span),
$I_{\text{repetition}}$ might boost severity if the fallacy is repeated or
reinforced in text, etc. Each $I$ factor is normalized to [0,1], and if not
applicable it defaults to 1. For logical fallacies that don't rely on emotion (like
circular reasoning), $I_{\text{emotional}}=1$. As a simpler scheme, we might
assign a base severity weight $w_f$ per fallacy type (e.g., slippery slope might
have $w_{\text{slippery}}=0.7$ if considered moderately severe, whereas
appeal to fear could have $w_{\text{fear}}=0.9$ due to strong manipulative
intent). Then:
s = c× w .
f
We ensure $s$ is capped at 1.0. If multiple fallacies occur in the document, we
may list each with its own $s$. For the document as a whole, we can aggregate
an overall fallacy severity vector (one dimension per fallacy type, each being
max $s$ seen or frequency-weighted score).
Logical flow disruption ($\ell$): We estimate how much each fallacy breaks
the reasoning flow. Some fallacies (e.g., Red Herring or Strawman)
intentionally divert the argument, causing high disruption. We can model logical
coherence by analyzing discourse structure or argument graphs. A simple
proxy: $\ell = s$ for the most disruptive fallacy in the document (i.e., treat
severity of worst fallacy as coherence breaker). Or more formally, let ${s_1,
s_2, \dots, s_k}$ be severities of fallacies in the doc, and let $d_f$ be a
disruption weight for fallacy type $f$ (e.g., $d_{\text{red_herring}}=1.0$ as it
directly diverts, $d_{\text{hasty_generalization}}=0.5$ as it’s a logical error
but not a structural diversion). Then define:
ℓ = max (s × d )
i=1..k i f
i
for each sentence or for the whole document’s logical flow score. We could also
invert this to a logical flow coherence score = $1-\ell$ to indicate coherence
(1 = fully coherent, 0 = very disrupted).

Aggregation: If multiple fallacies are found across sentences, each is reported
separately. For sentence-level output, fallacy_present is a boolean as above.
Document-level, we can compile a fallacy vector where each entry
corresponds to one type in $F$ (e.g., number or total severity of each fallacy in
the doc). This vector can feed into composite bias indices later.
Normalization: Confidence from the classifier is naturally [0,1]. Severity and
disruption, as defined, also fall in [0,1]. We may calibrate these so that an
“average” fallacy occurrence (as per some training data or expert labeling)
scores around mid-range severity (0.5). If our initial formula yields too high
values, we can apply a squashing function or adjust weights $w_f$.
Implementation Strategy
Approach: A hybrid approach combining rule-based cues and a
Transformer-based classifier. We leverage ML to capture subtle fallacies
(semantic/contextual cues), but also incorporate pattern matching for
explicit indicators (e.g., the presence of phrases like "everyone knows"
might flag a hasty generalization).
Primary Library: Hugging Face Transformers (v4.x) for implementing
a sequence classification model (e.g., fine-tune a BERT-based model to
label fallacy types). Additionally, use spaCy or regex for simple lexical
patterns that can boost detection (like matching "so you’re saying..." could
indicate a Strawman setup).
Pretrained Model: Start with a model like roberta-base or deberta-v3-
large fine-tuned on a logical fallacy dataset (if available). Research by Jin et
al. introduced a fallacy dataset, so we could fine-tune on that to get a
classifier $M(S) \to f$. Alternatively, use GPT-4 or similar in zero-shot
classification mode (noting that this is less deterministic). For
implementation, a fine-tuned model stored via HuggingFace’s model hub
can be loaded for inference.

Computational Complexity: If using a Transformer classifier, inference is
$O(n)$ in sentence length per sentence. The overall complexity per
document is $O(N_s \cdot L)$ where $N_s$ is number of sentences and $L$
is average tokens per sentence processed by the model. For 1M
documents, if each has ~30 sentences, that’s 30M sentences to classify –
which is heavy but can be batched. Batching 32 or 64 sentences at a time
on GPU significantly amortizes overhead. Complexity per batch is linear in
total tokens (with Transformer quadratic in sequence length, but sentences
are usually short, so manageable).
Scalability: This is one of the heavier components. To scale, use GPU
acceleration and possibly model distillation. We can preprocess with rules
to filter obviously non-fallacious sentences (e.g., factual statements) so the
model only runs on candidate sentences (~ maybe 50% of sentences). Use
distributed inference: frameworks like TensorFlow Serving or PyTorch
with DeepSpeed for multi-GPU, or break the data by chunks and use
multiple GPU machines. Another strategy: use a smaller model (e.g.,
distilroberta-base ) if accuracy remains acceptable. For 1M docs, we likely
schedule this as a batch job that might run for a few hours on a GPU
cluster. Caching model outputs for repeated sentences (if many similar
statements across articles) could also help – e.g., using a similarity search
(Faiss) to avoid re-computing embeddings for duplicate sentences.
Code Template
Python Run
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
# Load fine-tuned fallacy classifier (example model name)
model_name = "myorg/roberta-fallacy-detector"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name) # model outputs l
# Assume we have a list of sentences from the document
sentences = [sent["text"] for sent in doc_data["sentences"]]
# Batch classify sentences for fallacies
batch_size = 32
fallacy_labels = [] # will store detected fallacy type or None for each sentence
fallacy_confidences = []
for i in range(0, len(sentences), batch_size):
batch = sentences[i:i+batch_size]
enc = tokenizer(batch, return_tensors='pt', padding=True, truncation=True, max_length
with torch.no_grad():

outputs = model(**enc)
# Assuming model outputs raw logits of shape [batch, num_labels]
probs = outputs.logits.sigmoid() if model.config.problem_type == "multi_label_classif
for j, p in enumerate(probs):
if model.config.problem_type == "multi_label_classification":
# multi-label: pick any label above threshold
found = [(model.config.id2label[k], float(p[k])) for k in range(len(p)) if p[
if found:
# choose the top confidence label as primary
found.sort(key=lambda x: x[1], reverse=True)
label, conf = found[0]
else:
label, conf = None, 0.0
else:
# single-label: highest probability
conf, label_idx = torch.max(p, dim=0)
conf = float(conf); label = model.config.id2label[int(label_idx)]
if label == "no_fallacy":
label = None; conf = 0.0
fallacy_labels.append(label)
fallacy_confidences.append(conf)
# Integrate results back into sentence features
for idx, sent_feat in enumerate(doc_data["sentences"]):
if fallacy_labels[idx]:
f_type = fallacy_labels[idx]
conf = fallacy_confidences[idx]
sent_feat["fallacy_present"] = True
sent_feat["fallacy_type"] = f_type
sent_feat["confidence"] = conf
# Calculate severity based on type-specific weight
weight = fallacy_severity_weights.get(f_type, 1.0)
severity = conf * weight
sent_feat["severity"] = round(min(severity, 1.0), 3)
# Mark logical flow disruption if severity high and type is disruptive
disruption_weight = fallacy_disruption_weights.get(f_type, 1.0)
sent_feat["logical_flow_disruption"] = round(min(severity * disruption_weight, 1.
# Store text span that triggered (here we use full sentence; could refine to sub-
sent_feat["fallacy_span"] = sent_feat["text"]
else:
sent_feat["fallacy_present"] = False
# Document-level aggregation:
fallacy_vector = {f:0 for f in fallacy_severity_weights.keys()}
for f_type, conf in zip(fallacy_labels, fallacy_confidences):
if f_type:
fallacy_vector[f_type] += 1 # count occurrences (or sum severity)
doc_data["document"]["fallacy_vector"] = fallacy_vector
# E.g., doc_data["document"]["fallacy_vector"] might be {"Ad Hominem": 2, "Strawman": 1,

Pseudocode notes: We define fallacy_severity_weights as a dictionary mapping
fallacy types to a base weight (e.g., {"Ad Hominem":0.8, "Red Herring":0.9,
...} ), and similarly fallacy_disruption_weights mapping types to how much
they disrupt logical flow. In practice these weights could be set by experts or
tuned on a validation set. The code above treats the whole sentence as the
fallacy span; for finer granularity, we might use the model’s token attributions
or attention to highlight just part of the sentence.
Scoring & Calibration
The raw model confidence may not be calibrated (e.g., a model might output
0.9 for many sentences if slightly fallacious). We thus perform confidence
calibration using techniques like temperature scaling or Platt scaling on a
validation set of labeled fallacies. This ensures that the confidence score $c$
truly corresponds to probability of correctness. After calibration, we interpret
$c>0.5$ as moderate evidence and $c>0.8$ as strong evidence of a fallacy.
Severity scores are tuned so that:
Minor infractions (e.g., a slight exaggeration or a borderline false cause)
might get $s \approx 0.3$.
Egregious manipulation (e.g., a blatant fear appeal with strong language)
should approach $s \approx 1.0$.
We achieve this by adjusting the $w_f$ weights and any intensity factors.
For example, if we notice all Appeal to Emotion are scoring too low despite
containing strong language, we increase $w_{\text{emotion}}$. We can
also incorporate the frequency of a fallacy: repeated use of the same
fallacious argument in one article could increase severity (someone who
uses Ad Hominem once vs doing it 5 times – the latter indicates a more
systematically fallacious argument). Thus, an accumulation function can be
used at doc-level: e.g., if $n_f$ instances of type $f$ found, the document-
level severity for $f$ might be $1 - \exp(-n_f)$ (which grows towards 1 as
$n_f$ increases).

Logical flow disruption $\ell$ is by design in [0,1]. We calibrate it by checking
human judgments of coherence. For instance, if human annotators rate an
article with multiple red herrings as very incoherent, our $\ell$ for that article
should be high. We may adjust $d_f$ weights accordingly. If no fallacies are
present, $\ell=0$ (no disruption). If fallacies are present, $\ell$ has a minimum
floor (perhaps $\ell$ never 0 if any fallacy exists) to reflect that even one fallacy
introduces some noise in reasoning.
Thresholding: We set a global threshold $\tau$ for flagging a fallacy. For high
precision need (if we want to be very sure before accusing a text of a fallacy),
we might set $\tau=0.8$. For a more recall-oriented analysis (we want to catch
as many as possible), $\tau=0.5$. This threshold can also vary by type: e.g., we
might require higher confidence to label something False Cause (which might
be harder to detect) than to label a straightforward Ad Hominem (which may
have obvious keywords).
Edge cases are handled explicitly:
If a sentence contains keywords like "either...or" and a conclusion, it might
be a False Dilemma. If the model misses it, a rule can still flag it with low
confidence. We combine model and rules by taking $c =
\max(c_{\text{ML}}, c_{\text{rule}})$ for each type.
If multiple fallacy types are detected for the same span (overlap), we either
choose the highest confidence one or report both if they are conceptually
different (though usually one will dominate).
Ambiguity: If the model is unsure (e.g., many outputs around 0.4
confidence), we either report none (to avoid false positives) or label the
span as "Unclear fallacy" with low confidence for analyst review.
Validation
We validate the fallacy detection module on known examples and datasets:
Use the logical fallacy dataset by Jin et al. for quantitative evaluation.
Split into train/dev/test if fine-tuning, or use as gold standard for a zero-shot
model. We expect to measure precision/recall for each fallacy type. For
example, our system should catch a Strawman instance with high
confidence and highlight the span containing the misrepresentation.

Create synthetic test cases for each fallacy type to ensure the rules and
model cover them. E.g., "Opponent: We should improve public transport.
Response: So you want to bankrupt the city by giving out free rides to
everyone?" is a Strawman example. The system should tag "you want to
bankrupt the city..." as Strawman, with $\text{fallacy_present}=True` and
that text as the span.
Check false positives by running on factual, high-quality editorials or
academic text (which ideally contain no fallacies). The fallacy detector
should output no spans (or only very low confidences). If it flags something
incorrectly, we adjust the threshold or refine features.
Inter-annotator agreement: If possible, have human experts label a
sample of our system outputs as correct/incorrect to estimate the
accuracy. Aim for high agreement that flagged fallacies are genuine.
Continual improvement: We can maintain a small benchmark set of
paragraphs with known fallacies (from debate transcripts, forums, etc.) and
track the system’s performance (so we know if a code change or model
update improves detection rates).
Integration Notes
The fallacy detection ties into several other components:
Fallacy spans often coincide with propaganda techniques (many
propaganda methods are essentially fallacious arguments). For example,
Name-calling propaganda can be seen as a form of Ad Hominem fallacy.
We will ensure that these modules share signals (to avoid double counting
or conflicting outputs). If a span is identified as Ad Hominem, the
propaganda module might not need to separately label it as Name-calling,
or they both label it but we unify them in the explanation.
Explainability: Each detected fallacy provides a clear explanation point for
the end user: we can highlight the text span and say "This looks like a $X$
fallacy (confidence 90%)." This will be part of the user-facing dashboard.
The confidence and severity from fallacies will feed into the aggregate
manipulation score. E.g., multiple severe fallacies will strongly lower the
overall credibility or quality score of the document.
Dependencies: This module relies on good sentence segmentation and
sometimes coreference resolution (to understand references in e.g.
Strawman arguments). We might need coreference from the foundation if
an argument references "this proposal" vs "that", to fully catch the
misrepresentation.

We will store fallacy findings per document, likely in a separate table or
JSON field, with fields: fallacy_type, span_text, sentence_id, confidence,
severity . This detailed info may not be needed for every analysis query
(and could be heavy to store for millions of docs), but we at least store
aggregated counts and an indicator if any fallacy was present for quick
filtering. The detailed spans could be stored for a subset (e.g., most recent
articles or those with high manipulation scores).
During real-time operation, fallacy detection is costly. We may choose to
run this in batch for articles and not in a live on-demand API (unless we
have powerful GPUs available). For a real-time summary (like if a journalist
pastes a paragraph to check), we could run a distilled model for speed.
Batch vs real-time considerations will be discussed in the final section.
Propaganda & Rhetorical Technique Detection
Mathematical Foundation
We identify classic propaganda techniques in text, many of which overlap with
rhetorical fallacies but focus on emotional and persuasive language. Let $P =
{$*name_calling, loaded_language, glittering_generalities, fear_appeal,
appeal_to_prejudice, flag_waving, whataboutism, repetition, oversimplification,
exaggeration, minimization, obfuscation, thought_terminating_cliche$}$ be the
set of propaganda techniques to score (based on the provided list). For each
technique $p \in P$, we quantify:
$\text{intensity}(p) \in [0,1]$: how strong or blatant the usage of this
technique is in the document.
$\text{frequency}(p) \in \mathbb{N}$: how many times the technique
appears (e.g., count of distinct instances or phrases).
$\text{transparency_violation}(p) \in [0,1]$: the degree to which this
technique reduces transparency or honesty in communication. This is
higher for more deceptive techniques.

For each occurrence of a propaganda technique, we also mark the text span
and its location. For example, if a sentence uses Loaded Language
(emotionally charged words), we might mark the specific words or phrase
causing it (e.g., "brutal regime" could be flagged as loaded language).
Detection approach: Similar to fallacies, we can either do multi-class
classification of spans or use separate detectors per technique. A technique like
repetition can be detected by analyzing the text for repeated slogans or
phrases (e.g., if a 3-gram appears many times unusually). A technique like
flag_waving (appealing to patriotism) might be detected by the presence of
country/national symbols and valorizing language ("our great nation must...").
We define indicator functions and scores:
Let $I_p(s)$ be an indicator that sentence $s$ contains technique $p$. This
could be a binary from a classifier or rule. For example,
$I_{\text{whataboutism}}(s) = 1$ if sentence $s$ starts with "What about"
or makes a deflective comparison.
The frequency $f_p = \sum_{i=1}^m I_p(S_i)$, simply counting how many
sentences (or instances) use $p$ in the document.
Intensity: If a technique appears, how strongly is it applied? E.g., for loaded
language, intensity could be measured by the density of emotionally
charged words in that span. If $W_{\text{loaded}}(s)$ is the number of
loaded words in sentence $s$ and $N_s$ is sentence length, we might
define an intensity score $I!N_{\text{loaded}}(s) =
\frac{W_{\text{loaded}}(s)}{N_s}$ (proportion of loaded words), then
overall document intensity $ \text{intensity(loaded_language)} = \max_s
I!N_{\text{loaded}}(s)$ or a weighted average. For repetition, intensity
might correlate with how frequently a phrase is repeated; e.g., if a slogan
appears 10 times, intensity is high (close to 1 after normalization by a
reasonable maximum).

Transparency violation: This is a more subjective metric. Techniques like
name-calling, obfuscation, whataboutism are deliberate attempts to
mislead or avoid honest debate, so they have higher inherent transparency
violation weight. We can define a weight $u_p$ for each propaganda type
capturing its dishonesty (e.g., $u_{\text{obfuscation}}=1.0$ as it directly
violates clarity, $u_{\text{glittering_generalities}}=0.7$ as it glorifies
without specifics). Then:
\text{transparency_violation}(p) = \min(1, \; u_p \times \text{intensity}(p) +
\alpha \times \frac{f_p}{N_s})
where $\frac{f_p}{N_s}$ (frequency per sentence) accounts for repeated
use. $\alpha$ is a tuning parameter to incorporate frequency. We cap at 1.
For rarely used but very intense propaganda, intensity dominates; for
moderately intense but repeated propaganda, frequency contributes.
We output for each detected technique one or more spans. For example:
JSON
{ "technique": "Loaded Language", "intensity": 0.9, "text_span": "brutal regime of ruthle
This indicates the doc used loaded language 3 times, with a strong instance
shown, and overall it significantly undermines transparent communication.
Aggregation: At sentence-level, we can have boolean flags or counts for each
technique (similar to fallacy). At document-level, we can form a propaganda
vector of dimension $|P|$, containing either frequencies or aggregated scores
for each $p \in P$. For composite scoring, we may also sum across techniques
to get a total “propagandistic content” score, e.g.,
\text{PropagandaIndex} = 1 - \prod_{p \in P} (1 - \text{transparency_violation}
(p) \times w'_p)
where $w'_p$ might weight more serious techniques higher. This formula (one
minus product of (1-x)) essentially computes a combined effect that increases
as more techniques are present, without simply linear addition (it tends toward
1 as any component approaches 1).

Normalization: Frequency is normalized by document length to allow fair
comparison between a 100-word social post and a 2000-word article. Intensity
is naturally [0,1] as defined (if defined as proportion or a normalized count of
strong words). We might calibrate intensity so that, for instance, using one
strong word in a sentence yields ~0.5 intensity, while packing a sentence with
multiple slurs or emotional adjectives yields >0.8. Frequency normalization
might use a log scale for heavy repetition (10 repeated phrases is intense, but
20 is not twice as bad subjectively – diminishing returns, which the log or
saturating function can model).
Implementation Strategy
Approach: Use a hybrid rule-based and ML detection. Many propaganda
techniques can be reliably flagged with linguistic rules (e.g., regex or
keyword lists for slogans, detection of logical connectives like "what about").
Complement these with a multi-class classifier or multiple binary
classifiers fine-tuned to recognize propaganda spans. In fact, the SemEval-
2020 Task 11 provides a reference: a span-based multi-class model can
identify techniques like Loaded Language and Name Calling in news
articles.
Primary Library: Transformers (PyTorch) for model-based detection of
propaganda spans (e.g., fine-tune a bert-base-cased or roberta-large on
propaganda technique classification). Additionally, use spaCy for pattern
matching and Expert AI knowledge (like a dictionary of bias words). The
Propaganda Techniques Analysis could also use specialized libraries if
available (some research code from SemEval participants is on GitHub).
Pretrained Model: If available, use a model fine-tuned on the Propaganda
Techniques Corpus (PTC). Otherwise, use zero-shot classification (with a
prompt like "Does this text contain X?") via GPT or a NLI model. For
simplicity, we might fine-tune a RoBERTa on an annotated set where each
propaganda technique is labeled in text. We might even break it into two
steps as per SemEval: span detection (find propagandistic text spans) and
technique classification on those spans. Pretrained transformers (like
roberta-base or domain-specific ones like bert-large-uncased-news if exists)
would be starting points.

Computational Complexity: If using a model for span detection, it could
be similar complexity to fallacy detection: $O(N_t)$ per doc. However, fine-
grained span detection often uses sequence tagging (which is linear) or
sliding window classification. We might have to classify each candidate span
or token, which is more expensive. A practical approach: first do a quick
scan with rules (O($N_t$)) to mark potential propaganda-heavy sentences
(like those with many adjectives for loaded language, or certain cues), then
run the model on only those sentences or on fixed-length text segments
(like each sentence or paragraph). The worst-case complexity if run on all
text with a transformer is still manageable with batch processing and
perhaps using a slightly smaller model (distilBERT) if needed for speed.
Scalability: We can scale this by parallelizing similar to fallacy detection.
The tasks can even be merged to some extent: one could train a single
multi-task model to detect both fallacies and propaganda techniques
together (since they overlap and both require similar language
understanding). However, for modularity and explainability, separate
models might be clearer. Use distributed computing: e.g., process different
technique checks on different nodes or use pipelining (one worker identifies
candidate spans, another classifies them). Also, caching repeated phrases
across documents: if many docs share the same political slogans or clichés,
store their embeddings and results to avoid re-processing (this is where a
vector database (FAISS) can help: store vectors of known propagandistic
phrases; new text can be checked via nearest-neighbor search to quickly
flag known propaganda).
Code Template
Python Run
# Pseudocode for rule-based + ML propaganda detection
propaganda_flags = {tech: {"count": 0, "spans": []} for tech in P}
# 1. Rule-based scanning for cues
for sent in doc_data["sentences"]:
text = sent["text"].lower()
# Example rule checks:
if "what about" in text or "how about" in text:
propaganda_flags["whataboutism"]["count"] += 1
propaganda_flags["whataboutism"]["spans"].append(sent["text"])
# Check for name-calling via derogatory keywords
for insult in ["idiot", "racist", "ignorant"]: # extend this list
if f" {insult}" in text:
propaganda_flags["name_calling"]["count"] += 1
propaganda_flags["name_calling"]["spans"].append(insult)

# Loaded language: count strong subjective words using a lexicon
loaded_count = sum(1 for word in text.split() if word in loaded_words_set)
if loaded_count/len(text.split()) > 0.2: # if >20% words are loaded terms
propaganda_flags["loaded_language"]["count"] += 1
# store the phrase or sentence triggering it
propaganda_flags["loaded_language"]["spans"].append(sent["text"])
# ... (similar for other techniques like flag_waving, etc.)
# Mark repetition later (will need full document context)
# 2. Detect repetition propaganda
from collections import Counter
phrases = Counter()
for sent in doc_data["sentences"]:
# take a window of 3-5 words as potential slogan
words = sent["text"].lower().split()
for i in range(len(words)-3):
phrase = " ".join(words[i:i+3])
phrases[phrase] += 1
# Find phrases repeated unusually often
for phrase, count in phrases.items():
if count >= 3 and len(phrase.split()) > 1:
propaganda_flags["repetition"]["count"] += 1
propaganda_flags["repetition"]["spans"].append(phrase)
# 3. ML-based classification for more complex cases (e.g., flag_waving which might need c
technique_model = AutoModelForSequenceClassification.from_pretrained("myorg/bert-propagan
technique_tokenizer = AutoTokenizer.from_pretrained("myorg/bert-propaganda-techniques")
for sent in doc_data["sentences"]:
enc = technique_tokenizer(sent["text"], return_tensors='pt', truncation=True)
outputs = technique_model(**enc)
probs = outputs.logits.softmax(dim=1)[0] # assume single sentence input
# Suppose label mapping is: 0=none, 1=flag_waving, 2=glittering_generalities, etc.
label_idx = int(probs.argmax())
if label_idx != 0 and float(probs[label_idx]) > 0.8: # if high confidence propaganda
tech = technique_model.config.id2label[label_idx]
propaganda_flags[tech]["count"] += 1
propaganda_flags[tech]["spans"].append(sent["text"])
In this pseudocode:
We first use simple rules/lexicons to catch obvious instances.
Then we handle repetition by counting phrase occurrences.
Finally, we use an ML model for techniques that require understanding (the
example assumes a model that classifies a sentence into one of the
techniques or none). In reality, one might have to do a multi-label
classification since a sentence could use multiple techniques. This can be
adjusted by using sigmoid on logits and checking each technique
probability.
After detection, we calculate intensities and transparency violation:

Python Run
technique_outputs = []
for tech, info in propaganda_flags.items():
if info["count"] > 0:
intensity = 0.0
if tech == "loaded_language":
# intensity as max proportion of loaded words in any flagged span
intensity = max((sum(1 for w in span.split() if w.lower() in loaded_words_set
for span in info["spans"])
elif tech == "repetition":
# intensity based on max repetition count normalized (e.g., count/10)
max_phrase = max(info["spans"], key=lambda ph: phrases[ph])
intensity = min(1.0, phrases[max_phrase] / 10.0)
else:
# for others, use count or presence as a proxy for intensity
intensity = min(1.0, info["count"] / 5.0) # e.g., 5+ occurrences saturates i
# transparency violation using predefined weight
base_violation = transparency_weights.get(tech, 0.8) * intensity
trans_violation = min(1.0, base_violation + 0.2 * info["count"]/len(doc_data["sen
technique_outputs.append({
"technique": tech,
"intensity": round(intensity, 3),
"text_span": info["spans"][0][:100] if info["spans"] else "", # example span
"frequency": info["count"],
"transparency_violation": round(trans_violation, 3)
})
doc_data["document"]["propaganda_vector"] = { item["technique"]: item["frequency"] for it
Scoring & Calibration

Each propaganda technique’s detection may have its own confidence if using
ML; we will calibrate those similar to fallacies (via a validation set or using
known precision levels from literature). The intensity calculation may need
calibration: for example, our rule might flag any sentence with >20% loaded
words, but perhaps that threshold needs tuning so we don’t mark slightly
emotional language as fully propagandistic. We might use a development set of
news articles labeled for propaganda intensity to adjust these thresholds.
Technique weighting: Not all techniques are equally malicious. Glittering
Generalities (using vague positive terms) is propaganda but relatively benign in
terms of deception, so even if detected, its transparency_violation might be
moderate. On the other hand, Whataboutism actively evades accountability, so
we might assign it a higher base transparency violation. These weights ($u_p$
as mentioned) are set with expert input or by learning from rated data (if some
articles are rated for overall propagandistic content, we could do regression to
find which techniques correlate with low trust and set weights accordingly).
Composite scoring within this module: We might want an overall
Propaganda Score for the document. This could be something like
PropScore = 1 − ∏ (1 − v )
p∈P p
where $v_p$ is the transparency_violation for technique $p$. This ensures that
if any $v_p$ is high, PropScore is high (tending to 1). If none are present
($v_p=0$ for all), PropScore = 0 (no propaganda). We will calibrate this so that
an average news article (with maybe minor bias but not explicit propaganda)
scores low (around 0.1 or 0.2), while known propaganda pieces (like state-
sponsored disinfo articles) score above 0.8. Calibration might involve testing on
examples: e.g., articles known to be propaganda (perhaps from propaganda
corpora) and adjusting formula or weights until their scores align with
expectations.
Thresholding and Edge Cases:
If a technique is detected only once with low intensity (e.g., one mild loaded
word), we may not list it at all, or list with very low intensity. Possibly set a
threshold that intensity must exceed 0.2 to be considered noteworthy.

We ensure that overlapping concepts between techniques and fallacies are
handled: e.g., an ad hominem might trigger both Name-calling and a logical
fallacy. We can either report both (since they are different perspectives:
one is rhetorical technique, one is logical flaw) or unify them in explanation.
For scoring, if it's the same span, we should avoid double penalizing. One
way: if a span is already marked as a fallacy with severity, perhaps reduce
the propaganda transparency_violation for that span to not double-count
the impact.
False positives: Emotional language in a genuinely emotional context (e.g.,
a tragic news story) might look like loaded language but isn’t propaganda.
Our validation and calibration should catch this: if an article is simply sad
(uses words like "heartbreaking"), it might trigger loaded_language rules.
We can mitigate by recognizing context (maybe propaganda typically co-
occurs with political topics or persuasive intent). In such cases, we could
incorporate topic checks (if the article is straight news reporting on a
disaster, loaded words might not be propaganda but empathetic tone). This
is complex, but we note it for careful threshold tuning or additional context-
based rules.
Validation
We validate propaganda detection rigorously:
Use benchmark datasets: The SemEval-2020 Task 11 dataset provides
news articles with labeled propaganda spans and their technique
categories. We can directly evaluate our system on its dev/test set. We
would measure F1 score for span detection and classification accuracy for
technique labels. Given the complexity, a good system might achieve F1 in
the 0.4-0.6 range for span detection (as the task is challenging).
Manual review: Take a sample of articles across the political spectrum and
have domain experts or annotators identify propaganda techniques.
Compare with system output: Are we over-flagging benign content as
propaganda? Are we missing subtle propaganda? For instance, an opinion
piece might use oversimplification by presenting a complex issue in black-
and-white terms. If our system misses that, we refine by adding cues (like
detecting absence of nuance words or presence of extreme general
statements).

Frequency distribution: We’ll analyze how often each technique is
flagged across a large corpus. If, say, thought-terminating cliché is never
flagged, either it’s truly rare or our detection isn’t working; we then test on
known examples ("it is what it is" is a cliché that ends debate) to adjust
accordingly. If loaded language is flagged in almost every article, perhaps
our criteria are too lax, and we need to tighten to reduce false positives.
Overlap with fallacies: We specifically check cases where an instance
could be labeled by both modules. Ensure that if fallacy detection missed
something but propaganda caught it, or vice versa, we understand why.
This helps refine patterns. For example, if propaganda module flags many
Name-calling that fallacy missed as ad hominem, maybe the fallacy model
needs more training data for personal attacks, or our threshold was too
high there.
We use sanity checks: feed in deliberately neutral text (e.g., Wikipedia
articles) – we should get near-zero propaganda scores. Feed in overt
propaganda (like wartime propaganda texts or certain biased op-eds) – we
expect high scores. If results deviate, recalibrate.
Integration Notes
Interplay with Bias and Sentiment: Propaganda often correlates with
strong sentiment (highly positive or negative tone) and bias. Our system will
cross-reference: e.g., if loaded_language is flagged, the linguistic bias
module will likely also note the presence of loaded adjectives (there’s
intentional redundancy to ensure multiple perspectives on the same signal).
Pipeline modularity: This module can run in parallel or sequentially with
logical fallacies. In practice, they can be parallel since they analyze text
spans independently. However, to avoid duplication, we might combine
them into one text annotation pass: one loop over sentences can
compute both fallacy and propaganda features to save time. This is feasible
if we unify the model or do multi-task learning. For clarity, we separated
them conceptually.
Storage: For each document, we will store a summary of propaganda
techniques found (perhaps in a JSON field propaganda_hits listing technique
and span excerpts). We will also store the propaganda_vector of counts or
scores for quick filtering (e.g., find articles with flag_waving > 0 ). The
transparency_violation could feed into an overall “Manipulation Index”.

Use in Composite Score: The transparency_violation scores from this
module directly inform the document’s transparency_score (likely an
aggregate of propaganda and bias flags). For instance, if an article heavily
uses obfuscation and loaded language, its transparency_score will be low
(close to 0, meaning not transparent).
Explainability: Each technique can be displayed with an explanation. For
instance, highlight repeated phrases in the text or list the loaded words
identified. This is valuable for users to understand why the system flagged
something as propaganda.
Real-time vs batch: The rule-based part is very fast, but the ML
classification part is similar in cost to fallacy detection. If real-time
operation is required, we might rely more on the rules (giving a quick
approximate flag), and run the ML refinement later. Alternatively, have a
fast text classification (like a logistic regression on n-grams for propaganda
vs not) to give a quick score in real-time, then do the fine-grained labeling
in batch mode for detailed reports.
Linguistic Bias Analysis
Mathematical Foundation
Linguistic bias manifests in how information is presented rather than what is
said. We break this into subcategories:
Framing Bias: The polarity of framing (positive or negative light) and use
of subjective language to influence perception.
Source & Attribution Bias: How sources and actors are described (active
vs passive voice, credibility language, imbalance in who is quoted).
Lexical Bias: Loaded descriptors, euphemisms, dysphemisms, and toxic or
emotionally charged terms that reflect bias.
For each bias instance, we want to output:
Python Run
{
"bias_type": str, # e.g., "Framing Bias", "Attribution Bias", "Lexical Bias"
"polarity": float, # in [-1,1], where negative means bias against or negative
"affected_entities": [str], # which entities or groups are impacted by this bias (if a
"linguistic_markers": [str], # specific words or phrases that indicate the bias
"transparency_score": float # [0,1], 1 = fully transparent/unbiased language, 0 = stro
}

Several specific phenomena to capture:
Positive/Negative framing: e.g., describing the same fact with positive or
negative connotations. This can be measured by sentiment towards
entities: if an article consistently describes one group with positive words
and the opposing group with negative words, that’s asymmetric framing.
Asymmetric verb choice: e.g., using "X claims" vs "Y states". Words like
"claims" or "admits" can signal doubt or guilt. We identify such verbs and
measure if one entity is predominantly associated with more skeptical
verbs.
Hedging: presence of hedging phrases ("allegedly", "reportedly", "might").
We count these and note if they cluster around certain claims (maybe
indicating bias by downplaying commitment to a statement).
Presuppositions & Implicatures: These are tricky to automate. A
presupposition might be flagged by certain structures (e.g., "When did X
stop doing Y?" presupposes X did Y). We might look for common
presuppositional triggers (like "stop", "continue", "again" implying prior
events) and mark them.
Implicature: implied meaning beyond literal; we might not detect directly
but can catch some via semantic analysis (e.g., if statement A logically
implies B but B is not stated, or rhetorical questions).
Modal certainty: Look at modal verbs and adverbs indicating certainty:
words like "must, definitely, clearly" vs "maybe, possibly, arguably". We can
define an epistemic modality score for each sentence: +1 for strong
certainty, -1 for strong uncertainty. The presence of many hedges
(uncertainty) can indicate either cautious language or bias if unevenly
applied (e.g., hedging only when discussing one side).
Quote imbalance: We count quotes from different entities: If one side of a
debate is quoted 10 times and the other 0, that’s bias (coverage bias). We
can quantify: $Q_{entity}$ = number of quotes by or about an entity. Then
measure imbalance as a ratio or difference. If an entity of interest (like a
political candidate) is quoted significantly less than their opponent in an
article about both, bias is indicated.
Source credibility framing: Look for phrases that introduce sources with
biasing language: e.g., "According to reputable scientist Dr. A..." vs "so-
called expert Dr. B...". Adjectives around sources (reliable, extremist, etc.)
are markers. We can extract [ADJ + noun] patterns around named entities
in source attributions.

Active vs Passive voice: Passive voice can hide who did an action (e.g.,
"protestors were shot" vs "police shot protestors"). We can measure
passive voice usage especially in contexts that might shift blame. Using
dependency parse, identify sentences without an explicit subject (or with
passive constructions – in spaCy, check token.tag_ == 'VBN' and a
dependency of 'nsubjpass'). Compute passive_ratio = (# of passive
sentences) / (total sentences). Then see if passive voice appears
particularly when describing certain actors, indicating bias (like always
passive when military from one's own country does harm, to avoid naming
them).
Claim-evidence mismatch: If an article makes many assertions without
providing evidence, that’s a bias towards narrative over factual support. We
measure: for each claim (factual statement, maybe identified by presence
of verifiable detail or by our factuality module), check if it’s immediately
followed or supported by evidence (like a quote, a statistic, or a citation).
We can approximate by: if a sentence contains a claim (e.g., contains a
number or a specific allegation) and the next sentence does not contain a
quote, citation, or further detail, increment a counter for unsupported
claims. The ratio of unsupported claims can indicate bias/slant (as biased
pieces might assert things without backup, whereas balanced journalism
provides sources).
Loaded adjectives/adverbs: We compile a lexicon of words that carry
positive or negative charge beyond factual description (e.g., brutal, heroic,
alleged, allegedly). We scan text for these. For each, we note the context
(which entity or action is described). If Entity X is often near "brutal" and
Entity Y is near "heroic", that’s clear bias.
Euphemisms vs Dysphemisms: Euphemisms are mild or vague terms
for harsh realities (e.g., "enhanced interrogation" for torture), dysphemisms
are harsh terms for neutral things (e.g., "scheme" for plan). We can
maintain small lists of known euphemisms and their plain terms, as well as
dysphemistic synonyms. If these appear, note them. For example, calling a
government program a "scheme" (when not referring to a literal scheme)
could indicate bias.
Toxicity-weighted vocabulary: If the article uses insults or slurs (which
also overlap with name-calling), that indicates extreme bias or at least
strong negative tone. We can use a toxicity detector (like Perspective API’s
model or a RoBERTa toxic classifier) to score each sentence for toxicity. The
maximum toxicity or the fraction of sentences above a toxicity threshold
can be recorded.

Scoring:
Polarity: We can compute a bias polarity score in [-1,1] for each identified
bias instance or overall per entity. For example, if the language about a
politician is mostly negative (more negative sentiment words than positive),
that politician’s bias score might be -0.7. If positive, +0.7. At document-
level, if the article overall favors one side, we might give an overall polarity
(e.g., -0.5 if generally against the subject).
A simple approach: For each entity, take all words around it (within a
window or in same sentence) and sum their sentiment or connotation
values (we can use a sentiment lexicon or model to rate words).
Normalize to [-1,1]. That yields per-entity sentiment as a proxy for bias.
The affected_entities field can list those entities.
If bias is not entity-specific (e.g., framing bias in narrative),
affected_entities might be empty or a general audience.
Linguistic markers: We output the actual words/phrases found, e.g.
["claims", "allegedly", "extremist"] for attribution bias markers. These
come from the lists above (hedges, loaded words, etc.) that were triggered.
Transparency score: This is similar to the idea in propaganda: how much
does this kind of bias obfuscate the truth? If an article is full of loaded
language and hides responsibility with passive voice, transparency suffers.
We can derive a linguistic transparency as: 1 minus some weighted sum of
bias signals. For example:
\text{linguistic_transparency} = 1 - \gamma_1 \text{(hedge_density)} -
\gamma_2 \text{(loaded_word_density)} - \gamma_3 \text{(passive_ratio)}
- ...,
where each density or ratio is normalized [0,1] and $\gamma_i$ are
weights. This transparency score is 1 when language is neutral and clear,
and decreases as bias markers accumulate. We ensure it stays >=0. If
multiple bias types are present, we might output a combined transparency
score (or per bias type as well).
Implementation Strategy
Approach: Rule-based and lexicon-based methods first, backed by
statistical modeling for subtler patterns. Many bias indicators (hedges,
loaded words, passive voice) are straightforward to detect with rules and
dictionaries. For more complex aspects like polarity towards an entity or
implicature, we can use NLP models (e.g., sentiment analyzers, or even an
NLI model to catch implied meanings).

Primary Library: Use spaCy for dependency parsing (to catch passive
voice and subject-object relations), NLTK or TextBlob for sentiment
lexicons (or VADER for targeted sentiment towards entities), and sklearn
for any simple classifiers needed (e.g., we might train a logistic regression
to classify a sentence as biased vs neutral based on features count of bias
words, etc.). For hedging detection, use a curated list from linguistics
research (there are known hedge word lists). For toxicity, use Hugging
Face Transformers with a model like unitary/toxic-bert or Google’s
Perspective API if external API is allowed.
Pretrained Model: We might use a pretrained sentiment model (like
nlptown/bert-base-multilingual-uncased-sentiment for general sentiment) to
gauge tone towards entities. Also, a dependency-based rewriter to test
for presuppositions isn't readily available, but we can use an NLI model
(like roberta-large-mnli ) to check for implicit assertions: e.g., feed a
hypothesis “X did Y” and see if the text entails or presupposes it.
Computational Complexity: The rule/lexicon checks are linear in text
length (fast). Running a sentiment model or NLI per entity mention might be
costly: if an article has 20 sentences and 10 entities, running a transformer
on each entity context is at most 200 inferences, which is okay if
distributed. Many can be vectorized: e.g., sentiment on all sentences in one
batch.
Scalability: This module is not too heavy except any transformer usage.
For millions of docs, we lean on the lexicon approach primarily. The heavy
models (like NLI to detect implicature or subtle bias) might be reserved for
smaller batches or research mode. The pipeline will be designed to allow
toggling off some deep checks if we need pure speed (like skip NLI and
settle for obvious lexical cues). The rest (counts of words, passive voice
detection via parse) scales easily using spaCy’s efficient parsing. If needed,
we distribute documents across nodes and each does the parsing and
lexicon checks. The sentiment model can be run on a GPU in batches to
process thousands of sentences per minute.
Code Template
Python Run
bias_outputs = []
# Framing Bias detection
entity_sentiments = {} # accumulate sentiment for each entity
for ent in doc.ents:
if ent.label_ in ["PERSON","ORG","GPE","GROUP"]: # focus on entities that could be f

entity_sentiments[ent.text] = entity_sentiments.get(ent.text, 0.0)
# Use a sentiment analyzer (could be VADER or a transformer)
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
for sent in doc.sents:
sent_text = sent.text
# overall sentiment
vs = sia.polarity_scores(sent_text)
# Check if sentence contains any entity, distribute sentiment to those entities
for ent in doc.ents:
if ent.text in sent_text:
# use compound sentiment as a proxy (-1 to 1)
entity_sentiments[ent.text] += vs["compound"]
# Normalize entity sentiment and identify bias polarity
for ent, score in entity_sentiments.items():
if score != 0:
polarity = max(-1.0, min(1.0, score)) # Vader compound is already -1 to 1 roughl
# If entity has strong pos or neg sentiment, mark framing bias
if abs(polarity) > 0.3: # threshold for noteworthy bias
markers = []
if polarity < 0:
# find negative words near entity
for token in doc:
if token.text == ent and token.i+1 < len(doc):
# simplistic: next word if adjective
if doc[token.i+1].pos_ == "ADJ":
markers.append(doc[token.i+1].text)
else:
# find positive words near entity
for token in doc:
if token.text == ent and token.i+1 < len(doc):
if doc[token.i+1].pos_ == "ADJ":
markers.append(doc[token.i+1].text)
bias_outputs.append({
"bias_type": "Framing Bias",
"polarity": round(polarity,3),
"affected_entities": [ent],
"linguistic_markers": markers,
"transparency_score": None # will fill later after computing all
})
# Attribution Bias detection (reporting verbs and voice)
reporting_verbs_skeptical = {"claimed","alleged","admitted"} # etc.
reporting_verbs_neutral = {"said","stated","according"}
for sent in doc.sents:
for token in sent:
if token.lemma_ in reporting_verbs_skeptical:
# If found, that's a marker of bias (casting doubt)
markers = [token.text]
# Who is subject of this verb?

subj = [child.text for child in token.children if child.dep_ == "nsubj"]
affected = subj or []
bias_outputs.append({
"bias_type": "Attribution Bias",
"polarity": -0.5, # assuming skeptical verbs imply negative bias toward
"affected_entities": affected,
"linguistic_markers": markers,
"transparency_score": None
})
elif token.lemma_ in reporting_verbs_neutral:
# If exclusively one side gets neutral verbs and the other gets skeptical ver
pass
# Passive voice and agency hiding
passive_count = 0
for sent in doc.sents:
# if sentence is passive
for token in sent:
if token.dep_ == "nsubjpass": # passive subject
passive_count += 1
# We could mark the sentence or entity as being hidden
break
passive_ratio = passive_count / len(list(doc.sents))
if passive_ratio > 0.3: # if >30% passive, possible bias in hiding actors
bias_outputs.append({
"bias_type": "Attribution Bias",
"polarity": 0.0,
"affected_entities": [],
"linguistic_markers": ["passive_voice"],
"transparency_score": None
})
# Lexical Bias (Loaded words, Euphemisms/Dysphemisms)
loaded_markers = []
for token in doc:
if token.lower_ in loaded_words_set:
loaded_markers.append(token.text)
if loaded_markers:
# Determine polarity: if mostly negative words, bias negativity; if positive glitteri
polarity = 0
for w in loaded_markers:
polarity += loaded_words_sentiment.get(w.lower(), 0)
polarity = max(-1, min(1, polarity/len(loaded_markers)))
bias_outputs.append({
"bias_type": "Lexical Bias",
"polarity": round(polarity,3),
"affected_entities": [], # could refine: assign to entity if the word is describ
"linguistic_markers": loaded_markers[:5], # list top 5 markers
"transparency_score": None
})
# Calculate transparency_score for each bias output if not set

for b in bias_outputs:
# Example: base transparency score inversely related to intensity of markers
# If many markers, transparency suffers.
marker_intensity = min(1.0, len(b["linguistic_markers"])/10.0)
# Lower transparency more if polarity is extreme (absolute near 1)
polarity_factor = (abs(b["polarity"]) if b["polarity"] is not None else 0)
The above pseudocode illustrates:
Using VADER for quick sentiment as a proxy for framing (a transformer
model could be used similarly).
Checking reporting verbs and passive voice via dependency parse for
attribution bias.
Scanning for loaded words for lexical bias.
Calculating a simple transparency score: if many markers and strong
polarity, we reduce transparency.
We’d likely expand this significantly in production (more sophisticated checks,
integration with entity analysis). Also, integrate with the entity sentiment
computed in the next module to avoid double work.
Scoring & Calibration
Bias is nuanced, so calibration requires care:
Polarity calibration: Ensure that the polarity score corresponds to
meaningful bias. For instance, if an article is neutral, the sum or average of
polarity for all entities should be near 0. If our method shows a bias (say
-0.2) for some neutral text, we might adjust thresholds (maybe requiring a
higher sentiment imbalance to flag). Conversely, known partisan articles
should yield strong polarity differences for subjects (like a partisan article
might mention one politician with +0.8 tone and another with -0.8).
We might calibrate using known bias datasets (e.g., articles labeled
left/right or pro/anti on an issue) to see if our polarity measure correlates. If
an article is rated as strongly conservative (pro one side), our entity polarity
should reflect that side favored positively and the other negatively.
Hedge and certainty scoring: We set thresholds for what constitutes
heavy hedging. Perhaps measure hedge_density = (# of hedge
words)/(total words). If above, say, 5%, that's significant hedging. We
calibrate by analyzing reference corpora: quality journalism vs gossip blogs
might have different levels.

Transparency score: Since this is somewhat subjective, we may calibrate
it by comparing to expert judgments of article clarity. If experts rate an
article as very transparent (straightforward), our score should be high. If
our score is low for such an article, maybe we are penalizing something like
hedges too much (some hedging is normal and not deceitful). So we adjust
weights $\gamma_i$. For example, maybe passive voice frequency
shouldn't lower transparency too harshly unless it's extreme.
We will also ensure that transparency_score here is in line with the
propaganda transparency_violation: they might be combined later. So if
an article has both propaganda and biased language, both modules will
output low transparency and combined should be low. We might avoid
double counting by dividing responsibilities: propaganda module hits more
on emotional manipulation, linguistic bias module hits on tone and framing.
If both find issues, it's truly low transparency.
Thresholding: Not every instance of bias language should trigger an output.
We might only list bias_outputs for notable cases. E.g., if loaded_markers are
just 1-2 mild words in a long article, that might be normal. So require a
minimum count or intensity (like we did: >20% loaded words or multiple
occurrences to flag loaded_language bias). Similarly for reporting verbs: if an
article uses "claimed" once but mostly "said", maybe not flag unless it's clear
only one person gets the "claimed" treatment repeatedly. Thus, thresholds like
more than 2 instances of skeptical verbs aimed at same entity.
Edge case: some articles explicitly labeled as opinion might intentionally use
strong language – our system can still flag bias, but perhaps the context
(metadata) says it's an opinion piece, which might be acceptable bias. We can
reflect on integration (maybe lower severity if genre=opinion).
Validation
Validation for bias features can use:
Labeled datasets: There are datasets for media bias detection at the
article level (classifying left vs right bias). We can see if our features
correlate. For example, an article classified as extreme left or right likely
has strong linguistic bias signals (like very negative toward the other side).
If our system doesn’t pick that up, we missed something. If it flags bias in
something rated center, maybe we overtuned.

Manual case studies: Take pairs of articles on the same event from
sources with different slants. Our system should highlight different word
choices (markers) and produce different bias vectors. Example: one calls a
group "freedom fighters", another calls them "terrorists". The system
should list "freedom fighters (positive bias)" vs "'terrorists' (negative bias)"
markers, affected entity is that group. These known examples validate
lexicon approach to euphemisms/dysphemisms.
Statistical checks: We expect certain words to be top markers across a
corpus for bias: e.g., "allegedly", "claims" often appear in biased contexts.
We can gather all linguistic_markers output and see if they align with known
bias-indicative words. If nonsense words appear, our detection might be off.
We will test extreme scenarios: a clearly biased opinion piece and a dry
news report. Ensure the opinion piece yields multiple bias outputs (low
transparency, strong polarity) while the news report yields minimal. If not,
adjust detection rules.
Integration Notes
This module works closely with the Entity-Level Sentiment & Bias
Analysis (coming next). In fact, the computation of entity sentiment is
shared. We may integrate them: the entity-level module will produce the
sentiment per entity, which we used here for framing bias. To avoid
duplication, we might compute entity sentiment once and share.
Dependency on NER: We rely on named entity recognition to know
who/what is being discussed (for affected_entities). That comes from the
foundation stage. Good NER ensures we attribute bias correctly (e.g., if NER
fails to detect an entity and we see a negative word, we might list no
affected_entity, losing context).
The outputs from this module (especially the lists of linguistic_markers )
are very useful for explanation. In the dashboard, we might have a section
"Loaded Language Used:" listing the emotional words, or "Hedging Words:"
listing "allegedly, reportedly". This helps users see subtle bias cues.
Overlap with propaganda: There is some overlap (loaded language
appears in both). We must ensure consistency: perhaps propaganda
module focuses on the presence and intensity, while bias module focuses
on the polarity direction of such loaded language. The transparency_score
we output here might be combined with the one from propaganda to an
overall transparency rating. We should decide how (maybe a weighted
average or max).

Storage: Each bias output can be stored. Possibly we have a table of bias
instances: doc_id, bias_type, entity, polarity, markers. This might be a lot of
entries, but it allows queries like "find all instances where media used
'terrorist' to describe someone". Alternatively, store just aggregated info
(like counts of certain markers).
Downstream, when computing composite scores, the bias indicators will
contribute to an Overall Bias Score for the document. We might
construct an overall_bias_vector (as per the specification) which includes
things like average sentiment bias, hedge density, etc. This vector
essentially is built from the features here.
Real-time usage: Linguistic bias detection is relatively fast because it’s
mostly rule/lexicon. It could be run in real-time easily (a few milliseconds
per doc for lexicon scans, plus sentiment model if used – VADER is fast,
transformer sentiment would be slower but still possibly under 0.5s per doc
on CPU). So this component could be enabled in a live system. It doesn't
require heavy GPUs, except maybe if using an NLI model for implicatures
(which we can skip in real-time due to latency).
Factuality, Truthiness & Data Accuracy
Mathematical Foundation
This component evaluates the verifiability and accuracy of factual claims in the
text. We define several metrics:
Claim Count ($N_c$): number of factual claims or assertions in the
document. (A "claim" here means a statement that can be checked or
verified, such as a statistic or a concrete fact.)
Verified Claim Ratio ($r_{vc}$): proportion of claims that are backed by
evidence or citation. If $N_v$ is the number of claims with at least one
supporting source (citation, quote from expert, or reference to data), then
r = N v
vc N
c
(If $N_c=0$, define $r_{vc}=0$ by convention.)
Factuality Score ($F$): an overall measure [0,1] of how fact-based and
truthful the document is. This will aggregate multiple signals: specificity,
verifiability, consistency, etc. Higher means more factual.
Misleading Score ($M$): [0,1] indicating use of misleading techniques
(out-of-context stats, overgeneralization). High if many such issues present.
Data Quality Score ($D$): [0,1] focusing on numeric data quality –
whether numbers are consistent, plausible, and contextualized.

Transparency Score ($T$): [0,1] indicating how open the article is about
sources and methods (similar to previous transparency but here specific to
factual sourcing).
Numerical Consistency ($C_n$): [0,1] how internally consistent the
numbers and stats are in the document. 1 means no contradictions, 0
means blatant contradictions.
Logical Flow Score ($L_f$): [0,1] coherence of the argumentation
structure from a factual/logical standpoint (distinct from emotional or
rhetorical flow). 1 means the argument logically flows without
contradiction, 0 means severe logical inconsistency.
Now, how to compute these:
Claim identification: We use a combination of patterns and possibly an
information extraction model to count claims. For example, sentences with
numerical figures, dates, or specific names often indicate a factual claim. Also,
sentences with assertive verbs ("is", "has", "will") about verifiable facts. We
might use a simple classifier or regex (e.g., any sentence with a number or
proper noun can be considered a claim for counting purposes).
Let $S_{\text{claims}}$ be the set of sentences identified as claims. Then $N_c
= |S_{\text{claims}}|$. Each such sentence $s$ might be checked for
evidence:
Does it contain a reference (like a URL, or “according to [source]”)? Does it
cite a study or have a quote from an expert?
We define an indicator $I_{\text{source}}(s) = 1$ if $s$ or its neighboring
sentence contains an explicit source. Sum $N_v = \sum_{s \in
S_{\text{claims}}} I_{\text{source}}(s)$.

Claim specificity: Another sub-metric is specificity: vague statements
("Experts say X", "It could be that Y") are less verifiable. We can estimate
specificity by presence of concrete details: numbers, proper nouns, named
dates, etc. A sentence specificity score could be
σ(s) = 1 − 1{contains vague phrases or lacks proper nouns/numbers}.
So a sentence with no specific info might get $\sigma(s)=0$ (very vague), while
a fully detailed claim $\sigma(s)=1$. The average specificity of claims can
weigh into factuality.
External citation count: If the text has footnotes or hyperlinks (common in
web articles), count them. More citations generally increase $T$ (transparency)
and potentially factuality, but quality matters too:
We could differentiate high-quality sources (mainstream media, academic
journals) vs low-quality ("some blog"). If we had a source reliability DB, we
assign quality scores to citations. Lacking that, count all citations.
Fact density: We define fact density as claims per sentence or per word. $
\text{fact_density} = \frac{N_c}{\text{total sentences}}$ (this can be part of
output as in sentence-level we had something similar). A higher fact density
usually indicates more informative content, but could also correlate with dry
reporting. It's not directly a score but can feed into Factuality Score.
Logical flow (factual): Check if conclusions follow from evidence presented.
This can be partly assessed by looking at discourse markers and whether
premises are provided for assertions. We might create a simple graph of claims
and see if they contradict: e.g., if sentence A says "X increased" and sentence B
later says "X decreased", that’s a logical inconsistency. Use an NLI model for
contradiction: pair up statements that refer to the same entity or quantity. For
each pair $(s_i, s_j)$ in document that discuss same topic, let $NLI(s_i, s_j)$
output "contradiction/neutral/entailment". If any contradiction is found with high
confidence, logical flow score $L_f$ drops significantly. For example, if one
contradiction, maybe $L_f = 0.5$, if multiple, $L_f=0$.
Numerical consistency: Implement rules:
If two numbers refer to the same thing (check if they share nouns or
entities) and differ significantly, flag. Example: "the population is 5 million"
vs "in that city of 7 million" – conflict.

Sum rule: if percentages are listed like "A 50%, B 30%, C 25%", sum=105%
> 100% is a red flag. We can attempt to catch any list of percentages
summing outside 90-110% range (account for rounding).
Range rule: If any number is clearly out-of-range given context words (like
"age 200", "1000% increase" might be possible in rare cases but likely
exaggeration if context doesn’t justify).
Units check: if units are mentioned, ensure consistency (e.g., if earlier "10
km" later "6 miles" referring to same distance, check if they match
conversion roughly; this is complex, might skip conversion but ensure same
units or clarify unit changes).
We quantify $C_n$ as 1 minus penalty for each inconsistency found. If no
issues, $C_n=1$. If one minor issue, maybe $C_n=0.8$. If a major outright
contradiction or impossible stat, $C_n$ could be 0.0. We might set $C_n = 1
- \frac{\text{# of numeric inconsistencies}}{\text{# of numeric claims}}$
as a simple metric (clamped to 0).
Misleading Indicators: We track presence of phrases that are known to be
misleading:
Overgeneralizations: words like "always", "never", "everyone", "no one".
We can flag sentences containing universal quantifiers.
Unverifiable claims: phrases like "It is said that...", "Many people
believe..." with no source. These can be detected by patterns ("it is said",
"people are saying", "many believe", "experts claim" without naming). Each
instance adds to a counter.
Correlation vs causation: harder to detect automatically, but clues:
usage of correlation language ("linked to", "associated with") misinterpreted
as causation ("causes"). If we see "X causes Y" without evidence and it’s a
known debated correlation, we might not catch without external
knowledge. But maybe if "cause" is claimed where data only shows
correlation (we might flag use of "cause" if the text lacks explanation).
Clickbait phrases: "You won’t believe", "shocking truth", etc. Those we
can list and search.
We combine these into a misleading count or score. For example, if 3
different misleading indicators appear, $M$ could be high. Alternatively,
define
M = 1 − exp(−k ⋅n )
mislead
for some $k$ to quickly ramp up towards 1 with more issues.

Factuality Score (F): This is an aggregate intended to summarize truthiness.
We could formulaically combine:
| F   | = w | r + | w σˉ | + w | C + w | L + w (1 − M)+ | w D′ |
| --- | --- | --- | ---- | --- | ----- | -------------- | ---- |
|     | 1   | vc  | 2    |     | 3 n   | 4 f 5          | 6    |
|     |     |     |      |     |       |                |      |
where $\bar{\sigma}$ is average specificity of claims, $D^{\prime}$ is data
quality (we incorporate $C_n$ in that already). Also consider external signals: if
we had an external fact-check result or the publisher’s reliability, but in-text
features alone might be these. The weights $w_i$ would be chosen so that $F$
aligns with human judgments of factuality (maybe learned via regression on
some labeled set or set heuristically). For now, consider equal weighting or
emphasize more important ones: e.g., $w_1, w_3, w_4$ might be larger
because evidence, consistency, coherence are critical.
Data Quality Score (D): Focus on numeric and data handling. This could
combine numeric consistency ($C_n$), context (presence of baseline
comparisons, sample sizes if claiming studies, etc.), and completeness (e.g., if
stats are given, do they mention source or methodology?). We can start with
| D   | = 1(C | +   | I         | +   | I           | )   |     |
| --- | ----- | --- | --------- | --- | ----------- | --- | --- |
|     |       | n   | baselines |     | methodology |     |     |
|     | 3     |     |           |     |             |     |     |
where $I_{\text{baselines}}$ is an indicator or small score (0/1 or 0-1) if
baseline/context is provided for key numbers, $I_{\text{methodology}}$ if
methods or sample size mentioned for surveys/polls. These are binary-ish; we
can treat them as contributions (1 if present, 0 if absent, perhaps 0.5 if
partially). If none applicable, those terms might be just 1 (meaning no penalty if
no data given at all, though that itself might reduce F as fewer facts).
Transparency Score (T) (for this module’s outputs) would align with $r_{vc}$
largely: if many claims are sourced, transparency is high. Also if the author
clearly distinguishes fact vs opinion (which might show by less misleading
language). So:
1(r
| T   | =   | +   | I         | )   |     |     |     |
| --- | --- | --- | --------- | --- | --- | --- | --- |
|     | 2   | vc  | citations |     |     |     |     |
|     |     |     |           |     |     |     |     |
where $I_{\text{citations}}$ is normalized count of external references (e.g., #
of hyperlinks / # of claims, capped at 1). If there are no claims, transparency
about sources is moot; we could define transparency as 1 in trivial case of no
factual claims (or exclude such pieces from this measure). If $N_c=0$ and the
piece is pure opinion, we might treat factuality-related transparency as not
applicable.
Implementation Strategy

Approach: Rule-based for many checks (regexes for patterns, numeric
comparisons), and lightweight ML for claim detection or contradiction
detection. We want minimal supervision: rather than training a heavy fact-
check model, we rely on logic and public knowledge. For claim identification
and contradiction, we might use off-the-shelf models: e.g., an NLI model for
contradiction (not trained on our data but general).
Primary Library: Python’s standard text processing and some math:
Use regex and parsing for finding numbers and percentages.
Possibly use spaCy dependency parse to link numbers to entities (e.g.,
if two numbers have the same nearest noun, they refer to same thing).
NumPy/Pandas for any statistical calcs (like sum of percentages).
Huggingface Transformers for NLI (e.g., roberta-large-mnli model
to detect contradictions between sentences).
Maybe use heuristics or SciPy for outlier detection if we had
distributions (but we likely won’t unless comparing to external data).
Pretrained Model:
NLI model (RoBERTa MNLI) to evaluate consistency: e.g., for each pair
of claim sentences, we check entailment vs contradiction.
Perhaps a question generation+question answering approach for
verification (though probably too advanced for unsupervised). But one
idea: try to verify claims via a search or a QA system (like ask a QA
model if the claim is supported by the article’s own content or known
facts). This might be out of scope, but worth noting if future extension
uses e.g. google/flan-t5 for truthiness.
Possibly use a fact-checking model like one from the FEVER task to
get a sense if a claim is likely true or not by retrieving from Wikipedia.
However, that goes beyond just reading the article’s content.
Computational Complexity: Counting and regex is linear. The heavy part
is NLI pairwise comparisons which could be $O(N_c^2)$ in worst case if we
compare each claim sentence with every other. If an article has 20 claims,
that's 190 pairs, which is okay. If an article has 100 claims (rare), that's
4950 pairs, a bit heavy but still under a few thousand checks. We can
optimize by only comparing claims on same topic: cluster by entity or noun
overlap first.
Checking numeric consistency is linear in number of numeric mentions
but might involve pairwise comparison of numeric mentions which is
similar complexity (comparing all number pairs maybe).

Searching for sum of percentages is linear in text (just find if "%"
appears multiple times in a context of a list).
Scalability: At 1M docs, the NLI step for each doc could be too slow if done
naïvely. We can scale by:
Only run NLI when potential contradiction cues exist (like antonyms or
negations present). Or randomly sample pairs for efficiency.
Use vector embeddings for sentences: e.g., encode all claim sentences
with a sentence transformer, then find potentially contradictory ones by
similarity (contradictions often have the same context but we could
identify likely pairs by high semantic similarity and presence of negation
words). This reduces pairs to check.
Use multiprocessing: each process or GPU can handle NLI for one doc
at a time or batch multiple comparisons from many docs (the NLI
model can take a batch of pairs).
If extremely needed, skip NLI for speed and rely on simpler
contradiction checks (like contradictory phrases).
Many of these checks (overgeneralization, "everyone says") are trivial
to scale (just text scan).
Summation and numeric checks are trivial computationally.
So the potential bottleneck is the NLI; if performance is an issue in
production, we can disable or scale it down for batch runs only on
suspicious docs.
Code Template
Python Run
factuality = {
"claim_count": 0,
"verified_claims": 0,
"unverifiable_phrases": 0,
"external_citations": 0,
"misleading_indicators": 0,
"numeric_issues": 0,
"contradictions": 0
}
claims = []
# Identify claims (simple heuristic: sentences with numbers or proper nouns or factual ve
for i, sent in enumerate(doc_data["sentences"]):
text = sent["text"]
# A quick heuristic: contains a digit or "according to" or year or factual trigger wo
if re.search(r'\d', text) or re.search(r'\baccording to\b', text, flags=re.IGNORECASE
claims.append((i, text))

factuality["claim_count"] += 1
# Check for evidence in or after this sentence
if re.search(r'\baccording to\b|\bstudy\b|\bresearch\b|\breported (by|in)\b|http'
factuality["verified_claims"] += 1
else:
# maybe check next sentence for continuation of evidence
if i+1 < len(doc_data["sentences"]):
nxt = doc_data["sentences"][i+1]["text"]
if re.search(r'\baccording to\b|\bstudy\b|source|report', nxt, flags=re.I
factuality["verified_claims"] += 1
# Check for vague language in the claim
if re.search(r'\bexperts say\b|\bpeople are saying\b|\bsome suggest\b', text):
factuality["unverifiable_phrases"] += 1
# External citations count (hyperlinks or references)
if "http://" in text or "https://" in text or "[" in text and "]" in text:
factuality["external_citations"] += text.count("http")
# Misleading indicators scanning whole doc
full_text = " ".join([s["text"] for s in doc_data["sentences"]])
# Overgeneralizations
for term in ["always","never","everyone","no one","nobody","all of them"]:
if re.search(fr'\b{term}\b', full_text, flags=re.IGNORECASE):
factuality["misleading_indicators"] += 1
# Clickbait phrases
for term in ["won't believe","shocking","secret revealed","undisputed truth"]:
if re.search(term, full_text, flags=re.IGNORECASE):
factuality["misleading_indicators"] += 1
# Numeric consistency checks
numbers = [] # list of (number, context)
for match in re.finditer(r'\b\d+(\.\d+)?\b', full_text):
num = float(match.group())
# capture a few words around the number as context
context = full_text[max(0, match.start()-10): match.end()+10]
numbers.append((num, context))
# Compare numbers for contradictions or inconsistencies
for j, (num1, ctx1) in enumerate(numbers):
for k, (num2, ctx2) in enumerate(numbers):
if k <= j:
continue
# If numbers refer to same context (simple check: share a word in context)
common_words = set(ctx1.split()) & set(ctx2.split())
# e.g., if both mention "million" or an entity name
if len(common_words) > 0:
# If they differ significantly
if abs(num1 - num2) > max(5, 0.2 * max(num1, num2)):
# If difference is not explainable by time context (ignoring advanced log
factuality["numeric_issues"] += 1
# Percentage sum check
if re.search(r'\b\d+%.*\d+%.*\d+%', full_text):
# If multiple percentages in one sentence or paragraph
percents = [float(p.strip('%')) for p in re.findall(r'\d+%', full_text)]
total = sum(percents)

if total > 110: # allow some slack for rounding
factuality["numeric_issues"] += 1
# Contradiction detection using NLI model for claims (simplified: compare each pair of cl
from transformers import AutoModelForSequenceClassification, AutoTokenizer
nli_tokenizer = AutoTokenizer.from_pretrained("roberta-large-mnli")
nli_model = AutoModelForSequenceClassification.from_pretrained("roberta-large-mnli")
for i, (idx_i, claim_i) in enumerate(claims):
for j, (idx_j, claim_j) in enumerate(claims):
if j <= i:
continue
# Only compare if likely related (common entities or nouns)
common = set([ent.text for ent in nlp(claim_i).ents]) & set([ent.text for ent in
if not common:
continue
pair_input = nli_tokenizer.encode(claim_i, claim_j, return_tensors='pt', truncati
outputs = nli_model(pair_input)[0]
# MNLI labels: 0 = contradiction, 1 = neutral, 2 = entailment
pred = int(outputs.argmax())
if pred == 0: # contradiction predicted
factuality["contradictions"] += 1
(Note: In practice, we would batch NLI calls rather than one by one. Also, we
used nlp for NER in contradiction check for simplicity — that’s the spaCy
model already loaded earlier.)
After gathering counts:
Python Run
# Compute final scores
claim_count = factuality["claim_count"]
verified = factuality["verified_claims"]
if claim_count > 0:
verified_ratio = verified / claim_count
else:
verified_ratio = 0.0
# Factuality Score combine factors
# Normalize counts to [0,1] by scaling by some constants or relative to doc length
contradiction_penalty = min(1.0, factuality["contradictions"] / 2) # each contradiction
misleading_penalty = min(1.0, factuality["misleading_indicators"] / 5)
numeric_penalty = min(1.0, factuality["numeric_issues"] / 3)
transparency_score = (verified_ratio + min(1.0, factuality["external_citations"] / max(1,
data_quality = 1 - numeric_penalty # simple: if no numeric issues, perfect; some issues
logical_flow = 1 - contradiction_penalty
misleading_score = misleading_penalty
factuality_score = (verified_ratio*0.4 + (1-misleading_penalty)*0.2 + data_quality*0.2 +
# Assign to doc_data
doc_data["document"].update({

"factuality_score": round(factuality_score, 3),
"claim_count": claim_count,
"verified_claim_ratio": round(verified_ratio, 3),
"misleading_score": round(misleading_score, 3),
"data_quality_score": round(data_quality, 3),
"transparency_score": round(transparency_score, 3),
"numerical_consistency": round(1-numeric_penalty, 3),
"logical_flow_score": round(logical_flow, 3)
})
Scoring & Calibration
We combine components carefully:
If $N_c$ is small, factuality_score should possibly rely less on some ratios.
For example, an opinion piece with 0 claims would get $N_c=0$,
$r_{vc}=0/0$ (we set 0). We should interpret that as "not fact-based, but
also not making false claims". Possibly we consider factuality not applicable
or give a medium score. We might choose to default factuality_score to 0.5
for pieces with no claims, indicating neither factual nor unfactual. Or we
treat opinion pieces separately via metadata.
We calibrate weights $w_i$ in factuality_score by testing on known truthful
vs misleading articles. If we have a set of articles flagged by fact-checkers
as unreliable, our score should be low. We can iterate weight adjustments.
For instance, if our system under-penalizes lack of sources, we raise that
weight.
Verified claim ratio $r_{vc}$ will often be low for media like TV transcripts
(no citations in text). We calibrate not to punish too harshly if domain
typically doesn’t cite. However, the academic use-case might consider
citation very important. The weighting can be adjusted per context or given
domain expert input.
Numerical consistency: calibrate what constitutes a major issue vs minor.
E.g., two close numbers (100 vs 101) might trigger a naive difference
check, but we should ignore minor differences. We put thresholds (like in
code, >20% diff or >5 absolute).
Outlier detection calibration: If an article says "5 million attended" and we
suspect it's improbable, without external data it's guesswork. We might skip
labeling something outlier without context.
Misleading indicators: These are binary-ish; too many triggers might
exaggerate $M$. We ensure multiple occurrences of the same phrase don't
overcount if not intended (maybe count unique categories of misleading
patterns rather than raw count).

We set threshold guidelines: for example, if factuality_score < 0.3, it's likely
a very unreliable article (multiple contradictions, no sources, etc.). If > 0.7,
quite factual. We might calibrate these thresholds by reviewing some
known examples manually.
Validation
For factuality and accuracy, we test against:
Known ground truth: If we have some articles that have been fact-
checked (e.g., those labeled by fact-checkers as true/false or high-
quality/low-quality), see if our scores correlate. E.g., an article debunked as
false should get low factuality_score, high misleading_score.
Synthetic checks: Create a fake paragraph with a clear contradiction:
e.g., "Ten people attended the event. Later in the report: Twenty people
attended the event." The system should catch this and set
numerical_consistency low and contradiction count at least 1. Verify that
logical_flow_score goes down accordingly.
Test numeric consistency: input a simple scenario: "That's 120% of the
population." (which is impossible >100%). Our numeric check should flag
that as an issue.
Test verification: give a sentence "According to a study by XYZ, coffee cures
disease." The system should count 1 claim, detect "according to" so mark it
verified, thus transparency high for that claim.
Conversely, "Experts say coffee cures disease." (no specific source) should
count as a claim and unverifiable phrase, thus lower transparency.
Cross-validation: We might not have a labeled dataset for all these sub-
metrics, but we can do internal consistency. For instance, if $r_{vc}$ is low
and also $M$ is high (lots of misleading cues), likely factuality_score should
be low – ensure our formula reflects that synergy (by being weighted to
drop a lot in that case).
Check distribution: run on a sample of 1000 random articles. If 90% get
factuality_score ~0.9, maybe our criteria are too lax. If many get ~0.2,
maybe too strict. Adjust until distribution seems reasonable (maybe a slight
skew toward high if most mainstream articles are indeed fairly factual, with
some outliers low).
Ensure that logical_flow_score correlates with fallacy detection (if our
fallacy module found a lot of logical issues, logical_flow_score here should
be low too). We might unify those or cross-check. If there's conflict,
something is off.
Integration Notes

Inter-module links: The factuality analysis links with stance and entity
analysis. For example, if our stance detection finds the article contradicts
itself on a stance, that is effectively a factual consistency issue (internal
conflict). We could feed that info here (the conflict_score from stance could
reduce logical_flow_score).
The metadata like publisher reliability can provide prior for factuality:
known disinformation sites could have a baseline lower factuality. We might
incorporate that later when aggregating (like a prior probability).
The outputs here (factuality_score, etc.) are key parts of the final
aggregate quality score. Likely, factuality_score will be one of the most
heavily weighted factors for overall article quality.
Data storage: We store at least the aggregate fields in the document
record. We might also store some details (maybe a boolean if any
contradiction found, number of misleadings, etc.). Potentially, we could
store the text of contradictory sentences or the mismatched numbers for
explanation. E.g., in a separate table of detected issues: doc_id, issue_type,
description ("Contradiction between sentence 2 and 5"), or ("Sum of
percentages = 120%").
Explainability: We will surface key issues: e.g., "No sources cited for 5
claims," "Contains absolute terms like 'never' which might be misleading,"
"Inconsistent figures: reported 5 million in one place and 7 million in
another." These can be part of a report or tooltip for users. The numeric
and contradiction checks provide concrete things to highlight.
Real-time vs Batch: This component can be partially real-time. Simpler
checks (counts, regex) are fine. The heavy part is contradiction checking.
For a quick assessment, we might skip NLI and just do the easy checks,
yielding a partial factuality score near instantly. The full thorough analysis
with NLI can be done in batch or on demand when deeper analysis is
requested. So we design it to degrade gracefully: a flag to turn off deep
consistency checks for speed.
Dependency: It uses NER and parsing from earlier, as well as the sentence
splitting. Also uses entity analysis (for contradictions, we used NER to find
common entities between claims to reduce comparisons).
This module will also inform stance detection indirectly: if $N_c$ is large
and factuality high, stance might be more evidence-based; if factuality low
and bias high, stance might be more propagandistic.

Weighting with Bias: Sometimes an article can be factual (no false info)
but still biased in tone. We keep those dimensions separate (factuality vs
bias). In final aggregation, we consider both. We should ensure an article
that is factual but biased doesn’t get a too low "overall quality" – it should
get credit for factuality, but flagged for bias. Conversely, an article could be
neutral tone but factually incorrect (that’s rare, but possibly a
misinformation piece that sounds calm but has false claims) – that would
score low factuality but maybe low bias, still overall problematic. So these
scores must be used in a composite carefully.
Entity-Level Sentiment & Bias Analysis
Mathematical Foundation
For each named entity $E$ (person, organization, group, etc.) in the text, we
compute a profile with the following fields:
sentiment ($S_E$): float in [-1,1] indicating overall sentiment toward the
entity in this document (positive means the entity is portrayed favorably,
negative unfavorably).
toxicity ($X_E$): float [0,1] indicating the level of toxic language (insults,
slurs) directed at or associated with the entity.
quote_count ($Q_E$): integer count of how many quotes are attributed to
this entity (how often they get to speak or are quoted).
threat_association_score ($T_E$): float, measuring how strongly the
entity is associated with threat or fear-related terms (higher if the text links
the entity to danger, crime, etc.).
framing_score ($F_E$): float capturing empowering vs undermining
language used with the entity. (Higher might mean the entity is shown as
powerful or positive, lower means portrayed as weak or negative. Possibly
this is similar to sentiment, but can focus on verbs: e.g., "leads" vs "flees".
We can define it separately.)
moral_valence ($M_E$): float on a hero-villain spectrum. Positive if entity
is framed as morally good/heroic, negative if as villainous/immoral.
conflict_involvement (could be binary or float): whether the entity is
portrayed as part of a conflict (antagonist/protagonist). We can derive a
score or simply a boolean flag if they are in a conflict context.
To calculate these:

Sentiment ($S_E$): We accumulate sentiment of all mentions of $E$. If
$E$ appears in multiple sentences, for each mention, get the local
sentiment (which can be from a sentiment model focusing on context
around the name). $S_E$ could be an average of those sentiments.
Alternatively, use an aspect-based sentiment approach: treat the entity as
the aspect and determine sentiment. A formula:
S = 1 ∑ sentiment(context around mention )
E N
E
mention i i
clipped to [-1,1]. We also ensure any direct descriptions (adjectives
attached to $E$) influence this strongly. If conflicting sentiments appear, it
might average near 0 (neutral) unless we want to reflect conflicting
portrayal (which could be flagged separately as inconsistent).
Toxicity ($X_E$): Use a toxic language classifier on sentences mentioning
$E$. Or use a lexicon of insults – if any insult or derogatory term is used
with $E$, that's toxic. We can define:
X = 1 − ∏ (1 − x ),
E i:E∈S
i
i
where $x_i$ is the toxicity probability or score of sentence $S_i$ containing
$E$. Essentially 1 minus the product of probabilities of each mention being
non-toxic, giving overall probability that at least one toxic reference exists.
Or simpler: the maximum toxicity among mentions as the representative (if
one sentence calls them a "traitor", that's enough to flag high toxicity).
Threat association ($T_E$): For each mention, check nearby words for
threat indicators (e.g., "dangerous, terrorist, criminal, threat, fear,
security"). We can count or weight these occurrences. For example:
T_E = \frac{\text{# of threat words within N words of any mention of E}}
{\text{total words near E across mentions}}
which yields a percentage of context that is threat-related. Or a simpler
approach: if any strong threat word is used with E, $T_E$ is high (like 1 if "E
is a threat"), otherwise moderate if some hints. We might just do a
normalized count and cap at 1.
Quote count ($Q_E$): We parse the document for quotations and
attributions. For example, if we have quotations identified (via regex for
quotes or by speaker verbs like said [Person]), we count how many times
$E$ appears as the speaker. Some logic: find patterns like "..." , $E$ said
or $E$ : "..." . If using spaCy, we could attempt to use the dependency
parse to find $E$ as a subject of a speech verb.

Framing score ($F_E$): We measure verbs and roles associated with $E$.
For each occurrence, note whether $E$ is subject or object of verbs, and
what those verbs are. Some verbs connote power (e.g., "led", "organized",
"announced") vs weakness ("admitted", "was defeated"). We could maintain
two lists or a scoring function for verbs. For each mention, if $E$ is subject
of a verb $v$, add score $verb_strength(v)$ (some verbs +1 strong
positive, some -1 negative). If $E$ is object, consider that too (if $E$ is
object of "arrested", that portrays them negatively, as they are the target
of a bad action). Summing these and normalizing could give $F_E$. For
instance:
F
E
= tanh
(N
1
E
∑
i
N
=
E
1
frame_score(E,context
i
)
)
,
where frame_score might add +1 if $E$ did a positive action, -1 if $E$ had
a negative action done to them or did a negative action, etc. $\tanh$ to
keep it in [-1,1] range without extreme jumps.
Moral valence ($M_E$): This relates to whether the entity is cast as good
or evil. We can base this on words around $E$ that have moral
connotations (like "innocent", "brave" vs "corrupt", "evil"). Also, if $E$ is in a
conflict, are they described as the aggressor or victim? We might
incorporate sentiment plus a focus on moral/emotive words. Possibly:
M = f(positive moral words near E − negative moral words near E),
E
normalized to [-1,1]. We can use a moral sentiment lexicon or even the
Moral Foundations outputs (if "Authority/Subversion" or "Care/Harm"
mentions revolve around E, that can feed into valence).
Conflict involvement: Determine if $E$ is part of a binary conflict in text.
If the article discusses a conflict (war, debate, lawsuit) and $E$ is a
participant, mark them. Perhaps simpler: If $E$ appears in sentences with
versus/against or competing claims, or is pitted against another entity in
sentiment (one positive, one negative), then yes. We might output this as a
boolean or 0/1 score. Possibly derive from stance detection: if the
document has multiple stances or sides, entities on those sides are in
conflict.
All these metrics are computed per entity and can be stored as a dictionary or
table.
Implementation Strategy
Approach: This is partly extraction and aggregation. Use NER results
from spaCy to get all entities, then apply:

Sentiment: reuse sentiment analysis but target it to each entity's
context (aspect-based sentiment). Possibly use a dedicated tool like
huggingface pipeline for sentiment for each sentence containing
$E$. Or since we already have sentence sentiment and maybe entity
co-mention, use weighted average.
Toxicity: use a pretrained toxicity classifier on each sentence or a
lexicon of slurs.
Quote count: use rule-based parsing of quotes.
Threat words: lexicon approach (list of threat-related words).
Framing verbs: utilize dependency parse (subject, object relationships).
Possibly Coreference resolution (if pronouns refer to $E$, include
those mentions too). If using spaCy coref (if available via a component
or an external library like NeuralCoref or transformers like bert-base-
coref ), we could gather all mentions including pronouns "he/she" for a
person.
Primary Library: spaCy for NER and dependency roles; Huggingface
Transformers for sentiment and toxicity classification (e.g., distilbert-base-
uncased-finetuned-sst-2-english for sentiment on sentence, or a multi-
lingual one if needed; and unitary/unbiased-toxic-roberta for toxicity).
Could also use Perspective API if allowed, but let's assume local model.
Possibly NetworkX or similar if we wanted to build a graph of co-
occurrence (for co_mentioned_entities network in metadata).
Pretrained Model:
Sentiment: nlptown/bert-base-multilingual-uncased-sentiment (gives 1-5
stars which can map to -1 to1).
Toxicity: unitary/toxic-bert or facebook/bart-large-mnli tuned on toxic
detection.
Alternatively, use a simpler approach for sentiment like VADER as done,
though it’s not aspect-specific.
Framing verbs: no direct model, we encode via rules.
There are models for targeted sentiment (e.g., you can fine-tune QA
models to get sentiment toward a given target, or use zero-shot: "The
text expresses [positive/negative] sentiment about X").
Computational Complexity: For each entity, iterating through mentions
(which is essentially all sentences containing that entity). If many entities,
this could be heavy in a doc, but typically an article has a limited set of
main entities. Also often dominated by a few main players. If an article has
50 entities but many minor, focusing on top N may suffice for output.

If we do a sentiment model inference per mention, that's like per
sentence with that entity. If doc ~30 sentences and maybe 5 mentions
of main entity, 5 inferences. Summed for all, maybe a few dozen
inferences per doc, which is fine if model is small or we can batch by
collecting all mentions across docs (less straightforward due to context
differences).
Scalability: At 1M docs, doing a transformer inference for each mention
might add up. We can optimize by:
Using the sentence sentiment already computed in sentiment analysis
module (if not aspect-specific, maybe good enough approximation).
Use lexicons for threat and moral words (fast).
Use a simpler method for toxicity (like just check if any known slur or
extreme word is near the entity).
Or mark toxicity at token-level (we had a token-level toxicity field, could
propagate to entity if any token in entity’s context had high toxicity).
Parallelize across docs obviously.
Also, skip minor entities: we could decide to produce full info only for
significant entities (like those that appear multiple times or are central).
For others, we might not need all metrics (or we output but it might not
matter).
Building a big co-mention graph for network features (like connecting
entities across corpus) could be heavy, but that's in metadata.
Code Template
Python Run
entity_analysis = []
# Assume doc_data["sentences"] exists and spaCy doc with ents (from foundation step)
doc = nlp(doc_text) # or we reuse the spaCy doc from earlier
# Precompute sentence sentiment and toxicity to reuse
sentiments = []
toxicity_scores = []
for sent in doc.sents:
vs = sia.polarity_scores(sent.text) # using VADER for speed
sentiments.append(vs["compound"])
# Toxicity: simple check via lexicon
toxic = 0.0
for bad_word in ["idiot","stupid","hate","kill"]: # simplified toxic lexicon
if re.search(fr"\b{bad_word}\b", sent.text, flags=re.IGNORECASE):
toxic = 1.0
break
toxicity_scores.append(toxic)

# For quote attribution, simple approach: regex for quotes
quote_speakers = []
for match in re.finditer(r'“([^”]+)”\s*[,\\-]\s*(said|says|stated|according to)\s*([A-Z][
speaker = match.group(3)
quote_speakers.append(speaker.strip())
for ent in doc.ents:
if ent.label_ in ["PERSON","ORG","GPE","NORP"]: # focus on meaningful entities (NORP
E = ent.text
indices = [i for i, sent in enumerate(doc.sents) if E in sent.text]
if not indices:
continue
# Sentiment for E: average compound of sentences containing E
avg_sent = sum(sentiments[i] for i in indices) / len(indices)
avg_sent = max(-1, min(1, avg_sent))
# Toxicity for E: max toxicity of sentences containing E
max_tox = max(toxicity_scores[i] for i in indices)
# Threat association: check threat words near E in those sentences
threat_words = ["threat","danger","terror","security","fear","crime","criminal"]
threat_count = 0; total_count = 0
for i in indices:
words = [w.lower_ for w in list(doc.sents)[i]]
total_count += len(words)
if any(tw in words for tw in threat_words):
threat_count += 1
threat_score = threat_count / max(1, len(indices)) # fraction of mentions with a
threat_score = max(0.0, min(1.0, threat_score))
# Quote count
q_count = sum(1 for speaker in quote_speakers if speaker.startswith(E))
# Framing: Check verbs around E
frame_score_sum = 0; frame_instances = 0
for token in doc:
if token.text == ent.text:
# If E is subject of a verb
for child in token.children:
if child.dep_ == "agent" or child.dep_ == "nsubj":
verb = child.head.lemma_
if verb in ["lead","organize","announce","defend"]:
frame_score_sum += 1
elif verb in ["admit","deny","blame","accuse"]:
frame_score_sum -= 0.5
frame_instances += 1
# If E is object of a verb
if token.dep_ == "dobj" or token.dep_ == "pobj":
verb = token.head.lemma_
if verb in ["kill","attack","arrest","defeat"]:
frame_score_sum -= 1
frame_instances += 1
frame_score = frame_score_sum/max(1, frame_instances)
frame_score = max(-1, min(1, frame_score))
# Moral valence: look for moral descriptors around name
moral_good = ["hero","honest","innocent","brave"]

moral_bad = ["villain","corrupt","evil","criminal"]
moral = 0
for i in indices:
text = doc_data["sentences"][i]["text"].lower()
for w in moral_good:
if w in text:
moral += 1
for w in moral_bad:
if w in text:
moral -= 1
moral_val = 0
if moral != 0:
moral_val = max(-1, min(1, moral/len(indices)))
# Conflict involvement: simple flag if "against" or "vs" appears around name
conflict_flag = 0
for i in indices:
sent_text = doc_data["sentences"][i]["text"].lower()
if re.search(fr"{E.lower()} (vs|versus|against)", sent_text) or re.search(fr"
conflict_flag = 1
break
entity_analysis.append({
"entity": E,
"entity_type": ent.label_,
"sentiment": round(avg_sent,3),
"toxicity": round(max_tox,3),
"quote_count": q_count,
"threat_association_score": round(threat_score,3),
"framing_score": round(frame_score,3),
"moral_valence": round(moral_val,3),
"conflict_involvement": bool(conflict_flag)
})
# Sort entities by frequency (optional)
(The code above is simplified. For example, identifying verbs related to the
entity in spaCy requires checking dependency properly. A better approach:
iterate through tokens and use token.ent_type_ or use coref, but this gives an
idea.)
Scoring & Calibration
We interpret these entity-level scores as follows:
Sentiment: should correlate with the Linguistic Bias’s per-entity findings.
We calibrate so that if an entity is described in clearly favorable terms (e.g.,
"accomplished, respected leader"), sentiment ~ +0.8. If very negative
("corrupt, notorious criminal"), sentiment ~ -0.8. Neutral reporting yields
near 0. We may use a sentiment model for more precise scoring per
mention if VADER is not enough, calibrating on a small set of manually
annotated entity mentions.

Toxicity: Typically 0 for most mainstream text. If any insults are present, it
might jump to 1. Calibration wise, we could consider partial credit: if minor
name-calling (like calling someone "incompetent" might be toxic-ish but not
a slur), the model or lexicon should reflect moderate toxicity (maybe 0.5).
Using a ML toxicity model will naturally output a probability which we can
threshold (e.g., >0.5 means likely toxic).
Threat score: If the text consistently associates the entity with fear (like
"people fear X", "X is a danger"), then this should be high, maybe >0.7. If
just one mention of "X could pose a threat", maybe moderate ~0.3. We
adjust the measure accordingly. Possibly weight direct statements "X is a
threat" more strongly than "X said there is a threat".
Framing score: Ideally align with sentiment but focusing on power
dynamics. E.g., If all verbs are powerful ("X led, X commanded"), frame ~
+1. If "X was arrested, X was accused", frame ~ -1. A mix would center
near 0. We calibrate by verifying the verb lists. Possibly refine using lists
from journalism (like we did for reporting verbs). If needed, adjust the
increment values in code.
Moral valence: Rarely, an entity might be explicitly called a "hero" or
"villain". If so, we want +1 or -1. More often, subtle moral framing occurs. If
our moral word list is limited, we calibrate with caution. If none of the words
appear, moral_val stays 0 (neutral). If multiple positive moral terms, maybe
saturate at +1. We can also incorporate moral foundation analysis for a
deeper measure (in advanced frameworks).
Conflict involvement: If flagged true, it's basically a category, not a
continuous score. If needed, we can output it as 1/0 or as part of stance
distribution (like which side they are on if known). Calibration not needed
beyond correct detection.
We ensure these values make sense collectively. For example, if an entity has
toxicity=1 (called names), likely sentiment will be very negative too. If we see
mismatch (toxicity high but sentiment positive?), there's an issue.
We might adjust by verifying on known examples:
A news article about a criminal: sentiment likely negative, threat high (talks
about crimes), moral valence negative, conflict maybe no (not a two-sided
conflict unless cops vs criminal).
A profile praising someone: sentiment positive, moral valence positive
(maybe calls them hero), framing positive, etc.

An opinion piece attacking a politician: sentiment negative, possibly some
toxic epithets, threat might be portrayed (like "X endangers the country"),
conflict yes if opposing someone.
We test a few and see if output matches intuition.
Validation
Validation can be done by:
Manual inspection: Take an article, list the top entities and their scores.
Does it align with how a human reader would characterize it? If it says
Entity A: sentiment -0.6, we check if the language was indeed mostly
negative about A.
Comparison with external: If we have labeled data like stance or bias for
a particular entity (maybe from a dataset: e.g., in a dataset of political
ideology, how media describe a politician might be annotated), we can
compare. Not straightforward to find, but maybe one can see if known
partisan news portray certain figures more negatively and if our system
catches that difference.
Check consistency: If an entity appears in multiple articles in our system,
and one source is known left (should portray a right-wing figure negatively)
vs a right source (positively), do we see corresponding sentiment
differences? That would validate our entity sentiment measure as capturing
media bias toward that entity.
Edge cases: Entities with common names might get merged incorrectly
(two different people with same name), our analysis might conflate them.
Coreference can help but is error-prone. For validation, we'd watch out for
weird results like one person being assigned contradictory scores due to
mixing contexts. This is hard to systematically validate, but a known risk to
mention.
We also verify the quote_count: pick an article, count quotes manually for
an entity vs system output.
Threat words: ensure context is properly considered (maybe a false
positive: "X said 'we will not tolerate threats'" should not mark X as a threat,
it's them talking about threats).
Tweak lexicons or context windows if needed to improve precision.
Integration Notes

Integration with bias: The entity sentiment is essentially what we used in
the linguistic bias section for framing bias. We will unify these to avoid
duplication. The bias module might output that "Entity X is framed
negatively" – that directly comes from sentiment here.
We should ensure that if multiple names refer to same entity (like
"President Biden" and "Biden"), we unify them. Possibly do coreference or
simple string matching normalization. This matters for completeness.
Downstream use: The system can aggregate sentiments of all persons to
see overall tone distribution. E.g., a visualization could show which entities
got the worst vs best portrayal in the article.
Network features: The co_mentioned_entities graph (from metadata
section) is built by linking these entities across articles or within. Within an
article, co-mentions could form an edge (if A and B appear in same
sentence or article, they’re connected). We can easily derive that from this
list by connecting all entities in this doc (maybe weighted by how many
sentences they co-occur).
Storage: We will likely store a separate collection of entity results per doc,
as shown with the JSON list. Or in a relational DB, an entity table linking to
doc by doc_id, with those fields. That allows queries like "give me all docs
where entity='Climate Change' and sentiment is highly negative".
Use in stance detection: If stance detection tries to find if the document
supports or opposes a certain entity or topic, the entity sentiment
essentially is the stance towards that entity. So if a question is "Is the article
in favor of X or against X?", one clue is sentiment(X) .
Real-time performance: The entity analysis as coded (with VADER and
lexicons) is fast. If we replaced with transformers for sentiment/toxicity,
that's slower but not too bad for a few entities. So it can be done real-time
if needed, especially if we use cached results from earlier (like reusing
sentence sentiment).
Dependencies: On NER and on earlier sentiment analysis. If the sentiment
module has per-sentence results, we reused those. Similarly, toxicity could
reuse a token-level or sentence-level evaluation from earlier (like if we ran
a toxicity model on entire doc).
There's interplay with Moral Foundations (advanced frameworks) –
moral_valence might be informed by that if, say, the text triggers
Care/Harm foundation about the entity (like calling someone cruel triggers
harm foundation negative).

Quote count connects to source bias: if the article rarely quotes certain
groups, that's coverage bias. We might in final scoring include something
like "voice balance". If an entity is central but has zero quotes vs another
has many, that imbalance is a sign of bias.
The conflict_involvement flag might feed into stance or into advanced
conflict framing (like "conflict frame: yes/no").
Stance Detection
Mathematical Foundation
Stance detection determines the position of the document (or speakers within
it) towards a target (claim, topic, or entity). In our context, major claims or
topics can be identified (like the main issue or person the article is about), and
stance is classified as support, oppose, or neutral. We also measure:
Stance strength: a float [0,1] indicating how strongly the article supports
or opposes (e.g., 1 for extremely partisan support, 0.1 for very mild or
mixed).
Explicitness: whether the stance is explicitly stated or implicitly conveyed.
Could be a binary or a score (1 = very explicit, 0 = very implicit).
Internal consistency: whether the document’s stance is consistent
throughout or if it contains contradictory stances.
Conflict check: identify if conflicting stances on the same topic appear
(which ties to internal consistency but also could mean the article presents
multiple viewpoints intentionally).
To formalize:
Let’s denote by $T$ the set of key topics or claims in the document. Often
$T$ might include the central issue and possibly sub-issues. For each $t \in
T$, we assign a stance value $st(t) \in {-1, 0, +1}$ for oppose, neutral,
support, respectively. We might also consider a confidence or strength for
that classification.
Stance strength could be represented as $|s|$ if we map oppose=-1,
support=+1 (so magnitude is strength, sign is direction). Or treat it
separately as a non-negative value with direction separate.
We can also define a stance vector for the document if multiple targets are
relevant.

If our target is each major entity:
We actually did something similar with entity sentiment. For example, an article
might "support" a politician (praising them) or "oppose" them (criticizing). The
sentiment towards that entity can be interpreted as stance (assuming stance
means favorability). However, stance is often used for opinions on issues or
claims (like "does the text agree or disagree with a policy proposal?").
One approach:
Identify the main claim or thesis of the article, if any. (In news, maybe not
applicable unless it's an editorial or argumentative piece.)
For each known controversial topic (like climate change, etc.) or each major
entity, attempt stance classification:
For an entity, stance (support/oppose) correlates with our sentiment
polarity: e.g., if sentiment to entity is positive, stance = support that
entity; if negative, stance = oppose that entity. Neutral sentiment =
neutral stance.
For issues, might need a model or keyword approach: e.g., if topic is
"gun control", does the text argue for it or against it? That requires
understanding content beyond sentiment because both sides could be
presented neutrally too.
We can incorporate:
Use a stance lexicon: words like "should", "must" often come with
proposals (e.g., "We should [do X]" indicates support for X). Phrases like "X
is a bad idea" indicates opposition.
Use NLI or textual entailment: represent the stance task as checking if the
text entails or contradicts a known proposition. For example, if we want
stance on "Policy P", we can feed the model: premise = article text,
hypothesis = "Policy P should be implemented." If it predicts entailment,
likely support; contradiction => oppose; neutral => neutral. This is a clever
repurposing of NLI for stance (common in zero-shot stance tasks).
Explicitness: If stance words are directly used ("I support X", "We oppose
Y"), that's explicit. If the article just frames things in certain ways but never
says "I support", that's implicit. We can mark explicitness = 1 if specific
stance verbs or statements appear.

Internal consistency: We can check if the document expresses both
support and opposition for the same thing. E.g., one paragraph supports,
another opposes (maybe quoting different people, as in news covering both
sides). If the document is meant to be neutral news, it might present both
sides without taking one, which is neutral stance overall but contains
conflicting viewpoints as quotes. That scenario means the document itself is
neutral (the author not taking a stance) but it contains conflicting stances
from sources.
We might measure consistency by checking variation in
sentiment/stance signals across the text. If they’re all same sign,
consistent; if mixed, either the article is neutral or just contradictory.
We might use position or attribution to tell: if contradictions come from
quotes, it might be just presenting debate (which might still be neutral
stance of the article).
For our output, "internal_consistency" could be a boolean or fraction of
text that is consistent. Possibly, we define it as 1 if the article doesn't
contradict itself in its own voice. If it does, 0.
Conflict check: similar to above, but could also mean if the article itself
seems to argue with itself. Likely the same measure.
We output likely:
{
"topic": str or entity,
"stance": "support"/"oppose"/"neutral",
"stance_strength": float,
"explicit": bool,
"consistency": float or bool,
"conflict": bool
}
However, the spec says:
"For each major claim, topic, or entity, determine:
stance classification,
stance strength,
explicitness,
internal consistency,
conflict check"
So possibly multiple outputs (for each major entity or claim).
Alternatively, at document-level we could summarize:

e.g., "Stance towards [TopicX]: Oppose (strength 0.8, explicit)" etc.
Implementation Strategy
Approach: Use a combination of sentiment-based heuristic for stance
towards entities and NLI/zero-shot classification for stance on
statements or topics.
For known topics or if the user is likely to query stance on specific issues,
we might incorporate a pre-specified list of issues or derive topics via topic
modeling and then see stance. But likely focusing on entities and obvious
claims in text is enough.
Identify if text is argumentative vs neutral: if it's neutral reporting, stance
might be "neutral" on everything. If it's an editorial, stance will be strong on
something.
Tools:
Use the entity sentiment from earlier for entity stance.
For issues, if we have a knowledge base of major controversies, we
could see if any are mentioned and how. But that's broad.
Possibly use BERT NLI (like we used roberta-large-mnli ) by crafting
hypotheses. This needs a known target though.
If the article has a title like "Why X should be Y", stance is implicit in
title.
Could use keywords: e.g., for each sentence, see if it contains
"should/need to" and an action, that might reveal stance on that action
(if preceded by not, then oppose).
Implementation:
Parse for modal verbs and opinion expressions ("I believe", "we
should").
Check if it's written in first person (if yes, likely an opinion article with
explicit stance).
To systematically do it, one might do:
Summarize the article's main claim or conclusion sentence (maybe
last sentence in an op-ed or a title).
Or apply an LDA to get main topic (like "climate policy") and then
see sentiment around that topic.
Without external training, a simpler route:

Leverage earlier results: if there is a major entity or idea that has
very high absolute sentiment, likely the stance is support or oppose
that entity/idea.
We can define "major entity" as one with the most mentions or part
of title.
Then stance classification for that: if sentiment >0.3 -> support, <
-0.3 -> oppose, otherwise neutral.
Stance strength = |sentiment|.
Explicitness: if we found phrases like "support" or "oppose" explicitly
or first-person voice, mark True.
If multiple entities or claims with both positive and negative
directions, internal_consistency = False (meaning multiple stances
are present).
If quotes present both sides, that might set conflict_check = True.
Actually, conflict_check likely refers to whether the content includes
opposing perspectives. For a balanced news piece, conflict_check
might be True (because it shows conflict viewpoints), but
internal_consistency (from author) is still True because the author
isn't contradicting themselves, just reporting conflict.
We may treat:
internal_consistency: Are the author's stance signals consistent? If the
article is opinion, they should be consistent. If we see the author voice
(maybe in intro or conclusion) taking one side clearly, and no reversal, then
consistent.
If it's news that is neutral (no stance), consistency is moot because no
stance taken (we could call that consistent in being neutral).
If an article wavers (some paragraphs endorsing, some rejecting without it
being quotes), then inconsistent (maybe not likely unless poorly written or
multi-author).
Computational complexity: minimal, it's mostly analyzing outputs we already
have (sentiments, etc.). NLI use on entire article might be heavy, but we can
skip heavy ML if heuristics suffice. If we do use NLI, it could be one or two
inferences (like article vs a hypothesis of support/opposition).
Code Template
Python Run
stance_outputs = []
# Determine primary topic or entity of the article (e.g., most mentioned entity or from m

main_entities = sorted(entity_analysis, key=lambda e: len([m for m in doc.ents if m.text=
if main_entities:
main_ent = main_entities[0]
else:
main_ent = None
if main_ent:
# Use sentiment as stance
ent_name = main_ent["entity"]
pol = main_ent["sentiment"]
if pol > 0.2:
stance_label = "support"
elif pol < -0.2:
stance_label = "oppose"
else:
stance_label = "neutral"
stance_strength = abs(pol)
# Check explicitness: look for "support [entity]" or "oppose [entity]" explicitly
explicit = False
if re.search(fr"support(s|ed)? {ent_name}", doc_text, flags=re.IGNORECASE) or re.sear
explicit = True
# internal consistency: If more than one main stance in the text about this entity
# (We can check if some sentences have positive and some negative sentiment toward sa
ent_sentiments = []
for sent in doc.sents:
if ent_name in sent.text:
vs = sia.polarity_scores(sent.text)
ent_sentiments.append(vs["compound"])
if ent_sentiments:
if max(ent_sentiments) > 0.2 and min(ent_sentiments) < -0.2:
consistency = 0.0 # both positive and negative contexts found
else:
consistency = 1.0
else:
consistency = 1.0
# conflict check: if other entities or quotes present opposing views
conflict = False
if main_ent and len(main_entities) > 1:
# if another entity has opposite stance sentiment
second_ent = main_entities[1]
if second_ent["sentiment"] * main_ent["sentiment"] < -0.2: # opposite signs sign
conflict = True
# Also, if explicit "However, ..." style signals
if re.search(r'\bhowever\b', doc_text):
conflict = True
stance_outputs.append({
"target": ent_name,
"stance": stance_label,
"stance_strength": round(stance_strength,3),
"explicitness": explicit,
"internal_consistency": consistency,
"conflict": conflict

})
# If there is a clearly identified topic (maybe from metadata or title)
topic = None
# Suppose we extract a topic from title keywords
title_words = [w.lower() for w in doc_data["document"].get("title","").split()]
for known_topic in ["climate","abortion","economy","election"]:
if known_topic in title_words:
topic = known_topic
break
if topic:
# Determine stance on that topic via keywords
text = doc_text.lower()
support_cues = ["should "+topic, "necessary", "the case for "+topic]
oppose_cues = ["should not "+topic, "wrong", "the case against "+topic]
stance_label = "neutral"; explicit = False
for cue in support_cues:
if cue in text:
stance_label = "support"; explicit = True
for cue in oppose_cues:
if cue in text:
stance_label = "oppose"; explicit = True
stance_strength = 0.5 if stance_label!="neutral" else 0.0
# (This is simplified; ideally use NLI or sentiment around the topic mentions)
stance_outputs.append({
"target": topic,
"stance": stance_label,
"stance_strength": stance_strength,
"explicitness": explicit,
"internal_consistency": 1.0, # assume consistent if identified single stance
"conflict": False # assume no conflict for a single-stance detection
})
(This code is very heuristic and simplistic. A real stance detection might
integrate more robust text understanding, but this gives an idea.)
Scoring & Calibration
We calibrate stance detection by verifying on known editorial content:
If the article is labeled (explicitly or by ground truth) as pro or anti
something, our stance outputs should reflect that. If not, adjust approach.
If using an NLI approach: we would calibrate by testing it on known pairs.
For example, "The government should do X." vs article text. If model
outputs entailment or contradiction as expected.
Stance_strength is essentially the confidence or intensity. A neutral piece
would have stance_strength near 0. If our calculation gave it 0.5
erroneously, we adjust threshold or method.

We ensure explicitness is correctly flagged by presence of clear phrases.
Could expand the list of explicit stance markers and calibrate on a sample
of op-eds (they often say "we support the measure because...").
internal_consistency: If article is just presenting debate (like a news piece
quoting two sides), our method might mark conflict True (because it has
both views), but is the "internal_consistency" of the article considered
broken? This depends on interpretation:
If the article itself isn't advocating, then stance = neutral, explicitness
false, consistency might be high (since it's consistently neutral, not
actually self-contradictory).
So maybe revise: internal_consistency should mainly apply if the article
attempted a stance. If stance is neutral, consistency could be not
applicable or just True as in "no single stance to be inconsistent about".
conflict check: likely similar to internal_consistency but we use it maybe to
flag multi-perspective content.
We can calibrate conflict check on multi-perspective articles or identify if our
pipeline tends to flag every balanced news story as conflict; if so, maybe refine
to consider quoting others as not a conflict in the author's stance.
Validation
Use known cases: e.g., an editorial endorsing a candidate vs one opposing –
check stance detection picks that up correctly.
A neutral news story – ensure it outputs stance "neutral" or maybe outputs
nothing significant.
If possible, small labeled dataset: stance detection was popular in rumor
analysis (FNC competition had agree/disagree/neutral stance for headlines
vs article, but here we only have one text).
We might craft a few test sentences: "X is great" vs "X is terrible" and see
that stance flips.
For implicit stance, test something like "While X has some benefits, it
ultimately causes more harm." This implicitly opposes X. See if our signals
catch that (like negative words harm vs benefits etc).
Without an ML model specifically for stance, our approach might miss
subtle cases.
Integration Notes
This module relies heavily on results from others:
Entity sentiment from entity-level analysis for stance toward persons.

Possibly the framing analysis for issues.
If we implemented advanced topics (like LDA topics or provided
trending keywords from metadata), we could treat each significant
topic similarly to an entity: derive a sentiment or tone for it.
The outputs can populate a stance_distribution in the document
features. For example, stance_distribution: {"support": X%, "oppose": Y%,
"neutral": Z%} if it covers multiple opinions. Or a list of stances by target as
produced.
Visualization: We could display stance as a label (like a colored tag "Pro-
[Topic]" or "Anti-[Topic]") if applicable. Or a bar showing stance strength on
a bipolar scale.
In usage, a researcher might ask "What stance does this article take on
climate change?" – our system should have an entry if climate change is
discussed. If not, it’s neutral by omission.
Real-time: This is light-weight enough to run quickly, especially if reusing
previous computations.
Dependencies: On NER for entities, sentiment results. Possibly on topic
classification if used. If metadata had an "section_category" like "Opinion",
we might treat those differently (like more likely to have an explicit stance).
There might be overlapping logic with moral framing or propaganda:
e.g., a strongly negative stance could coincide with name-calling
(propaganda) if it’s a smear piece. But stance is just about position, not
method; our integrated system will combine all (like it can be anti-X (stance)
and uses propaganda to do so).
Ensuring consistency: If entity sentiment said A is -0.8 (very negative
portrayal), we better label stance towards A as "oppose, strength ~0.8".
Those must align or else user might see contradictory info. Our method
basically does that, so fine.
Stance detection across documents: In a large analysis, one might
cluster articles by stance on an issue. Our stance outputs per doc will allow
that (like filter all that oppose vs support a certain policy).
Structural & Syntactic Analysis
Mathematical Foundation
This covers syntax complexity and discourse structure:

POS tag distribution: fraction of nouns, verbs, adjectives, etc. For doc
$D$, if $N_{\text{NOUN}}$ is number of nouns, etc., we record these
counts or ratios (could form a vector that sums to 1 over major POS
categories).
Passive voice percentage: as computed earlier, $ \text{passive_ratio} =
\frac{\text{# passive sentences}}{\text{total sentences}}$. Passive
detection can be done via dependency tags (nsubjpass) or by regex (be +
VBN forms).
Nominalization frequency: count of nominalizations (using nouns that
could be verbs, often ending in -tion, -ment, -ance, etc.). We can count such
nouns and divide by total nouns or total sentences. A high nominalization
frequency can indicate a formal or obfuscated style.
Sentence complexity: we can measure by parse tree depth or average
number of clauses. If using spaCy, each sentence's parse tree depth can be
approximated by the longest chain in the dependency tree. Or simply
average sentence length in words or syllables as a proxy. We can also count
subordinate conjunctions (which indicate complex sentences).
Readability scores:
Flesch-Kincaid Grade Level: $0.39 \frac{N_\text{words}}
{N_\text{sent}} + 11.8 \frac{N_\text{syllables}}{N_\text{words}} -
15.59$ (approx).
Flesch Reading Ease: $206.835 - 1.015 \frac{N_\text{words}}
{N_\text{sent}} - 84.6 \frac{N_\text{syllables}}{N_\text{words}}$.
SMOG Index: $1.0430 \sqrt{N_{\text{poly-syllable}} \cdot \frac{30}
{N_{\text{sent}}}} + 3.1291$ (for 30-sentence sample).
Gunning Fog: $0.4(\frac{N_\text{words}}{N_\text{sent}} +
100\frac{N_{\text{complex_words}}}{N_\text{words}})$ where
complex_words are words >2 syllables.
We can compute some of these if needed.
Discourse connectives frequency: count words like "however",
"moreover", "in contrast", "therefore", etc. This indicates explicit logical
structure. Could be measured per sentence or per 100 words.
Topic coherence score: If the text jumps topics or stays on one theme.
We can measure similarity between adjacent sentences or paragraphs
using embeddings. For each adjacent pair of sentences, compute cosine
similarity of their sentence embeddings. Then average that; a low average
might indicate many shifts (low coherence). Or train an LDA topic model on
the doc in segments and see how many topics appear – multiple distinct
topics in one doc might indicate shifts.

Narrative shift detection: specifically look for transitional phrases that
indicate a change ("On the other hand", "Turning to..."). Also can be flagged
by a drop in similarity between sections.
Coreference density: measure of how entangled the coreference graph
is. Possibly the average size of coreference clusters (bigger clusters = more
pronouns referencing same entity = cohesive narrative). Or number of
pronouns per sentence as a ratio might indicate complexity in tracking
references.
Another measure: how many unique entities vs total mentions – high ratio
of mentions to unique suggests repeated discussion of same entities
(cohesive focus), whereas many unique ones suggests scattered content.
Also how often long pronoun chains (like 'he... he...' linking across
sentences).
We might define coreference density as (total number of coreference links)
/ (total sentences). Hard to compute exactly without a coref algorithm, but
if we had one: if one pronoun is linked to a previous noun, that's a link.
Aggregation: Many of these can be aggregated to doc-level easily (averages,
percentages). We may store some in the document's feature vector (like
readability and complexity metrics, average POS distribution) for use in
composite scores.
Normalization: POS distribution we often just present as relative frequencies
(no further normalization needed). Readability scores have their own scales
(Flesch ease is 0-100, we might map to 0-1 by dividing by 100 for internal use if
needed). Or just keep their standard scale since they're known formulas.
Complexity metrics like depth can be normalized dividing by something (like
max observed depth ~ maybe 20?).
We also ensure these metrics don't overly fluctuate with length (except
readability tries to adjust for that).
Implementation Strategy
Approach: Purely rule-based and formulaic using linguistic outputs. This is
straightforward once we have the parse and tokenization.
Primary Libraries:
spaCy for POS, dependency (we have that already).
textstat (a Python library for readability) could compute Flesch etc. If
we don't want external, can code formulas directly.
For syllable count, we might use textstat.syllable_count() or a simple
heuristic (vowel group counting).

For discourse connectives, just a set of words to count in text.
For topic coherence, using something like sentence-transformers to get
embeddings and compute similarities would be ideal. But that's heavy
for a quick structural measure. Alternatively, an LDA from sklearn or
gensim could find how many topics in one doc (but per doc not stable).
Possibly skip heavy modeling and do simpler: measure if certain
content words repeat (coherent) vs each sentence introduces lots of
new content words (less coherence).
Pretrained Model: Not needed except maybe a transformer for
embeddings if doing coherence with semantic similarity. Could use
sentence-transformers/paraphrase-MiniLM-L6-v2 which is lightweight to
embed sentences.
Computational Complexity: Very low for counting and formula. For
embedding-based coherence, computing BERT embeddings for each
sentence (like 30 sentences) is fine.
Scalability: trivial for counts; if we add an embedding step, that on 1M
docs might be heavy but could be done in parallel or skipped in faster runs.
Possibly using a smaller model or only approximate with word overlap (like
measure lexical overlap between sentences as an easier coherence
measure).
Code Template
Python Run
import textstat
# Already have doc, doc_data from earlier
tokens = [t for t in doc]
num_tokens = len(tokens)
num_sents = len(list(doc.sents))
num_words = sum(1 for t in tokens if t.is_alpha)
num_syllables = sum(textstat.syllable_count(t.text) for t in tokens if t.is_alpha)
# POS distribution
pos_counts = Counter(t.pos_ for t in tokens)
pos_dist = {pos: pos_counts[pos]/num_tokens for pos in ["NOUN","VERB","ADJ","ADV","PROPN"
# Passive voice count (using dependency labels)
passive_sents = 0
for sent in doc.sents:
for token in sent:
if token.dep_ == "nsubjpass":
passive_sents += 1
break

passive_ratio = passive_sents / num_sents
# Nominalizations count (simple: nouns ending in -tion, -ment, -ness etc.)
nominalizations = 0
for t in tokens:
if t.pos_ == "NOUN" and re.search(r'(tion|ment|ness|ity|ance|ence|ship)\b', t.text.lo
nominalizations += 1
nominalization_freq = nominalizations / num_sents
# Sentence complexity via dependency depth
depths = []
for sent in doc.sents:
# depth: max distance from root
max_depth = 0
def recurse_depth(token, depth):
nonlocal max_depth
if depth > max_depth:
max_depth = depth
for child in token.children:
recurse_depth(child, depth+1)
# find root(s) of sentence
roots = [token for token in sent if token.head == token]
for root in roots:
recurse_depth(root, 0)
depths.append(max_depth)
avg_depth = sum(depths)/len(depths) if depths else 0
avg_sent_length = num_words/num_sents if num_sents>0 else num_words
# Readability scores
flesch_ease = textstat.flesch_reading_ease(doc_text)
fk_grade = textstat.flesch_kincaid_grade(doc_text)
smog = textstat.smog_index(doc_text) if num_sents >= 3 else None # SMOG needs >= 3 sente
gunning_fog = textstat.gunning_fog(doc_text)
# Discourse connectives frequency
connectives = ["however","although","moreover","therefore","meanwhile","in contrast","on
connective_count = sum(full_text.lower().count(conn) for conn in connectives)
connective_density = connective_count / num_sents
# Topic coherence via adjacent sentence similarity
import numpy as np
# If we had sentence embeddings prepared, else use simple Jaccard of content words as pro
sim_scores = []
sent_texts = [sent.text for sent in doc.sents]
# Using a very naive approach: Jaccard similarity of content words for adjacent sentences
for i in range(len(sent_texts)-1):
words1 = set(w.lower() for w in re.findall(r'\w+', sent_texts[i]) if len(w)>3)
words2 = set(w.lower() for w in re.findall(r'\w+', sent_texts[i+1]) if len(w)>3)
if words1 or words2:
sim = len(words1 & words2)/len(words1 | words2)
else:
sim = 0

sim_scores.append(sim)
avg_adj_similarity = sum(sim_scores)/len(sim_scores) if sim_scores else 1.0
# Narrative shift detection
narrative_shifts = 0
for conn in ["on the other hand","however","but","meanwhile"]:
narrative_shifts += full_text.lower().count(conn)
shift_score = narrative_shifts / max(1, num_sents/5) # shifts per 5 sentences
# Coreference density:
# Without a coref tool, approximate by pronoun frequency relative to entities
pronouns = sum(1 for t in tokens if t.pos_ == "PRON")
entities = len(doc.ents)
coref_density = pronouns / max(1, entities)
# (If we had coref clusters, we could do average cluster length etc.)
doc_data["document"].update({
"pos_distribution": pos_dist,
"passive_voice_ratio": round(passive_ratio,3),
"nominalization_freq": round(nominalization_freq,3),
"avg_sentence_length": round(avg_sent_length,1),
"avg_dependency_depth": round(avg_depth,1),
"flesch_reading_ease": round(flesch_ease,1),
"flesch_kincaid_grade": round(fk_grade,1),
"gunning_fog_index": round(gunning_fog,1),
"connective_density": round(connective_density,3),
"adjacent_sentence_similarity": round(avg_adj_similarity,3),
"narrative_shift_score": round(min(1.0, shift_score),3),
"coreference_density": round(coref_density,3)
})
Scoring & Calibration
Most of these are raw metrics rather than "scores" to calibrate in [0,1], except
when used in composite indices:
We might want to incorporate some into a single "complexity score". For
example, a difficult piece might have high passive_ratio, high
nominalization, high depth, etc. We could define
\text{complexity_score} = \sigma(\alpha \cdot \text{FK\_grade} + \beta
\cdot \text{avg\_depth} + \gamma \cdot \text{nominalization\_freq})
mapping to [0,1] via a sigmoid or normalization relative to typical values.
That could be done if needed for final quality (like an extremely complex
piece might confuse readers, possibly relevant).
But mostly, these metrics are for analysis rather than scoring bias directly.
They might correlate with manipulative intent if someone uses very
convoluted language to obfuscate (which could lower transparency).

Calibration: ensure the formulas (like readability) produce plausible results.
E.g., a normal news article often gets Flesch ease ~50-60 (fairly hard) or
grade ~10-12. If our result says 5th grade for a scholarly article,
something's off. We trust textstat but can sample check.
Adjacent similarity threshold: if our threshold is always high or always low,
adjust. Possibly expecting a value like >0.2 for cohesive text, near 0 for
disjoint text. We'll see distribution and calibrate.
Narrative shift: if the piece is argumentative, one "however" is normal. If
count a lot, means many contrasts. Not necessarily bad, just a
characteristic. But in propaganda analysis, lots of "but/however" could show
constant refutation style.
We calibrate coref_density: typical pronoun to entity ratio maybe ~1 or 2
pronouns per entity. If it's extremely high (like more pronouns than entities
by far), the text might rely on pronouns (maybe long narrative focusing on
few entities repeatedly).
No strict [0,1] needed except maybe narrative_shift_score we capped at 1.
Validation
Use known text samples: a legal document or academic paper should have
higher grade level, longer sentences. We test an academic abstract and
expect our metrics reflect that (very low ease, high grade, high
nominalization).
A simple news piece or blog - should have shorter sentences, ease maybe
70 (more readable).
The distribution of these metrics across a sample of news vs opinion vs
academic content will be validated to ensure differences align with
expectations.
Coref and coherence: if we feed a deliberately jumbled text (like random
sentence order), we expect adjacent_similarity low. Feed a well-structured
narrative, expect higher.
Passive voice detection: test on known passive vs active examples to
ensure our method catches them.
Nominalization: check that words like "implementation" are counted, and
normal nouns like "apple" aren't.
Possibly compare with external tools (like MS Word's readability) for a sanity
check.
Integration Notes

These structural features primarily support analysis of writing style and can
indirectly hint at bias or deception (e.g., obfuscation via jargon, too high
complexity might hide weak arguments, or extremely simple might be
aimed at broad consumption).
In composite scoring, we might include an obfuscation score that is high
if readability is very low (complex language) and transparency is also low. If
so, suspect the piece might be intentionally convoluted.
Or include an engagement score: maybe shorter sentences, simpler
words means more accessible (depending on what the research aims for).
We have to store these maybe not all as separate fields for each doc
(though we can). Perhaps store a JSON field of these metrics.
Visualizations: could show a radar/spider chart of writing style features or
compare outlets by average reading level.
Real-time: trivial to compute quickly for one doc.
Dependencies: on parse, which we have. If needed, we could skip heavy
stuff like embedding for coherence, or precompute them offline if doing a
big batch analysis on corpus.
There's little overlap with other modules except they complement
factuality: e.g., if a piece is very complex and filled with jargon, maybe we
downweight its transparency. But be careful, complexity isn't inherently
malicious (some topics are just complex).
Possibly use in detection: extreme values might signal something unusual
(like propaganda might either be very simplistic slogans or overly
convoluted conspiracy theories).
These also could feed into the advanced "Framing theory dimensions"
indirectly (like human interest framing might have simpler narratives
focusing on individuals, vs conflict framing might have many adversarial
connectives).
Advanced Theoretical Frameworks (Framing & Moral
Dimensions)
Mathematical Foundation
These frameworks provide higher-level interpretation of content:
Framing Theory Dimensions (Economic, Moral, Conflict, Human Interest,
Responsibility). We quantify each on [0,1]:

Economic frame: content focusing on cost/benefit, financial aspects.
We can detect by keywords (e.g., "cost, price, budget, benefit,
economy") and context discussing money or economics.
Moral frame: content invoking moral/ethical judgments. Keywords like
"right, wrong, moral, immoral, ethical, corrupt", or references to
religious/ideological principles. Also overlaps with Moral Foundation
analysis.
Conflict frame: emphasis on conflict, winners/losers, us vs them.
Indicators: war metaphors ("battle, fight, clash"), two-sided language,
usage of vs/against, a high conflict_involvement from entity analysis,
quotes from opposing sides, etc.
Human interest frame: focusing on individuals and emotion to tell the
story (like a personal anecdote or emotional angle in a policy issue).
Indicators: presence of personal stories, a lot of emotional language
specifically tied to an individual's experience, perhaps frequent use of
proper names and less statistics (contrasting with an economic or
policy frame).
Responsibility frame: focus on blame or credit – who is responsible for a
problem or solution. Indicators: sentences that explicitly pin blame ("X
is responsible for Y", "due to X's actions"), or praise ("thanks to X").
Could measure by number of times an actor is mentioned as cause or
solution. Possibly using dependency (e.g., X subj->cause Y).
We score each by presence of corresponding cues:
\text{frame}_d = \min(1, \frac{\text{# of indicators of frame } d}
{N_{\text{sent}}} \cdot k_d )
for some scaling factor $k_d$ (we can tune to have typical content
~0.5 if moderately present).
Or more simply, 0 if not present, approaching 1 if heavily present.
Moral Foundations Theory (Haidt): five axes with values -1 to +1:
Care/Harm: Does text emphasize compassion, caring vs harm,
suffering? A positive value if advocating care or highlighting harm as
negative (compassionate tone), negative if inciting or justifying harm or
lacking care.
Fairness/Cheating: Mentions of fairness, justice, equality vs cheating,
corruption.
Loyalty/Betrayal: language about loyalty, patriotism, betrayal, treason.
Authority/Subversion: references to respecting authority, tradition, law
vs subverting, rebellion.

Sanctity/Degradation (Purity): talk of purity, sanctity, chastity vs disgust,
degradation, contamination (often in moral/religious contexts).
We likely use a lexicon approach:
There are known Moral Foundation Dictionaries with words for each
foundation. We count words from each category and their opposite.
For each axis, we compute something like:
#(care words)−#(harm words)
M =
care #(care/harm words total)
which yields -1 (all harm, no care) to +1 (all care, no harm). If no
related words, maybe 0 (no signal).
We do similarly for fairness, loyalty, etc.
Alternatively, some words might map to moral endorsement vs moral
violation (like "helping the poor" = high care; "cruelty" condemnation =
also showing value of care, but context matters).
But lexicon approximate: count appearances of virtue vs vice words of
each foundation.
Aggregation: Provide each dimension's score. Possibly output a dictionary:
moral_foundations: {"Care": x, "Fairness": y, ...}
framing: {"Economic": a, "Moral": b, ...} .
Normalization: The lexicon counts will be normalized by text length or by total
moral words to avoid length bias. Typically, we can just yield ratios or
differences as above.
Implementation Strategy
Approach: These are mostly lexicon-based classification tasks, perhaps
augmented with simple ML if needed. Given minimal training data likely,
lexicons from literature are the go-to.
Primary Libraries: Possibly none specialized in moral foundations except
retrieving a dictionary. We might manually encode small sets of words for
each (or find an open list).
For framing, similar: define word lists or simple rules.
For moral foundations, one could use a pre-trained classifier (some
research fine-tuned BERT to predict moral foundations from text, like on
tweets or arguments, but that may require data).
We'll stick to lexicons for transparency.
Pretrained: If available, maybe use a model like the HuggingFace model
from the Moral Foundation Twitter Corpus (if one exists publicly).
But safer: lexicon from Graham et al. (the original MFD).
Complexity & Scalability: Very fast (just scanning words).

Code Template
Python Run
# Framing detection via keywords
frames = {"Economic":0, "Moral":0, "Conflict":0, "HumanInterest":0, "Responsibility":0}
economic_words = ["cost","price","economic","investment","financial","tax","benefit"]
moral_frame_words = ["moral","immoral","ethic","sin","honor","virtue","integrity"]
conflict_words = ["vs","fight","battle","war","conflict","attacked","clashed","tension"]
human_interest_words = ["family","children","story","personal","heart","emotion","tragedy
responsibility_words = ["responsible","blame","fault","credit","accountable","cause"]
text_lower = doc_text.lower()
# Count occurrences
def count_words(wordlist):
return sum(text_lower.count(w) for w in wordlist)
frames["Economic"] = min(1.0, count_words(economic_words) / max(1, num_sents/2))
frames["Moral"] = min(1.0, count_words(moral_frame_words) / max(1, num_sents/2))
frames["Conflict"] = min(1.0, count_words(conflict_words) / max(1, num_sents/2))
frames["HumanInterest"] = min(1.0, count_words(human_interest_words) / max(1, num_sents/2
frames["Responsibility"] = min(1.0, count_words(responsibility_words) / max(1, num_sents/
# Moral Foundations via lexicon
moral_axes = {"Care/Harm":0, "Fairness/Cheating":0, "Loyalty/Betrayal":0, "Authority/Subv
care_words = {"care":1,"compassion":1,"kind":1,"help":1,"harm":-1,"hurt":-1,"suffer":-1,"
fairness_words = {"fair":1,"justice":1,"equal":1,"inequality":-1,"cheat":-1,"fraud":-1,"u
loyalty_words = {"loyal":1,"patriot":1,"ally":1,"betray":-1,"traitor":-1,"treason":-1}
authority_words = {"duty":1,"obedien":1,"respect":1,"honor":1,"authority":1,"law":1,"orde
purity_words = {"pure":1,"clean":1,"sacred":1,"holy":1,"virtuous":1,"degenerat":-1,"disgu
# Helper to compute axis score
def axis_score(word_dict):
total = 0; count=0
for word, val in word_dict.items():
if word in text_lower:
cnt = text_lower.count(word)
total += val * cnt
count += cnt
if count == 0:
return 0.0
# Score -1 to 1 as average valence
return max(-1.0, min(1.0, total/count))
moral_axes["Care/Harm"] = round(axis_score(care_words),3)
moral_axes["Fairness/Cheating"] = round(axis_score(fairness_words),3)
moral_axes["Loyalty/Betrayal"] = round(axis_score(loyalty_words),3)
moral_axes["Authority/Subversion"] = round(axis_score(authority_words),3)
moral_axes["Purity/Degradation"] = round(axis_score(purity_words),3)
doc_data["document"]["framing_scores"] = frames
doc_data["document"]["moral_foundation_scores"] = moral_axes

Scoring & Calibration
Framing:
The scores are in [0,1] representing proportion of sentences with that
frame. We calibrate by looking at typical news:
Many articles have some conflict frame if politics, some responsibility
assignment. If an article triggers none of the keywords, all zeros.
Possibly refine by any presence = significant. But better differentiate heavy
usage vs just a mention.
Could calibrate with manual classification: if known an article is heavily
human-interest (lots of personal story), see if our count picks it up (like
many personal words).
Might combine cues: e.g., human interest might also correlate with high
emotion from sentiment analysis. Could incorporate that (but we keep it
simple).
If we find frame values all low, might be a generic piece. If multiple high,
means mixed frames, which can happen but maybe one is usually
dominant.
Moral foundations:
Lexicon approach is coarse but should find some signals. If text is full of
fairness talk, fairness axis might come out positive.
We ensure to handle context: e.g., "unfair" will count as negative on
fairness axis (makes fairness axis negative meaning it highlights unfairness,
which ironically might be advocating fairness is violated so the writer values
fairness... it's tricky).
Actually, our approach might interpret mention of a vice (unfairness) as
negative, but the presence of that word likely means the author condemns
it, which actually is support for fairness. This is a nuance: a text complaining
"this policy is unfair" uses "unfair" (a negative word) but the stance of
author is that fairness is important and it's being violated. So lexicon naive
approach might misinterpret that as the text being morally negative on
fairness, whereas morally it's upholding fairness by calling out unfairness.
This limitation is known; however, capturing nuance requires more NLP or
context. Perhaps if negative term appears with negation, etc.
For our scope, we accept some noise but mention it.
We calibrate by checking if obviously moralizing texts (like religious
sermons focusing on purity or authority) reflect strongly in those scores.
If needed, weight words differently or add phrases to catch context (e.g.,
"no * respect for authority" is actually negative authority).
The output [-1,1] is straightforward.

Validation
Test on sample texts known to emphasize a foundation: e.g., an article
about caring for the poor should yield care/harm positive.
A law-and-order speech should yield authority positive.
The lexicon approach might not catch all synonyms; we could refine
lexicons by verifying results on a development set and adding obvious
missing terms.
Framing: if we have examples labeled for frames (like from communication
studies), test on them. E.g., an economic news piece should show high
economic frame, etc.
Check if any frame dimension is always high erroneously (like maybe
conflict words "attack" can be literal physical or in argument, which is
correct for conflict frame though).
The output should be interpreted as presence of frame, not necessarily that
the author endorses that perspective (just that it's used as a narrative lens).
Integration Notes
These advanced scores add depth to analysis:
The framing_scores can be part of final output or used to cluster
content by narrative style.
Could correlate framing with bias: e.g., partisan outlets might favor
conflict frame and blame (responsibility) frame more.
Or compare how different sources frame the same event (one might
use human interest, another economic).
The moral foundation scores highlight ideological bent:
E.g., some political rhetoric appeals more to loyalty or purity (often
seen in certain conservative messaging) vs fairness or care (often
liberal messaging). This aligns with Haidt's theory.
So this can identify subtle biases in value appeals.
We'll store these scores with the document (maybe a small vector of 5
each).
Visualization: a radar chart for moral foundation distribution could be
interesting, or comparing an article's moral profile to the audience's values.
Use in composite indices: Possibly not directly in "quality" score but good for
classification or clustering.
Real-time: trivial overhead, just scanning.
Dependencies: none new, just uses the text.

We ensure no overlapping logic double counts (if a word falls in multiple
categories, e.g., "honor" might count for loyalty and authority? Possibly, but
we've segregated for simplicity).
Possibly note that these should be taken as one of many signals, not
definitive (explainable to user as "the article uses a lot of conflict language"
etc.)
Metadata & Contextual Integration
Implementation & Design
(This section is more about integration rather than calculation; I'll describe
rather than give code, maybe just conceptual or some pseudo for database
linking.)
The metadata (publisher, date, author, etc.) and external reliability info will be
integrated at ingestion or analysis time:
When a document is ingested, we attach its metadata. The analysis pipeline
can use it for context (like if section is "Opinion", we expect certain patterns
like first-person, explicit stance).
We might have a database table of publishers with columns like
bias_rating, factuality_rating (from sources like MediaBiasFactCheck or
AllSides).
At runtime, we can lookup the publisher of the article and retrieve
bias_rating (Left/Center/Right) and a numerical bias score (maybe -1 left to
+1 right) and factuality (0-1).
Similarly, if author is known and we have historical reliability of authors
(maybe an aggregate of their past articles' scores), we could include that.
share_count and trending keywords: these likely come from outside (like
social media API or trending analysis across corpus). If available, integrate
as features (they might correlate with sensationalism).
co_mentioned_entities : we can build a graph. At doc level, co-mention
means any two entities in same doc or same sentence. On corpus level, we
can accumulate edges between entities weighted by co-occurrence
frequency. Perhaps maintain a network and allow queries like "how often
are X and Y mentioned together".
Storage: likely a graph DB or just a list of edges if needed.
Integration in analysis:

The source reliability might modulate the output scoring: e.g., if publisher is
known extremely biased, our overall bias score might be adjusted upward
(though ideally our content analysis finds it anyway). But it’s an extra
context check.
Or at least, we present it to user: e.g., "Publisher X is rated as Right bias,
Low factual by MBFC".
The pipeline should be flexible to incorporate these fields: e.g., an initial
step reads metadata into the doc structure, and a final step appends these
to the output JSON.
Batch vs real-time:
Metadata lookup is quick (DB query) but if needed, could be cached for
known publishers.
If in real-time we don't have share_count (since that's dynamic), maybe
skip or have last known.
No code needed beyond perhaps how to attach DB results to doc_data. But
could illustrate a database fetch:
Python Run
# Example: attach publisher info from database
publisher_name = doc_metadata["publisher"]
pub_info = publisher_db.get(publisher_name) # pseudo call to DB or dict
if pub_info:
doc_data["document"]["publisher_bias_rating"] = pub_info["bias_rating"] # e.g., "Rig
doc_data["document"]["publisher_bias_score"] = pub_info["bias_score"] # e.g., 0.8
doc_data["document"]["publisher_factuality"] = pub_info["factuality_score"]
# attach trending keywords if any known for date or so
doc_data["document"]["trending_keywords"] = get_trending_keywords(doc_metadata["date_publ
And so on.
The database schema design is asked in Integration & Aggregation questions,
I'll answer there thoroughly instead of code here.
Composite Scoring & Aggregation
Composite Score Aggregation
To combine 50+ features into composite metrics, we define several high-level
indices:

Overall Bias Score: an aggregate of all bias-related signals (linguistic bias,
propaganda, framing, sentiment imbalance). Likely 0 = no bias, 1 =
extremely biased. We can derive this via a weighted sum or machine
learning if labeled data (like predict left/right or bias presence). Without
labels, use expert weighting:
e.g., overall_bias = average of normalized linguistic bias polarity,
propaganda intensity, framing extremity, etc.
Manipulation Index: combine propaganda techniques severity, logical
fallacies severity, misleading score, emotional appeals. This indicates how
manipulative the piece is. Could be 0-1 with 1 = highly manipulative.
Perhaps heavily weight propaganda intensity and fallacy severity.
Factuality Rating: We already have factuality_score (0-1) from that
module, which is itself composite. This can be final or we incorporate
publisher reliability (if known unreliable, we might adjust downward).
Quality or Credibility Score: incorporate factuality, bias, data accuracy,
transparency. Could be a weighted formula: e.g.,
\text{Quality} = w_f F + w_t T + w_b (1-\text{overall_bias}) + w_d D,
so that high factuality, transparency, low bias, high data quality yield high
quality.
Possibly also an Engagement or Clarity Score if needed: combining
readability, clarity, structure (some systems might measure how well-
written or clear an article is, though it's not asked directly, but could be a
byproduct).
We must make weights explicit:
Without training data, we might say equal weights for components of
similar importance, or emphasize factuality as most important (e.g.,
factuality 40%, bias 25%, propaganda/manipulation 25%, style 10%).
We also might produce separate composite indices rather than one uber-
score since different users may care about different aspects (like a
"Propaganda Index" vs "Bias Index" vs "Truth Index").
Feature Weighting
Given not all features equal:
Use domain expert weighting: e.g., a blatant factual error (factuality) is
more serious than slightly loaded language (bias). So factuality may get
higher weight in overall credibility.
Some features might correlate, we should avoid double counting (like
fallacy and misleading score overlap).

Could do principal component or correlation analysis on a development
dataset to see which features cluster, then reduce or weight accordingly.
Possibly allow a learning approach: If we had some articles rated by experts
on bias and reliability, we could use regression to find weights. But absent
that, manual weighting:
Highly weight: factual accuracy, major logical fallacies, major
propaganda (these directly mislead).
Medium weight: subtle linguistic bias, framing (these are important but
sometimes less overt).
Low weight: structural complexity (less about bias, more style).
We can create a weighting scheme table.
Dimensionality Reduction & Visualization
We can treat each article as a point in high-dimensional feature space (like
50 dims). To visualize, use PCA or t-SNE:
e.g., reduce to 2D with PCA, color points by publisher or bias rating to
see clustering.
UMAP could cluster articles by writing style or propaganda content.
Or we specifically reduce certain subsets: maybe a 2D bias space (one axis
for partisan bias (left-right), another for sensationalism or tone).
We should mention how we'd use these:
Might produce interactive plots where one can see clusters of similar
articles (maybe propaganda-heavy ones cluster).
Also, create composite axes manually: e.g., "factual vs emotional" could be
two axes that are combos of our features.
Database Schema
We design a scalable storage:
Likely use a relational DB (SQL) for structured attributes and maybe a
separate index for full text (Elasticsearch) if needed for content search.
Tables:
Document table: columns: doc_id, title, publisher_id, date, author,
section, bias_score, factuality_score, bias_flags (maybe JSON of bias
features), propaganda_flags, etc. Could also have an
aggregate_quality_score field.
Sentence table (if needed): doc_id, sentence_id, text, sentiment,
fallacy_flag, etc.

Entity table: doc_id, entity_name, sentiment, toxicity, etc.
Token table: probably not, too large (millions of tokens times million
docs is too big).
Or store tokens/sentences in JSON in document table if needed (like a
JSON blob field for sentences with their features).
Publisher table: publisher_id, name, bias_rating, factuality_rating, etc
(populated from external sources).
Possibly IssueStance table: doc_id, issue, stance, strength.
PropagandaSpan table: doc_id, technique, span_text, etc if we want to store
specific spans for reference.
If using NoSQL or a graph:
Could use a graph DB for entity co-mentions: nodes = entities, edges =
co-mention count. But that can also be derived on the fly or in memory
for analysis.
Or a vector DB (like FAISS) to store article embeddings (maybe an
embedding of the whole article content or the feature vector). That
allows similarity search (find similar articles by content or by feature
profile).
We could compute an embedding combining our features (or use a
language model embedding) and store in Faiss for clustering or
retrieving comparables.
The schema should allow efficient queries:
e.g., "SELECT title FROM Document WHERE factuality_score < 0.5 AND
bias_score > 0.7 AND publisher_id = X".
Or join with publisher to filter by certain bias category.
We mention also using indexing on key fields (like publisher_id, date for time
queries).
We might consider storing the feature vectors in a vector search for more
complex similarity queries (that's where Faiss fits in).
For example, store a 10-dim "bias vector" for each doc in Faiss so one can find
which articles are closest in bias features.
Visualization Dashboard
Key visualizations:

Bias & factuality chart: e.g., scatter plot with X = bias score, Y =
factuality score, each point an article (colored by publisher or category).
This could show clusters (e.g., low factuality high bias cluster might be
clickbait sites).
Radar charts for propaganda techniques frequencies in an article, or
moral foundation distribution.
Heatmaps or bar charts for logical fallacy occurrence by type across a
collection.
Entity sentiment bar chart: showing how positively/negatively each
entity is portrayed.
Timeline: if analyzing articles over time, show trending bias over time or
changes in stance.
Network graph of co-mentioned entities or sources connections (maybe
show which entities appear together, or which publishers cover similar
topics with bias).
Article text annotations: highlight text spans in the article with color
codes for different features (like red underline for fallacies, blue for
propaganda phrase, etc). This is crucial for explainability.
Distribution histograms: e.g., distribution of reading level by publisher,
or distribution of propaganda index in our dataset.
Clustering: maybe cluster articles by feature similarity and show cluster
topics (e.g., cluster of highly emotional conspiracy posts vs cluster of
neutral factual reports).
Possibly a dashboard that allows filtering: user selects a publisher or date
range, then sees aggregated metrics (like average bias, common
propaganda techniques for that subset).
For stance: maybe a summary like "Out of 100 articles on topic X, 30%
support, 50% neutral, 20% oppose".
It's important visualizations convey uncertainty or intensity properly, e.g.,
using color gradients or tooltips with actual scores.
Real-time vs Batch Processing
Decide which components can be real-time:
Real-time (sub-second per doc) possible for:
Tokenization, POS, NER (spaCy small model can do a doc in maybe
~0.1s).
Sentiment (using VADER or a small model) quick.
Lexicon-based checks (instant).

Simpler ML models (like a small linear model for propaganda might be
quick).
Many of the counts (propaganda via regex, bias words count).
So an approximate analysis (without heavy transformers) could run in
<1s.
Batch-only (things that are too slow or require large models/data):
Transformer-based fallacy and propaganda detection (especially if
many sentences, need GPU).
Deep coreference resolution or NLI checks for contradictions (these are
heavy).
Possibly stance with NLI (one could skip NLI for real-time and rely on
sentiment).
Summaries across corpus (like trending keywords require batch
calculations across docs).
Vector indexing or PCA ( done after processing many docs).
So we might implement a tiered system:
A real-time API that given a new article uses mostly heuristic and small-
model components to give a quick bias/factuality estimate (maybe less
precision).
Then an offline pipeline that periodically uses full models (BERT, etc.) to
refine analysis on all collected docs for research outputs.
Real-time components specifically: sentiment, entity analysis (light version),
basic bias word detection, maybe even a distilled classifier for propaganda
(if we train a tiny model).
Batch: all the heavy stuff described.
We articulate that:
Some features (like share_count trending) inherently are batch (need global
data).
The user might not need real-time in academic research, but if building a
live tool, one should pick and choose.
We likely finish by summarizing all parts are integrated into a pipeline with
modular stages, citing any necessary references we used.
Finally, ensure citations are included for research mentions:
We have a few citations prepared:
Fallacy detection poor in LMs
Propaganda detection uses transformers

Reporting verbs bias example
We should place them in relevant sections:
I think I placed [1] in fallacy section, [6] in propaganda, [7] in linguistic bias
(Attribution bias).
Yes, check:
I did cite [1] and [6] and [7] in the sections above (analysis part). Good.
We should ensure those citations are correct and beneficial:
[1†L58-L65] in fallacy part: yes, explains difficulty and structure needed.
[6†L63-L70] in propaganda: yes, says pre-trained transformers and tasks, which
backs our approach.
[7†L447-L455] in bias: yep that part about "explained vs claimed".
No other external citations used except perhaps [4†L93-L100] I referenced for
sanity on verifying base features (though [4] was a systematic review, but lines
93-100 is just listing dataset etc, not directly needed).
But I wrote:
"We verify correctness by comparing with known readability baselines." Actually
[4†L93-L100] is a random point in abstract, not specifically about readability
baseline. Might remove or adjust that citation:
Better not to cite [4] out of context. Could remove that citation as it doesn't
clearly support a statement I made (I used it as if verifying baseline but [4]
didn't mention readability, it was about identifying 17 forms of bias etc).
I'll remove [4†L93-L100] mention to avoid misuse. Instead, maybe cite [4†L71-
L75] "Transformers outperform RNNs in bias detection" if relevant. But we
already plan to use transformers in many parts, it's fine.
Everything else seems self-contained.
We should double-check formatting:
The headings and subheadings usage is consistent with user request.
We have a main title (# ...).
Sections as ## ... each dimension.
Subsections as ### ...
We did bullet points where suitable (especially in Implementation Strategy).
Paragraphs are reasonably sized.
We included code fences as requested with ```python.
We preserved citations as needed.

We should ensure images: We didn't embed any images because the content
didn't require. The instruction said no need to specifically search images unless
found. It's fine.
Now, summarizing in the final output:
We probably should cover integration questions directly in the final section:
the prompt lists 1 to 6:
1. Composite Score Aggregation (we have something).
2. Feature Weighting (we touched in composite scoring portion).
3. Dim reduction (we did).
4. Database Schema (did).
5. Visualization (did).
6. Real-time vs Batch (did).
I think it's covered but perhaps we should format these as sub-sub headings or
bullet list under Composite Scoring section?
We named section "Composite Scoring & Aggregation".
We can break into subheads:
Composite Score Aggregation
Feature Weighting
Dimensionality Reduction & Visualization
Database Schema
Real-time vs Batch Processing
This will clearly answer each. I'll do that to mirror the integration questions
structure.
Yes, let's structure the final section accordingly.
Alright, let's integrate that clearly.
Final Aggregation & Composite Scoring System
Composite Score Aggregation
To provide overall assessments, we combine the myriad features into a few
interpretable composite scores:

Overall Bias Score (0–1): Represents the extent of partisan or slanted
bias. We aggregate linguistic bias polarity, propaganda intensity, framing
skew, and entity sentiment imbalance. For example, we can compute an
overall bias as a weighted sum:
BiasScore = 1 w (avg entity sentiment polarity)+
Z ( 1
w (bias markers density)+ w (propaganda intensity)+
2 3
w (framing asymmetry) ,
4
)
normalized to [0,1]. Here $Z$ is sum of weights. If an article consistently
uses one-sided language (strong negative sentiment toward one side, many
loaded words, propaganda techniques like name-calling), BiasScore will
approach 1. A neutral, balanced article would score near 0. For
interpretability, we might label ranges as “Low Bias” (0–0.3), “Moderate”
(0.3–0.6), “High Bias” (0.6+).
Manipulation Index (0–1): Combines features indicating manipulative or
deceptive tactics. This would heavily weight propaganda technique
intensity, logical fallacy severity, misleading indicators, and emotional
appeals. For instance:
ManipulationIndex = 1 − ∏ (1 −
feature∈{fallacy,propaganda,misleading}
feature_score),
which yields near 1 if any one of these components is very high. A simpler
linear combo could also be used with high weights on fallacy severity and
propaganda frequency. A piece with multiple fallacies and propaganda
techniques would get a high index, flagging it as highly manipulative.
Factuality Rating (0–1): We use the factuality_score from the factual
analysis module as the core. This already blends verifiability, consistency,
and accuracy. We might adjust it with source credibility if available: e.g., if a
known unreliable publisher, we might cap the factuality rating or subtract a
small amount. But generally, factuality_score as computed (with
verified_claim_ratio, contradiction checks, etc.) is our final factual accuracy
measure.

Overall Quality Score (0–1): An aggregate “credibility” or quality metric
that accounts for bias, factuality, clarity, etc. One formula could be:
QualityScore = w F + w T + w D + w (1 − M)+ w (1 − BiasScore),
f t d m b
where $F$ = factuality_score, $T$ = transparency_score, $D$ =
data_quality_score, $M$ = misleading_score, BiasScore as above. We
subtract bias and misleading components so that lower bias/misleading
yield higher quality. Weights $w_i$ reflect importance; likely $w_f$
(factuality) is highest. For example, we might choose $w_f=0.4, w_t=0.2,
w_d=0.1, w_m=0.1, w_b=0.2$. Then an article that is factual, transparent,
with accurate data and low bias will score high. This composite can be
scaled to a 5-star rating or letter grade for convenience.
We ensure all component scores are normalized to comparable ranges (most
are already 0–1 or –1 to 1 which we convert). In absence of training data, these
formulas are hand-tuned; they can be refined by comparing with expert
evaluations. If available, we would validate by correlating our QualityScore with
independent credibility ratings of articles and adjust weights accordingly.
Importantly, we keep composite scores interpretable: the user can drill down
into why a score is low (e.g., a low factuality sub-score or high bias sub-score).
Each composite is essentially an overview: BiasScore focuses on ideological
slant, ManipulationIndex on deceptive technique, FactualityScore on
truthfulness, and QualityScore on overall reliability.
Feature Weighting Strategy
Not all features contribute equally – we apply a weighting scheme reflecting
their impact:
Factual accuracy features are given strong weight in credibility
assessments. A single outright false claim or glaring contradiction is very
damaging, so factuality com high weight. For instance, a factual error might
single-handedly cap the FactualityRating regardless of other positives.
Propaganda and fallacies have high weight in the ManipulationIndex.
E.g., the presence of a blatant Ad Hominem or Fear Appeal might push the
ManipulationIndex high even if other measures are mild, because such
techniques strongly indicate manipulation.
Subtle linguistic bias (like hedging or mild loaded language) is given
moderate weight – these contribute to BiasScore but might not overwhelm
an otherwise factual piece. They accumulate: many small bias signals
together matter.

Structural features (like complexity or passive voice) are weighted lower
in overall quality. They are more about style and may not directly indicate
deception or bias. We use them mainly for diagnostic purposes or
secondary indicators (e.g., extremely convoluted language might slightly
reduce the Transparency score, but it won’t overshadow factuality).
Source metadata can act as a prior weight: if a publisher has a known
bias or reliability rating, we may incorporate that as an offset. For example,
if Publisher X is rated “Mostly Factual” and Center bias, that sets an
expectation. Our system’s computed scores might be adjusted or at least
interpreted in light of that (e.g., giving benefit of doubt or highlighting when
our analysis deviates from the expected rating).
Learned weighting (if possible): In a later phase, we could use machine
learning on a small labeled dataset (articles labeled as propaganda, biased,
etc.) to fine-tune these weights. For now, we rely on domain expertise: e.g.,
an outright false statistic (factual error) might be considered twice as
important as the presence of a few emotionally loaded adjectives.
In practice, we will document the weighting rationale and allow user override.
For instance, researchers might assign their own weights if they care more
about bias than factuality for a particular study. The system could provide
sliders for “importance of factual accuracy vs bias vs style” to recompute
composite scores on the fly, since our modular scores make this feasible.
Dimensionality Reduction & Visualization
With dozens of features per document, we use dimensionality reduction
techniques to visualize and explore the high-dimensional space:
PCA (Principal Component Analysis): We can project the feature space
onto the top 2 or 3 principal components. This can reveal clusters of
documents with similar profiles. For example, perhaps PC1 correlates with
factuality vs misinformation, and PC2 correlates with partisan bias. Plotting
articles on PC1–PC2 could separate, say, highly factual balanced news in
one quadrant and highly biased low-factuality pieces in another.
t-SNE / UMAP: These nonlinear reducers are useful for clustering similar
documents. We could take, for instance, the 10 most salient features (or
even an embedding of the article text combined with our features) and run
t-SNE to see grouping. We might find clusters corresponding to different
propaganda styles or topics. For example, t-SNE might cluster all
conspiracy-theory articles together if they share patterns (high
manipulation, certain moral foundation signals).

Feature correlation analysis: We can also reduce dimensionality by
analyzing correlation: if some features are redundant (e.g., our toxicity
score might correlate with name-calling frequency), we might drop or
combine them to simplify. A correlation heatmap can guide which features
to merge or ignore in composite indices to avoid overweighting similar
signals.
Visualization Dashboard Ideas:
A scatter plot with x-axis = BiasScore, y-axis = FactualityScore, each point
an article, colored by publisher or topic. This immediately shows the
landscape of media: ideally, quality journalism clusters in high-factuality,
low-bias corner, whereas fringe propaganda might cluster low-factuality,
high-bias.
Spider/Radar charts for individual articles showing the profile of scores
(e.g., one spoke for each propaganda technique intensity, or each moral
foundation). A propaganda-heavy article might spike on certain spokes (like
high name-calling, high fear), whereas a neutral factual report stays near
center.
Time-series plots to track metrics over time or per event. For instance,
plot the average bias score of all articles about a specific topic month by
month to see if coverage is getting more polarized.
Network graph visualizations for co-mentioned entities: nodes as
people/organizations, link two nodes if frequently mentioned together in
articles, with edge thickness proportional to co-mention count. We could
color nodes by average sentiment (how they are portrayed). This could
uncover, say, polarizing figures and which “side” they’re more positively
mentioned by.
Interactive article viewer: A view to highlight the text itself: using
colored highlights or underlines for different features (red for fallacies
【1†L58-L65】【6†L63-L70】, orange for propaganda, blue for loaded
language, green for evidence/citations, etc.). This helps a user see exactly
why an article was scored a certain way – e.g., hover over a highlighted
phrase to see “Propaganda: Loaded Language (intensity 0.8)”.
Comparison charts: e.g., bar charts comparing different outlets on
average scores (bias or factuality), or a stacked bar showing distribution of
propaganda techniques in left-leaning vs right-leaning sources.
Dimensionality reduction plots can also be used in the dashboard: e.g.,
an interactive 2D t-SNE plot where each point is an article, and the user can
filter points (show only from a certain publisher or topic) to explore
patterns.

These visualizations communicate complex data to both technical and non-
technical audiences. Journalists might love the text highlight view and
bias/factual scatter; researchers might use the PCA cluster view to identify
outliers or groups of interest. We will ensure that every number in the
composite scores can be traced to raw features (transparency in the
dashboard is as important as in the analysis!).
Database Schema Design
To manage millions of documents and their features, we propose a hybrid
storage approach:
Documents Table ( ): Each record corresponds to one article/post
Document
with key metadata and top-level scores. Columns might include:
doc_id  (primary key),
|            | ,   |                  | ,              |     |                    | ,      | ,       | .             |       |
| ---------- | --- | ---------------- | -------------- | --- | ------------------ | ------ | ------- | ------------- | ----- |
| title      |     | publisher_id     | date_published |     |                    | author | section |               |       |
|            |     | ,                |                |     | ,                  |        |         | ,             |  (the |
| bias_score |     | factuality_score |                |     | manipulation_index |        |         | quality_score |       |
composite metrics for quick filtering).
| JSON or separate columns for sub-scores like  |     |     |     |     |     |     |     | ,   |     |
| --------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
fallacy_vector
|                   |     |     | ,                      |     |     |     | , etc., depending on query |     |     |
| ----------------- | --- | --- | ---------------------- | --- | --- | --- | -------------------------- | --- | --- |
| propaganda_vector |     |     | linguistic_bias_vector |     |     |     |                            |     |     |
needs. We could use a JSONB column (if using PostgreSQL) to store the
entire structured output for flexibility.
text  or a reference to the text (the raw text could be stored in a text
search engine or a separate table if needed for full-text queries).
Publisher Table ( Publisher ): fields:  publisher_id ,  name ,  bias_rating
(categorical),  bias_score  (numeric, e.g., -1 left to +1 right or 0-1 scale),
factuality_rating  (e.g., "High", "Mixed") and possibly numerical factuality
| score,  |     |     |     |  (could be an aggregate score of past accuracy). |     |     |     |     |     |
| ------- | --- | --- | --- | ------------------------------------------------ | --- | --- | --- | --- | --- |
reliability_history
This table is small (one entry per source) and can be joined to Document.
Sentence Table ( SentenceFeatures ): if we need to query sentences (for
example, find all sentences that contain a fallacy), we can have:  ,
doc_id
|     |     | ,  ,  |     | ,   |     | ,   |     | ,   | ,   |
| --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
sentence_id text sentiment has_fallacy fallacy_type has_propaganda
, etc. But storing every sentence of 1M docs = many millions of
technique
rows, which may be heavy. Alternatively, we could store sentences in a
JSON array in the Document JSON field (since typically we retrieve by
document anyway).

| Entity Table ( |     |                |               | ):  |        | ,             |     | ,           | ,          |
| -------------- | --- | -------------- | ------------- | --- | ------ | ------------- | --- | ----------- | ---------- |
|                |     | EntityFeatures |               |     | doc_id | entity_name   |     | entity_type |            |
|                | ,   |                | ,             |     | ,      |               |     | ,           | , etc., as |
| sentiment      |     | toxicity       | framing_score |     |        | moral_valence |     | quote_count |            |
defined in entity-level analysis. This allows queries like “SELECT * FROM
EntityFeatures WHERE entity_name='Facebook' AND sentiment < -0.5” to
find documents where Facebook is portrayed very negatively.
| Issue Stance Table (       |     |     |        | ):       |          | ,      |  (entity or topic),       |     |        |
| -------------------------- | --- | --- | ------ | -------- | -------- | ------ | ------------------------- | --- | ------ |
|                            |     |     | Stance |          | doc_id   | target |                           |     | stance |
| (support/oppose/neutral),  |     |     |        |          | ,        |        |  (boolean). This helps to |     |        |
|                            |     |     |        | strength | explicit |        |                           |     |        |
query, for example, all docs that support a given policy.
Scores History Table (optional, for time series): If we re-run analysis or
update scores, we might keep historical records to track changes. But for
static corpora, not needed.
Share/Trend Table (optional): If we ingest social media info, e.g.,
SocialMetrics :  doc_id ,  share_count ,  like_count , etc., and maybe
| trending_score |     |  or trending keywords list per date range. |     |     |     |     |     |     |     |
| -------------- | --- | ------------------------------------------ | --- | --- | --- | --- | --- | --- | --- |
For performance:
Index important fields: e.g., index on  publisher_id  for quick filter, on
date_published  for time queries, on composite scores for range queries (to
quickly find all low-factuality articles).
The JSON fields (if used) can be indexed on specific keys if the database
supports it (like GIN indexes on JSONB in Postgres).
The volume: 1M documents is manageable with proper indexing. Each
document’s feature JSON might be, say, a few KB (since it's mostly
numbers and short text spans). 1M * few KB ~ a few GB, which is fine.
If full text search is required (e.g., find articles mentioning a certain phrase
or to allow regex on content), integrating Elasticsearch or another search
engine is advisable. We could store  doc_id  and  text  in an ES index, and
store analysis scores as fields there too, enabling combined queries (like ES
can filter by bias_score range and text content simultaneously).
Vector search: For high-dimensional similarity search (maybe to find
similar articles or cluster), we can use a vector database or library. For
example, store each document’s embedding vector (could be a
concatenation of key scores or a neural embedding of the content) in FAISS
or Milvus. This allows queries like “find 10 articles most similar to this one”
or clustering. We likely generate these embeddings offline and keep them
updated as new docs come in.

Graph database: If doing extensive network analysis of entities or
sources, a graph DB (Neo4j, etc.) could store relationships: e.g., an "Entity"
node connected to "Document" nodes or to other entities via co-mentions.
But this might be overkill; many network queries can be answered with SQL
(JOIN on EntityFeatures to find common doc counts, etc.). For large-scale, a
graph approach or precomputed adjacency matrix might be needed for
performance on complex network queries.
Our design ensures that one can query the database for complex conditions.
For example:
SELECT D.title, D.publisher_id, D.bias_score, D.factuality_score
FROM Document D
JOIN Publisher P ON D.publisher_id = P.publisher_id
WHERE P.bias_rating='Right'
AND D.bias_score > 0.7
AND D.factuality_score < 0.5;
This could retrieve highly biased, low-factual articles from right-leaning outlets.
Or one could filter by propaganda_vector contains a specific technique if stored
in JSON, etc. We will carefully design the schema and possibly use partitioning
or sharding if the volume grows beyond a single server’s efficient handling (1M
is fine on one server, but 100M might need distributed solutions).
Visualization & Dashboard Integration
(Combined with above “Visualization Dashboard” section) The dashboard will tie
into the database via queries or an API layer. It will present composite scores
prominently, with the ability to expand into sub-features. For example, clicking
on an article’s BiasScore could pop up a breakdown of contributions (e.g.,
“Loaded language: 0.8, One-sided reporting: 0.7”), and even highlight examples
from the text (like the actual loaded words).
We will include interactive filtering controls on the dashboard:
A filter by date range, publisher, topic, or score thresholds.
The ability to select a subset of articles (say, one outlet’s content) and see
aggregate bias/propaganda patterns for that subset (e.g., an average
propaganda technique profile).
Dimensionality reduction results like PCA can also be visualized interactively:
e.g., a 2D plot where each point is an article, and user can zoom or click a point
to see which article it is and its scores. Clusters could be annotated (perhaps via
clustering algorithms) to indicate if they correspond to certain topics or styles.

Real-time vs Batch Processing
The system distinguishes components suitable for real-time analysis versus
those reserved for batch/offline processing:
Real-time (streaming or on-demand) components:
Basic NLP parsing (tokenization, POS, NER, sentence splitting) – spaCy
can handle a single document quickly (tens of milliseconds).
Lightweight lexicon/rule features: sentiment (using VADER or a small
model), counting loaded words, detecting passive voice, etc. These run in
milliseconds.
Pre-computed ML models that are small or distilled: e.g., a distilled
transformer or logistic regression for sentiment or even propaganda
detection. If we have a distilled model for propaganda techniques (say a
smaller BERT or even an SVM with n-gram features), it could run near real-
time for a single document.
Shallow scoring: computing composite scores from pre-derived features
is trivial (just arithmetic on the feature values).
Components that can likely be done <1 second per document on a single CPU
include: sentiment analysis, bias lexicon scan, readability, even a single forward
pass of a small neural model. For instance, a distilbert-base-uncased can
process a few hundred words in under 0.5s on CPU.
Batch (offline or high-latency) components:
Heavy transformers per sentence: The full logical fallacy classifier
(RoBERTa) or fine-grained propaganda classifier on each sentence is
expensive. For 1M docs, we schedule these on a GPU cluster offline. We
might run them overnight or on a sample of data. In real-time, we’d omit or
use simplified heuristics instead.
Coreference resolution and NLI checks: Running anaphora resolution
or pairwise NLI contradiction detection across all sentences is too slow for
on-demand. These are done in batch to enrich the data. If a user queries a
specific article in the UI, we might not immediately run coref or NLI;
instead, we rely on precomputed results. Alternatively, if the user
specifically requests a deep analysis of one article, we could trigger these
with a delay (showing a “detailed analysis is loading” spinner).

Trend analysis & ML training: Anything that requires looking at many
documents (like computing trending keywords, updating an LDA topic
model, or retraining a stance classifier on new data) is done in batch. We
might update trends daily or weekly.
Dimensionality reduction & clustering for visualization is done batch on
the dataset and updated periodically (unless we implement it client-side for
a subset of data).
Large-scale similarity search: If a user wants to find similar articles, a
pre-built FAISS index of embeddings is used (which is created in batch). The
query itself (finding nearest neighbors) is fast, but the index building is
batch.
Hybrid strategy: We maintain a pipeline where new incoming documents first
go through a fast lane: assign preliminary scores using lightweight methods
(perhaps no transformers, just rules and a smaller model). This can populate
the database quickly. Then, in the background, a rrocess runs heavier analyses
and updates the records (e.g., it might add detected fallacy spans or adjust
scores slightly after full analysis). This way, the data is available almost
immediately with reasonable accuracy, and improves over time. We also set up
periodic batch jobs to re-process data if we improve algorithms or add new
features, ensuring consistency.
For interactive use (like a browser extension that analyzes one article on the
fly), we would embed only the real-time components. That might include a
subset of propaganda/fallacy detection (perhaps using a single multi-label
model or even GPT-4 via API if allowed, though GPT-4 is not deterministic or
explainable enough for our needs). Mostly, the extension could use the
precomputed insights if the article is known in our database, or run a scaled-
down analysis locally.
In summary, computationally intensive tasks are siloed to batch processing on
a server with parallelization (using Spark for big data distribution or Ray for
parallel Python, as noted). The system is designed to be modular so that real-
time pipelines can skip or stub out the heavy parts and still deliver an analysis,
while the full pipeline can be run on a large corpus asynchronously to generate
the comprehensive dataset for research.
Sources

ChatGPT can make mistakes. Check important info.