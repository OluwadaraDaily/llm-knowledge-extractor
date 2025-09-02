import nltk
from collections import Counter

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

def extract_three_most_common_nouns(text):
    words = nltk.word_tokenize(text.lower())
    tagged = nltk.pos_tag(words)
    nouns = [word for word, pos in tagged if pos.startswith("NN")]
    freq = Counter(nouns)
    return [word for word, _ in freq.most_common(3)]
