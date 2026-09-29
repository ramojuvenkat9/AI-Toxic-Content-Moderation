import streamlit as st
import pandas as pd

from src.database import (
    create_database,
    register_user,
    login_user,
    add_comment,
    get_history,
    get_all_history
)

from src.predict import predict_comment
from src.severity import get_severity
from src.user_profile import UserProfile
from src.risk_score import calculate_risk_score
from src.rehabilitation import calculate_rehabilitation_score
from src.rewrite import rewrite_comment
from src.decision_engine import make_decision
from src.explain import create_explanation

# -------------------------------------------------------
# Database
# -------------------------------------------------------

create_database()

# -------------------------------------------------------
# Streamlit Config
# -------------------------------------------------------

st.set_page_config(
    page_title="AI Toxic Content Moderation System",
    page_icon="🛡️",
    layout="wide"
)



# -------------------------------------------------------
# Session State
# -------------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------

st.sidebar.title("🛡️ Navigation")

if st.session_state.logged_in:

    choice = st.sidebar.radio(
        "Select Page",
        [
            "Dashboard",
            "Analyze Comment",
            "History",
            "Admin Dashboard"
        ]
    )

    st.session_state.page = choice

    st.sidebar.divider()

    st.sidebar.write(
        f"Logged in as **{st.session_state.username}**"
    )

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

else:

    choice = st.sidebar.radio(
        "Menu",
        [
            "Login",
            "Register"
        ]
    )

# -------------------------------------------------------
# LOGIN PAGE
# -------------------------------------------------------

