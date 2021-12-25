import csv
import json
import re


def symbolic_name(text):
    words = re.findall(r"(\w+)|[^\w\s]", text.lower())
    return "_".join(filter(lambda x: x, words))


def digest_english_verbs():
    basic = re.compile("^\d+\.\s+(\w+)\s*")

    with open("res/common-verbs.txt") as textfile:
        content = textfile.readlines()

    common_verbs = set()
    for line in content:
        if m := basic.match(line):
            common_verbs.add(m.group(1))

    all_verbs = dict()

    with open("res/english-verbs.csv") as csvfile:
        reader = csv.reader(csvfile)

        verb_form = tuple(symbolic_name(name) for name in next(reader))

        for row in reader:
            verb = dict()
            for i, value in enumerate(row):
                form_key = verb_form[i]
                verb[form_key] = re.findall(r"\w+", value)
            base_form = row[0]
            verb["is_common"] = base_form in common_verbs
            all_verbs[base_form] = verb

    with open("english-verbs.json", "wt") as file:
        json.dump(all_verbs, file, indent=4)

    print(len(all_verbs), "verbs saved to json")


def digest_english_nouns():
    nouns = set()

    with open("res/english-nouns.csv") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[1]:
                nouns.add(row[1])
            else:
                print("noun row data seems corrupted:", row)

    with open("english-nouns.json", "wt") as file:
        json.dump(list(nouns), file, indent=4)

    print(len(nouns), "nouns saved to json")


def digest_english_adjectives():
    adjectives = set()

    with open("res/english-adjectives.csv") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[1]:
                adjectives.add(row[1])
            else:
                print("adjective row data seems corrupted:", row)

    print(f"{len(adjectives)} adjectives found")

    common_adjectives = dict()
    with open("res/most-common-adjectives-english.csv") as csvfile:
        reader = csv.reader(csvfile)

        header = tuple(symbolic_name(name) for name in next(reader))

        for row in reader:
            base_form, comparative, superlative = row

            comparative_forms = comparative.split()
            use_more = "more" in comparative_forms
            if use_more:
                comparative_forms.remove("more")

            superlative_forms = superlative.split()
            use_most = "most" in superlative_forms
            if use_most:
                superlative_forms.remove("most")

            adjective = dict(
                base=base_form,
                comparative_forms=comparative_forms,
                use_more=use_more,
                superlative_forms=superlative_forms,
                use_most=use_most,
            )
            common_adjectives[base_form] = adjective

    with open("english-adjectives.json", "wt") as file:
        json.dump(common_adjectives, file, indent=4)

    print(len(common_adjectives), "common adjectives saved to json")


if __name__ == "__main__":
    digest_english_verbs()
    digest_english_nouns()
    digest_english_adjectives()
