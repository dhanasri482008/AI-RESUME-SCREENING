import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

from utils.parser import extract_text
from utils.preprocess import clean_resume
from utils.nlp_pipeline import preprocess_nlp
from utils.skill_extractor import extract_skills
from utils.matcher import match_skills
from utils.similarity import semantic_similarity


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

/* Background */
.stApp,
[data-testid="stAppViewContainer"]{
    background:#07170E;
    color:white;
}

[data-testid="stHeader"]{
    background:transparent;
}

/* Text */
h1,h2,h3,h4,h5,h6,p,label{
    color:white !important;
}

/* =========================
   Upload Box
========================= */

[data-testid="stFileUploader"]{
    background:#11331d;
    border:2px solid #22c55e;
    border-radius:15px;
    padding:20px;
}

/* Upload Button */

[data-testid="stFileUploader"] button{
    background:white !important;
    color:black !important;
    border-radius:10px !important;
    border:1px solid #ccc !important;
}

[data-testid="stFileUploader"] button span{
    color:black !important;
}

[data-testid="stFileUploader"] button svg{
    fill:black !important;
}

/* Upload text */

[data-testid="stFileUploader"] small{
    color:white !important;
}

[data-testid="stFileUploader"] label{
    color:white !important;
}

/* =========================
   NORMAL BUTTONS
========================= */

div.stButton > button{
    background:#16a34a !important;
    color:white !important;
    border:none !important;
    border-radius:10px;
    font-weight:bold;
}

div.stButton > button:hover{
    background:#15803d !important;
}

/* =========================
   Metrics
========================= */

[data-testid="metric-container"]{
    background:#12351d;
    border:2px solid #22c55e;
    border-radius:15px;
    padding:15px;
}

/* =========================
   Dataframe
========================= */

[data-testid="stDataFrame"]{
    background:#0d1f14;
}

/* Toolbar */

[data-testid="stDataFrame"] button{
    background:white !important;
    color:black !important;
}

[data-testid="stDataFrame"] button svg{
    fill:black !important;
}

/* Remove floating white boxes */

button[title="View fullscreen"]{
    background:white !important;
}

/* Download Buttons */
div.stDownloadButton > button{
    background:#16a34a !important;
    color:white !important;
    border:none !important;
    border-radius:10px !important;
    font-weight:bold !important;
    padding:12px 22px !important;
}

div.stDownloadButton > button:hover{
    background:#15803d !important;
}

div.stDownloadButton > button *{
    color:white !important;
    fill:white !important;
}

/* Best Candidate Card */
.card{
    background:#12351d;
    border:2px solid #22c55e;
    border-radius:15px;
    padding:20px;
    margin-bottom:20px;
}

/* Skill Tags */
.skill-green{
    display:inline-block;
    background:#16a34a;
    color:white;
    padding:6px 12px;
    border-radius:20px;
    margin:4px;
    font-weight:bold;
}

.skill-red{
    display:inline-block;
    background:#dc2626;
    color:white;
    padding:6px 12px;
    border-radius:20px;
    margin:4px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)



# ==========================================================
# TITLE
# ==========================================================

st.title("🤖 AI Resume Screening System")

st.write("Upload multiple resumes and compare them against a Job Description.")

st.markdown("""
### The system performs

- Resume Parsing
- NLP Cleaning
- Skill Extraction
- Skill Matching
- Semantic Similarity
- Candidate Ranking
""")
st.divider()


# ==========================================================
# INPUTS
# ==========================================================

resumes = st.file_uploader(
    "📄 Upload Resume(s)",
    type=["pdf"],
    accept_multiple_files=True
)

job = st.text_area(
    "📝 Paste Job Description",
    height=260,
    placeholder="Paste the complete Job Description here..."
)

analyze = st.button("🚀 Analyze Resumes")


# ==========================================================
# ANALYSIS
# ==========================================================

