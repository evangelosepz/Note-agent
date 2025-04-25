import streamlit as st
import dateparser
import re

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
    words = re.findall(r'\b[\w\-άέίήύόώΆΈΊΉΎΌΏ]+\b', text.lower())
    common_words = {"και", "το", "να", "που", "σε", "με", "για", "στην", "της", "της", "ένα", "μια"}
    tags = [word for word in words if word not in common_words and len(word) > 3]
    return list(set(tags))[:10]

def extract_date(text):
    date = dateparser.parse(text, languages=["el"])
    return date.strftime("%Y-%m-%d") if date else "-"

st.set_page_config(page_title="Note Engine Minimal", layout="centered")
st.title("Note Engine - Τελική έκδοση")

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
