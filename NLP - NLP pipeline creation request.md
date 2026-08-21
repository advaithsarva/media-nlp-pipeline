Save as PDF

Tue, Dec 16 at 5:25 AM

hi

Hi 👋

How are you doing right now?

Tue, Dec 16 at 2:08 PM

NLPpipline.zip
Zip Archive

Comprehensive Stra…
Document

FALLACY DETECTIO…
Document

Fallacy Feature extr…
Document

Feature extraction.t…
Document

File Formats.txt
Document

NLP.txt
Document

Pipline.txt
Document

THE BEST FORMAT …
Document

Go through the given ﬁles, you a very senior NLP
engineer cum mathematician, devops engieer,

linguistic expert, combine everything in the given

ﬁles, not even missing a single line from all of them

and create the best pipeline, everything, literally

everything from all the ﬁles, you are not going to

miss even, from math to pseudo code to
integration part in pipeline, to all the libraries,
everything, take time in generating,literaly

everything, i ahve reaserched everthing but not
able to combine em all, so ill check them again

Thanks for sharing the detailed background and ﬁles. To generate the

comprehensive NLP pipeline you requested, could you please clarify a few

points so I can align it with your exact needs:

1.  Intended Output Format: Should I generate this as a markdown

document, code ﬁle, or report-style text with sections, pseudocode,

formulas, and code blocks?

2.  Scope and Depth:

Do you want a fully modular pipeline (with deﬁnitions for each layer like

ingestion, normalization, fallacy detection, bias scoring, etc.)?

Should it include infrastructure deployment suggestions (e.g.,

Spark/Ray, cloud options)?

3.  Focus Areas: Are there any areas you’d like me to emphasize more (e.g.,

argument mining logic, fallacy scoring math, feature schemas,

DevOps/data engineering integrations)?

4.  Final Usage: Is this meant for academic research, enterprise deployment,

or something else?

Let me know and I’ll begin compiling and structuring the most complete and

accurate version of this pipeline for you.

Thanks for sharing the detailed background and ﬁles. To generate the
comprehensive NLP pipeline you requested, could you please clarify a few points so

I can align it with your exact needs: 1. **Intended Output Format**: Should I…

Show more

Great — I’ll now begin building a full-length, step-by-step NLP pipeline

architecture and implementation report for your media/news analysis platform.

It will cover everything: ingestion, feature extraction, argument mining,

fallacy/bias/taxonomy scoring, storage, pseudocode, formulas, integrations,

and deployment tips — with clear explanations and comments aimed at your

intermediate NLP level.

I’ll let you know as soon as the full report is ready.

1.report style or whatever style you like that can genarte sedo code, formulas, integration and code blocks,2. everthing3. evething , rather more on building pipline and maintinging it, everthing from extaring, processing and giving output , intergating codes or endparts for other devleopers to delpoy4. this is meant for Media/ news analysis ( comapny ) and tell me everthing what is going on each and ever step cause i am a begginer and ill learn what 1.report style or whatever style you like that can genarte sedo code, formulas, integration and code blocks,2. everthing3. evething , rather more on building pipline and maintinging it, everthing from extaring, processing and giving output , intergating codes or endparts for other devleopers to delpoy4. this is meant for Media/ news analysis ( comapny ) and tell me everthing what is going on each and ever step cause i am a begginer and ill learn what Research completed in 73m · 9 sources

Production-Ready NLP Pipeline for Media/News
Bias and Fallacy Analysis

Introduction

This report presents a comprehensive design for a production-grade Natural

Language Processing (NLP) pipeline tailored to a media/news analysis

platform. The goal of the system is to ingest news content and systematically

detect rhetorical fallacies, propaganda techniques, and biases in the

text, producing structured outputs that highlight manipulative content and

provide bias/fallacy scores. The design integrates best practices and

responsibilities from all key roles – Lead Engineer, NLP/Data Engineer,

Backend Engineer, and QA Tester – to ensure the solution is scalable,

deterministic, reproducible, and secure. We will explain each stage of the

pipeline in detail, including data ingestion, text processing, feature extraction,

taxonomy-based classiﬁcation, scoring logic, and deployment considerations.

Throughout, we emphasize traceability (every result can be traced through

versioned data and logs) and determinism (the same input yields identical

output on every run) as top priorities.

The pipeline is designed with a layered medallion architecture

(Bronze→Silver→Gold) to organize data processing stages. At a high level, raw

data from various sources is ingested and stored as Bronze (raw canonical

form), then cleaned and normalized into Silver (structured text form), then

enriched with analytical features and annotations in Gold (feature-rich records

with scores). Final outputs are served via secure APIs, providing JSON results

that include content highlights and tags for easy visualization on the front-end.

A versioned data store and a rigorous testing framework ensure that changes

to the pipeline do not introduce regressions or non-reproducible results.

In the following sections, we break down the entire pipeline, explaining each

component and its integration:

System Architecture & Data Flow – The overall pipeline structure from

ingestion to serving, including Bronze/Silver/Gold data lake zones and how

components connect.

Data Ingestion and Preprocessing – Supported input ﬁle types,

ingestion mechanisms, and normalization (cleaning, metadata enrichment).

Argument Segmentation & Structure Mapping – Sentence splitting

and building an argument graph of claims and premises to enable fallacy

detection.

Feature Extraction Layers – A multi-layer feature engineering stack

(structural, lexical, syntactic, semantic, entity, sentiment, narrative, etc.)

producing a rich set of signals for each text.

Fallacy & Rhetorical Technique Detection – Specialized detectors (rule-

based and ML) for logical fallacies, propaganda techniques, and biases, and

how their outputs are represented.

Taxonomy Classiﬁcation & Scoring Matrix – Classifying content into a

predeﬁned taxonomy of categories and computing a composite scoring

matrix from all signals, yielding bias/fallacy scores.

Storage, Formats, and Versioning – How data is stored at each stage

(JSONL, Parquet, Vector DB), schema design, feature registry management,

and versioning for models and features.

Backend Integration & Serving – The backend API design that exposes

analysis results (with highlighted text spans and scores) to other systems,

plus DevOps considerations for deployment (containerization, CI/CD,

logging, monitoring).

Quality Assurance & Testing Strategy – Ensuring determinism and

correctness through comprehensive test cases, regression tests, audit logs,

and reproducibility checks, aligned with the QA role’s practices.

This blueprint is intended for engineers with basic NLP experience (beginner to

intermediate level) and avoids deep mathematical formalisms, focusing instead

on practical implementation and clarity. We include pseudocode snippets, data

schemas, and formulas where useful to illustrate the logic. By the end of this

report, a reader should have a clear understanding of every step in the

pipeline – from raw news text input to ﬁnal bias/fallacy scores – and how to

implement and maintain such a system in a real-world production environment.

System Architecture and Data Flow

Overview: The NLP pipeline follows a staged architecture with clear separation

of concerns. Figure 1 outlines the data ﬂow through the major pipeline

components (from data sources to ﬁnal output):

[SOURCES]

 ├─ Files (txt, PDF, HTML, JSON)

 ├─ Databases (SQL, NoSQL)

 ├─ Streams/APIs (Kafka topics, REST feeds)

 ↓

[INGESTION LAYER] – Bulk import via Spark/Ray jobs or streaming consumers

 ↓

[BRONZE ZONE] – Raw data stored (e.g., Parquet) + minimal metadata

 ↓

[PREPROCESSING] – Cleaning, normalization, language detection, metadata enrichment

 ↓

[SILVER ZONE] – Cleaned canonical text in structured format

 ↓

[ARGUMENT MINING] – Sentence segmentation; extract claims, premises, relations

 ↓

[GOLD ZONE] – Rich features and annotations stored (feature columns, scores)

 ↓

            ├──► **Vector DB** (embeddings index for semantic search)

            ├──► **Feature Registry** (YAML schema of features, in Git)

            └──► **Taxonomy Engine** – apply taxonomy classification & scoring

                     ↓

                 Fallacy & Bias Scores, Content Labels

                     ↓

[SERVING DB] – Results in SQL for fast lookup by APIs

 ↓

[API & FRONTEND] – RESTful API returns JSON with highlights/tags for UI:contentRefe

Bronze, Silver, Gold zones: We implement a medallion architecture to

manage data through stages. In the Bronze stage, ingested data is stored

nearly raw (with maybe minimal parsing), providing an immutable record of

original content with basic metadata (source, timestamp, etc.). In the Silver

stage, data is cleaned and normalized into a canonical structured format,

ready for NLP analysis (e.g., text extracted from PDFs, standardized encoding,

language normalized). In the Gold stage, the dataset is enriched with all

analysis results: token-level and sentence-level annotations, extracted features,

and preliminary scores or ﬂags for various signals. Separating these layers

enforces logical separation of raw vs. processed data, making the pipeline

easier to maintain and debug. Each zone uses the same underlying storage

format (Parquet ﬁles in our design) but with diﬀerent guarantees and schema

enrichments.

Data Flow Coordination: A pipeline orchestrator (e.g., an Airﬂow DAG or a

custom scheduler) manages the sequence – ensuring that ingestion completes

before triggering preprocessing, which then triggers feature extraction, and so

on. The Lead Engineer oversees integration points between components, so

each stage’s output is the next stage’s input via well-deﬁned interfaces. For

instance, after Silver data is prepared, the argument mining module reads the

cleaned text and outputs argument structures into a Gold dataset, which then

feeds the feature extractors. This modular design allows each component

(ingestion, cleaning, feature extraction, etc.) to be developed and tested in

isolation and then integrated – a practice the Lead Engineer enforces through

code reviews and interface deﬁnitions.

Determinism and Reproducibility: A crucial architectural requirement is that

the pipeline yields deterministic results – given the same input content and

the same pipeline version, the output analysis must be identical on every run.

To achieve this, we use pure or seeded algorithms (for example, setting

random seeds for any pseudo-random processes in NLP libraries) and avoid

nondeterministic approaches where possible. The pipeline version (and sub-

component versions) is stamped on every output record for traceability. This

means each result carries metadata like  pipeline_version ,  feature_version ,

taxonomy_version , and timestamp ( processed_at ), so we can audit how it was

produced. The QA Tester role speciﬁcally veriﬁes this by re-running the pipeline

on the same inputs to conﬁrm identical outputs and by checking that version

identiﬁers propagate correctly in logs and data records.

High-Level Data Structures: Internally, we represent each document as a

structured record. In formal terms, let a document D consist of sentences S₁ …

S_m, and each sentence S_i consist of tokens t_{i1} … t_{in_i}. Each token and

sentence will get annotated with various features (POS tags, sentiments, etc.),

and the document as a whole will accumulate aggregates (like overall bias

scores). We deﬁne a canonical Parquet schema for the Silver/Gold data that

can hold this information. For example, a single news article record might be

stored as a Parquet object with ﬁelds like:

JSON

{

  "doc_id": string,

  "source": string,

  "source_type": string,        // e.g. "web" | "pdf" | "social"

  "language": string,

  "raw_text": string,

  "clean_text": string,

  "tokens": [string],

  "sentences": [string],

  "entities": [                // nested list of entity mentions

      { "text": string, "label": string, "start": int, "end": int }

  ],

  "labels": {                  // various content-level labels/scores

      "sentiment": float,

      "bias_score": float,

      "toxicity": float,

      "...": ...

  },

  "metadata": {

      "author": string,

      "published_at": datetime,

      "url": string,

      ...

  },

  "pipeline_version": string,

  "processed_at": datetime

}

All pipeline stages will conform to and evolve this one canonical schema

(adding columns or nested ﬁelds as needed). This uniﬁed structure means we

don’t have to convert formats between stages, and we can easily join new

features to existing records by  doc_id . The use of Parquet allows nested

structures (for tokens, entities, etc.) and eﬃcient columnar access when

running analytics or model inference over the data.

Technology Stack: We leverage Apache Parquet as the backbone storage

format in the data lake for its speed, compression, and schema evolution

support. Ingestion and processing can be done with distributed frameworks like

Apache Spark or Ray, which integrate well with Parquet and allow scaling to

large document collections. A vector database (such as FAISS or Milvus) is

used to store high-dimensional embeddings for semantic similarity search and

clustering tasks, complementing the structured Parquet data. For model serving

and API, a containerized RESTful API (e.g., a Flask or FastAPI app in Python, or

Node.js service) will expose endpoints for content analysis, retrieving processed

results from the serving database. The system will be deployed via containers

(Docker) and orchestrated possibly by Kubernetes, following Infrastructure-as-

Code principles and CI/CD pipelines managed by the Lead Engineer. Security is

baked in at the API layer (authentication, authorization) and data layer

(encryption of sensitive data, secured access), in line with best practices for

conﬁdential projects.

In summary, the architecture is built to separate raw vs processed data,

ensure structured and well-deﬁned data exchange between components,

and maintain auditability and reproducibility at every step. Next, we dive

deeper into each stage of this pipeline.

Data Ingestion and Preprocessing

At the front of the pipeline is the ingestion layer, which handles pulling in

content from various sources and preparing it for analysis. This system must be

ﬂexible in accepting multiple ﬁle formats and data sources common in

media analytics.

Supported Input Types: The pipeline can ingest data from:

Plain text ﬁles ( .txt ,  .md , etc.) – e.g. raw text dumps of articles.

Document ﬁles ( .pdf ,  .docx , etc.) – often used for reports or print

media; these may require parsing of text from layouts or OCR for scanned

PDFs.

HTML/XML – web pages or RSS feeds providing news content, requiring

HTML parsing and cleaning of tags.

JSON/JSONL feeds – data from news APIs or internal databases might

arrive as JSON. We especially use JSONL (newline-delimited JSON) as a

convenient streaming format where each line is one article or document.

CSV/TSV – occasionally, structured datasets (like labeled data or content

metadata) may come in spreadsheets or CSV form.

Databases – large archives of content may reside in SQL tables or NoSQL

stores. We support connecting to relational DBs (PostgreSQL, etc.) or

MongoDB to fetch text ﬁelds.

Streaming sources – e.g. Kafka topics, news API streams, or webhooks

that provide a continuous feed of articles. The system can consume these

and treat them similar to ﬁles (by writing them into our Bronze store).

Audio/Video – for completeness, audio sources like podcasts or video news

can be processed by ﬁrst running speech-to-text (ASR) to generate

transcripts (using tools like OpenAI Whisper or Kaldi). The resulting text

then enters the pipeline.

Each input type may need a speciﬁc handler. For example, PDFs are processed

via an extraction library (like Apache Tika or PyPDF) to get raw text, HTML is

parsed with an HTML parser (BeautifulSoup, etc.) to remove HTML tags, and

JSONL might be directly read line by line. Language detection is performed if

we expect multi-lingual input, to route content to appropriate language-speciﬁc

models or stop early if unsupported (in our NDA project, we might limit to

English content for now, but the design keeps it extensible).

Ingestion Layer Implementation: We aggregate incoming data using a

combination of batch jobs and streaming processes:

For bulk historical data (e.g., a dump of thousands of articles), a batch job

(Spark job or Python ETL script) reads the source ﬁles/DB, converts each

record into our internal JSONL schema (assigning it a unique  doc_id ,

capturing source info), and writes it to the Bronze Parquet store. We

favor writing directly to Parquet for Bronze to avoid losing structure, but we

could also stage in JSONL then convert. In practice, writing Bronze as

Parquet with minimal ﬁelds ( doc_id ,  raw_text , basic metadata) is eﬀective.

For streaming new data (e.g., listening to a Kafka queue of new articles), a

consumer will parse each message and immediately append it to the

Bronze store (in micro-batches or via a stream append). Alternatively, if

real-time processing is needed, the streaming ingestion can directly trigger

downstream processing of each item (but careful design is needed to

maintain throughput).

Bronze Zone (Raw Storage): In the Bronze dataset (which could be a

directory of Parquet ﬁles partitioned by date, for example), each entry contains

the content as ingested. Very little transformation happens here – this is

essentially a data lake landing zone. We do attach some basic metadata:

Source identiﬁers (e.g., source name or ID, source type like “web” vs

“print”).

Ingested timestamp.

Possibly an initial unique  doc_id  (if not provided) or use a hash of the

content as ID.

If available, any upstream metadata like article title, author, publish date,

etc., might be captured here as well (otherwise it can be added in Silver).

No heavy cleaning is done in Bronze; content might still have HTML entities,

extra whitespaces, etc. The philosophy is to store ﬁrst, clean later. This

provides a fall-back if our cleaning or parsing has a bug – we can always refer

back to the raw source.

Preprocessing and Cleaning: The next step is a preprocessing module that

reads Bronze records and produces Silver records. Preprocessing tasks

include:

Text normalization: Removing or converting non-UTF8 characters,

normalizing whitespace, standardizing quotes/apostrophes, lowercasing if

appropriate (though for proper nouns we often keep case), etc.

Boilerplate removal: If the content came from HTML or PDFs, there

might be header/footer noise, navigation menus, or other non-content text.

