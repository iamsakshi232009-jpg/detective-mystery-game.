import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Detective: Solve the Mystery", page_icon="🕵️", layout="wide")

BASE = Path(__file__).parent
ASSETS = BASE / "assets"

SUSPECTS = {
    "Rajiv Malhotra": {
        "role": "The host", "portrait": "rajiv_malhotra.png",
        "intro": "I invited everyone to see the Heera. I last saw it in the study before the lights flickered.",
        "questions": [
            ("Ask about the diamond", "I locked the case at 8:45. The study key stayed in my waistcoat pocket."),
            ("Ask about the window", "That window sticks. I did not open it tonight."),
            ("Ask about Arjun", "He asked me for money last week. I refused, but I never thought he would steal from family.")
        ]
    },
    "Meera Sharma": {
        "role": "The housekeeper", "portrait": "meera_sharma.png",
        "intro": "I have worked in this house for twelve years. I heard a floorboard creak near the study.",
        "questions": [
            ("Ask about the study", "I saw Arjun near the bookshelf around nine. He said he was looking for a poetry book."),
            ("Ask about the footprints", "Those prints look odd. The rain started after nine, but the room floor is too clean."),
            ("Ask about the spare key", "There is a spare study key. It used to be kept behind the poetry books.")
        ]
    },
    "Arjun Kapoor": {
        "role": "The nephew", "portrait": "arjun_kapoor.png",
        "intro": "Me? I was in the music room all evening. I never went near the study or touched the diamond.",
        "questions": [
            ("Ask about the window", "I did not go near it. I was nowhere near the study."),
            ("Ask about the green thread", "Lots of people wear green. That proves nothing."),
            ("Ask about the note", "I have no idea what that note means. You cannot accuse me over one letter.")
        ]
    }
}

CLUES = {
    "book": ("Book pulled out of place", "Behind a poetry book is a torn note: 'West window. 9:15. Bring the spare key. — A'. The initial is visible."),
    "box": ("Empty jewellery box", "The velvet case is empty and undamaged. The thief knew how to open it quietly."),
    "window": ("Open west window", "The latch has no fresh scratches. It could be opened from inside without force."),
    "footprints": ("Muddy footprints", "The prints point toward the window, not into the room. The inside floor is clean: the break-in may have been staged."),
    "fabric": ("Torn green fabric", "A piece of green fabric is caught on the rug near the fireplace. Its colour matches Arjun's blazer, but one clue alone is not proof."),
    "note": ("Partly burned note", "The surviving words read: '...sell it before morning'. Its torn edge matches the note hidden in the book.")
}

