"""
TO READ:
* Nathalie Nahali - Webs of Influence - The psychology of online persuasion


https://copyblogger.com/proven-headline-formulas/

Headline strategies:

1. Say it simply and directly
   * Pure Silk Blouses … 30% Off
   * The Ultimate Tax Shelter
   * Proven Shortcuts for Starting Your Newsletter in Record Time

2. State the big benefit
   * Now! Moonlight Your Way to a Million Dollars
   * Create Your Own Cards, Posters, and Banners in Minutes
   * Get a FREE Vase When You Buy a Dozen Roses

3. Announce exciting news
   * At Last, American Scientists Have Created the Perfect Alternative to a
   Mined Diamond
   * Introducing the Newest Idea in Cross-Training, from NordicTrack
   * This Breakthrough in Driverless Cars Is Going to Change Everything

4. Appeal to the “how-to” instinct
   * How to Make Money Working from Home with Your PC
   * Stop Smoking in 30 days … or Your Money Back
   * Profit From the 3 Greatest Service Businesses of the Decade
   * Travel Central America on $17 a day

5. Pose a provocative question
   * Do You Make These Six Common Mistakes On Your Taxes?
   * Got a Speeding Ticket Recently? Read This
   * How Do I Know Which Mutual Funds Are Right for Me?

6. Bark a command
   * Grow Your Personal Brand on YouTube in 30 days
   * Call Anyone, Anywhere, without a Phone Line for FREE
   * Don't Risk Getting Hacked. Secure Your WordPress Site with iThemes Hosting

7. Offer useful information
   * The 20 Most Important Steps to Live Longer
   * The Best Kept Secrets in America [FREE]
   * Free Brochure Shows You How to End Your Money Worries for Good

8. Relay an honest, enthusiastic testimonial
   * “Quite simply, the finest design software ever released”
   * “This diet program worked for me. It can work for you, too”
   * “It's the first book on personal finance that really made sense to me”

9. Authenticate your proposition with a little something extra
   * Ohio Man Has 21-year Tested Formula to Create Multimillion-Dollar Business
   from Scratch, without Bank Loans, Venture Capitalists, or Selling Stock
   * Small Company's New Golf Ball Flies Too Far, Could Obsolete Many Golf Courses
   * Frustrated Bartender Develops Incredible Device to Clean and Disinfect Your
   Entire Home

10. Get relevant from the start
   * Have Two Left Feet? Even YOU Can Learn to Hip-Hop Dance with This Fail-Proof
   Method
   * The Easy Way to Fit Back into Your Favorite Pre-Pandemic Jeans
   * If You Don't Look at What's in Your Toothpaste Right Now, You'll Regret It
   Later

11. Add emotionally stirring and action words to your headline
   * Everyone in Our Community Has Lower Back Pain (but They Know How to Combat It)
   * Get Ready to Turn the Tables the Next Time You See Your Old Boss
   * 10 Smart Tips that Transform Your Dull Workspace into a Productivity Paradise

Persuasive words:
1. You
2. Free
3. Because
4. Instantly
5. New


To introduce your topic
* Picture this ...
* Although it's commonly believed ...
* When was the last time you ... ?
* I'm sure you've heard of [blank], but ...
* Ready to discover a new way to ... ?

To make a point
* Also ...
* In other words ...
* Therefore ...
* Supporting evidence shows ...
* I reached this conclusion after finding ...

To support your point
* For example ...
* Especially in this case ...
* In fact ...
* According to this study ...
* Independent test results show ...

To end your case
* In conclusion ...
* To wrap things up ...
* As you understand by now ...
* Try [blank] for yourself, if you want to see similar results.
* Got it?
"""

import json
import random
import string
from itertools import chain

from humanize_lite import spell_number, pluralize