The cleaner strips out HTML tags and script/style content for web pages. It

might use rules or an HTML diﬀ algorithm to extract main text (readability

algorithms).

Segmentation: Here or in the next stage we perform sentence

segmentation – splitting the cleaned text into sentences using NLP

libraries (e.g., spaCy’s sentence tokenizer). This is critical for downstream

analysis since many features are sentence-based. If the text is large, we

also mark paragraph breaks.

Metadata enrichment: We attach any contextual metadata needed. For

example, if the source provides a publication date, we parse it into a

datetime ﬁeld (for time-based analysis). If an author or source outlet name

is available, attach those. We might also include a content category or

section if given (like “Politics” section, etc.). These become part of the

record’s  metadata .

Language detection: If the content language isn’t known, use a fast

language ID tool to set the  language  ﬁeld and possibly ﬁlter out non-English

content if the analysis is only for English (the system could be extended to

other languages with multilingual models).

Minimal NLP parsing: In Silver, we might also do lightweight NLP parsing

to prepare for feature extraction – e.g., tokenization and part-of-speech

(POS) tagging of the text. However, we may defer full tokenization until the

feature extraction stage. At minimum, we ensure the text is segmented

into sentences and tokenized suﬃciently to detect sentence boundaries.

Consistency checks: Ensure the cleaned text is not empty (if it is, possibly

drop the record or mark it). Ensure encoding issues are resolved. This stage

might also remove articles that are too short or out-of-scope (if, say, we

have a length threshold for analysis).

The output of preprocessing is the Silver Parquet dataset. Each record in

Silver includes the clean text and the structural metadata (sentences, perhaps

tokens) in a structured format. For example, a Silver record might look like:  {

doc_id, clean_text, sentences: [...], language, title, author, published_date,

source, ... } . The Silver schema conforms to the canonical schema outline

above, with ﬁelds gradually ﬁlled in. Silver is considered the canonical text

that all further NLP processing (feature extraction) will work on. By storing it,

we avoid redoing cleaning for diﬀerent experiments – Silver is like a normalized

corpus.

To illustrate cleaning, consider pseudocode for preprocessing one document:

Run

Python

def preprocess_raw(doc):

    text = doc.raw_text

    meta = doc.metadata

    # Normalize unicode, remove weird characters

    text = normalize_unicode(text)

    text = fix_whitespace(text)

    # Remove HTML if present

    if meta.source_type == "html":

        text = strip_html_tags(text)

    # Basic boilerplate removal (e.g., "Advertisement" labels, etc.)

    text = remove_boilerplate(text)

    # Sentence segmentation

    sentences = nltk.sent_tokenize(text)  # or spaCy

    # Language detection

    lang = detect_language(text)

    # Populate silver record

    return {

       "doc_id": doc.doc_id,

       "clean_text": text,

       "sentences": sentences,

       "language": lang,

       "metadata": {

           "title": meta.title, "author": meta.author, "published_at": parse_date(meta.da

       }

    }

(This is a simpliﬁed view – in practice we’d also handle errors, log any changes,

and possibly preserve the raw text as well for reference.)

The QA tester will later verify that this preprocessing is consistent. For instance,

given the same PDF input, the extracted text should always be identical

(modulo any timestamp diﬀerences), ensuring reproducibility. They also check

that metadata like dates are parsed correctly and that no content is

inadvertently dropped. For example, if an article has an unusual structure that

confuses the HTML parser, QA might catch that the  clean_text  is unexpectedly

empty, prompting an improvement in the cleaner.

Ingestion Logging: Every item processed through this stage is logged. We

maintain ingestion logs (in a  .log  or JSON log format) that record when each

doc_id was ingested, from what source, and any errors encountered. These

logs aid traceability and allow monitoring of pipeline health (e.g., using them to

feed a monitoring dashboard that shows ingestion rates, error rates, etc.). The

QA tester can review these logs to ensure all expected inputs have been

accounted for and to spot any anomalies (like spikes in errors).

At this point, we have a corpus of clean, segmented documents in Silver, ready

for deep NLP analysis. The next component will build on this by analyzing the

argument structure of the text, which is a foundation for detecting logical

fallacies.

Text Segmentation and Argument Structure Mapping

One distinguishing aspect of this pipeline is its focus on understanding the

argument structure of the content, not just surface features. Many rhetorical

fallacies can only be identiﬁed by examining how claims and evidence are

presented in context. Therefore, after basic preprocessing, we perform an

Argument Mining step to map out claims, premises, and conclusions within

each article.

Sentence Tokenization: By the time we reach this stage, each document’s

text is split into sentences (as part of preprocessing). We treat the sentence as

a fundamental unit for many analyses (like sentiment per sentence, fallacy

ﬂags per sentence). Using an NLP library (spaCy or NLTK), each sentence is

further tokenized into tokens with linguistic annotations (POS tags, dependency

parse, etc.). The token-level analysis (POS, lemmas, etc.) gives us a basis for

more complex feature extraction later. For example, for each token t, we

record attributes like lemma(t), POS(t), is_stopword(t), NER(t) (named entity

label if any). This token feature mapping is deterministic given the library’s

model; to ensure consistency, we lock the version of the NLP model (e.g., use

spaCy model v3.x with a speciﬁc model ﬁle hash) and note it in our

feature_version .

Argument Component Identiﬁcation: We next identify spans of text that

correspond to argumentative components:

Claims/Conclusions: These are statements that express a stance or

assertion, especially the main point of the article or sub-claims supporting

it.

Premises/Evidence: These are statements that provide support or

reasons for the claims (could be factual evidence, quotes, logical

reasoning).

Opposing or Counterarguments: In balanced articles, sometimes

counterarguments are presented only to be refuted; identifying them can

be useful (though many biased articles omit them, which is itself a feature).

To detect these, we use a combination of rule-based cues and ML classiﬁers:

Rule-based: Look for key phrases indicating conclusions (e.g., “therefore”,

“thus”, “in summary”) or premises (“because”, “since”, “due to”). These

causal or concluding discourse markers are strong signals. We can use

dependency parsing to see if a clause is an assertion followed by a

rationale (e.g., “<claim>, because <premise>”). Also, check for quotation

marks or references which might indicate evidence (quotes from sources).

ML approach: Train or ﬁne-tune an argument mining model if available (for

example, a BERT-based classiﬁer that labels sentences as {Premise, Claim,

None}). Given the conﬁdential nature and timeline, a simpler approach

might be suﬃcient: e.g., use a pre-trained model from research (some

models can label argument components in text).

We also identify argumentative relations: which premises support which

claim. This can be complex (it’s essentially building a directed graph of

arguments). For our purposes, it might suﬃce to link premises to the nearest

claim or the article’s main conclusion. If using ML, there are models for

argument relation classiﬁcation; otherwise, heuristics like “premise sentences

directly following a claim sentence likely support that claim” can be a start.

The output of this step is essentially an Argument Graph for the document:

nodes representing statements (or whole sentences) tagged as claim/premise,

and edges indicating support or attack relations. We store this in the Gold

dataset. For example, we could add to the Parquet schema a ﬁeld

argument_structure  which could be a nested structure or even a small

adjacency list. Or we could maintain a separate graph (possibly using a graph

database if needed for complex querying). In our design, since we want

everything in one record, we might have something like:

JSON

"argument_structure": {

   "claims": [

      {"sentence_id": 2, "text": "X", "implicit": false}

   ],

   "premises": [

      {"sentence_id": 3, "text": "Y", "supports": 2}

   ],

   "conclusion": {"sentence_id": 1, "text": "Z"}

}

This indicates sentence 1 is a conclusion, sentence 2 a claim, sentence 3 a

premise supporting claim 2, etc. The speciﬁcs can vary, but the key is we

capture the presence (or absence) of a logical argument ﬂow.

Why this matters: Many fallacies are essentially argumentative errors. For

example:

A non sequitur is when the conclusion doesn’t follow from premises – we

can catch this if we map premises to conclusion and ﬁnd a logical gap.

Circular reasoning (begging the question) is when a premise is basically

the same as the conclusion – if our argument graph ﬁnds a cycle or the

conclusion repeats a claim, ﬂag it.

Missing premises or hidden assumptions can be ﬂagged by noting an

isolated claim that has no supporting premises (especially if it’s a strong

claim).

Slippery slope arguments often are a chain of claims where one implies

another without support – if the argument chain jumps too far (A→Z with no

logical steps), that’s a signal.

By inserting an argument graph layer, we ensure fallacy detection isn’t just

“bag of words” guessing. As one critique pointed out, without explicit argument

structure, fallacy detection becomes fragile and may rely on shallow cues.

Thus, this stage is critical.

From a pipeline perspective, this stage can be computationally heavy if using

ML models for every sentence. But since articles aren’t extremely long (news

articles might be a few dozen sentences), it’s manageable. We might use

spaCy’s dependency parse as a ﬁrst cut (which is eﬃcient in pipeline) and only

resort to heavier ML if needed.

Pseudocode Example: (Conceptual example of argument mapping logic)

Python

Run

doc = nlp(clean_text)  # spaCy model that provides dependency parse

sentences = list(doc.sents)

argument_graph = {"claims": [], "premises": [], "conclusion": None}

for i, sent in enumerate(sentences):

    text = sent.text

    # Identify conclusion by keywords or position (e.g., last sentence with a summary ton

    if any(word.lower_ in ["in conclusion", "overall", "thus"] for word in sent):

        argument_graph["conclusion"] = {"sentence_id": i, "text": text}

    # Identify premise by causal markers

    if any(word.lower_ in ["because", "since", "as a result"] for word in sent):

        argument_graph["premises"].append({"sentence_id": i, "text": text})

    # Identify claims as sentences that make bold statements (could refine with classifie

    if sent[-1].lemma_ == "?":

        continue  # skip questions

    if sent.root.pos_ == "VERB" and sent.root.dep_ == "ROOT":

        # a simple heuristic: root-level assertion

        argument_graph["claims"].append({"sentence_id": i, "text": text})

# (In reality, would need to link premises to claims via adjacency or ML model)

In practice, we would improve the above by e.g. using a classiﬁer for claim vs

premise. But it illustrates capturing the pieces.

All this structured argument information is then added to the Gold dataset for

use by the fallacy detectors. We ensure that this process is also versioned (if

we tweak our argument mining approach, that’s a change in  feature_version

or a new  argument_version ).

The QA tester will create test cases for this module as well. For example,

provide a known argument text: “Because X, therefore Y.” and check that the

graph identiﬁes “X” as a premise and “Y” as a conclusion with a supporting link.

They also verify that content with no obvious premises (e.g., an opinion piece

that just makes claims without saying “because”) still gets processed without

error (the graph might just have claims and no premises, which itself is a

feature indicating unsubstantiated claims).

Having mapped out arguments, the pipeline is now ready to extract a wide

array of features at token, sentence, and document level, and then speciﬁcally

detect instances of fallacies or biased language. We proceed next to the

feature extraction stage, which will consume both the raw text and the

argument structure we just built.

Feature Extraction Layers

Feature extraction is the heart of the NLP pipeline’s intelligence. We design it in

layers, from fundamental linguistic features up to high-level semantic and

rhetorical indicators. This layered approach ensures that simpler features (like

word counts or POS tags) provide a foundation for more complex inferences

(like detecting a slippery-slope argument). Each layer produces outputs that are

added to the Gold dataset. We also maintain a Feature Registry (as a YAML or

similar in Git) enumerating all features to be extracted, along with their

deﬁnitions and data types. This registry is referenced by the extraction code to

know what to compute. By deﬁning features before extraction, we guarantee

consistency and can easily track changes (adding/removing features) in version

control.

The major feature layers include:

1. Structural & Textual Features (Foundation Layer): These are

straightforward metrics about the document’s structure and formatting:

Document length in tokens, characters, and sentences.

Average sentence length (tokens per sentence).

Paragraph count (if applicable) and paragraph length distribution.

Presence of certain punctuation: e.g., counts of question marks ( ? )

indicating rhetorical questions, exclamation points indicating emotional

tone.

Quote density: how many quotations (e.g., sentences containing  "..."  or

quote HTML tags) – high quote density might indicate more factual

reporting (multiple sources quoted) or could indicate certain biases

depending on who is quoted.

Title vs body discrepancy: If we have the headline separate, features like

headline length and whether the headline contains sensational words or

clickbait phrases.

These structural features “stabilize everything else” in the sense that they often

explain variance in text independent of content – e.g., extremely short articles

or extremely long sentences can aﬀect readability and are often correlated

with certain styles (a very manipulative article might have either very short,

punchy sentences or very long, convoluted ones).

We compute these easily from the tokenized text. For example:

Python

Run

num_tokens = len(doc.tokens)

num_sentences = len(doc.sentences)

avg_sentence_length = num_tokens / num_sentences if num_sentences > 0 else 0

question_count = text.count('?')

exclamation_count = text.count('!')

quote_count = text.count('"') // 2  # roughly number of quoted segments

These become ﬁelds in the feature set (most of these are numeric scalar

features). According to our storage plan, scalar features are new columns in

the Parquet (e.g.,  avg_sentence_length  column).

2. Lexical & Vocabulary Features: These features look at the actual words

used – vocabulary richness, tone, and indicators of bias in word choice:

Type–Token Ratio (TTR): a measure of lexical diversity (unique tokens /

total tokens).

Lexical diversity indices: possibly more sophisticated measures (e.g.,

Shannon entropy of word frequency).

Rare word density: proportion of words that are uncommon (e.g., not in

top 5k common words) – some propaganda uses simple language to appeal

to masses, others use jargon.

Abstract vs concrete language: using a lexicon to classify words as

abstract or concrete and computing the ratio. Highly abstract language

could indicate more ideological content vs concrete data.

Loaded language: count of emotionally charged words (e.g., “disaster”,

“outrageous”, “brilliant”). We might have a predeﬁned lexicon of loaded

terms (or use an existing one, such as NRC emotion lexicon for

negative/positive words).

Intensiﬁers: count of words like “very”, “extremely”, “absolutely” that

amplify statements.

Absolutist terms: count of universal quantiﬁers like “always”, “never”,

“everyone”, “no one” (these often signal overgeneralization or black-and-

white framing).

Ideological lexicon usage: detect words that are known to be associated

with partisan or ideological rhetoric. For instance, terms like “liberal

agenda” or “deep state” could indicate certain biases. We may maintain

small lists of such terms and count their occurrences.

Polarizing adjectives and slanted descriptors: e.g., using “so-called”

before a term to undermine it, or adjectives like “corrupt” leader vs

“esteemed” leader can show bias.

These lexical features are critical for early bias detection because the words

chosen can reveal sentiment and bias even before analyzing deeper structure.

For example, heavy use of derogatory names (name-calling) will show up here

as well (and later in propaganda features).

Implementation-wise, many of these counts are straightforward using the token

list:

Python

Run

intensifiers = {"very", "extremely", "deeply", "highly"}

absolutes = {"always", "never", "everyone", "no one", "all", "none"}

intensifier_count = sum(1 for t in tokens if t.lower_ in intensifiers)

We also might leverage sentiment lexicons or word lists from prior research for

loaded terms. Each count can be normalized by text length to get a frequency.

3. Syntactic & Grammatical Features: These examine the grammatical

structure of sentences:

POS tag distribution: e.g., percentage of nouns, verbs, adjectives,

adverbs in the text. Unbalanced distributions might be characteristic (lots of

adjectives and adverbs can indicate opinionated or emotional content, lots

of nouns and numbers might indicate factual reporting).

Syntactic complexity: average parse tree depth, or the frequency of

subordinate clauses. Complex, convoluted sentences might indicate

obfuscation or just an academic tone; extremely simple sentences might

indicate a certain style as well.

Nominalizations: count of nominalizations (turning verbs into nouns, e.g.,

“the destruction of” instead of “destroying”). Heavy use of nominalizations

can make text abstract and impersonal.

Passive voice usage: percentage of sentences in passive voice. Passive

voice can be a way to obscure responsibility (e.g., “Mistakes were made” vs

“We made mistakes”). This can hint at bias or evasion.

Hedging and certainty: count of hedging phrases (“might”, “it is possible

that” etc.) vs strong modal verbs (“must”, “undoubtedly”). Biased content

might use fewer hedges when making strong claims, or conversely, use

certain hedges to appear cautious.

Attribution verbs: how often verbs like “claims”, “admits”, “alleges”

appear. Using “claims” instead of “says” when quoting someone, for

example, can inject doubt or bias about the quote’s veracity. This falls

under subtle linguistic bias.

Many of these require using dependency parse or POS tagging results from

earlier. For instance, to detect passive voice, we look for constructions like a

form of “to be” + past participle, or use the dependency label if available (in

spaCy,  passive  or looking for nsubjpass dependencies).

Example formula: Passive voice ratio = (count of passive sentences) / (total

sentences). If above a threshold (say > 50%), it might signal the text frequently

avoids assigning direct blame or action to agents.

Syntactic patterns can also hide propaganda: e.g., using questions to make

insinuations (“Why does [target] always do X?” is a loaded question technique).

We can ﬂag loaded questions by seeing question sentences that contain an

assumption (e.g., “why” at start and a second clause).

4. Semantic & Topic Features: Now we move to deeper semantic content:

Embeddings: We generate vector embeddings for diﬀerent text spans –

token embeddings (contextual if using BERT or static if word2vec), sentence

embeddings, and a document embedding. These embeddings (likely 768-

dimensional or similar for BERT) are not stored in Parquet (that would be

huge) – instead, we push them to the Vector DB for semantic similarity

queries. The Parquet can store references or keys to retrieve them. For

example, each document might have a vector ID that corresponds to an

embedding in the vector index. The vector DB allows us to do things like:

ﬁnd similar articles (clustering propaganda by narrative) or detect if a

sentence is very similar to known propaganda exemplars (by nearest-

neighbor search). We ensure the vector DB is updated in parallel with

Parquet so that the embedding corresponds to the same version of text.

Topic modeling or distribution: Using techniques like LDA or simply

categorizing by known keywords, assign the article a topic or a distribution

over a set of topics (politics, health, etc.). Topic can be treated as a feature

because bias often interacts with topic (e.g., political news might have

more partisan language than a sports article). If we have a predeﬁned

taxonomy of content topics, we might classify the article into those as well.

Known narrative similarity: If we have corpora of known biased

narratives, we could measure similarity. But that’s advanced; in general,

the embedding + vector DB already helps cluster narratives.

Contradiction checks (logic consistency): Using a Natural Language

Inference (NLI) model to check if any two sentences contradict each other.

For instance, the model might label pairs of sentences as entailment,

contradiction, or neutral. If we ﬁnd an internal contradiction within the

article, that’s a strong sign of either poor quality or deliberate inconsistency

(which could be a sign of manipulation). We can produce a feature like

internal_contradiction = True/False  or a count of contradictory sentence

pairs.

Headline-Body coherence: If the headline is sensational but not

supported by the body, that’s a bias tactic. We can compute similarity

between the headline and the rest of the text. For example, get embedding

for headline and for the article body; compute cosine similarity. A very low

similarity might indicate the headline is potentially misleading or oﬀ-topic

(clickbait).

Semantic coherence: Compute the semantic similarity between

consecutive sentences or paragraphs. If the article abruptly shifts topics or

has a very low coherence score, it might indicate a narrative jump or

insertion (some propagandists insert unrelated points). We could compute

an average cosine similarity between adjacent sentence embeddings;

extremely low values signal poor coherence.

Concept drift: Are there concepts introduced that don’t appear to relate

to the main topic (e.g., random mention of a diﬀerent issue)? This might be

captured by topic segmentation algorithms or unusual word occurrence.

These semantic features “power your vector DB” as noted. Essentially, we

produce the embeddings and other semantic metrics that allow cross-doc

analysis. We will use some of these in scoring, e.g., an internal contradiction

ﬂag or headline/body divergence penalty can feed the score.

5. Entity & Attribution Features: This layer focuses on who and what is

mentioned, and how:

Named Entity Recognition (NER): Identify all entities (People,

Organizations, Locations, etc.) in the text. For each entity, note its type and

the tokens comprising it. We store entities in a nested list in Parquet as

shown in the schema (text, label, position).

Entity frequency and prominence: How often is each major entity

mentioned? E.g., counting person names. Biased content might focus on a

particular entity (repeating their name many times to villainize or lionize

them).

Sentiment toward entities: For each entity, compute the sentiment of

the sentences in which they appear. This can create an entity-speciﬁc

sentiment score. If one entity is consistently mentioned with positive words

and another with negative words, it signals bias (especially if those entities

are opposing sides of an issue).

Toxicity or abusive language toward entities: Check if the context

around an entity name contains insults or hate speech (for instance, using a

hate lexicon or a toxicity classiﬁer). A toxicity score from a model like

Google’s Perspective API could be applied to sentences with the entity. If

high toxicity is directed at an entity, that suggests an ad hominem attack.

Quotation and sourcing: Determine which entities are quoted or cited as

sources versus which entities are talked about but not given a voice. For

example, count how many quotes by person A vs person B. If an article

quotes only one side of a debate, that’s a bias (we call it quote imbalance).

Attribution bias: Note verbs used for diﬀerent entities. Perhaps the article

says “Alice said...”, but “Bob claimed...” – implying doubt in Bob’s

statement. We can track verbs associated with entities and ﬂag if loaded

attribution verbs (claimed, admitted, insisted) are used mainly for a

particular entity or side.

Entity absence: Identify key stakeholders in the topic and see if any

expected entity is never mentioned (harder, requires external knowledge).

But for example, in a political story if one party is entirely not mentioned,

that omission is notable.

Power dynamics: Tag entities as elite (politicians, CEOs) vs non-elite

(general public, unnamed sources). Bias might be revealed by always

framing elites positively and ordinary people negatively or vice versa. This

is advanced, but we mention it for completeness.

All entity-level features can be aggregated. We likely produce an entity bias

summary structure for the article, capturing each major entity and some stats

(sentiment toward them, times quoted, etc.). In the Gold Parquet, this could be

a nested ﬁeld  entity_analysis  listing entities with attributes.

For example:

JSON

"entity_analysis": [

   {"entity": "Alice", "mentions": 5, "sentiment": 0.2, "quotes": 2},

   {"entity": "Bob", "mentions": 3, "sentiment": -0.5, "quotes": 0}

]

Here it appears Alice is quoted twice and Bob not at all, and Bob’s mentions

carry negative sentiment on average, hinting at bias.

6. Sentiment & Subjectivity Features: These measure the emotional tone

and objectivity of the text:

Overall Sentiment Polarity: Using a sentiment analysis model (like a

ﬁnetuned Transformer or VADER for simplicity), compute a sentiment score

from –1 (very negative) to +1 (very positive) for each sentence and

aggregate for the document. Media content is often neutral, but

propaganda might have extreme sentiment (very negative toward a target

or overly positive toward something).

Sentiment volatility: The variance or range of sentiment across

sentences. An article that swings wildly from very positive to very negative

might be using emotional manipulation or sarcasm.

Emotion categories: Using an emotion classiﬁer or lexicon (e.g., NRC

Emotion Lexicon), count words or infer the presence of emotions like anger,

fear, joy, sadness, disgust, hope, outrage, etc.. Particularly, anger and fear

frequencies are important – propaganda often appeals to these emotions.

We might produce an emotion vector, e.g., {anger: 0.3, fear: 0.4, joy: 0.1,

...} indicating relative prominence.

Subjectivity: A score or ratio of subjective sentences vs objective

sentences. We can use a subjectivity classiﬁer or a simple rule: sentences

with opinion words or ﬁrst-person might be subjective. The pipeline could

compute a subjectivity ratio = (number of subjective sentences) / (total

sentences). Highly subjective content indicates opinion or bias, whereas

factual reporting is more objective.

Assertiveness vs hedging: as mentioned earlier, how assertive are the

statements (count of “certainly”, “undoubtedly” vs “maybe”, “perhaps”).

We can derive an assertion score based on modal verbs and adverbs that

shows certainty level. A high certainty combined with low evidence is a red

ﬂag (could be assertion fallacy).

Emotional appeal ﬂags: If emotion scores are high and factual content

low, that suggests Appeal to Emotion fallacy. We can explicitly compute,

say, an “emotional appeal index” = (count of emotional words) / (count of

factual references) and set a ﬂag if above threshold.

For sentiment, we might use HuggingFace’s  distilbert-base-uncased-finetuned-

sst-2  for polarity. For emotions, perhaps a multi-class model or lexicon lookup.

Pseudocode example for emotional appeal:

Python

Run

emotion_scores = emotion_model(text)  # yields probabilities for each emotion

# Suppose it returns a dict like {"anger":0.4, "joy":0.1, "sadness":0.2, ...}

dominant_emotion = max(emotion_scores, key=emotion_scores.get)

if dominant_emotion in ["anger","fear"] and emotion_scores[dominant_emotion] > 0.5:

    flags["emotional_appeal"] = True  # strong anger/fear tone detected

This is akin to what our strategy described: if anger/fear is very high relative to

neutral, label it as an emotional appeal.

7. Framing & Narrative Features: This layer tries to capture how the story is

framed at a thematic level:

Issue frames: We check for the presence of known framing devices:

Conﬂict frame (us vs them, winners vs losers).

Human interest frame (personal stories to evoke sympathy).

Morality frame (arguments made in terms of morals or religion).

Economic frame (focus on cost/beneﬁt).

Nationalism frame (using patriotic or nationalistic rhetoric).

Victim vs oppressor narrative.

These can be detected by keywords or by more complex modeling. For

example, a conﬂict frame might be indicated by warlike metaphors or

binary oppositions. A morality frame might use words like “immoral,

righteous, duty”.

Narrative arcs: Identify if the story casts actors as heroes or villains. For

instance, check if a certain entity is consistently associated with positive

words (hero) and another with negative (villain). Also, see if the story

provides a resolution or just paints a crisis with no solution【8†L179-L187}.