def init_state():
    defaults = {
        "page": "menu", "found": [], "questioned": [], "suspect": "Rajiv Malhotra",
        "dialogue": "", "selected_clue": None, "accusation": None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def new_game():
    st.session_state.found = []
    st.session_state.questioned = []
    st.session_state.suspect = "Rajiv Malhotra"
    st.session_state.dialogue = ""
    st.session_state.selected_clue = None
    st.session_state.accusation = None
    st.session_state.page = "scene"

def show_image(filename, caption=None, width=None):
    path = ASSETS / filename
    if path.exists():
        if width is None:
            st.image(str(path), caption=caption)
        else:
            st.image(str(path), caption=caption, width=width)
    else:
        st.warning(f"Image not found: {filename}")

init_state()

st.title("🕵️ DETECTIVE: SOLVE THE MYSTERY")
st.caption("CASE 001 • THE MISSING HEERA")
st.write("A priceless diamond has vanished from a Delhi mansion. Question everyone. Trust no one. Follow the evidence.")

if st.session_state.page == "menu":
    show_image("mansion_study.png", "The mansion study")
    st.subheader("Your case begins here")
    left, right = st.columns(2)
    with left:
        if st.button("🗝️ NEW GAME", use_container_width=True, type="primary"):
            new_game()
            st.rerun()
    with right:
        if st.button("CONTINUE CASE", use_container_width=True):
            st.session_state.page = "scene"
            st.rerun()
    st.info("Investigate six clues, interview three suspects, then make your accusation.")

elif st.session_state.page == "scene":
    st.subheader("The Mansion Study")
    show_image("mansion_study.png", "Look carefully around the room.")
    st.progress(len(st.session_state.found) / 6, text=f"Clues collected: {len(st.session_state.found)} / 6")
    st.markdown("### Investigate the evidence")
    clue_keys = list(CLUES.keys())
    cols = st.columns(3)
    for i, key in enumerate(clue_keys):
        with cols[i % 3]:
            title, _ = CLUES[key]
            if key in st.session_state.found:
                st.button(f"✓ {title}", key=f"done_{key}", disabled=True, use_container_width=True)
            elif st.button(f"🔎 {title}", key=f"clue_{key}", use_container_width=True):
                st.session_state.selected_clue = key
                st.session_state.page = "clue"
                st.rerun()
    st.divider()
    a, b, c = st.columns(3)
    with a:
        if st.button("📓 Detective's Notebook", use_container_width=True):
            st.session_state.page = "notebook"
            st.rerun()
    with b:
        if st.button("💬 Interview Suspects", use_container_width=True, type="primary"):
            st.session_state.page = "interview"
            st.rerun()
    with c:
        if st.button("⚖️ Make an Accusation", use_container_width=True):
            st.session_state.page = "accuse"
            st.rerun()

elif st.session_state.page == "clue":
    key = st.session_state.selected_clue
    if key not in CLUES:
        st.session_state.page = "scene"
        st.rerun()
    title, detail = CLUES[key]
    st.subheader("🔍 Evidence Discovered")
    st.markdown(f"### {title}")
    st.write(detail)
    st.info("Add this evidence to your notebook and compare it with the suspects' stories.")
    x, y = st.columns(2)
    with x:
        if st.button("ADD TO NOTEBOOK", type="primary", use_container_width=True):
            if key not in st.session_state.found:
                st.session_state.found.append(key)
            st.session_state.page = "scene"
            st.rerun()
    with y:
        if st.button("BACK TO ROOM", use_container_width=True):
            st.session_state.page = "scene"
            st.rerun()

elif st.session_state.page == "notebook":
    st.subheader("📓 Detective's Notebook")
    st.markdown("### Collected Evidence")
    if not st.session_state.found:
        st.info("No clues yet. Return to the room and inspect the evidence.")
    for key in st.session_state.found:
        title, detail = CLUES[key]
        with st.expander(title, expanded=False):
            st.write(detail)
    st.markdown("### Interview Records")
    if not st.session_state.questioned:
        st.info("No interviews yet.")
    else:
        for name in st.session_state.questioned:
            st.write(f"• {name}")
    a, b = st.columns(2)
    with a:
        if st.button("BACK TO ROOM", use_container_width=True):
            st.session_state.page = "scene"
            st.rerun()
    with b:
        if st.button("MAKE ACCUSATION", type="primary", use_container_width=True):
            st.session_state.page = "accuse"
            st.rerun()

elif st.session_state.page == "interview":
    st.subheader("💬 Suspect Interview")
    names = list(SUSPECTS.keys())
    selected = st.selectbox("Choose a suspect", names, index=names.index(st.session_state.suspect))
    st.session_state.suspect = selected
    person = SUSPECTS[selected]
    col1, col2 = st.columns([1, 2])
    with col1:
        show_image(person["portrait"], selected)
    with col2:
        st.markdown(f"### {selected}")
        st.caption(person["role"])
        st.write(person["intro"])
        st.markdown("#### Choose a question")
        for i, (question, answer) in enumerate(person["questions"]):
            if st.button(question, key=f"q_{selected}_{i}", use_container_width=True):
                st.session_state.dialogue = answer
                if selected not in st.session_state.questioned:
                    st.session_state.questioned.append(selected)
                st.rerun()
        if st.session_state.dialogue:
            st.success(st.session_state.dialogue)
    if st.button("BACK TO ROOM", use_container_width=True):
        st.session_state.page = "scene"
        st.rerun()

elif st.session_state.page == "accuse":
    st.subheader("⚖️ Who took the Heera?")
    st.write("Compare the clues and statements before you decide.")
    cols = st.columns(3)
    for i, name in enumerate(SUSPECTS):
        with cols[i]:
            person = SUSPECTS[name]
            show_image(person["portrait"], name)
            st.caption(person["role"])
            if st.button(f"ACCUSE {name.upper()}", key=f"accuse_{i}", use_container_width=True):
                st.session_state.accusation = name
                st.session_state.page = "ending"
                st.rerun()
    st.info(f"Evidence collected: {len(st.session_state.found)} / 6")
    if st.button("BACK TO NOTEBOOK", use_container_width=True):
        st.session_state.page = "notebook"
        st.rerun()

elif st.session_state.page == "ending":
    name = st.session_state.accusation
    st.subheader("Case Result")
    if name == "Arjun Kapoor" and len(st.session_state.found) >= 3:
        st.success("🎉 CASE SOLVED!")
        st.write("You caught Arjun Kapoor. The hidden note, green thread and staged footprints expose his story. He used the spare key to take the Heera and tried to make it look like a break-in. Rajiv recovers the diamond, and the mansion finally falls quiet.")
    elif name == "Arjun Kapoor":
        st.warning("RIGHT SUSPECT — NOT ENOUGH PROOF")
        st.write("Your suspicion is correct, but you need more evidence. Arjun denies everything and the case remains open. Return to the study, collect more clues and question the family again.")
    else:
        st.error("WRONG ACCUSATION!")
        st.write(f"You accused {name}. The evidence does not support that conclusion, and the real thief slips away. A good detective checks every clue before making a claim. Try again.")
    rating = "MASTER INVESTIGATOR" if len(st.session_state.found) >= 5 else "CASE STILL DEVELOPING"
    st.markdown(f"**Evidence gathered:** {len(st.session_state.found)} / 6")
    st.markdown(f"**Detective rating:** {rating}")
    a, b = st.columns(2)
    with a:
        if st.button("PLAY AGAIN", type="primary", use_container_width=True):
            new_game()
            st.rerun()
    with b:
        if st.button("MAIN MENU", use_container_width=True):
            st.session_state.page = "menu"
            st.rerun()

st.divider()
st.caption("Class 12 Python project • Built with Python and Streamlit • Your progress stays during this browser session.")