if not st.session_state.logged_in and choice == "Login":

    st.title("🛡️ AI Toxic Content Moderation")

    st.subheader("Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        user = login_user(username, password)

        if user:

            st.session_state.logged_in = True
            st.session_state.username = username

            st.success("Login Successful")

            st.rerun()

        else:

            st.error("Invalid Username or Password")

# -------------------------------------------------------
# REGISTER PAGE
# -------------------------------------------------------

elif not st.session_state.logged_in and choice == "Register":

    st.title("Create Account")

    new_username = st.text_input("Username")

    new_password = st.text_input(
        "Password",
        type="password"
    )

    confirm = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button("Register"):

        if new_username.strip() == "" or new_password.strip() == "":

            st.warning("All fields are required.")

        elif new_password != confirm:

            st.error("Passwords do not match.")

        else:

            success = register_user(
                new_username,
                new_password
            )

            if success:

                st.success(
                    "Registration Successful. Please Login."
                )

            else:

                st.error("Username already exists.")

# -------------------------------------------------------
# AFTER LOGIN
# -------------------------------------------------------

elif st.session_state.logged_in:
    

    # ===================================================
    # DASHBOARD
    # ===================================================
    

    if st.session_state.page == "Dashboard":

        st.title("🛡️ AI Toxic Content Moderation System")

        st.markdown(
            """
### Research Project

This application performs

- Toxic Comment Detection
- Severity Prediction
- Explainable AI
- User Behaviour Analysis
- Risk Score Calculation
- Rehabilitation Score
- AI Comment Rewriting
- Adaptive Decision Making
"""
        )

        history = get_all_history()

        total_comments = len(history)

        total_users = len(
            set([row[1] for row in history])
        )

        if total_comments == 0:

            avg_toxicity = 0

            avg_risk = 0

        else:

            avg_toxicity = round(

                sum(row[3] for row in history)

                / total_comments,

                3

            )

            avg_risk = round(

                sum(row[5] for row in history)

                / total_comments,

                2

            )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("👤 Users", total_users)


        with col2:
            st.metric("💬 Comments", total_comments)

        with col3:
            st.metric("☣ Average Toxicity", avg_toxicity)

        with col4:
            st.metric("⚠ Average Risk", avg_risk)

        st.divider()

        st.subheader("Project Modules")

        st.success("✔ Toxic Comment Detection")

        st.success("✔ Explainable AI")

        st.success("✔ Severity Prediction")

        st.success("✔ User Behaviour Analysis")

        st.success("✔ Risk Score")

        st.success("✔ Rehabilitation Score")

        st.success("✔ AI Rewrite")

        st.success("✔ Adaptive Decision Engine")
            # ===================================================
    # ANALYZE COMMENT PAGE
    # ===================================================

    elif st.session_state.page == "Analyze Comment":

        st.title("📝 Analyze Comment")

        user_id = st.session_state.username

        st.write(f"Logged in as: **{user_id}**")

        comment = st.text_area(
            "Enter Comment",
            height=180,
            placeholder="Type your comment here..."
        )

        if st.button("Analyze Comment"):

            if comment.strip() == "":

                st.warning("Please enter a comment.")

            else:
                

                # -------------------------------
                # Toxic Prediction
                # -------------------------------
                with st.spinner("Analyzing Comment..."):
                    progress = st.progress(0)
                    progress.progress(10)
                    prediction = predict_comment(comment)
                    progress.progress(30)
                    severity, action = get_severity(prediction)
                    progress.progress(50)


                

                st.success("Prediction Completed")

                st.subheader("Toxicity Scores")

                prediction_df = pd.DataFrame({
                    "Category": prediction.keys(),
                    "Score": prediction.values()
                })

                st.dataframe(
                    prediction_df,
                    use_container_width=True
                )

                current_toxicity = max(
                    prediction.values()
                )
                st.subheader("Overall Toxicity")
                st.progress(float(current_toxicity))
                st.write(
                     f"Overall Toxicity : {current_toxicity:.2%}"
                )

                # -------------------------------
                # Explainable AI
                # -------------------------------

                st.divider()

                st.subheader("Explainable AI")

                explain_df = create_explanation(
                    prediction
                )

                st.bar_chart(
                    explain_df.set_index("Category")
                )
                highest = explain_df.iloc[0]
                TOXICITY_THRESHOLD = 0.50
                if highest["Score"] >= TOXICITY_THRESHOLD:
                    predicted_category = highest["Category"]
                else:
                    predicted_category = "SAFE"
                    # ---------------------------------------
# Display Prediction
# ---------------------------------------
                if predicted_category == "safe":
                    st.success("Prediction: SAFE")
                else:
                    st.warning(
                        f"Prediction: {predicted_category}"
                    )
                st.metric(
                    "Confidence",
                    f"{highest['Score']:.2%}"
                )
                st.markdown("### Why was this prediction made?")

                if predicted_category == "safe":
                    st.success(
                        "The model did not detect any significant toxicity in the comment."
                    )
                elif highest["Score"] >= 0.80:
                    st.warning(
                        "The model detected a very strong presence of this toxicity category."
                    )
                elif highest["Score"] >= 0.50:
                    st.info(
                        "The model found a moderate presence of this toxicity category."
                    )
                    
                    

                # -------------------------------
                # Severity
                # -------------------------------

                severity, action = get_severity(
                    prediction
                )
                st.markdown(
    f"""
### Model Summary

- **Predicted Category:** {predicted_category}
- **Confidence Score:** {highest['Score']:.2%}
- **Severity Level:** {severity}
- **Recommended Action:** {action}
"""
)

                st.divider()

                st.subheader("Severity")

                c1, c2 = st.columns(2)

                with c1:

                    if severity == "SAFE":

                        st.success(severity)

                    elif severity == "MILD":

                        st.info(severity)

                    elif severity == "HIGH":

                        st.warning(severity)

                    else:

                        st.error(severity)

                with c2:

                    st.metric(
                        "Recommended Action",
                        action
                    )

                # -------------------------------
                # User History
                # -------------------------------

                history = get_history(user_id)

                user = UserProfile()

                risk_history = []

                for row in history:

                    user.add_comment(row[3])

                    risk_history.append(row[5])

                    if row[4] == "MILD":

                        user.add_warning()

                    elif row[4] == "HIGH":

                        user.add_warning()

                    elif row[4] == "SEVERE":

                        user.add_moderator_review()

                # -------------------------------
                # User Behaviour
                # -------------------------------

                st.divider()

                st.subheader(
                    "User Behaviour Analysis"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Previous Comments",
                        len(user.previous_scores)
                    )

                    st.metric(
                        "Warnings",
                        user.warnings
                    )

                with col2:

                    st.metric(
                        "Average Toxicity",
                        round(
                            user.average_toxicity(),
                            3
                        )
                    )

                    st.metric(
                        "Moderator Reviews",
                        user.moderator_reviews
                    )

                with col3:

                    st.metric(
                        "Rewrite Accepted",
                        user.rewrites_accepted
                    )
                    # -------------------------------
# User Toxicity Trend
# -------------------------------

                    st.divider()

                    st.subheader("📈 User Toxicity Trend")

                    if len(user.previous_scores) == 0:

                          st.info("No previous comments available to display trend.")

                    else:

                          trend_df = pd.DataFrame({

                            "Comment": list(range(1, len(user.previous_scores) + 1)),

                            "Toxicity": user.previous_scores

                       })

                          st.line_chart(

                         trend_df.set_index("Comment")

                        )

                # -------------------------------
                # Risk Score
                # -------------------------------
                progress.progress(70)

                risk_score = calculate_risk_score(
                    current_toxicity,
                    user
                )

                st.divider()

                st.subheader("Risk Score")

                st.metric(
                    "Risk Score",
                    risk_score
                )

                # -------------------------------
                # Rehabilitation Score
                # -------------------------------

                if len(risk_history) == 0:

                    risk_history = [risk_score]

                else:

                    risk_history.append(
                        risk_score
                    )

                rehab_score = (
                    calculate_rehabilitation_score(
                        risk_history
                    )
                )

                st.divider()

                st.subheader(
                    "Rehabilitation Score"
                )

                st.metric(
                    "Score",
                    rehab_score
                )

                # -------------------------------
                # Rewrite Suggestion
                # -------------------------------
                # ---------------------------------------

                if severity == "SAFE":

                    st.divider()

                    st.success("✅ This comment is safe. No rewrite is required.")

                else:

                    rewritten = rewrite_comment(comment)

                    st.divider()

                    st.subheader("AI Suggested Rewrite")

                    edited_comment = st.text_area(
                    "Edit the rewritten comment if needed",
                     value=rewritten,
                    height=120
    )
                    if st.button("Re-analyze Rewritten Comment"):

                        st.divider()

                        st.header("Re-analysis Results")

    # ---------------------------------
    # Predict rewritten comment
    # ---------------------------------

                        new_prediction = predict_comment(
                            edited_comment
                        )

                        new_toxicity = max(
                            new_prediction.values()
                        )

                        new_severity, new_action = get_severity(
                            new_prediction
                        )

                        new_risk = calculate_risk_score(
                            new_toxicity,
                            user
                        )

                        new_rehab = calculate_rehabilitation_score(
                            risk_history
                    )

                        new_decision = make_decision(
                            new_severity,
                            new_risk,
                            new_rehab
                      )

    # ---------------------------------
    # Show comparison
    # ---------------------------------

                        col1, col2 = st.columns(2)

                        with col1:

                            st.subheader("Original")

                            st.metric(
                               "Toxicity",
                              f"{current_toxicity:.2%}"
                            )

                            st.metric(
                               "Severity",
                                severity
                            )

                        with col2:

                            st.subheader("Rewritten")

                            st.metric(
                             "Toxicity",
                            f"{new_toxicity:.2%}"
                            )

                            st.metric(
                                "Severity",
                                 new_severity
                            )

                        improvement = (
                            current_toxicity - new_toxicity
                        ) * 100

                        st.divider()

                        st.metric(
                            "Improvement",
                           f"{improvement:.1f}%"
                        )

                        st.subheader("Final Decision")

                        if "Publish" in new_decision:

                           st.success(new_decision)

                        elif "Rewrite" in new_decision:

                           st.warning(new_decision)

                        else:

                           st.error(new_decision)

                    
                
                

                
                # -------------------------------
                # Final Decision
                # -------------------------------
                progress.progress(90)

                final_decision = make_decision(
                    severity,
                    risk_score,
                    rehab_score
                )

                st.divider()

                st.subheader(
                    "Decision Engine"
                )

                if "Publish" in final_decision:

                    st.success(
                        final_decision
                    )

                elif "Rewrite" in final_decision:

                    st.warning(
                        final_decision
                    )

                else:

                    st.error(
                        final_decision
                    )

                # -------------------------------
                # Save Comment
                # -------------------------------

                add_comment(
                    user_id,
                    comment,
                    current_toxicity,
                    severity,
                    risk_score,
                    final_decision
                )
                progress.progress(100)

                st.success(
                    "Comment Saved Successfully."
                )
                    # ===================================================
    # HISTORY PAGE
    # ===================================================

    elif st.session_state.page == "History":

        st.title("📜 Comment History")

        history = get_history(st.session_state.username)

        if len(history) == 0:

            st.info("No previous comments found.")

        else:

            df = pd.DataFrame(
                history,
                columns=[
                    "ID",
                    "User",
                    "Comment",
                    "Toxicity",
                    "Severity",
                    "Risk Score",
                    "Decision"
                ]
            )

            search = st.text_input(
                "Search Comments"
            )

            if search:

                df = df[
                    df["Comment"].str.contains(
                        search,
                        case=False,
                        na=False
                    )
                ]

            severity_filter = st.selectbox(
                "Filter Severity",
                [
                    "All",
                    "SAFE",
                    "MILD",
                    "HIGH",
                    "SEVERE"
                ]
            )

            if severity_filter != "All":

                df = df[
                    df["Severity"] == severity_filter
                ]

            st.dataframe(

                df.style.highlight_max(

                   subset=["Risk Score"],

                   color="red"
     ),

               use_container_width=True

               )

            st.download_button(
                "Download History CSV",
                df.to_csv(index=False),
                "history.csv",
                "text/csv"
            )

    # ===================================================
    # ADMIN DASHBOARD
    # ===================================================

    elif st.session_state.page == "Admin Dashboard":

        st.title("📊 Admin Dashboard")

        history = get_all_history()

        if len(history) == 0:

            st.warning(
                "No comments available."
            )

        else:

            df = pd.DataFrame(
                history,
                columns=[
                    "ID",
                    "User",
                    "Comment",
                    "Toxicity",
                    "Severity",
                    "Risk",
                    "Decision"
                ]
            )

            st.subheader("System Statistics")

            c1, c2, c3, c4 = st.columns(4)

            with c1:

                st.metric(
                    "Total Users",
                    df["User"].nunique()
                )

            with c2:

                st.metric(
                    "Total Comments",
                    len(df)
                )

            with c3:

                st.metric(
                    "Average Toxicity",
                    round(
                        df["Toxicity"].mean(),
                        3
                    )
                )

            with c4:

                st.metric(
                    "Average Risk",
                    round(
                        df["Risk"].mean(),
                        2
                    )
                )

            st.divider()

            st.subheader("Severity Distribution")

            severity_counts = (
                df["Severity"]
                .value_counts()
            )

            st.bar_chart(severity_counts)

            st.divider()

            st.subheader("Decision Distribution")

            decision_counts = (
                df["Decision"]
                .value_counts()
            )

            st.bar_chart(decision_counts)
            st.divider()
            st.subheader("Toxicity Distribution")
            toxicity_df = pd.DataFrame({
                 "Range": [
        "0-0.25",
        "0.25-0.50",
        "0.50-0.75",
        "0.75-1.00"
    ],
                    "Count": [
                        len(df[df["Toxicity"] <= 0.25]),
                        len(df[(df["Toxicity"] > 0.25) &
               (df["Toxicity"] <= 0.50)]),
               len(df[(df["Toxicity"] > 0.50) &
               (df["Toxicity"] <= 0.75)]),
               len(df[df["Toxicity"] > 0.75])
                    ]
                })
            st.bar_chart(
                toxicity_df.set_index("Range")
            )
            
            st.divider()

            st.subheader("Top High Risk Users")

            risk_df = (
                df.groupby("User")["Risk"]
                .mean()
                .sort_values(
                    ascending=False
                )
                .reset_index()
            )
            st.bar_chart(
                risk_df.set_index("User")
            )
            st.divider()
            st.subheader("Most Active Users")
            active_users = (
               df["User"]
               .value_counts()
            )
            st.bar_chart(active_users)
            st.divider()

            st.subheader("Recent Comments")

            st.dataframe(
                df.iloc[::-1],
                use_container_width=True
            )
            st.divider()

st.markdown(
"""
<center>

### AI Toxic Content Moderation System

Integrated M.Tech Final Year Project

2026

</center>
""",
unsafe_allow_html=True
)