Biased media might emphasize problems without resolution to incite anger.

Blame attribution: Does the article explicitly blame a person/group for a

problem consistently? If yes, it might be framing that group as the

scapegoat.

Agenda cues: If multiple articles share the same talking points or phrases,

they might be part of a coordinated narrative (but detecting that requires

cross-doc analysis).

Framing features are somewhat higher-level and might not be fully automated

without training. We might start with simple proxies: e.g., count occurrences of

words from lists associated with each frame. For conﬂict frame, words like

“battle, attack, defend, enemy”; for human interest, words like “family, child,

individual stories”; for morality, words like “sin, ethics, moral, corrupt”, etc. The

presence of a signiﬁcant number of these might tick a binary indicator for that

frame.

We also consider omission framing: not exactly framing, but bias by omission

– however, that is hard to quantify internally (it requires external reference to

what should be mentioned).

8. Rhetorical & Persuasion Techniques: This is a critical layer focusing on

classical rhetoric modes and persuasive tricks:

Ethos, Pathos, Logos: While harder to quantify directly, we can

approximate:

Ethos (credibility): Does the text rely on authority ﬁgures or personal

credentials? E.g., quoting experts (appeal to authority) is ethos-based,

but if misused it’s a fallacy.

Pathos (emotion): We have emotional appeal features already – high

pathos content.

Logos (logic): Are arguments logically structured and evidence-based?

Our argument structure analysis and factual evidence count contribute

here.

Persuasion tactics: Many overlap with fallacies (which we detail in the

next layer). Some common tactics:

Appeal to fear: already captured via emotional features.

Appeal to authority/tradition: checking if arguments lean on

“experts say” or “we’ve always done it this way” without evidence.

Whataboutism: responding to an accusation by accusing someone

else of something. We could detect this if the text structure is “X event

happened… but what about Y?” – presence of “what about” or similar

phrasing.

Slippery slope: if we see a chain of conditionals or an argument that A

will lead to Z without support.

Strawman: distort an opponent’s stance (we’ll detail in fallacies).

Name-calling/Ad hominem: use of derogatory epithets for people

(we catch via toxicity and lexicons).

Loaded questions: a question that contains an unproven assumption

(“Have you stopped wasting money?” implies you were wasting

money).

Repetition: repeating a message to drum it in (we can measure

repeated phrases or identical sentences).

This layer conceptually overlaps with the next, which is explicitly logical

fallacies. Essentially, by layer 8 and 9 we are dealing with the signature

techniques of manipulation that set this system apart. We treat them with

special focus.

9. Logical Fallacy Detection (Signature Layer): This is the marquee

feature of our system: automatically spotting logical fallacies in text. We have

prepared for this by building the argument graph and extracting various

supporting features (like causal words, quantiﬁers, etc.). We now combine those

to ﬂag speciﬁc fallacy types. Based on the taxonomy and features deﬁned in

earlier planning, we target a comprehensive list of fallacies, including but not

limited to:

Strawman Argument – misrepresenting an opponent’s stance to refute it.

Ad Hominem – attacking the person instead of the argument.

Slippery Slope – claiming a minor step will inevitably lead to an extreme

outcome without evidence.

Red Herring – diverting to another topic to distract.

Cherry Picking – selectively using evidence that supports your claim while

ignoring counter-evidence.

False Cause (Correlation != Causation) – assuming A caused B just

because A came before B or is correlated.

Equivocation – using ambiguous language or switching meaning of a term

mid-argument.

Bandwagon (Appeal to Popularity) – suggesting something is true or

good because “everyone” believes or is doing it.

Appeal to (Misused) Authority – referencing an authority ﬁgure or

expert opinion outside of its proper context or without proper evidence.

Appeal to Emotion – using emotional rhetoric to replace logical

arguments.

False Dilemma – presenting only two choices when more exist (“you’re

either with us or against us”).

Hasty Generalization – drawing a broad conclusion from a small or

unrepresentative sample.

No True Scotsman – dismissing counterexamples as invalid to uphold a

universal claim (purity test).

Burden of Proof Shift – saying the burden of proof lies not on the

claimant but on others to disprove (e.g., “prove I’m wrong”).

Circular Reasoning – conclusion is same as premise in diﬀerent words.

Loaded Question – a question that embeds an assumption (this can be

considered a fallacy too, though it’s more a rhetorical trick).

For each of these, we have devised speciﬁc detection strategies (drawing from

our “Comprehensive Strategy” document and feature design):

Strawman Detection: We look for instances where the author describes

someone’s argument or quote and then refutes it, especially if

exaggerated. Signals: use of phrases like “some say that [extreme version

of opponent argument]” or mentioning an opponent’s stance in a derisive

way. Also, comparing the “paraphrase distance” – if the text paraphrases

another argument, is it a fair paraphrase or an extreme one? We can use

semantic similarity between an opponent’s actual stated position and how

the article presents it (though actual opponent stance may not be in the

text, so this is tricky). But if we ﬁnd “straw man keywords” or clearly an

argument attributed to a vague group (“critics argue X” where X is absurd),

we ﬂag it. We set  fallacy_strawman = True  if found.

Ad Hominem Detection: Using the entity sentiment/toxicity analysis: if a

person entity is targeted by insults or highly negative language, and

especially if that appears when arguments about issues are lacking, it’s

likely an ad hominem. Example: sentences like “John Doe is an idiot and

therefore his policy is wrong.” The presence of direct insults (“idiot”)

triggers an ad hominem ﬂag. Our toxicity model on person-related

sentences can catch this. We output  fallacy_ad_hominem = True  for such

cases.

Slippery Slope Detection: We inspect causal chains. If the text has a

sequence of conditional or causal statements linking a minor event to a

catastrophic outcome (look for phrases like “if we allow A, then next there

will be B, and eventually Z”), it’s likely slippery slope. We use the argument

graph: if we have a chain of claims each leading to another with little

evidence, we mark it. Also, keywords like “without evidence” in our internal

logic – e.g., a premise “if A then B” with no evidence for that jump. The

presence of long “if... then... then...” reasoning can be ﬂagged. We produce

fallacy_slippery_slope  indicator.

Red Herring Detection: Look for sudden topic shifts. If our topic modeling

shows an oﬀ-topic paragraph (e.g., an article about economy suddenly has

a paragraph about a politician’s personal life with no connection), that

could be a red herring diversion. Also rhetorical cues like “By the way, ...”

or “Interestingly, ...” then discussing something else. Hard to automate

fully, but big drops in semantic coherence between adjacent paragraphs

might hint at this. We might ﬂag if a late paragraph has a totally new topic

distribution. We label  fallacy_red_herring  if so.

Cherry Picking Detection: This is partly covered by evidence counting. If

the article makes a claim that should be backed by evidence but provides

only one side of evidence or only one example, it’s cherry-picking. Also if

external data says there’s contradictory evidence not mentioned (hard

unless we compare sources). Internally, we measure evidence count per

claim and diversity of sources. If a claim has zero or very few pieces of

evidence, or if all evidence cited supports one side and none acknowledges

the other, that’s a sign. We create a metric like  evidence_support_ratio .

Cherry-picking might be ﬂagged if (number of supporting evidence >=1

and number of opposing/reference evidence = 0 when normally there

should be some). We set  fallacy_cherry_picking = True  in such cases.

False Cause Detection: Use our causal analysis features. If there’s

temporal language linking events (“after X, Y happened”) without a causal

explanation, or correlation words (“coincided with”), or explicit causal

claims without evidence (“X caused Y” but no backing), ﬂag it. Our system

can ﬁnd phrases “because of X, Y” – if many such claims appear without

robust evidence, false cause is possible. Also look for post hoc ergo propter

hoc (after this, therefore because of this) situations by checking if the only

reason given for a claim is that something came earlier in time. We output

fallacy_false_cause  if triggered.

Equivocation Detection: Detect if a word is used in two diﬀerent senses.

This one is tricky automatically. Perhaps track if the same word appears

