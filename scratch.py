def summarize(text: str, max_words: int = 50) -> str:
    words = text.split()
    return " ".join(words[:max_words])

# Hints don't enforce anything at runtime — they document and enable tooling:
result = summarize("a long piece of text here", max_words=3)

# Modern syntax you'll see everywhere (3.10+):
def find_user(user_id: int) -> dict | None:   # returns a dict OR None
    ...

def tag_counts(tags: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for t in tags:
        counts[t] = counts.get(t, 0) + 1
    return counts

def word_count(text: str) -> int:
    words = text.split()
    print(words)
    length = len(words)
    print(length)
    return length

def unique_tags(tags: list[str]) -> list[str]:
    return list(set(tags))

def first_match(items: list[str], needle: str) -> str | None:
    for item in items:
        if item == needle:
            return item
    return None


print(first_match(["apple", "banana", "orange"], "banana"))
