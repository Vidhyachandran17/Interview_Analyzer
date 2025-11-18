# modules/filler_words.py
def count_filler_words(text):
    """
    Counts filler words in the given text.
    """
    filler_list = ["um", "uh", "like", "you know", "hmm"]
    found = {}

    words = text.lower().split()

    for filler in filler_list:
        count = words.count(filler)
        if count > 0:
            found[filler] = count

    return found