with diﬀerent meanings (requires either Word Sense Disambiguation or

noticing if an uncommon meaning is used later). For example, the word

“law” used as “natural law” vs “law (legal)” in an argument could confuse

things. Full automation is beyond scope, but we can attempt to catch

obvious cases: e.g., repeated phrases in quotes implying sarcasm or

changed meaning. We might not have a strong implementation, but we

include a placeholder for  fallacy_equivocation .

Bandwagon Detection: This we can do quite directly with lexicon of

group/allusion terms. Count phrases like “everyone says”, “most people

believe”, “the majority”, “all of us” etc. We did something similar in earlier

lexical features (absolutist terms). If the frequency of such inclusive terms

is high relative to text length, that suggests an appeal to popularity

(bandwagon). For instance, we deﬁne  bandwagon_score =

count_bandwagon_phrases / num_tokens . If  bandwagon_score > threshold  (say

0.01), we set  fallacy_bandwagon = True . Pseudo-code example:

Python

Run

bandwagon_terms = ["everyone", "everybody", "all of us", "most people", "the majority"]

count = sum(1 for token in tokens if token.lower_ in bandwagon_terms)

bandwagon_score = count / len(tokens)

if bandwagon_score > 0.001:

    flags["bandwagon_effect"] = True  # bandwagon fallacy detected

This matches the approach described in the strategy. We store the ﬂag and

possibly the score itself.

Appeal to Authority Misuse: Using NER, we ﬁnd occurrences of authority

ﬁgures (like titles “Dr. X”, “Professor Y”, or generic “experts”, “scientists

say”). Then check the context: is it accompanied by an actual evidence or

just taken as truth? If we see phrases like “According to [Person], ...” or “…,

experts agree.”, that’s an authority appeal. Not all authority appeals are

fallacious (experts are often right), but if it’s used in lieu of evidence or

outside their expertise, it is. We might not verify the domain expertise

automatically, but we can ﬂag generic appeals: e.g., content heavily relying

on “experts say” without citing speciﬁcs. Pseudocode approach given in the

strategy is:

Python

for ent in doc.ents:

Run

    if ent.label_ == "PERSON" and ent._.has_title:  # person with title like Dr.

        window = doc[max(0, ent.start-3): min(len(doc), ent.end+10)]

        if re.search(r"\b(said|claims?|according to)\b", window.text, re.IGNORECASE):

            authority_references.append(window.text)

if len(authority_references) > 0:

    flags["authority_misuse"] = True

. We implement similar logic. So output  fallacy_authority_misuse = True  if

triggered.

Appeal to Emotion: We largely covered this – if the emotional tone is

disproportionate and replacing factual arguments, we mark it. For example,

if an article is extremely fear-inducing about an issue without providing

factual evidence, it’s an appeal to fear. We already have

flags["emotional_appeal"]  from sentiment features possibly. We

incorporate that into fallacies:  fallacy_appeal_to_emotion = True  if

triggered.

False Dilemma: Identify binary choices. Typical phrases: “either X or Y”,

“no alternative”, “the only way”. We parse for “either/or” constructions.

Also, if the argument structure contains exactly two options presented for a

complex issue, that’s suspicious. We can ﬂag if “either” and “or” appear in

proximity, or the phrase “the only option”. We set  fallacy_false_dilemma =

True  if found.

Hasty Generalization: We check for words like “all”, “never”, and if a

general claim is made right after a single example. For instance, “This one

case happened, therefore it always happens.” If an absolute term (from our

lexical features) is used but we detect only an anecdote as evidence, that’s

a sign. Also, short pieces that leap to broad conclusions. If  absolute_count  is

high and evidence count low, we ﬂag  fallacy_hasty_generalization .

No True Scotsman: Hard to detect automatically, but clues are when

counter-examples are redeﬁned out. Look for phrases like “no real X would

do Y”. For example, “No true patriot would criticize the war” – implies those

who do are not patriots. We could have a small list of such constructs to

search for (the phrase “no true [group]”). If found,  fallacy_no_true_scotsman

= True .

Burden of Proof Shift: Phrases like “can you prove that I’m wrong?” or

“nobody has proven X false, so it’s true” are indicative. We search for

“prove” and context of challenges. If found,  fallacy_burden_shift = True .

Circular Reasoning: Using the argument graph, detect cycles or

repetition. If the conclusion is identical or nearly identical to a premise,

that’s circular. E.g., conclusion sentence and some premise sentence have

very high similarity (or one references the other). We can measure if the

main claim appears paraphrased in supporting sentences. If yes,

fallacy_circular_reasoning = True .

Each detected fallacy will be recorded with:

Type: e.g., "slippery_slope"

Text span or sentence where it occurs (to highlight it in output).

Conﬁdence/score: if applicable. Many of our detectors are rule-based (so

essentially binary ﬂag with implicit conﬁdence). If we use an ML classiﬁer

for any, we would output a probability. For example, if we had a BERT

model trained to detect propaganda techniques, it might output a

probability for each technique; we’d set a threshold to convert to ﬂag and

also keep the probability as intensity.

We ensure these fallacy features are binary indicators + intensity scores

as needed. They become part of the document’s feature set. For instance, we

may have a struct  fallacies  listing each fallacy found, or simply columns like

has_strawman ,  has_ad_hominem , etc., and perhaps a count of total fallacies.

10. Factuality & Evidence Features: While not purely fallacies, these are

closely related – checking the truthfulness and evidence basis of content:

Presence of Factual Claims: We detect sentences that make veriﬁable

factual claims (e.g., containing numbers, dates, names). If none are

present in an ostensibly factual article, that’s odd.

Use of Numbers and Statistics: Count how many numbers or statistics

are present. A lack of concrete data could indicate a more opinion-based

piece; conversely, misuse can occur even if data is present.

Cited Sources: Check for references or citations (URLs, or “According to

[source]”) – if absolutely no external source is cited for factual claims, it

might be suspicious. Conversely, if many sources are cited, that can add

credibility.

Fact Density: Ratio of factual statements to opinion statements. We might

simply count numbers, proper nouns, etc., as a proxy for factual content.

Claim Speciﬁcity: Are claims speciﬁc (with concrete details like dates,

names) or vague (“some people in a European country” vs “5,000 people in

France on July 14”)? We might measure speciﬁcity by the presence of

proper nouns and numbers in claims. Low speciﬁcity combined with high

certainty can indicate deception.

Unveriﬁable Claims: Phrases like “experts say” (without naming), “it is

known that…”, “many people are saying…” – these are hard for a reader to

verify and are often used to spread rumors. We ﬂag such patterns.

Quantiﬁer misuse: Using terms like “millions” or “a few” without context

or basis. We check if quantiﬁers are attached to actual data or just thrown

in (e.g., "many people think..." with no source).

Clickbait indicators: If analyzing headlines, check for clickbait patterns

(exaggeration, question headlines, etc.).

Additionally:

Numerical consistency: If numbers are given, check if they contradict

each other (e.g., population in one sentence 5 million, another sentence 10

million). We can cross-scan all numbers in the text for obvious conﬂicts or

use NLI on numeric statements.

Percentage sum check: If percentages are cited (like polls or

breakdowns) do they sum to ~100% when expected?.

Outlier detection: If a number cited is wildly out of expected range (e.g.,

claiming 120% of people support something), ﬂag it.

Data omission/manipulation cues: Some are subtle, like “cherry-picked

stats” we covered, or “up 300%” without stating baseline. If we see phrases

like “X increased by 300%”, check if baseline is mentioned; if not, that’s

misleading. Also mention of “record high” or “unprecedented” without

context could be ﬂagged.

We incorporate these into a factuality score or a set of ﬂags:

e.g.,  has_unverifiable_claims ,  has_statistical_misuse , etc.

Possibly an overall factual reliability score: starting from 1.0 and deducting

points for each issue found (this could be part of scoring matrix later).

11. Temporal & Contextual Features: These relate to how the article uses

time and context:

Event timeline consistency: Does the article maintain chronological

order, or does it distort sequence for narrative? If we have timestamps in

content (e.g. “In 2010… later in 2005…” – that’s out of order, might

confuse readers).

Selective history: Does it omit relevant historical context? Hard to

measure, but we can note if it references past events or not. An absence of

historical context for a topic that typically needs it might be a clue (though

that’s more a journalism quality measure).

Repetition cycles: If the same message or slogan is repeated periodically

(could be more cross-document though).

Context omissions: Check if known crucial context is missing – e.g., an

article about a policy might not mention a known criticism. This requires

external knowledge to detect (maybe out of scope here, but a note).

Temporal features we can implement:

If  published_date  (from metadata) and the content references events far

from that date, note if those events are used properly. Or if it uses present

tense for something that happened long ago, that’s odd.

Narrative shift events: when the discourse marker indicates a shift (like

“however”, “meanwhile”), do we see a context change? We capture

discourse markers as features (count of words like “however”, “although”).

They often indicate contrasts or topic shifts – not necessarily a fallacy, but

high usage might indicate sophisticated argumentation or potential

confusion.

12. Cross-Document & Network Features: (These might be more

advanced and need external data or multiple articles):

Source comparison: If we have multiple sources reporting the same

event, how does this source’s language diﬀer? (For now, we may not

implement, but design allows it).

Narrative consistency across articles: If analyzing a network of

articles, see if this article uses language unique to a certain group.

Propaganda network signals: e.g., certain phrases or hashtags reused

(this is more for social media).

Source clustering: Position this article’s language in embedding space

relative to known left-leaning vs right-leaning vs center sources – see if

language is closer to one extreme cluster.

Though we won’t implement cross-document analysis initially, we structure the

pipeline so that such features can be added (e.g., by a batch job that after

processing many articles, computes network metrics and appends them to the

Gold records). Phase 3 of feature development includes such “elite” features

like narrative networks and temporal drift across sources.

13. Metadata & Provenance Features: We also incorporate any metadata

we have about the content source to enrich analysis:

Outlet information: If we know the publisher or outlet, we can join with

external data about that outlet’s bias or reliability rating. For instance,

MediaBiasFactCheck might have a rating for some domains. We could

include ﬁelds like  source_bias_rating  (e.g., lean left, center, lean right),

source_reliability_score  if available.

Author information: If known, perhaps track if an author is known for a

certain angle (maybe beyond scope unless we have data).

Publication context: Region or country of publication (if given), which

might inﬂuence perspective.

Social media traction: If we have  number_of_shares  or trending info,

that’s interesting but not directly a bias measure (though some use

popularity as “truth” – which is a bandwagon fallacy itself).

Network features: if the article is part of a coordinated network, e.g.,

same talking points as others, but again needs cross-doc analysis.

These metadata features amplify text signals (they provide context that might

explain certain biases). For example, an outlet with known extreme bias likely

inﬂuences how we interpret high sentiment scores.

We incorporate relevant metadata ﬁelds into our schema and ﬁll them either

from ingestion or external lookup.

Feature Storage and Schema: As features are extracted, they are stored in

the Gold Parquet. We follow a strategy:

Scalar features (single values like counts or scores) become new columns

in the Parquet (eﬃciently stored due to columnar format).

List features (like list of tokens, list of sentences) are stored as nested

arrays or separate structures within Parquet.

Structured features (like entities or argument graph) are stored as

nested structs within the record.

Embedding vectors are not stored in Parquet beyond maybe an ID; they

go to the vector DB for specialized retrieval. The Parquet might have a ﬁeld

like  embedding_vector_id  referencing the vector DB entry.

Scores (like ﬁnal scores or major metric outputs) can be stored and

versioned in Parquet as well. We may keep a separate score table or

include them in Gold.

This structured approach means the Gold dataset is quite rich. An advantage of

Parquet is we can select only needed columns when reading – so if we want to

run an analysis only on sentiment and bias scores, we don’t have to read the

heavy text or entity lists.

We also version the feature set deﬁnition. The YAML feature registry ﬁle

deﬁnes all features (like  avg_sentence_length: float ,  fallacy_strawman: bool ,

etc.). When we update features, we bump a  feature_version . The pipeline

attaches  feature_version  metadata so we know which deﬁnition was used for a

given record. This ensures traceability: if a score changed because we tweaked

how a feature is calculated, we can trace it.

Build Order and Phases: We prioritized implementing certain features ﬁrst

(Phase 1: must-haves) vs later (Phase 2: diﬀerentiators, Phase 3: advanced). In

Phase 1, we focus on core structural, lexical, entity, sentiment, and embeddings

– these cover the basics needed for any analysis. Phase 2 adds the more

complex narrative, rhetoric, fallacy, and attribution features, which truly

distinguish our system in detecting manipulation. Phase 3 would incorporate

cross-source and temporal network analysis for a research-grade solution. This

phased approach was recommended to ensure we deliver a working MVP

quickly, then enhance it.

Now that we have extracted a myriad of features and ﬂags, the pipeline moves

to classify and score the content using these features. Next, we describe how

we map the content into a taxonomy of categories and aggregate all signals

into a ﬁnal scoring matrix that quantiﬁes bias and fallaciousness.

Taxonomy Classiﬁcation and Content Scoring Matrix

At this stage, the pipeline has a rich set of features and detected signals for

each article. We now perform taxonomy-driven classiﬁcation to label the

content according to predeﬁned categories, and then compute composite

scores. This step is crucial for summarizing the analysis in a way that end users

(analysts, or the front-end application) can easily interpret, and it leverages a

controlled vocabulary (taxonomy) to describe ﬁndings.

Predeﬁned Taxonomy of Categories: The project deﬁnes a taxonomy

which could encompass:

Types of rhetoric or propaganda techniques (e.g., categories like “Fear-

mongering”, “Appeal to Authority”, “Disinformation”, “Personal Attack”,

etc.).

Bias categories (e.g., “Political Bias: Left”, “Political Bias: Right”, “Clickbait”,

“Satire”, etc., depending on scope).

Topical categories if needed (though that’s more classiﬁcation of topic,

which is separate from bias – likely our taxonomy is more about forms of

manipulation).

From the Data Engineer’s responsibilities, the taxonomy refers to mapping

content segments to predeﬁned labels as per internal guidelines. It sounds like

each sentence or content piece might be classiﬁed into one or more labels

from this taxonomy. Perhaps the taxonomy includes various fallacy/technique

labels (bandwagon, ad hominem, etc.) as well as maybe thematic labels like

types of bias (spin, propaganda, error).

For implementation:

We use the outputs of our detectors (the ﬂags and features from previous

section) as inputs to this classiﬁcation. For instance, if

fallacy_ad_hominem=True  and  toxicity_toward_entity  is high, the taxonomy

label “Ad Hominem Attack” should deﬁnitely be assigned. Some cases

might be fuzzier, where we have a continuous score or multiple signals.

We can create a rule-based mapping: e.g., if these signals, assign this label.

This is deterministic and traceable (preferred for reproducibility).

We could also train an ML classiﬁer that reads all feature values and

outputs one or multiple labels (multi-label classiﬁcation). But given our

emphasis on determinism, a rule-based or at least human-interpretable

logic is preferable.

For example, our taxonomy might have an entry for “Misleading Use of

Data” – we would deﬁne: if  fallacy_false_cause  or  statistical_misuse_flag  or

outlier_flag  is true, then mark that category. Or an entry “Emotionally

Manipulative” – if  fallacy_appeal_to_emotion  or  sentiment_extremes  are

present, mark that.

Additionally, taxonomy could include severity or combination labels. For

instance, if something triggers multiple fallacies, it might be labeled as “Highly

Manipulative” vs if just one minor issue, “Slight Spin”.

We ensure the taxonomy and the mapping logic are documented (likely in the

YAML registry or a separate conﬁg) and versioned ( taxonomy_version ). This

allows evolving the categories over time.

Sentence vs Document Classiﬁcation: Possibly, we might classify at the

sentence level ﬁrst, then aggregate to the document. For example, label each

sentence with any fallacy present: Sentence 3 = Ad Hominem, Sentence 5 =

Strawman, etc. Then at document-level, compile that into an array of labels

present in the whole piece. The Data Engineer likely manages updating

taxonomy deﬁnitions as project evolves.

Integration of Taxonomy Stage: In the pipeline, after features are

extracted, we pass the data through a Taxonomy Engine (which could be a

module or simply part of our code). It reads the feature ﬂags and decides on

labels:

E.g., create a set  labels = {} .

If  has_strawman  true, add label "Strawman Argument".

If  has_ad_hominem  true, add "Ad Hominem Attack".

If  bandwagon_score  above threshold, add "Bandwagon Appeal".

If many emotional words, add "Emotional Appeal".

If quotes are one-sided, maybe add "One-sided Sourcing".

If no counter-argument, add "Lacks Counterargument".

And so on, covering all relevant categories we want to present. This yields a list

of labels for the content.

These labels could also be organized hierarchically if the taxonomy is

hierarchical (e.g., broad category "Logical Fallacy" with subcategory

"Strawman"). But likely it’s a ﬂat list or a few top-level categories.

Scoring Matrix Construction: Alongside categorical labels, the pipeline

