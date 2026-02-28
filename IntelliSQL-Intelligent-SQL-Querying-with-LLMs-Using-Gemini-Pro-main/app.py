import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# ------------------ GEMINI CONFIG ------------------
genai.configure(api_key=os.getenv("API_KEY"))

prompt = ["""
You are an expert in converting English questions into SQLite SQL queries.

The database is SQLite.
There is a table named Students with columns:
name, class, marks, company.

Rules:
- Use only SQLite syntax.
- Do NOT use MySQL commands like SHOW TABLES.
- Return ONLY the SQL query.
"""]

# ------------------ LLM FUNCTIONS ------------------
def get_response(que, prompt):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(
        prompt[0] + "\nUser Question: " + que
    )
    return response.text.strip().replace("```sql", "").replace("```", "")


def read_query(sql, db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    return rows


# ------------------ HOME PAGE ------------------
def page_home():

    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1f1f1f, #2c3e50);
        color: white;
    }
    .main-title {
        text-align: center;
        color: #00E676;
        font-size: 2.7em;
        font-weight: bold;
    }
    .sub-title {
        text-align: center;
        color: #BBDEFB;
        font-size: 1.3em;
        margin-bottom: 30px;
    }
    .feature-box {
        background-color: #263238;
        padding: 25px;
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 class='main-title'>Welcome to IntelliSQL 🚀</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-title'>Transform Natural Language into Powerful SQLite Queries using Gemini 2.5 Flash</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.image(
            "https://cdn1.iconfinder.com/data/icons/business-dual-color-glyph-set-3/128/Data_warehouse-1024.png",
            width=300
        )

    with col2:
        st.markdown("""
        <div class='feature-box'>
        <h2 style='color:#00E676;'>🔥 Key Features</h2>
        <ul>
            <li>💡 Natural Language to SQL Conversion</li>
            <li>⚡ Powered by Gemini 2.5 Flash</li>
            <li>🗄 SQLite Database Integration</li>
            <li>📊 Real-time Query Execution</li>
            <li>🔐 Structured SQL Output</li>
            <li>🎯 Beginner Friendly Interface</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.success("✨ Powered by Gemini 2.5 Flash | Built with Streamlit | SQLite Integrated")


# ------------------ ABOUT PAGE ------------------
def page_about():

    st.markdown("""
    <style>
    .about-box {
        background-color: #263238;
        padding: 25px;
        border-radius: 15px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='color:#00E676;'>About IntelliSQL</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("""
        <div class='about-box'>
        <h3>📌 Project Overview</h3>
        <p>
        IntelliSQL converts natural language into executable SQLite queries
        using Gemini 2.5 Flash.
        </p>

        <h3>🛠 Technologies Used</h3>
        <ul>
        <li>Python</li>
        <li>Streamlit</li>
        <li>SQLite</li>
        <li>Gemini 2.5 Flash</li>
        </ul>

        <h3>🎯 Objective</h3>
        <p>
        To simplify SQL querying for non-technical users.
        </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.image(
            "https://www.logo.wine/a/logo/Oracle_SQL_Developer/Oracle_SQL_Developer-Logo.wine.svg",
            width=300
        )


# ------------------ QUERY PAGE ------------------
def page_intelligent_query_assistance():

    st.markdown("<h1 style='color:#00E676;'>Intelligent Query Assistance</h1>", unsafe_allow_html=True)

    st.write("Enter your question in English. The system will generate and execute SQLite query.")

    col1, col2 = st.columns([2, 1])

    with col1:
        que = st.text_input("Enter Your Query:")
        submit = st.button("Get Answer")

        if submit and que:
            try:
                response = get_response(que, prompt)
                st.write("### Generated SQL Query:")
                st.code(response, language="sql")

                data = read_query(response, "data.db")

                st.subheader("The Response is:")
                st.table(data)

            except Exception as e:
                st.error(f"An error occurred: {e}")

    with col2:
        st.image(
            "https://cdn-icons-png.flaticon.com/512/9850/9850877.png",
            width=300
        )


# ------------------ MAIN ------------------
def main():
    st.set_page_config(
        page_title="IntelliSQL",
        page_icon="🌟",
        layout="wide"
    )

    st.sidebar.title("Navigation")

    pages = {
        "Home": page_home,
        "About": page_about,
        "Intelligent Query Assistance": page_intelligent_query_assistance,
    }

    selection = st.sidebar.radio("Go to", list(pages.keys()))
    pages[selection]()


# ------------------ RUN ------------------
if __name__ == "__main__":
    main()