TRIGGER_WORDS = [
    "weird",
    "surprising",
    "secret",
    "mystery",
    "strange",
    "outrageous",
    "odd",
    "amazing",
    "bizarre",
    "essential",
    "incredible",
    # Health and hope
    "boost",
    "cure",
    "energize",
    "flush",
    "vibrant",
    "bright",
    "destiny",
    "empower",
    "overcome",
    "undo",
    # Anger and frustration
    "Arrogant",
    "Cruel",
    "Greed",
    "Hate",
    "Unscrupulous",
    "Had enough",
    "Never again",
    "Pointless",
    "Temporary fix",
    "Tired",
    # Betrayal and Revenge
    "Burned",
    "Conspiracy",
    "Disinformation",
    "Fleece",
    "Swindle",
    "Avenge",
    "Payback",
    "Reclaim",
    "Turn the tables",
    "Vindication",
    # The Forbidden and the Powerless
    "Banned",
    "Controversial",
    "Exposed",
    "Insider",
    "Taboo",
    "Agony",
    "Floundering",
    "Helpless",
    "Paralyzed",
    "Surrender",
    # Passion and Urgency
    "Blissful",
    "Delightful",
    "Jubilant",
    "Rave",
    "Thrilled",
    "Before you forget",
    "Deadline",
    "Limited",
    "Seize",
    "While it's fresh in your mind",
    # Attraction
    "Delicious",
    "Exceptional",
    "Satisfaction guaranteed",
    "Easy",
    "Unparalleled",
    # Love
    "Deep",
    "Natural",
    "Comfort",
    "Peace",
    "Joy",
    # Trust
    "Proven",
    "Third-party tested",
    "Backed by science",
    "Evidence-based research",
    "Pure",
]
SAMPLE_THIS = """
Sensory power words #1: Visual words
1. Bulky
2. Crooked
3. Drab
4. Gigantic
5. Glittering
6. Gloomy
7. Glow, glowing, to glow
8. Hazy
9. Shadowy
10. To shimmer, shimmering
11. To sparkle, sparkling

Emotional power words #2: Trust
12. Absolutely
13. Admiration, to admire
14. Authoritative, authority
15. Facts, factual
16. Faith, faithful
17. Fool-proof, sure-fire
18. Guaranteed
19. Proven
20. Reliable, reliability
21. Research-backed
22. Saint
23. Scientific, science
24. Trustworthy

Emotional power words #3: Fear
25. Abuse, abusive
26. Anxiety, anxious
27. Banned
28. Burning out
29. Despair
30. Failure, to fail
31. Freaking out
32. Horror
33. Miserable
34. Pussyfoot
35. Sabotage
36. Steal, stolen, plunder
37. Threat

Emotional power words #4: Surprise
38. Awe
39. Jaw-dropping
40. Mind-blowing
41. Mesmerizing
42. Spectacular
43. Remarkable
44. Enchantment, enchanting, to enchant
45. Astonishing
46. Terrific
47. Breath-taking
48. Spellbinding
49. To beguile
50. To bewitch

Emotional power words #5: Sadness
51. Austerity
52. Envy, envious
53. Grief-stricken
54. Heartbroken
55. Hostile
56. Lovesick
57. Resentful
58. Shame
59. Sobbing, to sob
60. Tearful
61. Teary-eyed
62. Troubled, trouble
63. Weepy

Emotional power words #6: Disgust
64. Crap, crappy
65. Icky
66. Junk
67. Lousy
68. Nasty
69. Obscene
70. Outrageous
71. Repellent, to repel, repulsive
72. Ridiculous
73. Scuzzy
74. Shit, shitty
75. Trash, trashy
76. Vulgar

Emotional power words #7: Anger
77. Annoying
78. Bitter
79. Flare up
80. Frenzy, frantic
81. Fury, furious
82. Grumpy
83. Hatred, to hate
84. Hysterics
85. Irritating
86. Panic
87. Rage, raging
88. Tantrum
89. To sulk

Emotional power words #8: Anticipation
90. Charming, to charm
91. Craving, crave
92. Discovery, to discover
93. Enthusiasm, to enthuse
94. Forgotten
95. Inspiration, to inspire
96. Little-known
97. Longing, to long for
98. Lust
99. Mystery, Mysterious
100. Passion, passionate
101. To woo
102. Yearning, to yearn
"""


NOUNS = None
# NO FLAT?
VERBS = None
VERBS_FLAT = None
ADJECTIVES = None
ADJECTIVES_FLAT = None

TRIGGER_ADJECTIVES = list()
TRIGGER_NOUNS = list()
TRIGGER_VERBS = list()