computes quantitative scores/metrics that summarize the degree of

manipulation or bias. The “scoring matrix” mentioned in Data Engineer’s role

likely refers to a set of numeric scores the team deﬁned internally. Without

revealing proprietary logic, we can describe it in general:

We might have multiple score dimensions, for example:

Overall Bias Score: A single score from, say, 0 to 1 (or 0–100) indicating

overall bias/manipulation level. 0 could mean completely neutral, factual

reporting; 1 means extremely biased/manipulative.

Subscores by category: e.g., Logical Fallacy Score, Emotional Tone

Score, Source Credibility Score, etc. Or possibly Left vs Right bias score if

we measure political leaning (less likely unless we speciﬁcally model that).

Credibility Score: Inverse of how many issues found; a high credibility

score if no fallacies or biases were detected, low if many were.

Sentiment Bias Score: maybe measuring if sentiment is heavily skewed

(like one side always positive, other negative).

etc.

The scoring logic likely takes into account multiple feature values. For

determinism, it might be a linear combination or rule-based sum. For example:

\text{ManipulationIndex} = w_1 \cdot \text{num_fallacies} + w_2 \cdot

\text{sentiment_variance} + w_3 \cdot (1 - \text{source_credibility}) + \dots

with weights chosen per internal calibration. Or even simpler, an additive

system:

Start at 0.

Add points for each fallacy: e.g., +10 for a major fallacy, +5 for a minor

one.

Add points if subjectivity > threshold.

Subtract points if multiple perspectives presented (a sign of balance).

etc.

Result could be scaled to 0–100.

We ensure that any such formula is documented and part of conﬁguration so

that it’s traceable (and testable). The Data Engineer and team can adjust these

weights or thresholds as needed, but each change is a new version of scoring

logic.

Example of Score Calculation (Hypothetical):

Let  F  = number of distinct fallacy types detected (or weighted count if

some are worse).

Let  E  = emotional appeal ﬂag (1 if present, 0 if not).

Let  B  = bias indicators count (like number of biased words, scaled).

Deﬁne an Overall Bias Score:
BiasScore = tanh(a ⋅ F + b ⋅ E + c ⋅ B)
(using tanh to squash to 0-1, where a, b, c are tuned constants).

Meanwhile, a Credibility Score could be $1 - \text{BiasScore}$ or

something similar.

This is just illustrative. The actual scoring matrix could be a matrix where each

row is a content piece and each column is a speciﬁc metric. For instance:

Column1: BiasScore,

Column2: FactualityScore,

Column3: EmotionalIntensity,

Column4: LogicalSoundness,

etc.

Because it’s matrix-like, we might store it in a separate table or attach to each

document record as a subﬁeld  scores: {bias: X, factuality: Y, ...} .

From the roles: the Data Engineer ensures the scoring matrix logic is

deterministic and documented, and the Lead Engineer ensures the output is

well-structured JSON so that these scores and labels appear in output clearly.

Testing and Adjusting: The QA tester will have speciﬁc test cases for scoring:

They might feed a clearly neutral article and expect a low bias score.

Feed a known biased op-ed and expect a high score.

They also verify that running the same article twice yields exactly the same

score (no randomness).

If any change in features or weights occurs, QA will regression-test previous

examples to see how scores shift, ensuring changes are intended.

Example Pseudocode for Taxonomy & Scoring:

Run

Python

labels = []

score = 0

# Rule-based classification

if flags["ad_hominem"]:

    labels.append("Ad Hominem Attack"); score += 10

if flags["strawman"]:

    labels.append("Strawman Argument"); score += 8

if flags["bandwagon_effect"]:

    labels.append("Bandwagon Appeal"); score += 5

if flags["emotional_appeal"]:

    labels.append("Emotional Appeal"); score += 5

# ... (and so on for all fallacies and bias types)

# Maybe also positive points if evidence of balance:

if features["counterargument_present"]:

    score -= 5  # reduce score because it’s more balanced

# Normalize score to 0-100

bias_score = min(100, max(0, score))

# Could also create categories like:

if bias_score > 80:

    labels.append("Highly Manipulative")

elif bias_score > 50:

    labels.append("Some Bias")

# The output structure

result = {

   "labels": labels,

   "scores": {"bias_score": bias_score}

}

This pseudocode demonstrates how labels might be assigned and a simplistic

score tallied. The actual logic might be more nuanced, but the principle is that it

is transparent and tunable.

Using the Taxonomy and Scores: These outputs inform end-users of the

system. For instance, the front-end could show: Labels: Ad Hominem, Cherry-

Picking, Emotional Appeal. And perhaps an overall bias meter at, say, 70/100.

The taxonomy labels also help drive what explanations to show (each label

corresponds to an explanation of that fallacy or bias type, educating users).

Internally, taxonomy also helps in development: it gives us a checklist of

techniques to ensure our detectors cover, and a structure to log how often

each type is found.

Finally, after classiﬁcation and scoring, the enriched results are stored and then

served via the backend API. We next describe how the backend prepares and

delivers this output, as well as infrastructure aspects like database and

deployment, followed by the testing regimen that keeps all these moving parts

reliable.

Backend Integration and Serving the Results

Once each document has been processed through the NLP pipeline (up to

computing labels and scores), the results need to be stored in a form that the

backend API can retrieve and provide to end-users or other systems. We

design the serving and integration with the following principles: structured

output, low-latency retrieval, secure and scalable serving, and

traceability (each result tied to a version and logs).

Gold Data to Serving DB: The Gold zone data (with features, labels, scores)

is written to a serving database for quick query. A relational database (SQL) is

often convenient for this, since we can query by document ID, date, etc., and

even do analytical queries. We could use PostgreSQL or similar to store ﬁnal

results (or an Elasticsearch index if search is needed). According to our pipeline

chart, we use a SQL serving DB at the end. This DB might have tables like:

ArticleAnalysis  with columns:  doc_id ,  bias_score ,  labels  (maybe as a

JSON array), etc., and possibly references to detailed tables.

ArticleSegments  with highlights: e.g., each fallacy instance or noteworthy

segment as a row (doc_id, sentence_num, text_span, label, conﬁdence).

We could also store the full JSON output in a JSONB column for ﬂexibility.

Alternatively, we might not need an extra DB if the Parquet Gold can be queried

directly by the API, but for production, a DB is easier for concurrent API calls

and updates.

RESTful API Design: The Backend Engineer will implement RESTful endpoints

to allow clients (like the front-end UI) to request analysis results. Key endpoints

could be:

POST /analyze  – Accept raw content (or URL) as input, run it through the

pipeline (or queue it for processing), then return the analysis result.

However, since our pipeline is heavy, we might not run synchronously on

demand, but rather pre-process content behind the scenes.

GET /analysis/{doc_id}  – Retrieve the analysis JSON for a previously

processed document. This would fetch from the serving DB.

GET /highlight/{doc_id}  – Possibly returns just highlighted text segments

and tags for front-end rendering.

Given the conﬁdentiality and controlled usage (NDA project), we might not

expose it publicly, but within the team or as an internal tool.

Structured JSON Output: The output JSON is structured for front-end

consumption, matching what the backend returns. It likely includes:

Original text (or maybe not needed if front-end already has it).

