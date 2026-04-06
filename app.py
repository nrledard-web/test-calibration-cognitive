import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Test de calibration cognitive",
    page_icon="🧠",
    layout="wide",
)
st.set_page_config(
    page_title="Test de calibration cognitive",
    page_icon="🧠",
    layout="wide",
)

st.image("a_digital_graphic_banner_for_the_cognitive_calibra.png", use_container_width=True)

st.title("Test de calibration cognitive")
# -----------------------------
# Données du test
# -----------------------------
QUESTIONS = [
    "Je comprends réellement comment fonctionne l’économie mondiale.",
    "Je pourrais expliquer clairement pourquoi certaines théories complotistes séduisent autant de gens.",
    "Je suis capable d’expliquer comment fonctionne une intelligence artificielle moderne.",
    "Je comprends vraiment les causes profondes du changement climatique.",
    "Je pourrais expliquer simplement comment fonctionne un vaccin.",
    "Je comprends pourquoi des personnes intelligentes peuvent croire à des choses fausses.",
    "Je pourrais expliquer comment fonctionne réellement la démocratie dans mon pays.",
    "Je comprends pourquoi certaines informations deviennent virales sur internet.",
    "Je pourrais expliquer clairement ce qu’est une inflation économique.",
    "Je comprends comment les algorithmes influencent ce que je vois en ligne.",
    "Je comprends pourquoi les gens changent rarement d’avis sur des sujets importants.",
    "Je pourrais expliquer pourquoi certaines décisions politiques semblent absurdes mais persistent.",
    "Je comprends comment mes propres biais cognitifs influencent mes jugements.",
    "Je pourrais expliquer comment se construit une théorie scientifique.",
    "Je comprends pourquoi certaines idées simples semblent si convaincantes.",
    "Je pourrais expliquer clairement pourquoi des experts peuvent se tromper.",
    "Je comprends comment mes opinions ont évolué au cours de ma vie.",
    "Je pourrais expliquer ce qui distingue une opinion d’une connaissance solide.",
    "Je comprends pourquoi certaines personnes paraissent très sûres d’elles tout en ayant tort.",
    "Je pourrais expliquer pourquoi moi-même je pourrais me tromper sur des sujets importants.",
]

PROFILES = [
    {
        "name": "Le Prophète Certain",
        "condition": lambda score: score < -2,
        "emoji": "🗿",
        "description": (
            "Votre certitude tend à dépasser votre ancrage. "
            "Vous avez le panache du verdict, mais parfois moins le poids du sol sous les pieds."
        ),
    },
    {
        "name": "Le Mécroyant Serein",
        "condition": lambda score: -2 <= score < 1,
        "emoji": "🎭",
        "description": (
            "Vous avancez avec assurance, parfois un peu trop, parfois juste assez. "
            "Votre rapport au savoir est stable, mais il gagne encore à être frotté à la contradiction."
        ),
    },
    {
        "name": "Le Sceptique Vigilant",
        "condition": lambda score: 1 <= score < 4,
        "emoji": "🕯️",
        "description": (
            "Votre certitude reste globalement proportionnée à votre compréhension. "
            "Vous savez douter sans vous dissoudre. C’est rare, et presque élégant."
        ),
    },
    {
        "name": "L’Arpenteur du Doute",
        "condition": lambda score: score >= 4,
        "emoji": "🌌",
        "description": (
            "Vous semblez faire preuve d’une prudence intellectuelle solide. "
            "Vous n’épousez pas trop vite vos certitudes, ce qui est souvent le signe d’un esprit bien charpenté."
        ),
    },
]


# -----------------------------
# Fonctions
# -----------------------------
def score_question(g: int, n: int, d: int) -> int:
    return (g + n) - d


def interpret_score(avg_score: float) -> str:
    if avg_score < 0:
        return (
            "Votre certitude moyenne dépasse votre ancrage moyen. "
            "Cela suggère une tendance possible à la fermeture cognitive : "
            "on croit tenir, alors qu’on tient parfois surtout à croire."
        )
    if 0 <= avg_score < 3:
        return (
            "Votre calibration est intermédiaire. Vous n’êtes ni prisonnier de vos certitudes, "
            "ni parfaitement ajusté à vos limites. Terrain vivant, donc intéressant."
        )
    if 3 <= avg_score < 6:
        return (
            "Votre calibration paraît bonne. Votre niveau de certitude reste assez cohérent "
            "avec ce que vous savez expliquer et ce que vous avez réellement confronté."
        )
    return (
        "Votre prudence intellectuelle semble forte. Vous ne confondez pas trop vite impression de comprendre "
        "et compréhension véritable. C’est une qualité rare, presque une hygiène de l’âme."
    )


def find_profile(avg_score: float) -> dict:
    for profile in PROFILES:
        if profile["condition"](avg_score):
            return profile
    return PROFILES[-1]


def reset_test():
    for i in range(len(QUESTIONS)):
        for suffix in ["d", "g", "n"]:
            key = f"{suffix}_{i}"
            if key in st.session_state:
                del st.session_state[key]


# -----------------------------
# Interface
# -----------------------------
st.title("🧠 Test de calibration cognitive")
st.markdown(
    """
Ce test explore le rapport entre :

- **D** : votre niveau de certitude
- **G** : votre capacité à expliquer
- **N** : votre expérience ou confrontation réelle au sujet

La formule utilisée est :

### **M = (G + N) − D**

Plus votre score est élevé, plus votre certitude semble proportionnée à votre ancrage.  
Plus il est négatif, plus la certitude risque de précéder la compréhension.
"""
)