if analyze:

    if not resumes:
        st.error("Please upload at least one resume.")
        st.stop()

    if job.strip() == "":
        st.error("Please paste a Job Description.")
        st.stop()

    progress = st.progress(0)

    cleaned_job = clean_resume(job)

    job_tokens = preprocess_nlp(cleaned_job)

    job_skills = extract_skills(job_tokens)

    results = []

    total = len(resumes)

    for index, resume in enumerate(resumes):

        progress.progress((index + 1) / total)

        resume_text = extract_text(resume)

        cleaned_resume = clean_resume(resume_text)

        resume_tokens = preprocess_nlp(cleaned_resume)

        resume_skills = extract_skills(resume_tokens)

        match = match_skills(
            job_skills,
            resume_skills
        )

        similarity = semantic_similarity(
            job,
            cleaned_resume
        )

        overall = (
            match["score"] +
            similarity
        ) / 2

        results.append({

            "Resume": resume.name,

            "Skill Match (%)":
                round(match["score"],2),

            "Semantic Similarity (%)":
                round(similarity,2),

            "Overall Match (%)":
                round(overall,2),

            "Matched Skills":
                match["matched"],

            "Missing Skills":
                match["missing"]

        })

    progress.empty()

    ranking = pd.DataFrame(results)

    ranking = ranking.sort_values(
        by="Overall Match (%)",
        ascending=False
    ).reset_index(drop=True)

    ranking.index += 1

    st.success("✅ Analysis Completed Successfully!")

    st.divider()
        # ==========================================================
    # ANALYSIS DASHBOARD
    # ==========================================================

    st.header("📊 Analysis Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📄 Total Resumes",
            len(ranking)
        )

    with col2:
        st.metric(
            "🏅 Best Match",
            f"{ranking.iloc[0]['Overall Match (%)']:.2f}%"
        )

    with col3:
        st.metric(
            "📈 Average Score",
            f"{ranking['Overall Match (%)'].mean():.2f}%"
        )

    st.divider()


    # ==========================================================
    # CANDIDATE RANKING TABLE
    # ==========================================================

    st.header("🏆 Candidate Ranking")

    display_table = ranking.copy()

    display_table["Matched Skills"] = display_table[
        "Matched Skills"
    ].apply(lambda x: ", ".join(x))

    display_table["Missing Skills"] = display_table[
        "Missing Skills"
    ].apply(lambda x: ", ".join(x))

    st.dataframe(
    display_table,
    use_container_width=True,
    height=420,
    hide_index=False
)

    st.divider()


    # ==========================================================
    # OVERALL MATCH CHART
    # ==========================================================

    st.header("📊 Overall Match Scores")

    plt.style.use("default")

    fig, ax = plt.subplots(figsize=(10,5))

    fig.patch.set_facecolor("#07170E")
    ax.set_facecolor("#07170E")

    ax.bar(
        ranking["Resume"],
        ranking["Overall Match (%)"],
        color="#2ecc71"
    )

    ax.tick_params(colors="white")
    ax.spines["bottom"].set_color("white")
    ax.spines["left"].set_color("white")
    ax.yaxis.label.set_color("white")
    ax.xaxis.label.set_color("white")
    ax.title.set_color("white")



    ax.set_facecolor("#07170E")
    fig.patch.set_facecolor("#07170E")

    ax.set_ylabel("Overall Match (%)")

    ax.set_xlabel("Candidates")

    plt.xticks(rotation=60)

    st.pyplot(fig)

    st.divider()


    # ==========================================================
    # BEST CANDIDATE
    # ==========================================================

    best = ranking.iloc[0]

    st.header("🥇 Best Candidate")

    recommendation = ""

    if best["Overall Match (%)"] >= 85:

        recommendation = "🟢 Excellent Match"

    elif best["Overall Match (%)"] >= 70:

        recommendation = "🟡 Good Match"

    elif best["Overall Match (%)"] >= 50:

        recommendation = "🟠 Average Match"

    else:

        recommendation = "🔴 Needs Improvement"

    st.markdown(f"""
    <div class="card">

    <h1>{best['Resume']}</h1>

    <h2>{best['Overall Match (%)']:.2f}%</h2>

    <h3>{recommendation}</h3>

    </div>
    """,
    unsafe_allow_html=True
    )

    st.divider()


    # ==========================================================
    # MATCHED SKILLS
    # ==========================================================

    st.header("✅ Matched Skills")

    if len(best["Matched Skills"]) == 0:

        st.info("No matched skills found.")

    else:

        for skill in best["Matched Skills"]:

            st.markdown(
                f'<span class="skill-green">{skill}</span>',
                unsafe_allow_html=True
            )

    st.divider()


    # ==========================================================
    # MISSING SKILLS
    # ==========================================================

    st.header("❌ Missing Skills")

    if len(best["Missing Skills"]) == 0:

        st.success("No missing skills.")

    else:

        for skill in best["Missing Skills"]:

            st.markdown(
                f'<span class="skill-red">{skill}</span>',
                unsafe_allow_html=True
            )

    st.divider()
        # ==========================================================
    # RESUME DETAILS
    # ==========================================================

    st.header("📋 Resume Details")

    for _, row in ranking.iterrows():

        with st.expander(f"📄 {row['Resume']}"):

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric(
                    "Skill Match",
                    f"{row['Skill Match (%)']:.2f}%"
                )

            with c2:
                st.metric(
                    "Semantic Similarity",
                    f"{row['Semantic Similarity (%)']:.2f}%"
                )

            with c3:
                st.metric(
                    "Overall Match",
                    f"{row['Overall Match (%)']:.2f}%"
                )

            st.markdown("### ✅ Matched Skills")

            matched = row["Matched Skills"]

            if len(matched) == 0:
                st.info("No matched skills.")
            else:

                cols = st.columns(3)

                for i, skill in enumerate(matched):

                    with cols[i % 3]:

                        st.success(skill)

            st.markdown("### ❌ Missing Skills")

            missing = row["Missing Skills"]

            if len(missing) == 0:

                st.success("No missing skills.")

            else:

                cols = st.columns(3)

                for i, skill in enumerate(missing):

                    with cols[i % 3]:

                        st.error(skill)

    st.divider()


    # ==========================================================
    # DOWNLOAD CSV
    # ==========================================================

    st.header("📥 Export Results")

    csv = display_table.to_csv(index=False).encode("utf-8")

    st.download_button(

        label="📄 Download CSV",

        data=csv,

        file_name="ranked_candidates.csv",

        mime="text/csv"

    )


    # ==========================================================
    # DOWNLOAD EXCEL
    # ==========================================================

    excel_buffer = BytesIO()

    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:

        display_table.to_excel(
            writer,
            index=False,
            sheet_name="Candidates"
        )

    st.download_button(

        label="📊 Download Excel",

        data=excel_buffer.getvalue(),

        file_name="ranked_candidates.xlsx",

        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )

    st.divider()


    # ==========================================================
    # PROJECT SUMMARY
    # ==========================================================

    st.header("📌 Project Summary")

    st.info(f"""
Total Resumes Analysed : **{len(ranking)}**

Highest Score : **{ranking['Overall Match (%)'].max():.2f}%**

Average Score : **{ranking['Overall Match (%)'].mean():.2f}%**

Lowest Score : **{ranking['Overall Match (%)'].min():.2f}%**
""")

    st.divider()


    # ==========================================================
    # FOOTER
    # ==========================================================

    st.markdown(
        """
        <hr>

        <center>

        <h3 style="color:#7CFC98;">
        🤖 AI Resume Screening & Job Matching System
        </h3>

        <p>
        Developed using
        <b>Python</b> •
        <b>Streamlit</b> •
        <b>NLP</b> •
        <b>Sentence Transformers</b>
        </p>

        <p>
        AI Recruiter | Intelligent Candidate Discovery
        </p>

        </center>
        """,
        unsafe_allow_html=True
    )