A list of highlighted segments with tags: e.g.,  [{ "text": "John Doe is an

idiot", "label": "Ad Hominem", "start": 100, "end": 119 }, ...] .

Document-level labels detected (the taxonomy labels).

Scores (overall and possibly per category).

Possibly, a breakdown or explanation for each label (the UI could have

static explanations keyed by label).

Metadata like document ID, analysis timestamp, pipeline version.

For example:

JSON

{

  "doc_id": "12345",

  "bias_score": 72,

  "labels": ["Ad Hominem Attack", "Cherry Picking", "Emotional Appeal"],

  "segments": [

     { "text": "John Doe is an idiot", "label": "Ad Hominem Attack", "start": 256, "end":

     { "text": "everyone knows that...", "label": "Bandwagon Appeal", "start": 310, "end"

  ],

  "metadata":

Production-Ready NLP Pipeline for Media/News
Analysis

This report presents a comprehensive blueprint for an NLP pipeline designed

to analyze media/news content for bias, rhetorical fallacies, and manipulation

techniques. It integrates best practices from data engineering, NLP,

backend development, QA/testing, and DevOps to ensure the system is

scalable, deterministic, and production-ready. We will walk through every

stage of the pipeline – from data ingestion (Bronze layer) to feature extraction

(Silver/Gold layers) to model inference and serving – explaining the

responsibilities of each component and how they connect. Emphasis is placed

on structured data formats (JSON/Parquet)【12†L480-L487】, a ron

architecture, taxonomy-driven classiﬁcation, a custom scoring matrix, and

end-to-end versioning and testing for reproducibility【4†L61-L68】【1†L19-

L27】. Pseudocode snippets and formulas are included to clarify the logic at

critical steps. By the end, you will have a clear blueprint of how to build, deploy,

and maintain this NLP system in a real-world environment.

System Arcdallion Data Pipeline)

At a high level, the pipeline follows a medallion architecture with distinct data

“zones” for proginement of content. We deﬁne three primary layers in a cloud

data lake, each stored in an Apache Parquet format for eﬃciency【12†L480-

L487】:

Bronze (Raw Ingestion) – Raw data with minimal parsing (original text +

basic metadata).

Silver (Cleaned Data) – Normalized, enriched text data (clean text,

language info, etc.).

Gold (Features & Scores) – Fully processed data with extracted features,

fallacy ﬂnal scores.

Each zone uses Parquet with a consistent schema but increasing data quality

guarantees (raw vs. cleaned vs. enriched)【29†L3-L11】. By sepae ensure

maintainability and traceability: raw inputs are preserved for auditing, and

each transformation stage produces a new dataset with versioned records

(including  pipeline_version  and timestamps) for reproducibility【32†L5-L13】.

Pipeline Flow: The diagram below outlines the modules and data ﬂow:

Sources: Content is collected from various sources – e.g. news APIs, RSS

feeds, web scrapers, PDF documents, audio transcripts, or message

streams. This covers everything from plain text ﬁles to social media APIs

and even audio/video (after speech-to-text)【10†L12-L20】【10†L257-

L265】.

Ingestion Layer: A distributed ingestion process (using Spark or Ray for

batch, and Kafka for streams) reads the sources and converts them into a

standardized JSONL (newline-delimited JSON) format【10†L105-L113】

【10†L123-L131】. Each line in JSONL represents one document with basic

metadata. JSONL is chosen for intake because it’s streaming-friendly and

“one document per line” ﬁts well with message queues and quick

debugging【10†L125-L133】. The ingestion layer attaches initial metadata

(source, timestamp, etc.) and ensures the data is ready for the pipeline.

Bronze Storage: The raw documents are then stored in the Bronze

Parquet dataset, essentially an append-only data lake table containing

ﬁelds like  doc_id ,  source_type , raw text, and any source-provided

metadata. At this stage, processing is minimal – we may strip out binary

data, but largely it’s the original content plus a unique ID and ingest

metadata【27†】. Storing raw content ensures we never lose

information and can re-process from scratch if needed (a key part of

reproducibility and auditability).

Preprocessing & Normalization: Next, a preprocessing module takes

Bronze data and performs cleaning and normalization tasks. This includes

removing or converting HTML markup, normalizing Unicode characters and

whitespace, standardizing punctuation, and maybe lowercasing (depending

on analysis needs). It also involves language detection if multilingual

content is possible (to route text to the correct language-speciﬁc models or

stopwords). We also segment the text into paragraphs and sentences at

this stage【4†L15-L23】. The output of this stage is clean text ready for

NLP analysis. We enrich the metadata with language code, content length,

etc., and store the results in the Silver Parquet table as new columns

(e.g., a  clean_text  ﬁeld alongside the raw text)【27†】.

Tokenization & Linguistic Annotation: Using an NLP library like spaCy or

NLTK【4†L37-L45】, each cleaned document is tokenized into sentences

and tokens. We attach linguistic features to tokens: e.g., part-of-speech tag,

lemma, whether it’s a stopword, and any named entity recognition (NER)

labels【21†】. For example, for each token t, we record alike POS(t),

lemma(t), is_stopword(t), NER(t)【22†】. Each sentence is also annotated

(e.g., sentence length, its text content). This information canin structured

ﬁelds (lists of tokens, list of sentences) within the Silver layer. Parquet’s

support for nested columns allows storing token lists or entity lists

e9†L314-L322】 (e.g., an  entities  array of structs with entity text, type, p

this point, we have a fully canonical representation of the text:

oricleaned text, and base linguistic structures, all under a consistent

schema for et【39†L379-L387】【39†L397-L405】.

Argument Mining (Claims & Premises): Before diving into advanced

features, the pipeline reconstructs the argument structure ot. This step

identiﬁes claims, premises, and conclusions in the text – thof any

argument. We use a mix of rule-based cues and ML models (argument

miners) to detect sentences that pres claim* (e.g., thesis statements or

conclusions) versus those providing premises/evidence【7†L4-L12】

【7†L94-L102】. We also look for argument indicators: discourse markers

like “because”, “therefore” indicating causal reasoning【7†L36-L44】, or

phrases signaling conclusions (e.g., “in summary”, “thus it follows”). The

output is an Argument Graph representing relationships: whichattack

which claims. This graph can be stored as nested structures in Parquet or in

a graph database (optional)【31†L11-L19】. For each document, we now

know its argumentative skeleton: how ideected logically. This is crucial for

fallacy detection, since many fallacies involve breaking the logical links or

misusing them (eing a non sequitur requires knowing the

premise→conclusion structure)【7†L28-L36】【7†L16-L24】.

Feature Extraction (Gold Layer): This is the core intelligence of the

pipeline. We compute a broad set of NLP features across multiple “layers”,

incrementally building up signals of bias or manipulation. Our design follows

a layered approach【8†L2-L11】 – starting from fundamental textual

features and moving toward high-level semantic anl features. All extracted

features are stored in the Gold Parquet dataset, which extends the

schema with numerous feature columns and score ﬁelds. Key feature

layers include:

1.  Textual & Structural Features: Basic stats about the document’s

structure【8†L10-L18】. For example: document length in

tokens/characters, number of sentences, average sentence length

【8†L10-L18】【8†L26-L34】, paragraph count, presence of certain

punctuation patterns (e.g., how many questions or exclamation marks).

Strrks can hint at manipulative tone【8†L32-L39】 – e.g., a very high

exclamation mark density might indicate emotional content. We also

note formatting cues like quote density (percentage of text in quotes)

or headline vs. body diﬀerenceing news articles. These features lay

the groundwork and are easy to verify.

2.  Lexical & Vocabulary Features: Metrics about the words used

【8†L39-L47】. We calculate vocabulary richness (ratio), lexical

diversity, and the frequency of rare words or jargon. We speciﬁcally

scan for *loade – emotionally charged or ideologically slanted terms

【8†L49-L57】. This includes lists of intensiﬁers (“very, extremely,

deeply”), absolutist terms (“always, never,】, and polarizing

adjectives that might indicate bias. For example, a high count of words

from an ideological lexicon (say, strong political buzzwords) early on

can ﬂag potential bias in framing【8†L58-L66】. act as early indicators

of content that is strongly opinionated or propagandistic.

3.  Syntactic & Grammatical Features: How the sentences are

constructed grammatically【8†L69-L77】. We analyze part-of-speech

(POS) tag distributions (e.g., % of adjectives or adverbs), dependency

parse patterns, and use of passive voice. High passive voice frequency

might suggest attempts to hide agency or responsibility in statements

(a known technique in biased writing)【6†L167-L175】【6†L169-L177】.

We also capture nominalizations (turning verbs into nouns, which can

obscure who’s doing what) and specs like hedging language (“it

seems”, “possibly”) or certainty modals (“must”, “undeniably”)【8†L79-

L87】. These features require parsing each sentence’s grammatical

structure. For example, we may compute the ratio of passive to active

constructions for each document. If  passive_count  is the number of

passive sentences and  total_sentences  the total, we deﬁne a passivity

score =  passive_count / total_sentences . A high passivity score might

raise a ﬂag for responsibility evasion tactics.

4.  Semantic & Thematic Features: Higher-level meaning

representations【8†L89-L97】. We generate embeddings for

sentences, paragraphs, or the whole document using a transformer

model (e.g., a pre-trained BERT or Sentence-BERT). These embeddings

capture the content’s semantic context. They are stored separately in a
Vectord later) for similarity search【12†L397-L405】.

Additionally, we infer topic distributions (using LDA or similar

topic models) to see the major themes of the document
【8†L98-L106】【8†L100-L108】. We also check for semantic

similarity between sections – e.g., does the headline align with

the body contenttions? A glaring headline–body mismatch

(headline says one thing, body another) is a sign of potential
manipulation or clickbait【8†L108-L115】. We might also pural

Language Inference (NLI) on statements to detect internal

contradictions (this uses an ML model to check if one sentence entails

or contradicts another). For instance, if claims X and another later says

not X, an NLI model would catch a contradiction with a high probability

【41†L83-L90】. Semantic features are the bridge to understanding

what the text is rent.

5.  Entity & Attribution Features: Detailed analysis of named entities

(people, organizations, groups, etc.) mentioned【8†L115-L123】

【8†L127-L135】. Using NER, we extract all entities and then assess

how they aroted or cited? Who is positively or negatively portrayed? An

important bias indicator is quote imbalance – e.g., if an article quotes

only sources from one side of an issue and ignore【6†L109-L117】

【6†L111-L118】. We also track sentiment per entity: for each

person or org, we aggregate sentiment of the sentences mentioning

them【6†L101-L109】【41†L115-L123】. Consistentlyne party vs.

positive framing of another can signal bias (this is akin to entity-level

sentiment bias). We examine attribution verbs around entities (“X

claims that...”, “Y admitted...”)【8†L81-L89】 – certain verbs carry

bias (e.g., “claimed” vs. neutral “said”). We identify power dynamics:

are only oﬃcials quoted, or also ordinary people? How are elites vs.

non-elites mentioned【8†L133-L141】? These features require linking

entities with linguistic context. For example, we might maintain a

dictionary  entity_sentiments  mapping each entif sentiment scores from

sentences about them, then compute average sentiment per entity and

compare【41†L127-L135】. If “EntityA” has average sent –0.5 (on a

polarity scale), that disparity is noted as potential partisan bias.

6.  Sentiment & Emotion Features: Overall sentiment polarity and

emotio6†L113-L121】【8†L143-L152】. We apply a sentiment analysis

model to each sentence (or an emotion classiﬁer tha, fear, anger). This

yields a sentiment score in [−1,1] for negativity/positivity and possibly a

subjectivity score【6†L119-L127】. We aggregate these per document

(e.g., average sentiment). We also speciﬁcally detect **gh frequency of

words indicating fear, anger, or moral outrage【8†L151-L159】

【8†L160-L168】. For example, an “appeal to fear” tse many fear-

inducing words (“dangerous, catastrophic, terrifying”)【5†L119-L127】

【5†L133-L137】. We might compute an emotion intensity score per

document – e.g., proportion of wouse an emotion classiﬁcation model

to get a probability that the text is meant to evoke fear vs. neutral. If

the *fearis above a threshold (say 0.8), we ﬂag an emotional appeal

technique【41†L23-L31】【41†L33-L39】. Importantly, we separate

emotion from sentiment: a piece could be negatively emotional

(anger/fear) but that isn’t just “negative sentiment” in a broad sense –

it’s targeted emotional manipulation. High emovidence can indicate an

Appeal to Emotion fallacy【7†L152-L160】【7†L168-L176】.

7.  Framing & Narrative Features: These look at how the story is

framed at a thematic level【8†L165-L173】【8†L1 draw from framing

theory in media studies: e.g., does the article use a (pitting groups

against each other), a morality frame, a human-interest frame focusing

on personal stories, etc. We can detect framing by keyword cues or by

comparing to known examples. For instance, describing an issue in

terms of law and order vs. in terms of compassion indicates diﬀerent

frames (moral vs. security frame). We also identify narrative structures

like Hero vs. Villain depictions【8†L177-L185】 – is someone portrayed

as the hero saving the day and another as a villain? A propagandistic

piece often elevates one side as virtuous and demonizes the other. We

look for victim/oppressor narratives, crisis language (“a looming

disaster” ﬁts a crisis frame), and whether the story assigns blame or

responsibility for problems explicitly【8†L171-L179】【8†L181-L189】.

These high-level features may use a combination of lexicons (for known

frames) and ML classiﬁers trained on annotated news for frames. They

help separate stanalism from content that pushes a speciﬁc narrative

agenda.

8.  Rhetorical & Persuasion Techniques: Identiﬁcation of classic

rhetorical strategies being used【8†L189-L197】. This overlaps with

logical fallacies (next layer) but is broader, including any persuasion

tactic. We check for use of ethos, pathos, logos appeals (credibility,

emotion, logic). For example, an appeal to authority (ethos) is a

technique where the argument leans on an authority ﬁgure’s opinion

rather than evidence【5†L62-L70】【5†L79-L87】. We detect that by

spotting references to experts or important ﬁgures (“According to Dr.

X…”)【5†L62-L70】【5†L88-L96】, especially if used out of context or

without supporting data (this would later be ﬂagged as a fallacy if

inappropriate). **Paeals (emotion) we covered via emotion features.

Logos – we check if actual logical reasoning is present or if it’s being

faked (for instance, using statistics or graphs in a misleading way). We

also detect propaganda techniques commonly studied in media bias:

e.g., name-calling, glittering generalities, whataboutism, ﬂag-

waving, thought-terminating clichés【6†L46-L54】【6†L68-L72】.

Each of these has telltale signs: name-calling involves derogatory

epithets (detected via insult lexicons or toxicity models), glittering

generalities use vague positive words (“freedom, greatness”) to evoke

approval without speciﬁcs【41†L109-L117】, whataboutism can be

ﬂagged by discourse structure (“what about X?” used to deﬂect) –

maybe by seeing a question retort that shifts topic. We incorporate

known lists and patterns from propaganda detection research. For

example, a loaded language metric calculates the percentage of

words that are highly positive or negative emotionally【41†L97-L105】

【41†L99-L107】; if that percentage is extreme, it indicates Loaded

Language propaganda technique. Eis recorded as a binary ﬂag and/or

intensity score in the feature set【6†L35-L43】【6†L74-L78】 (e.g.,

propaganda_name_calling = True  or an integer count of insults).

9.

Logical Fallacy Detection: This layer is critical for our system’s

mission – it speciﬁcally targets classic logical fallacies in the text

【8†L213-L221】【8†L229-L236】. The pipeline uses both heuristic rules

and ML classiﬁers to detect over a dozen fallacy types (many listed in

our feature design). Some key fallacies and their detection strategies:

Strawman: Misrepresenting an opponent’s argument to make it

easier to attack【6†L5-L13】. We detect this by analyzing how

arguments are presented vs. original sources. If the text

paraphrases an opponent’s potion or distortion (e.g., “They claim

X” when the opponent actually said something nuanced), it’s a

strawman. Features for strawman include checking for paraphrase

distance – how much the restated claim deviates from likely original

claim【7†L206-L214】【7†L216-L224】. If someone’s argument is

rephrased with extreme words or oversimpliﬁcation, we ﬂag it. We

also look for the presence of counter-arguments – absence of any

genuine counterpoint can indicate the author is knocking down a

straw man rather than real opposition.

Ad Hominem: Attacking the person instead of the argument

【6†L7-L15】. We use a toxicity detector (like Google’s

Perspective API or similar) to ﬁnd direct insults or name-calling,

especially when mentioning people【41†L49-L57】【41†L67-L70】.

If personal attacks (“idiot”, “liar”) appear in context with a person’s

name, we ﬂag ad hominem. We also identify subtler forms: e.g.,

character attacks or insinuations (“Of course he would say that,

he’s a banker”). High insult density relative to content length is a

numeric feature, and linking toxicity scores with PERSON entities in

the sentence is an eﬀective rule【41†L49-L57】【41†L67-L70】. For

example, pseudocode:  if toxicity_score > 0.9 and PERSON in

sentence_ents: flags["ad_hominem"]=True . This ecatch personal

attacks directed at individuals.

Slippery Slope: Claiming a minor step will inevitably lead to a

major (often negative) outcome without evidence【6†L9-L17】.

Detection involves ﬁn sequences in text (look for words like “if X

happens, then eventually Y” or “this will lead to…”) and checking if

the progression is speculative. We ﬂag sentences with "if ... then ..."

that escalate dramatically (e.g., “If we allow A, then Z will surely

happen”) – a cue for slippery slope reasoning. We might use a

simple rule: if a sentence or consecutive sentences contain a causal

connector (therefore, thus) leading to an extreme outcome with

modal verbs (“will surely”), mark as slippery slope. This pairs with

causality feature checks: looking at overuse of causal language

like "therefore, thus" connecting tenuous claims【7†L38-L46】

【7†L50-L58】.

False Cause (Post hoc): Assuming correlation implies causation

【6†L13-L21】. This is often signaled by causal language where

timing is the only linkage (e.g., “After X, Y happened, so X caused

Y”). We detect phrases that match “X happened after Y, therefore Y

caused X” or the Latin post hoc ergo propter hoc scenarios【7†L58-

L62】. We incorporate a check for temporal markers: if sentences

use temporal linking (“after”, “since”) without explaining a

mechanism, and especially if multiple events are listed

chronologically with an implied causal tone, we ﬂag a potential false

cause fallacy. A numeric feature might be “temporal_link_count” vs.

“explicit_cause_count”; if a claim has time links but no explicit

causal mechanism, that's a red ﬂag【7†L38-L46】【7†L48-L56】.

Red Herring: Diverting to an irrelevant topic【6†L11-L19】. We

look for sudden topic shifts in the text. A discourse analysis can

detect when a paragraph’s topic is unrelated to the main issue. If

an argument sequence is broken by an oﬀ-topic section (detected

via low semantic similarity between consecutive segments or an

abrupt introduction of a new entity/topic that isn’t revisited

【41†L91-L99】【41†L93-L101】), it could be a red herribject is

introduced in the middle of a logical argument without resolution.

Cherry Picking (Suppressed Evidence): Selectively presenting

evidence that supports your claim while ignoring counter-evidence

【6†L13-L21】【6†L27-L35】. The system tracks the evidence

provided for each claim (via the claim is made without any

supporting data or with only one example where multiple are

expected, we note it. Also, if external data (like known statistics or

opposing facts) are completely missing when context suggests they

should be present, we consider that cherry-picking. One metric is

source diversity: if all cited facts or quotes come from one side or

one type of source, it indicates selectivity【41†L79-L87】【41†L139-

L147】. For instance, if N supporting facts are given and 0 opposing

facts, and we know opposing evidence exists, cherry-picking

41†L77-L85】. We might compute a viewpoint diversity score; a

very low score (only one perspective present) triggers a ﬂag.

False Dilemma: Presenting only two choices when more exist

【6†L23-L31】. We detect either/or language: usage of “either X or

Y” or claims that “there is no alternative”. Phrases like “the only

choice” or “no middle ground” are strong indicators【7†L180-

L188】【7†L192-L200】. A simple pattern matcher can pick up

“either X or Y” constructs and set a binary feature for binary

framing. We also note if an argument explicitly says “we have no

choice but to [take extreme action]” – that often signals a false

dichotushed.

Circular Reasoning (Begging the Question): The conclusion is

the same as the premise, just rephrased【6†L31-L39】. rgument

structure, we check if a claim is essentially repeated or if a premise

assumes the truth of the claim. If our argument graph shows that a

claim node is directly or indirectly supporting itself with no

independent evidence, that indicates circular reasoning.

Linguistically, this might appear as reusing key phrases. We could

attempt an automated check: if a conclusion sentence and a

premise sentence have very high semantic similarity (almost

paraphrases) and are asserted as evidence of each other, ﬂag

circular reasoning【7†L20-L28】【7†L24-L32】.

(And many more: Hasty Generalization – detected via absolute

quantiﬁers like “all people” from one example【7†L68-L76】【7†L84-

L92】; Appeal to Authority – detected via NER for titles plus certain

verbs【5†L62-L70】【5†L88-L96】; Appeal to Popularity

(Bandwagon) – detected via words like “everyone, most

people”【5†L18-L26】【5†L42-L49】; No True Scotsman – via

phrasing like “no true member of group X would do Y”; etc. The system

has a rule or model for each fallacy listed in our design【6†L3-L11】

【6†L19-L27】.)

Each detected fallacy is stored as a **binary ﬂag plus an intenable【6†L1-

L9】【6†L35-L43】. For example,  fallacy_strawman = True  if triggered, and

perhaps  strawman_degree = 0.8  if we have a conﬁdence. We also capture

the text span involved【6†L37-L45】【6†L73-L78】 (so we know exactly

which sentence or phrase constitutes the fallacious argument), enabling the

frontend to highlight that portion.

10.  Factuality & Evidence Features: These evaluate the article’s factual

grounding【8†L237-L245】【8†L247-L254】. We count veriﬁable facts

(numbers, dates, statistics) and check if sources are cited for them

(presence of citations or links)【6†L139-L147】. A high “fact density”

with zero citations could be suspicious. We also attempt to assess

truthiness via external fact-checks: e.g., for major claims we might

query a fact-checking API or knowledge base. Another angle is Claim

Speciﬁcity – are the claims speciﬁc (with concrete details) or vague?

Vague general claims (“Many people say...”) get a lower credibility

score【6†L150-L158】【6†L152-L159】. We also ﬂag common

misleading indicators like misuse of quantiﬁers (“millions of people”

with no context)【6†L150-L158】 or clickbait styles in text. These

features feed into an overall factuality score for the piece (how

evidence-based vs. anecdotal it is).

11.  Temporal & Contextual Features: Checks for context manipulation

【8†L258-L266】【8†L267-L274】. We examine publication date vs.

event dates mentioned – e.g., is the article rehashing an old event as if

it’s new? We detect timeline distortion or selective history: if events

are described out of chronological order or historical context is omitted

(e.g., skipping what happened before an event to frame it misleadingly)

【7†L274-L282】【7†L283-L289】. One example: an article might

mention a response from one side without mentioning the provocation

that preceded it – creating a misleading cause-eﬀect. We also track

repetition over time if the same claims are repeated across many

articles (which could indicate a coordinated narrative, but that moves

into cross-document analysis).

12.  Cross-Document & Network Features (Advanced): If our system

has a large corpus, we can compute features that compare this

document to others【8†L275-L283】【8†L284-L292】. For instance, is

this article’s language signiﬁcantly diﬀerher articles on the same topic

(could indicate extreme bias or fringe narrative)? Does it use phrases in

common with known propaganda outlets (suggesting a shared source)?

**Network analysreveal if multiple sources are repeating the same

talking points (detectable via similar embeddings or n-grams)【8†L284-

L292】. These features are more relevanloyment and help identify

agenda-setting or coordinated spread of certain frames.

13.  Metadata & Source Features: Finally, we integrate metadata about

the article source【283】. The pipeline attaches known information

about the publisher (if available): e.g., outlet’s political leaning or

reliability rating from external databases, the author (if known) and

their history, publication region, etc. For ethe source is known to have a

strong bias, we take that into account in the scoring (though carefully,

to avoid circular reasoning – we don’t want to assume bias because of

source, but it’s part of context). We also capture social metrics if

provided (shares, likes) but mainly for analysis, not for the bias score.

Metadata helps contextualize the content: a highly partisan source

might require tighter scrutiny on certain fallacies. All metadata ﬁelds

are stored alongside textual features in Parquet (e.g.,  publisher ,

pub_date ,  author  columns)【6†L257-L265】【6†L277-L283】.

All these features – from simple counts to complex ML-derived signals – are

assembled into a feature vector for each document (and some at sentence-

level too). We maintain a Feature Registry (in YAML or a structured conﬁg)

that enumerates every feature name, description, and version. This registry is

referenced by the extraction code to ensure consistency【30†L1-L9】【30†L11-

L19】. In practice, before running extraction, the pipeline loads the registry to

know which features to compute; after computing, it stores only those deﬁned

features. This guarantees that the set of features is standardized and

versioned, preventing drift. The registry can be updated (with version bump)

when new features are added (e.g., if we introduce a new fallacy type) and the

code will produce a new column for it. The Feature Registry’s version is part of

the pipeline versioning.

All extracted feature values and intermediate ﬂags are appended as new

columns in the Gold Parquet dataset, which now contains: text, tokens,

entities, plus columns like  avg_sentence_length ,  passive_voice_ratio ,

sentiment_avg ,  fallacy_strawman ,  fallacy_strawman_span ,

propaganda_namecalling ,  bias_entity_sentiment_diff , etc., and ﬁnally the

scores (next section). The Parquet schema is designed to be canonical and

consistent across all stages【39†L379-L387】【39†L397-L405】 so that any

analysis or model downstream reads from a single uniﬁed data structure. An

example snippet of a canonical schema might look like:

JSON

{

  "doc_id": "string",

  "source": "string",

  "language": "string",

  "raw_text": "string",

  "clean_text": "string",

  "tokens": ["string"],

  "sentences": ["string"],

  "entities": [ { "text":"string", "label":"string", "start":int, "end":int } ],

  "features": {

    "num_sentences": int,

    "avg_sentence_length": float,

    "type_token_ratio": float,

    "passive_voice_ratio": float,

    "sentiment_avg": float,

    "emotion_dominant": "string",

    "fallacy_strawman": bool,

    "fallacy_strawman_span": "string",

    "fallacy_ad_hominem": bool,

    "propaganda_namecalling": bool,

    ...

    "bias_entity_sentiment_diff": float,

    ...

  },

  "scores": {

    "bias_score": float,

    "manipulation_score": float,

    "toxicity_score": float

  },

  "pipeline_version": "string",

  "processed_at": "timestamp"

}

(This is illustrative; actual schema might nest features diﬀerently. n handle

nested ﬁelds like the entity list and dictionary of features. Note the inclusion of

pipeline_version  and timestamp for traceability.)

Storage Design: All scalar features become individual Parquet columns, lists

are stored as arrays, and structured data as nested structs, which Parquet

handles seamlessly【9†L314-L322】. Embeddings (which are large ﬂoat

vectors) are not stored in Parquet beyond maybe an ID – instead, they are kept

in a Vector DB for earch【12†L386-L394】【12†L397-L405】. Any ﬁnal scores

we compute (bias scores etc.) are also stored in Parquet, and because they

might be updated with new methods, we treat them as versioned outputs

(e.g.,  score_version=1.0  in the data)【9†L315-L323】【9†L317-L324】. This

ensures all data is reproducible: if we pipeline with the same version on the

same input, we she same feature and score values (determinism).

#Classiﬁcation Layer

After raw feature extraction, the pipeline applies a taxonomy-driven

classiﬁcation stage. This stage maps each piece of content (or even sub-

components like sentences) into one or more predefries according to our

project’s taxonomy【4†L17-L25】. The taxonomy is essentially a controlled

vocabulary of labels that the project cares about. For a media bias analysis

system, the taxonomy could include categories like: types of rhetoPropaganda:

Appeal to Fear, Propaganda: Flag-Waving*), types of logical fallacies (the ones

described above), thematic bias categories (e.g. Ideological Bias: Left-Leaning,

Right-Leaning, Loaded Language), or content themTopic: Immigration, Topic:

Climate*, etc., if we also classify subject matter). The Data Engineer is

responsible for managing and updating this taxonomy as the project evolves

【4†L19-L27】【4†L21-L29】, ensuring it stays comprehensive and well-

structured.

How taxonomy classiﬁcation works: We feed the features and signals from

the previous layer into a classiﬁcation engine that assigns taxonomy labels.

In many cases, this is straightforward: if a speciﬁc fallacy ﬂag is true, that

document (or that segment) gets the corresponding category label (e.g.,

Fallacy → Ad Hominem). For more complex or overlapping categories, we might

use a rule-based logic or an ML multi-label classiﬁer. For example, “Loaded

Language” might be a category triggered by a combination of high emotional

tone and speciﬁc keywords【41†L97-L105】, while “Unsubstantiated Claims”

mchecking that a claim was made without evidence (cross-referencing

evidence count features). The taxonomy engine can be thought of as a set of if-

then rs that map the raw features to ﬁnal labels.

This stage is taxonomy-driven because the categories are deﬁned upfront (in

a conﬁg or code) rather than emerging ad-hoc. It’s possible to maintain this

mapping logic in a conﬁguration (like a YAML that says: Category X is triggered

if feature A > 0.8 and feature B is true for instance). That would allow non-

engineers or analysts to tweak how categories are assigned without touching

code. The pipeline commentary recommended making the taxonomexible to

allow creating new taxonomies or label sets easily【27†】.

Each classiﬁcation can also produce a conﬁdence score. For instance, if we use

a machine learning model to classify a to propaganda techniques, it might

output probabilities for each technique (we take those as conﬁdence scores).

Or a rule-based mapping can simply assign a binary 0/1 with an implicit full

conﬁdence if criteria are met.

Integratnomy with fallacy detection: The taxonomy provides a structured

way to report and aggregate the falas ﬁndings. Rather than dumping dozens of

raw feature values to an end user, we use taxonomy labels to summarize what

kind of issues were found. For example, multiple low-level features related to

fear (fear words, high negative sentiment, catastrophic predictions) can

collectively result in the taxonomy label “Appeal to Fear”. This label orms the

scoring matrix – diﬀerent categories might contribute diﬀerently to an overall

bias/manipulation score. The taxonomy essentially translates myriad signals

into humal categories which can be displayed or further analyzed.

The outpstage is a set of classiﬁcation labels per document (and possibly

per sentence). We store these in the data as well, perhaps in a column like

labels  or under the  scores / flags . For example, a document might end up

with  labels = {propaganda: ["Appeal to Fear", "Loaded Language"], fallacy:

["Slippery Slope"]}  with some associated probabilities. These labels will be

used in the ﬁnal output JSON for the frontend (so that the UI can show which

categories were detected, with perhaps a tooltip explanation for each

category).

Scoring Matrix Design and Calculation

One of the key responsibilities of the NLP/Data Engineer is to construct the

content scoring matrix or evaluation logic for the project【4†L21-L29】.

This scoring matrix takes all the signals (features, ﬂags, and taxonomy labels)

and computes one or mor that summarize the level of bias, manipulation, or

credibility of the content. The scores needrministic and reproducible** for a

given input【4†L25-L33】 – no randomness – so that the same article always

yields the same scores (essential for trust and QA).

Design of the scoring matrix: We can think of it as a weighted rubric. Each

category or feature contributes some points toward an overall score. For

example, we might deﬁne an overall “Manipulation Score” from 0 to 100,

which is composed of sub-scores in areas like Emotional Appeal, Logical

Fallacies, Imbalance/Bias, Source Credibility, etc. Each detected issue raises the

score. The exact formula is proprietary (in a real project, these weights might

be set by domain experts), but conceptually:

Start from 0 (no d points for each category of issue:

e.g., for each logical fallacy detected, add 5 points (maybe morus ones

like Ad Hominem or outright Falsehood).

If emotional language is high, add up to 10 points proportional to the

intensity.

If the article is one-sided (cherryo counter viewpoints), add e.g. 10

points.

Subtract points if the article shows balance or lots of evidence (a

positive indicator).

Cap the score at 100.

Alternatively, produce multiple scores: e.g score** and a Propaganda score

separately. The scoring matrix could be represented as a table where rows are

taxonomy categories and columns are contributions to each output score.

In a formulaic sense, one simple approach to combine signals is a weighted

sum:

manipulation_score =

  w   ⋅∑i
i

feature  ,i

where each feature or category   has a weight

 (positive for negative traits,

i

w  i

negative weight for positive traits like balance). For instance, if  fallacy_count  is

the number of distinct fallae might have a term w_{\text{fallacies}} \times

\text{fallacy_count}. Emotional appeal could contribute w_{\text{emotion}}

\times \text{emotion_intensity_score}, etc. We would calibrate these weights

based on internal guidelines or perhaps using a small labeled dataset of articles

with known bias levels.

Example: Suppose an article triggered Bandwagon (appeal to popularity)

and Loaded Language, and had an extremely one-sided sentiment toward

two entities. The scoring logic might assign 5 points for Bandwagon, 5 for

Loaded Language, and say 10 for the one-sided treatment, totaling 20 –

indicating a moderately manipulative piece. Another article wdiﬀerent fallacies

and very high emotional tone might score, say, 70 or 80, indicating a high level

of manipulation.

We also ensure to include any source reliability adjustment. If t has a

history of unreliability, we might modestly increase the score or at least tag it

(but do so carefully; we generally focus on the text itself to avoid bias).

The result of the scoring matrix is recorded in the data, e.g., under a  scores

ﬁeld as shown earlier ( bias_score ,  manipulation_score , etc.). These scores are

versioned and traceable – if we uoring formula, that would constitute a new

pipeline_version  or at least a  score_version .

From a testing perspective, the scoring logic is deterministic, so any change

in input or code should be intentional. The QA tester will have test cases to

ensure that, for example, an article with known properties yields aore range,

and that scores don’t ﬂuctuate across runs【1†L15-L23】【1†L19-L27】.

Vector Database for Embeddings and Similarity

In parallel to the main pipeline (which yields structured outputs and scores), we

maintain a Vector Database to store semantic embeddings【12†L386-L394】.

This is used for similarity search, content retrieval, and cross-document

analysis. After feature extraction, we take the document embedding (or

multiple embeddings, like one per paragraph) computed in the semantic

features stage and index them into a vector DB (such as FAISS, Milvus,

Weaviate, or Pinecone)【12†L386-L394dding entry is associated with the

document ID (and perhaps section ID).

Purpose: The vector DB allows the system (or analysts) to perform semantic

queries like “ﬁnd articles similar to this one” or “cluster articles by narrative”.

It’s especially useful to detect if aking point is being circulated across multiple

sources (agenda setting). For example, if we have an article that scored high on

propaganda, we can query the vector DB to see if there are other articles with

embeddings very close to it – indicating they likely use similar language or

narrative. This could reveal a network of content with the same message.

Importantly, the vector DB is not used directly to compute the bias

scores – it’s kept as a read-only semantic memory for analysis, not a part of

the deterministic scoring pipeline【33†L1-L9】【33†L11-L19】. This separation

is deliberate: eilarity is a statistical measure and may introduce

nondeterministic behavior (depending on the model), and using it in the core

scoring could undermine reproducibility. Instead, any insights from the vector

DB (like narrative clusters) are provided as supplementary info or for oﬄine

analysis.and scores) come from the explicit features and rules in the structured

pipeline【33†L3-L9】【33†L11-L19】.

The vector DB can be queried via an API. For instance, the backend might

expose an endpoint like  /similar_articles?doc_id=123  which will retrieve the

top-N nearest neighbor docue vector index (excluding those from the same

publisher, maybe). This could be presented in a dashboard to show context

around a piece (e.g., “These 5 articles share very similar language to the one

you analyzed”).

In summary, the vector store complements the pipeline by enabling semantic

search and clustering, while the sdeterministic scoring and explanation*. We

therefore store embeddings outside Parquet and put only their idehe main

data, to avoid bloating Parquet and because specialized vector indices are far

faster for similarity search【38†L376-L384】【38†L386-L394】.

Integr Backend API and Data Services

With the analysis complete, results need to be served to end-users (e.g.,

journalists or analysts using a web dashboard). The Backend Engineers

develop RESTful API endpoints that either trigger the analysis or retrieve stored

results【3†L14-L22】【3†L18-L26】. Given the pipeline design, there are two po.

On-demand analysis: The client (front-end) submits content (or a URL) via an

API call, the backend passes it to the NLP pipeline which runs on the ﬂy and

returns results. This requires the pipeline components to be ex containerized)

that can process a single document quickly. We must ensure the pipeline is

optimized for low latency in this scenario (caching models in memory, etc.).

2.  Preprocessing + he pipeline runs continuously or on a schedule

(for example, ingesting new articles every hour), stores all

resbase (SQL or NoSQL), and the API simply queries that DB when clients

request data【27†】. This is more suitable for a system tracking a stream

of media content.

In our case, since conﬁdentiality and determinism are key, we likely do batch

processing on a controlled schedule, save resultfrom there. The SQL serving

DB could be a relational database with tables for articles, sities, etc., linking to

the Parquet store or containing a subset of data for quick retrieval【27†】.

Alternatively, we can query Parquet ﬁles directly using something like park SQL

when needed (though latency might be higher for user-facing requests, so a

cache or DB is usually added).

The backend’s responsibility is to ensure well-structured JSON output for

each request【3†L16-L24】. This JSON would include all analysis details needed

by the frontend for visualization. For example, for each article ID requested, the

backend might return a JSON like:

JSON

{

  "doc_id": "123",

  "title": "...",

  "source": "...",

  "bias_score": 75.0,

  "manipulation_score": 80.0,

  "labels": ["Propa:contentReference[oaicite:136]{index=136} to Fear", "Fallacy: Slippery

  "highlights": [

     { "text_span": "If we allow this, society will collapse", "label": "Slippery Slope"

     { "text_span": "hordes of criminals", "label": "Loaded Language" }

  ],

  "entities": [

     { "name": "John Doe", "avg_sentiment": -0.6, "mentions": 3 }

  ],

  "published": "2025-12-10",

  "processed_at": :contentReference[oaicite:137]{index=137}:contentReference[oaicite:138]

}

The highlight spans are prepared by the pipeline (we stored the text and

indices of each ﬂagged segment). The backend might do server-side rendering

logic to attach those highlights/tags so the frontend just displays colored text

【3†L18-L26】. This means the backend uses the spans and original text to

create HTML or annotated text. Alternatively, the frontend could do it if we just

provide indices and categories.

Security and performance are handled at the backend layer: ensuring ce this is

conﬁdential/internal) can query the API, and that one heavy request can’t

starve others. The Lead Engineer will have set up authentication and

authorization for the API (e.g., API keys or OAuth)【2†L19-L27】, along with

encryption TPS for data in transit, etc.)【2†L17-L25】【2†L45-L48】.

The backend also interfaces with our data stores: it will query the SQL DB or

Parquet/Vector stores to fetch the requested data. It must follow best practices

for error hagging – e.g., if a requested article analysis is not found, return a

graceful error; if the pipeline throws an exception, catch it and return an error

code, etc.【2†L19-L27】. Logging is critical both for debugging and for audit:

every API call can be logged (with user ID, time, doc ID, etc.) to an audit log for

traceability【1†L21-L】.

To integrate the pipeline, the backend engineers and lead engineer ensure

that the pipeline’s oute frontend needs【3†L20-L27】【4†L29-L33】. For

example, if the frontend expects highlighted text segments with tags, the

pipeline must output those segments in a structured way (which we did via

spans They also ensure that the pipeline can be invoked from the backend code

(maybe as a library or microservice). If the pipeline is heavy (using Spark, etc.),

we might not integrate Spark into the API call; instead, we’d run Spark oly serve

results. For on-demand, we might rely on a lighter-weight implementation

(perhaps a distilled version of the pipeline using spaCy in-memory for single

documents).

DevOps and Deployment: The entire system is containerized (Docker) and

deployed in a cloud environment (AWS/GCP/Azure) by the lead engineer

【2†L29-L37】【3†L45-L53】. CI/Cre set up so that when code changes (pipeline

or backend), tests run and then it deploys to a staging environment, and then to

production upon approval【2†L31-L39】【2†L21-L24】. Infrastructure-as-code

is used to maintain, Terraform or CloudFormation templates for the data lake

storage, databases, etc.)【2†L31-L39】. We use monitoring tools to ensure the

pipeline jobs run on schedule and the APIs have high uptime【2†L19-L27】. The

lead engineer will also set up performance monitoring (like timing logs for how

long analysis takes per document, memory usage, etc.) to catch bottlenecks

【3†L23-L31】.

The backend and pipeline are conﬁgured to handle load: e.g., if analyzing

hundreds of articles per hour, the Spark job is scheduled accordingly or multiple

instances of the analysis service run in parallel. The backend API itself can scale

behind a load balancer (if it’s serving many user requests). Caching can be

used for repeated requests – e.g., if the same article is requested multiple

times, the result can be cached in memory or an HTTP cache.

All data, especially since it might irietary content, is secured. The data lake

(Parquet ﬁles) can be on an encrypted S3 bucket with limited access. ave

proper authentication and network policies. Under the NDA, all team members

operate with security best practices in mind【## Quality Assurance and Testing

Strategy

Quality Assurance is vital for this pipeline because of the complexity and need

for trust in the results. The QA/Tester’s role is to ensure reliability, accuracy,

and consistency of outputs【1†L4-L12】sting and validation at multiple levit

Tests for Components:** Each feature extraction function or rule is unit-tested

with controlled inputs. For example, we feed a known sentence to the

bandwagon detector (“Everyone knows the election was rigged.”) and assert

that  flags["bandwagon_effect"]  comes out True and the bandwagon score is

abovSimilarly, test the ad hominem detector with a sentence containing an

insult and a PERSON name, expecting a ﬂag. These tests ensure our patterns

and ML models are wired correctly.

**2. Integration Tests for Pipeline:set of sample articles (perhaps curated with

known issues) that we run through the entire pipeline. Because the system is

deterministic, we can store the expected full output for these samples

(expected features, ﬂags, and scores) and then compare the pipeline’s actual

output to them in regression tests. For example, for a test article that is

balanced, we expect a low bias score and no fallacy ﬂags. For a heavily biased

test article, we expect certain ﬂags to trigger. The QA tester will maintain these

expected outcomes. Whenever code changes, these tests catch if any output

changed unexpectedly【1†L15-L23】【1†L17-L24】. If a change is intentional

(e.g., we improved a feature), the expected results are updated accordingly

with version tracking. This is crucial for maintaining reproducibility – the same

input must produce identical output across runs and versions (unless we

deliberately change the logic and update version numbers)【1†L19-L28】.

3. Deterministic Reproducibility Checks: QA will run the pipeline on the

same input multiple times (with the same pipeline version) to conﬁrm that

results are bit-for-bit identical【1†L19-L27】. Any nondeterminism (perhaps

from parallel processing order or an ML mod identiﬁed and eliminated or

controlled (for instance, by setting random seeds for any algorithms that use

randomness, and by ensuring single-thread ordering where necessary). Our

pipeline design favors rule-based methods and seeded models to achieve this

【4†L61-L64】【4†L25-L33】. The tester also veriﬁes that the  pipeline_version

and other version metadata are correctly attached to outputs, so that if

anything ever does diﬀer, we can see if the version changed.

4. Performance and Load Testing: The QA process will include timing the

pipeline on various sizes of input to ensure it meets requirements. If processing

one article takes too long, that’s ﬂagged to engineers to optimize (maybe by

caching language models, etc.)【3†L16-L24】【3†L22-L24】. If doing batch

processing, test that the system can handle ech within an acceptable time

window. Also test memory usage (some stages like embedding generation can

be heavy).

5. Regression Testing on Updates: Whenever a new feature is added or

logic is changed, QA runs a full regression test suite: re-run all prior test articles

through the pipeline and compare scores and ﬂags to the preion. Ideally, with

no intended logic change, nothing should change (ensuring no side eﬀects). If

changes are intended (new fallacy detection added, etc.), QA checks that only

the expected new outputs appear and nothing else breaks (previous outputs

remain consistent)【1†L17-L24】【1†L25-L33】. They will also run a diﬀ on the

Parquet schemas to ensure no unwanted schema drift (like a feature

disappearing).

6. Logging and Traceability: The pipeline is instrumented with logging at key

points (especially if running in batch mode). For each document, a log might

note: “Doc 123: 2 fallacies detected (AdHominem, Strawman), bias_score=72”.

QA wille logs to ensure the numbers align with expectations and that every

document is processed. Additionally, all processing steps should be traceable

via logs or metadata – e.g., each run ID, and each output has  processed_at

timestamp and version info【1†L19-L27】【4†L63-L68】. QA can take an

output, trace through logs to conﬁrm which run produced it, and even

reproduce that run on a debugging environment.

7. Audit Trails and Version Control: Because this is conﬁdential and

sensitthat we maintain an audit trail of changes. Every change to code or

taxonomy is documented (in version contssibly in a changelog that’s linked to

the pipeline_version). Theecks that for a given output, one can identify exactly

which code version and conﬁg produced it【4†L61-L687】. This ties in with the

NDA compliance and need for inuntability – if a question arises “why did this

article get ﬂagged?”, we should be able to trace it down toic rules and version

that were applied【1†L19-L28】【4†L63-L68】.

8. End-to-End Acceptance Testing: The QA testerates the end-user

experience. This means checking the JSON or API outputs and making sure

tcorrectly in the frontend (if a UI exists). For instance, they would verify that

highlighted spans correspond exactly to te original article (no oﬀ-by-one index

errors, no missing context)【1†L25-L33】. They would also verify that the

output JSON structure strictly fol (perhaps by validating against a JSON Schema

deﬁnition). Any mismatch is report (e.g., if a ﬁeld is missing or of the wrong

type).

9. Automated Testing Tools: We incorporate basic for running these tests.

For example, a small test harness script can run a set of input docugh the

pipeline and compare outputs to expected, producing a report. For the API, we

might use integration tools like Postman or pytest to simulate API calls

(including authentication) and check we get correct responses (status codes

and JSO If we have a UI, even Selenium could be used to test that, for example,

uploument through the UI results in visible highlights and scores as expected

【1†L53-L61】 (though UI testing is secondary here).

10. Continuous Improvement: The QA is not just about catching bugs but

also about suggesting improvements. For instance, if the tester notices that two

similar articles yield inconsistent scores, they will bring it up: perhaps the rules

need adjustment or a new feature is needed. Given our small team structure,

the QA tester’s feedback loop is tight – issues found are immediately discussed

with engineers and lead to quick ﬁxes or enhancements【1†L85-L94】【1†L87-

L95】. This continuous feedback ensures the pipeline’s quality bar is kept high

even as new data or edge cases come in.

Example Test Case: As a concrete example, consider a test article that says:

“Accordi society is on the brink of collapse. Everyone agrees that if we allow the

new policy, it will lead to disaster.” Expected outcome: The pipeline should ﬂag

Appeal to Authority (for citing Professor Smith in a broad claim)【5†L62-L70】,

Bandwagon (“everyone agrees”)【5†L18-L26】, and Slippery Slope (policy ->

disaster)【6†L9-L17】. The QA tester would verify that these ﬂags are present

in the output, that their text spans correspond to the phrases, and that the ﬁnal

scores are bumped appropriateat’s a bug in detection. If extra ﬂags appear,

that could be a false positive to evaluate. This way, the test validates multiple

components together.

Finally, QA also checks consistency across environments – eine on a

developer’s machine vs. the production environment, do we get the same

results? Any discrepancy could hint at a dependency or conﬁguration issue

(which they would then help pinpoint, maybe something like a diﬀerent model

version installed).

By following these testing strategies and with the QA role acting as the

“guardian o1†L79-L87】, we ensure that the pipeline remains ﬂawless,

deterministic, and trustworthy as it moves into production. Every output is

correct by design and veriﬁed by tests, every code change is scrutinized for

unintended eﬀects, and every result can be traced and explained – which is

essential for a system analyzing media content where stakes (and client

expectations) are high.

Deployment and Logging/Monitoring

The pipeline and associated services are deployed in a production environment

with strong DevOps practices. Each component (ingestion, NLP processing, API,

vector DB, etc.) can be containerized (e.g., Docker images) and orchestrated

via Kubernetes or similar, under the supervision of the Lead Engineer【2†L21-

L30】【2†L31-L39】.

We set up a CI/CD pipeline such that merges to the main branch ted tests

(unit and integration tests as above) and then deployment to a staging

environment. Only if tests pass and possibly a manual review is the change

promoted to production. This ensures that no untested code goes live【2†L31-

L39】【1†L53-L61】.

Infrastructure: The system likely runs on cloud VMs or containers. We might

use for storing Parquet ﬁles (Bronze/Silver/Gold), Amazon RDS or DynamoDB

for the serving database, Amazon ES (Elasticsearch) or Neptune for any graph

if needed, and an EC2 or EKS (Kubernetee pipeline jobs and APIs. The vector DB

could be a managed service or running on our cluster. All secrets (API keys, DB

passwords) are stored securely (not hard-coded).

Logging: We implement comprehensive logging at all layers. The application

logs include:

Pipeline logs (per document or batch) with at least summary of what was

detected. Also error logs if any document fails processing (wite).

API access logs for each request (for auditing who accessed what).

System logs for resource usage.

We use a centralized log aggregator (like ELK stack or cloud watch) to

aggregate logs. The QA tester and engineers can then monitor these logs. For

example, if suddenly a batchvery high scores all at once, logs could help

determine if it’s a data issue or a bug.

Monitoring/Alerts: Metrics to monitor include:

Pipeline throughput (docs per hour) and latency (time per doc).

Error rate (any pipeline exceptions).

API latency and error rate (should be near 0 errors).

Resource utilization (CPU, memory of the pipeline job, to catch if we need

to scale up).

Drift in feature distributions: We can even monitor if the average number of

fallacies per article changes drastically over time (this could indicate either

a real trend in content or a pipeline issue; either way, it’s interesting).

If any metric goes out of bounds (e.g., pipeline taking too long or error rate >

X%), an alert (email/Slack) is sent to the team.

Traceability and Audit: Because of NDA and sensitivity, every piece of data

processed might need to be auditable – e.g., we might maintain an internal

ledger of exactly what data was processed when and by whom. The pipeline’s

deterministic nature and version tagging【32†L5-L13】 greatly facilitate audits:

ce the analysis of a given article by using the same pipeline version on the raw

text (which we have in Bronze). The QA’s checks on audit logs【1†L21-L28】

ensure we’re recording everything needed (like logging each run’s ID, input

source, output summary, etc.). If later someone asks “did your sXYZ on this

date and what did it output?”, we can answer conﬁdently by looking atults and

logs.

Maintaining Conﬁdentiality: All team members sign NDAs【2†L38-L46】 and

data is handled securely. The deployment likely sits in a private network. Access

to the data and system is restricted. The QA tester is vigilant about not

exposing any sensitive info – e.g., when writing bug reports, they refer to

content abstractly or by ID rather than copying sensitive text.

Continuous Improvement: As news manipulation tactics evolve, the pipelin

updates (new rules, new categories). Thanks to the modular design (feature

registry, taxonomy conﬁg, versioned models), we can update components

without overhauling everything. We plan periodic re-training of ML any are

used, e.g., updating a BERT model for propaganda detection with new data).

Each such update would be a new version and go through the same QA tests.

The Lead Engineer and **Data to coordinate these updates, ensuring all

integration points still work【2†L15-L23】【4†L29-L33】. Code reviews are

enforced for any changes (leveraging Git and perhaps pull request workﬂows)

【2†L49-L53】 to maintain code quality and consistency.

Finally, documentation is maintained: we have internal docs describing the

taxonomy, the scoring rationale, and how to interpret each feature. This helps

onboarding new team members and also helps in explaining the system’s

results to stakeholders (important for a system that might be used in media

consulting or analysis – clients will want to know why a certain article got a

certain score).

Pseudocode Summary: To tie everything together, here’s a pseudocode

walkthrough of the pipeline for grating all steps:

Python

Run

def analyze_document(doc, pipeline_version):

    # 1. Ingestion & Preprocessing

    raw_text = doc.fetch_content()  # get text from source (file, URL, etc.)

    metadata = doc.get_metadata()   #:contentReference[oaicite:217]{index=217}thor, etc.

    text = normalize_text(raw_text)  # cleaning, HTML removal, etc.

    lang = detect_language(text)

    sents = sentence_tokenize(text, lang)

    tokens = [tokenize(sent, lang) for sent in sents]:contentReference[oaicite:218]{index

    for token in tokens:

        token.pos = get_pos(token)

        token.lemma = get_lemma(token)

        token.is_stop = is_stopword(token, lang)

        token.ent_label = g:contentReference[oaicite:219]{index=219}:contentReference[oai

    argument_graph = build_argument_graph(sents)

    # 4. Feature Extraction

    features = {}

    features['num_sentences'] = len(sents)

    features['avg_sentence_length'] = sum(len(t) for t in tokens) / len(sents)

    features['passive_voice_ratio'] = calc_passive_ratio(sents)

    features['type_token_ratio'] = calc_type_token_ratio(tokens)

    features['sentiment_scores'] = [sentiment_analysis(sent) for sent in sents]

    features['sentiment_avg'] = sum(features['sentiment_scores'])/len(sents)

    features['emotion_counts'] = emotion_category_counts(text)

    features[':contentReference[oaicite:221]{index=221}:contentReference[oaicite:222]{ind

    features.update(entity_analysis(tokens, sents))  # e.g., sentiment per entity

    # (Add more feature calculations: bias indicators, etc.)

    # 5. Fallacy & Rhetorical Techniques Detection

    flags = {}

    # Example: Bandwagon

    bandwagon_terms = {"everyone","everybody","all of us","most people","the majority"}

    bandwagon_count = sum(1 for t in tokens if t.text.lower() in bandwagon_terms)

    bandwagon_score = bandwagon_count / len(tokens)

    if bandwagon_score > 0.01:  # threshold for significant usage

        flags["Bandwagon"] = True

        flags["Bandwagon_span"] = extract_span(text, bandwagon_terms)

    # Example: Appeal to Authority

    for sent in sents:

        if regex_search(r"\b(according to|expert|scientists say)\b", sent.text.lower()):

            if any(ent.label == "PERSON" for ent in sent.entities):

               :contentReference[oaicite:223]{index=223}eal_to_Authority"] = True

                # (We could store which person or the sentence as span)

                flags["Appeal_to_Authority_span"] = sent.text

    # ... other fallacy checks similarly ...

    # e.g., Ad Hominem via toxicity model

    for sent in sents:

        tox = toxicity_model(sent.text)

        if tox.score > 0.9 and any(ent.label == "PERSON" for ent in sent.entitie:contentR

            flags["Ad_Hominem_span"] = sent.text

    # 6. Taxonomy Classification

    labels = classify_taxonomy(features, flags)

    # (This could involve rule-based mapping or model predictions)

    # 7. Scoring

    scores = compute_scores(features, flags, labels)

    # e.g., scores['bias_score'] = 0.0

    # if flags contain serious issues, add to score accordingly

    if flags.get("Ad_Hominem"):

        scores['bias_score'] += 5

    if flags.get("Loaded_Language") or feat:contentReference[oaicite:226]{index=226}inant

        scores['bias_score'] += 5

    # ... etc for each category ...

    scores['bias_score'] = min(scores['bias_score'], 100)

    # 8. Output assembly

    result = {

       "doc_id": doc.id,

       "raw_text": raw_text,

       "clean_text": text,

       "language": lang,

       "features": features,

       "flags": flags,

       "labels": :contentReference[oaicite:227]{index=227}:contentReference[oaicite:228]{

       "pipeline_version": pipeline_version,

       "processed_at": current_timestamp()

    }

Comments: In this pseudocode, many helper functions ( normalize_text ,

tokenize , etc.) stand in for complex processes described earlier. The logic

shows how ﬂags are accumulated. For example, bandwagon detection simply

counts certain words and compares to a threshold【5†L42-L50】. Appeal to

authority looks for cue phrases plus a PERSON entity in the sentence【5†L62-

L70】【5†L88-L96】. Ad hominem uses a toxicity model score【41†L67-L70】.

The  classify_taxonomy  function would encapsulate the mapping from raw ﬂags

to high-level labels (like grouping multiple emotional indicators into "Propagao

Emotion"). Finally,  compute_scores  uses a simplistic additive scheme illustrated

for demonstration. In reality, the scoring might be more nuanced, but it will

deﬁnitely use the presence of ﬂags and magnitude of features as input.

This pseudocode also highlights how modular the pipeline is: each step can be

developed and tested and then they compose into the ﬁnal result.

Conclusion

This production-ready NLP pipeline architecture combines robust data

engineering practices with sophisticated NLP analysis to detect media bias

and manipulation. By leveraging a structured multi-layer approach – from

eaning to deep rhetorical analysis – the system ensures that each component’s

output is **deterministic, and easily updated. Key best practices have been

integrated throughout:

Structured Data Formats: JSONL for ingestion and Parquet for all

internal data to enable eﬃcient, schema-aware processing【36†】. A

canoni enforced across Bronze, Silver, Gold stages to avoid data drift and

ease integration with analysis tools【39†L379-L387】【40†L413-L420】.

Feature Layering: A thorough featuretrategy that builds from surface

features up to logical fallacies, ensuring that even subtle propaques are

captured【8†L189-L197】【8†L213-L221】. This layered design also helps in

debugging and extending the system – wy which layer each signal comes

from.

Taxonomy and Scoring: A predeﬁned taxonomy translates raw ﬁndings

into meaningful categoresults explainable to end-users and aligning with

project goals【4†L17-L25】【4†L21-L29】. The scoring matrix uses these

taxonomy outputs in formula to produce ﬁnal scores that are consistent

and tunable to stakeholder priorities.

Reproducibility and Versioning: Every data record carries version

metadata【32†L5-L13】, and the pipeline is engineered for determinism

(controlling randomness)【4†L61-L64】. This not only facilitates rigorous QA

testing【1†L19-L28】 but also builds trust – we can always retrace our steps

and reproduce an analysis exactly, which is crucial for an audit trail in a

media analysis context.

DevOps and Security: From containerized deployment to CI/CD, the

infrastructure side is handlnsuring that the pipeline runs reliably at scale

and that any changes go through proper testing and review【2†L31-L39】

【2†L21-L23】. Security best practices (authentication, data encryption)

protect the sensitive data ﬂowing through the system【2†L19-L27】

【2†L45-L53】.

QA and Monitoring: A comprehensive testing strategy catches issues

early and guarantees consistent outputs【1†L15-L23】【1†L25-L33】.

Continuous monitoring in production then closes the loop, alerting the team

to any anomalies or performance issues so they can be addressed before

they impact users.

By incorporating the responsibilities and insights of the Senior Lead Engineer,

Data/NLP Engineer, Backend Engineer, and QA Tester roles, we have a

pipeline that is not only technically sound but also aligned with real-world team

workﬂows. The lead engineer’s focus on reproducible results and secure

architecture is evident in our versioning and API design【2†L15-L23】【2†L35-

L38】. The data engineer’s domain expertise drove the complex feature and

taxonomy design, all while upholding determinism【4†L23-L30】【4†L25-L33】.

The backend engineer’s requirements for structured output and integration

informed the JSON output schema and API considerations【3†L18-L26】. And

the QA tester’s mandate for traceability and consistency inﬂuenced our exte,

testing, and documentation practices【1†L19-L27】【4†L63-L68】.

In essence, this document serves as a blueprint for building a media analysis

NLP pipeline that is comprehensive in capability and rigorous in execution. It

balances advanced NLP (for fallacy detection, etc.)ng (for speed, reliability, and

maintainability). Adhering to this design, a team can implement the system and

be conﬁdent in its outputs – every highlight and score it produces can be

explained and trusted, which is the ultimate goal in an analytical tool operating

under the scrutiny that media bias analysis demands.

Sources

ChatGPT can make mistakes. Check important info.