def load_nouns():
    global NOUNS

    with open("english-nouns.json") as textfile:
        data = json.load(textfile)

    print(f".:. loaded {len(data)} nouns")

    assert isinstance(data, list)
    NOUNS = data


def load_verbs():
    global VERBS
    global VERBS_FLAT

    with open("english-verbs.json") as textfile:
        data = json.load(textfile)

    print(f".:. loaded {len(data)} verbs")

    assert isinstance(data, dict)
    VERBS = data
    VERBS_FLAT = list(data.keys())


def load_adjectives():
    global ADJECTIVES
    global ADJECTIVES_FLAT

    with open("english-adjectives.json") as textfile:
        data = json.load(textfile)

    print(f".:. loaded {len(data)} adjectives")

    assert isinstance(data, dict)
    ADJECTIVES = data
    ADJECTIVES_FLAT = list(data.keys())


def load_trigger_words():
    global TRIGGER_NOUNS
    global TRIGGER_ADJECTIVES
    global TRIGGER_VERBS

    nouns = set(NOUNS)

    adjectives = set(ADJECTIVES_FLAT)
    verbs = set(VERBS_FLAT)

    for word in chain(TRIGGER_WORDS, SAMPLE_THIS.split("\n")):
        for real_word in word.lower().split():
            real_word = real_word.strip(string.punctuation)
            if real_word in nouns:
                TRIGGER_NOUNS.append(real_word)
            elif real_word in adjectives:
                TRIGGER_ADJECTIVES.append(real_word)
            elif real_word in verbs:
                TRIGGER_VERBS.append(real_word)
            # else:
            #     print("Cannot find a suitable category for", real_word)


def load_all_words():
    load_nouns()
    load_verbs()
    load_adjectives()
    load_trigger_words()


def make_promise():

    action = random.choice(VERBS_FLAT)
    action_ing = random.choice(VERBS[action]["present_participle"])
    subject = random.choice(NOUNS)
    characteristic = random.choice(ADJECTIVES_FLAT)

    forms = [
        f"that will {action} your {characteristic} {subject}",
        f"for {action_ing} your {characteristic} {subject}",
        f"to {action} your {characteristic} {subject}",
        f"you cannot {action} the {characteristic} {subject} enough",
        f"would you {action} the {characteristic} {subject} {action}",
    ]

    return random.choice(forms)


def make_headline(something):
    """
    Generate a random headline:
    Number + trigger word + adjective + keyword + promise
    """
    assert TRIGGER_ADJECTIVES
    assert TRIGGER_NOUNS
    assert TRIGGER_VERBS

    magic_numbers = range(1, 22)

    number = random.choice(magic_numbers)
    keyword = pluralize(random.choice(NOUNS), number)
    adjective = random.choice(ADJECTIVES_FLAT)
    promise = make_promise()

    words = [
        spell_number(number),
        adjective,
        keyword,
        promise,
    ]

    headline = " ".join(words)
    return headline.capitalize()


def make_sentence():

    subject = random.choice(NOUNS)
    trait = random.choice(ADJECTIVES_FLAT)
    action = random.choice(VERBS_FLAT)
    action_ing = random.choice(VERBS[action]["present_participle"])
    characteristic = random.choice(ADJECTIVES_FLAT)
    object = random.choice(NOUNS)
    magic_numbers = range(1, 22)
    number = random.choice(magic_numbers)

    forms = [
        f"somtimes the {trait} {subject} can {action} most {characteristic} {pluralize(object, 2)}.",
        f"{trait} {subject} can {action} almost any {characteristic} {object}.",
        f"quite often {spell_number(number)} {trait} {subject} will {action} {characteristic} {object}.",
        f"imagine this, {spell_number(number)} {trait} {subject} {action_ing} one {characteristic} {object}.",
        f"while {spell_number(number)} {trait} {subject} are {action_ing} then {characteristic} {object}...",
        f"who could {action} the {trait} {subject} without {characteristic} {object}?",
        f"I bet you cannot {action} the {trait} {subject}, not even the {characteristic} {object}.",
        f"{trait} {subject} will never {action} the {characteristic} {object}, no matter what!",
    ]

    return random.choice(forms)


if __name__ == "__main__":
    load_all_words()

    for i in range(13):
        head = make_headline("anything")
        print("\t", head)