with st.expander("Mode d’emploi", expanded=False):
    st.write(
        """
Pour chaque affirmation, réglez trois curseurs de **0 à 10** :

- **Certitude** : à quel point vous êtes sûr de votre compréhension
- **Capacité à expliquer** : à quel point vous pourriez l’expliquer clairement à quelqu’un
- **Expérience réelle** : à quel point vous avez étudié, expérimenté ou sérieusement confronté le sujet

Il ne s’agit pas d’un test clinique, ni d’un jugement moral.  
C’est un miroir. Et les miroirs, parfois, ont le mauvais goût d’être polis.
"""
    )

col_left, col_right = st.columns([3, 1])

with col_right:
    st.button("Réinitialiser le test", on_click=reset_test, use_container_width=True)

responses = []

for i, question in enumerate(QUESTIONS, start=1):
    progress = i / len(QUESTIONS)
    st.progress(progress)
    st.write(f"Question {i} sur {len(QUESTIONS)}")

    st.markdown("---")
    st.subheader(f"Question {i}")
    st.write(question)

    col1, col2, col3 = st.columns(3)

    with col1:
        d = st.slider(
            f"Certitude — Q{i}",
            min_value=0,
            max_value=10,
            value=5,
            key=f"d_{i-1}",
            help="À quel point êtes-vous sûr de votre compréhension ?",
        )

    with col2:
        g = st.slider(
            f"Capacité à expliquer — Q{i}",
            min_value=0,
            max_value=10,
            value=5,
            key=f"g_{i-1}",
            help="Pourriez-vous l’expliquer clairement à quelqu’un ?",
        )

    with col3:
        n = st.slider(
            f"Expérience réelle — Q{i}",
            min_value=0,
            max_value=10,
            value=5,
            key=f"n_{i-1}",
            help="Avez-vous réellement étudié ou confronté ce sujet ?",
        )

    m = score_question(g, n, d)

    responses.append(
        {
            "question": question,
            "d": d,
            "g": g,
            "n": n,
            "m": m,
        }
    )

st.markdown("---")

if st.button("Calculer mon score", type="primary", use_container_width=True):
    total_score = sum(item["m"] for item in responses)
    avg_score = total_score / len(responses)

    avg_d = sum(item["d"] for item in responses) / len(responses)
    avg_g = sum(item["g"] for item in responses) / len(responses)
    avg_n = sum(item["n"] for item in responses) / len(responses)

    profile = find_profile(avg_score)

    st.success("Résultat calculé.")

    st.markdown("## Résultat final")
    score_col, detail_col = st.columns([1, 2])

    with score_col:
        st.metric("Score moyen M", f"{avg_score:.2f}")
        st.metric("Certitude moyenne (D)", f"{avg_d:.2f}")
        st.metric("Explication moyenne (G)", f"{avg_g:.2f}")
        st.metric("Expérience moyenne (N)", f"{avg_n:.2f}")

    data = {
        "Certitude": avg_d,
        "Explication": avg_g,
        "Expérience": avg_n
    }

    fig = px.bar(
        x=list(data.keys()),
        y=list(data.values()),
        title="Votre calibration cognitive"
    )

    st.plotly_chart(fig, use_container_width=True)

    with detail_col:
        st.markdown(f"### {profile['emoji']} {profile['name']}")
        st.write(profile["description"])
        st.info(interpret_score(avg_score))

    st.markdown("## Votre profil")
    st.write(profile["name"])

    st.markdown("## Lecture rapide")
    if avg_score < 0:
        st.error(
            "Votre certitude tend à dépasser votre ancrage. "
            "Le risque n’est pas d’être stupide, mais d’être trop vite convaincu."
        )
    elif avg_score < 3:
        st.warning(
            "Votre équilibre cognitif est mitigé. "
            "Vous avez une base, mais certaines certitudes semblent encore courir devant le reste."
        )
    elif avg_score < 6:
        st.success(
            "Bonne calibration globale. "
            "Vous semblez assez bien proportionner confiance et compréhension."
        )
    else:
        st.success(
            "Très belle prudence intellectuelle. "
            "Vous semblez préférer la clarté lente au confort des certitudes rapides."
        )

    st.markdown("## Questions où votre score est le plus faible")
    lowest = sorted(responses, key=lambda x: x["m"])[:3]
    for item in lowest:
        st.write(
            f"- **{item['question']}** → M = **{item['m']}** "
            f"(G={item['g']}, N={item['n']}, D={item['d']})"
        )

    st.markdown("## Questions où votre score est le plus élevé")
    highest = sorted(responses, key=lambda x: x["m"], reverse=True)[:3]
    for item in highest:
        st.write(
            f"- **{item['question']}** → M = **{item['m']}** "
            f"(G={item['g']}, N={item['n']}, D={item['d']})"
        )

    st.markdown("## Remarque")
    st.caption(
        "Ce test propose une lecture heuristique de la calibration cognitive. "
        "Il ne mesure pas la vérité de vos opinions, mais le rapport entre votre assurance "
        "et l’ancrage que vous déclarez."
    )
