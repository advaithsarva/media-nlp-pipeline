"""Downloads real published text to validate the detectors against.

The gold set in eval/gold/ was written by the same person who wrote the detectors, so it
cannot answer the question that actually matters: **how often do these detectors fire on
real prose that nobody was trying to trip them with?** That needs text written by other
people for other reasons.

Two corpora, both fetched live so nothing copyrighted is committed to this repo:

  neutral      Wikipedia article extracts. Encyclopaedic register, written under a
               neutral-point-of-view policy by people who had never heard of this project.
               Every detector firing here is a candidate false positive.
               Licence: CC BY-SA 4.0. Attribution is written into the manifest.

  rhetorical   Public-domain political speeches from Wikisource. Openly persuasive text.
               These are not labelled, so this is not a recall measurement -- it is a
               sanity check that the detectors are not simply inert on real argument.

    python -m evaluation.fetch_corpus --out eval/corpus

The downloaded text is gitignored. The script is committed, so the corpus is reproducible
without this repo redistributing anyone else's writing.
"""

import argparse
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

USER_AGENT = "NLPpipline-eval/1.0 (research; contact via repository)"

# Deliberately varied. Politics and history are included on purpose: those are the pages
# most likely to contain charged vocabulary while still being neutrally written, so they
# are the hardest precision test available for free.
NEUTRAL_PAGES = [
    "Forth Bridge", "Photosynthesis", "Byzantine Empire", "Great Barrier Reef",
    "Quantum entanglement", "Marie Curie", "Amazon rainforest", "Bank of England",
    "Cuban Missile Crisis", "Antibiotic resistance", "Silk Road", "Mount Everest",
    "European Union", "Industrial Revolution", "Vincent van Gogh", "Plate tectonics",
    "World Health Organization", "Suez Canal", "Chernobyl disaster", "Alan Turing",
    "Kyoto Protocol", "Spanish flu", "Apollo 11", "Magna Carta",
    "Gross domestic product", "Panama Canal", "Black Death", "Nikola Tesla",
    "Hubble Space Telescope", "Universal Declaration of Human Rights",
]

# Public-domain speeches on Wikisource. Openly persuasive by design.
RHETORICAL_PAGES = [
    "We shall fight on the beaches",
    "Blood, toil, tears, and sweat",
    "The Gettysburg Address",
    "Cross of Gold speech",
    "I Have a Dream",
    "The Man with the Muck-rake",
    "Their Finest Hour",
    "Give Me Liberty or Give Me Death",
    "First Inaugural Address of Franklin D. Roosevelt",
    "Ain't I a Woman?",
]


def _get_json(url, attempts=5):
    """GET with backoff. The API returns 429 freely and a bare loop trips it in seconds."""
    delay = 2.0
    last_error = None
    for attempt in range(attempts):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            last_error = error
            if error.code not in (429, 503):
                raise
            time.sleep(delay)
            delay *= 2      # 2, 4, 8, 16 seconds
        except Exception as error:
            last_error = error
            time.sleep(delay)
            delay *= 2
    raise last_error


def fetch_extract(title, site="en.wikipedia.org"):
    """Plain-text extract of one page. explaintext strips the wiki markup for us."""
    params = urllib.parse.urlencode({
        "action": "query",
        "prop": "extracts",
        "explaintext": "1",
        "format": "json",
        "redirects": "1",
        "titles": title,
    })
    data = _get_json("https://" + site + "/w/api.php?" + params)
    pages = data.get("query", {}).get("pages", {})
    for page_id, page in pages.items():
        if page_id == "-1":
            return None
        return {
            "title": page.get("title", title),
            "text": page.get("extract", ""),
            "url": "https://" + site + "/wiki/" + urllib.parse.quote(page.get("title", title).replace(" ", "_")),
        }
    return None


def fetch_group(titles, site, label, out_dir, max_chars, pause):
    folder = out_dir / label
    folder.mkdir(parents=True, exist_ok=True)
    manifest = []

    for title in titles:
        # resume: a page already on disk is not fetched again, so an interrupted run
        # can simply be restarted
        existing = folder / ("".join(c if c.isalnum() else "_" for c in title).strip("_").lower() + ".txt")
        if existing.exists() and existing.stat().st_size > 500:
            manifest.append({"title": title, "file": label + "/" + existing.name,
                             "url": "https://" + site + "/wiki/" + urllib.parse.quote(title.replace(" ", "_")),
                             "chars": len(existing.read_text(encoding="utf-8")), "site": site})
            print("  " + title + " (cached)")
            continue
        try:
            page = fetch_extract(title, site)
        except Exception as error:
            print("  skip " + title + ": " + str(error))
            continue
        if not page or not page["text"].strip():
            print("  skip " + title + ": no extract")
            continue

        # Trim to keep runs quick; the cut is on a paragraph boundary so no sentence is
        # left half-finished, which would create artificial segmentation errors.
        text = page["text"]
        if len(text) > max_chars:
            text = text[:max_chars].rsplit("\n\n", 1)[0]

        slug = "".join(c if c.isalnum() else "_" for c in page["title"]).strip("_").lower()
        target = folder / (slug + ".txt")
        target.write_text(text, encoding="utf-8")

        manifest.append({
            "title": page["title"],
            "file": label + "/" + target.name,
            "url": page["url"],
            "chars": len(text),
            "site": site,
        })
        print("  " + page["title"] + " (" + str(len(text)) + " chars)")
        time.sleep(pause)      # be polite to a free API

    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description="Fetch real text for detector validation.")
    parser.add_argument("--out", default="eval/corpus")
    parser.add_argument("--max-chars", type=int, default=12000)
    parser.add_argument("--pause", type=float, default=1.5)
    args = parser.parse_args(argv)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("neutral (Wikipedia, CC BY-SA 4.0):")
    neutral = fetch_group(NEUTRAL_PAGES, "en.wikipedia.org", "neutral",
                          out_dir, args.max_chars, args.pause)

    print("\nrhetorical (Wikisource, public domain):")
    rhetorical = fetch_group(RHETORICAL_PAGES, "en.wikisource.org", "rhetorical",
                             out_dir, args.max_chars, args.pause)

    manifest = {
        "neutral": {
            "documents": neutral,
            "source": "English Wikipedia",
            "licence": "CC BY-SA 4.0",
            "note": "Neutral-point-of-view encyclopaedic prose. Any detector firing here "
                    "is a candidate false positive.",
        },
        "rhetorical": {
            "documents": rhetorical,
            "source": "English Wikisource",
            "licence": "public domain",
            "note": "Openly persuasive speeches. Unlabelled, so this is a sanity check "
                    "that the detectors are not inert on real argument -- not a recall "
                    "measurement.",
        },
    }
    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("\n" + str(len(neutral)) + " neutral, " + str(len(rhetorical)) + " rhetorical")
    print("manifest: " + str(out_dir / "manifest.json"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
