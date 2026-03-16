import json
import spacy
from spacy.tokens import DocBin
from spacy.util import filter_spans
import re

files = ["train", "dev", "test"]

skills_set = set()

def clean_text(text,
               remove_emails=False,
               remove_parentheses=False,
               split_hyphens=False,
               remove_special_char=False):

    if remove_emails:
        text = re.sub(r"\S+@\S+", " ", text)

    if remove_parentheses:
        text = re.sub(r"\(.*?\)", " ", text)

    if split_hyphens:
        text = text.replace("-", " ")

    if remove_special_char:
        text = re.sub(r"[^a-zA-Z\s]", " ", text)

    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()

    return text

def bio_to_spans(tokens, tags):
    spans = []
    start = None
    for i, tag in enumerate(tags):
        if tag == "B":
            start = i
        elif tag == "O" and start is not None:
            spans.append((start, i))
            start = None
    if start is not None:
        spans.append((start, len(tokens)))
    return spans


if __name__ == "__main__":
    nlp = spacy.load(
        "en_core_web_sm",
        disable=["parser", "ner"]
    )
    
    for file in files:
        INPUT_FILE = "./data/" + file + ".json"
        OUTPUT_FILE = "./data/" + file + ".spacy"

        doc_bin = DocBin()

        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            for line in f:
                data = json.loads(line)
                tokens = data["tokens"]

                tags_skill = data.get("tags_skill", ["O"] * len(tokens))
                tags_knowledge = data.get(
                    "tags_knowledge", ["O"] * len(tokens))

                if all(t == "O" for t in tags_skill) and all(t == "O" for t in tags_knowledge):
                    continue

                text = " ".join(tokens)
                doc = nlp.make_doc(text)

                spans_skill = bio_to_spans(tokens, tags_skill)
                spans_knowledge = bio_to_spans(tokens, tags_knowledge)
                spans = spans_skill + spans_knowledge

                token_positions = []
                char_pos = 0

                for token in tokens:
                    start = char_pos
                    end = start + len(token)
                    token_positions.append((start, end))
                    char_pos = end + 1

                entities = []

                for start, end in spans:
                    span = doc.char_span(
                        token_positions[start][0],
                        token_positions[end - 1][1],
                        label="SKILL"
                    )

                    if span:
                        entities.append(span)
                        skills_set.add(span.text.lower().strip())

                entities = filter_spans(entities)
                doc.ents = entities
                doc_bin.add(doc)

        doc_bin.to_disk(OUTPUT_FILE)
        print(f"{file}.spacy created")

    with open("skills_dictionary.txt", "w", encoding="utf-8") as f:
        for skill in sorted(skills_set):
            f.write(skill + "\n")

    print("skills_dictionary.txt created")
    print("Total unique skills:", len(skills_set))
