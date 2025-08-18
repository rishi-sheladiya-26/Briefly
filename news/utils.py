import re
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Download required NLTK data (run once)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def summarize_text(text, max_sentences=3):
    """
    Create a simple extractive summary of the text
    """
    if not text or len(text) < 100:
        return text
    
    try:
        # Clean and preprocess text
        text = clean_text(text)
        
        # Split into sentences
        sentences = sent_tokenize(text)
        if len(sentences) <= max_sentences:
            return text
        
        # Score sentences based on word frequency
        word_freq = get_word_frequency(text)
        sentence_scores = score_sentences(sentences, word_freq)
        
        # Get top sentences
        top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:max_sentences]
        
        # Sort by original order and join
        top_sentences.sort(key=lambda x: sentences.index(x[0]))
        summary = ' '.join([sent for sent, score in top_sentences])
        
        return summary
    
    except Exception as e:
        print(f"Error in summarization: {e}")
        # Fallback: return first few sentences
        sentences = text.split('.')[:max_sentences]
        return '. '.join(sentences) + '.'

def clean_text(text):
    """
    Clean and preprocess text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep sentence endings
    text = re.sub(r'[^\w\s\.\!\?]', ' ', text)
    
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def get_word_frequency(text):
    """
    Get frequency of important words in text
    """
    try:
        # Get English stopwords
        stop_words = set(stopwords.words('english'))
        
        # Tokenize and filter
        words = word_tokenize(text.lower())
        words = [word for word in words if word.isalnum() and word not in stop_words and len(word) > 2]
        
        # Get frequency
        word_freq = Counter(words)
        
        # Normalize frequencies
        max_freq = max(word_freq.values()) if word_freq else 1
        for word in word_freq:
            word_freq[word] = word_freq[word] / max_freq
        
        return word_freq
    
    except Exception as e:
        print(f"Error in word frequency calculation: {e}")
        return {}

def score_sentences(sentences, word_freq):
    """
    Score sentences based on word frequencies
    """
    sentence_scores = {}
    
    for sentence in sentences:
        words = word_tokenize(sentence.lower())
        words = [word for word in words if word.isalnum()]
        
        score = 0
        word_count = 0
        
        for word in words:
            if word in word_freq:
                score += word_freq[word]
                word_count += 1
        
        if word_count > 0:
            sentence_scores[sentence] = score / word_count
        else:
            sentence_scores[sentence] = 0
    
    return sentence_scores

def simple_summarize(text, max_length=300):
    """
    Simple summarization by taking first few sentences
    """
    if not text:
        return ""
    
    sentences = text.split('.')
    summary = ""
    
    for sentence in sentences:
        if len(summary + sentence) > max_length:
            break
        summary += sentence + ". "
    
    return summary.strip()

def test_summarization():
    """
    Test the summarization function
    """
    sample_text = """
    The quick brown fox jumps over the lazy dog. This is a sample text for testing 
    the summarization algorithm. The algorithm works by analyzing word frequencies 
    and scoring sentences based on the important words they contain. This helps in 
    extracting the most relevant sentences from a longer text. The final summary 
    should contain the most important information from the original text.
    """
    
    print("Original text:")
    print(sample_text)
    print("\nSummary:")
    print(summarize_text(sample_text))

if __name__ == "__main__":
    test_summarization()
