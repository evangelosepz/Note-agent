import streamlit as st
from textblob import TextBlob
import dateparser

CATEGORY_KEYWORDS = {
    "task": ["να ", "πρέπει", "ολοκληρώσω", "πάρε", "στείλε"],
    "journal": ["σκέφτηκα", "ένιωσα", "πήγα", "είδα", "θυμάμαι"],
    "shopping": ["αγόρασε", "πάρε", "ψώνια", "λίστα"],
    "reminder": ["μην ξεχάσεις", "υπενθύμιση"]
}

def detect_category(text):
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(kw.lower() in text.lower() for kw in keywords):
            return category.capitalize()
    return "General"

def extract_tags(text):
    blob = TextBlob(text)
    return [word for (word, tag) in blob.tags if tag in ("NN", "NNS", "NNP", "NNPS")]

def extract_date(text):
    date = dateparser.parse(text, languages=["el"])
    return date.strftime("%Y-%m-%d") if date else "-"

st.set_page_config(page_title="Note Engine Lite", layout="centered")
st.title("Note Engine Lite")

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
