import streamlit as st
import spacy
import dateparser
from collections import Counter

# Load English NLP model
nlp = spacy.load("en_core_web_sm")

# Κατηγορίες με βάση λέξεις-κλειδιά
CATEGORY_KEYWORDS = {
    "task": ["να ", "πρέπει", "ολοκληρώσω", "πάρε", "στείλε"],
    "journal": ["σκέφτηκα", "ένιωσα", "πήγα", "είδα", "θυμάμαι"],
    "shopping": ["αγόρασε", "πάρε", "ψώνια", "λίστα"],
    "reminder": ["μην ξεχάσεις", "υπενθύμιση"]
}

# Ανίχνευση κατηγορίας
def detect_category(text):
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(kw.lower() in text.lower() for kw in keywords):
            return category.capitalize()
    return "General"

# Εξαγωγή tags (ουσιαστικά & ονόματα)
def extract_tags(text):
    doc = nlp(text)
    return [token.text for token in doc if token.pos_ in ("NOUN", "PROPN") and not token.is_stop]

# Εξαγωγή ημερομηνίας
def extract_date(text):
    date = dateparser.parse(text, languages=["el"])
    return date.strftime("%Y-%m-%d") if date else "-"

# Streamlit UI
st.set_page_config(page_title="Giorgo's Note Engine", layout="centered")
st.title("Note Analysis Engine - Giorgo")

note = st.text_area("Γράψε εδώ τη σημείωση σου")

if st.button("Ανάλυση"):
    if note.strip():
        category = detect_category(note)
        tags = extract_tags(note)
        date = extract_date(note)

        st.subheader("Ανάλυση:")
        st.write(f"**Κατηγορία:** {category}")
        st.write(f"**Tags:** {', '.join(tags) if tags else '-'}")
        st.write(f"**Ημερομηνία:** {date}")
    else:
        st.warning("Παρακαλώ γράψε κάτι πρώτα.")
