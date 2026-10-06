import streamlit as st
import ollama

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="EduAnalytics AI",
    page_icon="🎓",
    layout="wide"
)

# --------------------------------------------------
# GRADE CONVERSION
# These are analysis equivalents, not official
# board/university grade conversions.
# --------------------------------------------------
GRADE_PERCENTAGES = {
    "A+": 95,
    "A": 85,
    "B+": 78,
    "B": 75,
    "C+": 68,
    "C": 65,
    "D": 55,
    "E": 45,
    "F": 35
}

GRADE_OPTIONS = list(GRADE_PERCENTAGES.keys())

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 17px;
    color: #666;
    margin-bottom: 30px;
}

.metric-card {
    background: #f8f9fa;
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    border: 1px solid #e5e7eb;
    margin-bottom: 15px;
}

.metric-title {
    font-size: 14px;
    color: #666;
    font-weight: 600;
}

.metric-value {
    font-size: 28px;
    font-weight: 800;
    margin-top: 5px;
}

.subject-card {
    background: #f8f9fa;
    border-left: 5px solid #4f46e5;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
}

.info-box {
    background: #eef2ff;
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown("""
<div class="main-title">
    🎓 EduAnalytics AI
</div>

<div class="subtitle">
    AI-Powered Academic Performance Analytics System
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# STUDENT INFORMATION
# --------------------------------------------------
st.header("👨‍🎓 Student Information")

col1, col2, col3 = st.columns(3)

with col1:
    student_name = st.text_input(
        "Student Name",
        placeholder="Enter student name"
    )

with col2:
    student_id = st.text_input(
        "Student ID",
        placeholder="Enter student ID"
    )

with col3:
    education_level = st.selectbox(
        "Education Level",
        [
            "10th",
            "Intermediate",
            "School",
            "Diploma",
            "Undergraduate",
            "Postgraduate",
            "Other"
        ]
    )

department = st.text_input(
    "Department / Stream",
    placeholder="Example: Computer Science, MPC, CSE, Mechanical, Commerce"
)

# --------------------------------------------------
# PERFORMANCE INPUT
# --------------------------------------------------
st.header("📊 Performance Input")

input_method = st.radio(
    "How do you want to enter the student's performance?",
    [
        "📊 Marks",
        "🏆 Grades"
    ],
    horizontal=True
)

# --------------------------------------------------
# NUMBER OF SUBJECTS
# --------------------------------------------------
number_of_subjects = st.number_input(
    "Number of Subjects",
    min_value=1,
    max_value=30,
    value=5,
    step=1
)

st.divider()

# --------------------------------------------------
# GRADE INFORMATION
# --------------------------------------------------
if input_method == "🏆 Grades":

    st.markdown("""
    <div class="info-box">
        <b>Grade Analysis</b><br>
        All subjects will use grades. The grades are converted
        to percentage equivalents only for analysis.
        These conversions are not official academic conversions.
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📖 View Grade Conversion"):

        for grade, percentage in GRADE_PERCENTAGES.items():
            st.write(
                f"**{grade}** → {percentage}% analysis equivalent"
            )

# --------------------------------------------------
# SUBJECT INPUT
# --------------------------------------------------
st.header("📚 Subject Performance")

subjects = []

for i in range(int(number_of_subjects)):

    st.subheader(f"Subject {i + 1}")

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        subject_name = st.text_input(
            "Subject Name",
            key=f"subject_name_{i}",
            placeholder="Example: Mathematics"
        )

    if input_method == "📊 Marks":

        with col2:
            maximum_marks = st.number_input(
                "Maximum Marks",
                min_value=1.0,
                max_value=10000.0,
                value=100.0,
                step=1.0,
                key=f"maximum_marks_{i}"
            )

        with col3:
            obtained_marks = st.number_input(
                "Obtained Marks",
                min_value=0.0,
                max_value=10000.0,
                value=0.0,
                step=1.0,
                key=f"obtained_marks_{i}"
            )

        subjects.append({
            "name": subject_name.strip(),
            "max_marks": maximum_marks,
            "obtained_marks": obtained_marks
        })

    else:

        with col2:
            grade = st.selectbox(
                "Grade",
                GRADE_OPTIONS,
                key=f"grade_{i}"
            )

        subjects.append({
            "name": subject_name.strip(),
            "grade": grade
        })

# --------------------------------------------------
# ANALYZE BUTTON
# --------------------------------------------------
st.divider()

analyze_button = st.button(
    "🚀 Analyze Student Performance",
    use_container_width=True,
    type="primary"
)

# --------------------------------------------------
# ANALYSIS
# --------------------------------------------------
if analyze_button:

    # --------------------------------------------------
    # VALIDATION
    # --------------------------------------------------
    if not student_name.strip():
        st.error("Please enter the student's name.")
        st.stop()

    entered_subjects = [
        subject for subject in subjects
        if subject["name"]
    ]

    if len(entered_subjects) == 0:
        st.error("Please enter at least one subject.")
        st.stop()

    subject_names = [
        subject["name"].lower()
        for subject in entered_subjects
    ]

    if len(subject_names) != len(set(subject_names)):
        st.error("Duplicate subject names are not allowed.")
        st.stop()

    # --------------------------------------------------
    # CALCULATE PERFORMANCE
    # --------------------------------------------------
    analyzed_subjects = []

    for subject in entered_subjects:

        if input_method == "📊 Marks":

            max_marks = subject["max_marks"]
            obtained = subject["obtained_marks"]

            if obtained > max_marks:
                st.error(
                    f"Obtained marks for {subject['name']} "
                    f"cannot be greater than maximum marks."
                )
                st.stop()

            percentage = (
                obtained / max_marks
            ) * 100

            analyzed_subjects.append({
                "name": subject["name"],
                "percentage": percentage,
                "obtained": obtained,
                "maximum": max_marks,
                "grade": None
            })

        else:

            grade = subject["grade"]
            percentage = GRADE_PERCENTAGES[grade]

            analyzed_subjects.append({
                "name": subject["name"],
                "percentage": percentage,
                "obtained": None,
                "maximum": None,
                "grade": grade
            })

    # --------------------------------------------------
    # OVERALL PERFORMANCE
    # --------------------------------------------------
    if input_method == "📊 Marks":

        total_obtained = sum(
            subject["obtained"]
            for subject in analyzed_subjects
        )

        total_maximum = sum(
            subject["maximum"]
            for subject in analyzed_subjects
        )

        overall_percentage = (
            total_obtained / total_maximum
        ) * 100

    else:

        overall_percentage = sum(
            subject["percentage"]
            for subject in analyzed_subjects
        ) / len(analyzed_subjects)

    # --------------------------------------------------
    # OVERALL GRADE
    # --------------------------------------------------
    if overall_percentage >= 90:
        overall_grade = "A+"
    elif overall_percentage >= 80:
        overall_grade = "A"
    elif overall_percentage >= 70:
        overall_grade = "B"
    elif overall_percentage >= 60:
        overall_grade = "C"
    elif overall_percentage >= 50:
        overall_grade = "D"
    elif overall_percentage >= 40:
        overall_grade = "E"
    else:
        overall_grade = "F"

    # --------------------------------------------------
    # PERFORMANCE CATEGORY
    # --------------------------------------------------
    if overall_percentage < 40:
        category = "Failed"
    elif overall_percentage < 60:
        category = "Weak"
    elif overall_percentage < 75:
        category = "Average"
    elif overall_percentage < 90:
        category = "Strong"
    else:
        category = "Excellent"

    # --------------------------------------------------
    # PASS / FAIL
    # --------------------------------------------------
    failed_subjects = [
        subject
        for subject in analyzed_subjects
        if subject["percentage"] < 40
    ]

    if failed_subjects:
        result = "FAIL"
    else:
        result = "PASS"

    # --------------------------------------------------
    # STRONGEST / WEAKEST
    # --------------------------------------------------
    strongest = max(
        analyzed_subjects,
        key=lambda x: x["percentage"]
    )

    weakest = min(
        analyzed_subjects,
        key=lambda x: x["percentage"]
    )

    # --------------------------------------------------
    # RESULTS
    # --------------------------------------------------
    st.success("✅ Student analysis completed!")

    st.header("📊 Overall Result")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">STUDENT</div>
                <div class="metric-value">
                    {student_name}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">OVERALL SCORE</div>
                <div class="metric-value">
                    {overall_percentage:.1f}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">GRADE</div>
                <div class="metric-value">
                    {overall_grade}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">RESULT</div>
                <div class="metric-value">
                    {result}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # --------------------------------------------------
    # PROGRESS
    # --------------------------------------------------
    st.subheader("📈 Overall Performance")

    st.progress(
        min(int(overall_percentage), 100)
    )

    st.write(
        f"**Performance Category:** {category}"
    )

    # --------------------------------------------------
    # SUBJECT ANALYSIS
    # --------------------------------------------------
    st.header("📚 Subject-wise Analysis")

    for subject in analyzed_subjects:

        percentage = subject["percentage"]

        if percentage >= 75:
            status = "🟢 Strong"
        elif percentage >= 40:
            status = "🟡 Needs Improvement"
        else:
            status = "🔴 Weak"

        if input_method == "📊 Marks":

            performance_text = (
                f"{subject['obtained']:.0f} / "
                f"{subject['maximum']:.0f}"
            )

        else:

            performance_text = (
                f"Grade: {subject['grade']}"
            )

        st.markdown(
            f"""
            <div class="subject-card">
                <strong>{subject['name']}</strong>
                <br>
                <small>
                    {performance_text}
                    &nbsp; | &nbsp;
                    Score: {percentage:.1f}%
                    &nbsp; | &nbsp;
                    {status}
                </small>
            </div>
            """,
            unsafe_allow_html=True
        )

    # --------------------------------------------------
    # PERFORMANCE HIGHLIGHTS
    # --------------------------------------------------
    st.header("🎯 Performance Highlights")

    col1, col2 = st.columns(2)

    with col1:
        st.success(
            f"🏆 Strongest Subject: "
            f"**{strongest['name']}** "
            f"({strongest['percentage']:.1f}%)"
        )

    with col2:

        if weakest["percentage"] < 40:

            st.error(
                f"⚠️ Weakest Subject: "
                f"**{weakest['name']}** "
                f"({weakest['percentage']:.1f}%)"
            )

        else:

            st.warning(
                f"📌 Lowest Subject: "
                f"**{weakest['name']}** "
                f"({weakest['percentage']:.1f}%)"
            )

    # --------------------------------------------------
    # GRADE DETAILS
    # --------------------------------------------------
    if input_method == "🏆 Grades":

        st.header("🏆 Grade Details")

        for subject in analyzed_subjects:

            st.write(
                f"**{subject['name']}** → "
                f"{subject['grade']} "
                f"({subject['percentage']}% analysis equivalent)"
            )

    # --------------------------------------------------
    # PERFORMANCE SUMMARY
    # --------------------------------------------------
    st.header("📝 Performance Summary")

    if result == "PASS":

        st.write(
            f"{student_name} has achieved an overall score of "
            f"**{overall_percentage:.1f}%** with an overall grade "
            f"of **{overall_grade}**."
        )

    else:

        st.write(
            f"{student_name} has an overall score of "
            f"**{overall_percentage:.1f}%**. "
            f"There are {len(failed_subjects)} subject(s) "
            f"that require immediate attention."
        )

    # --------------------------------------------------
    # AI ANALYSIS
    # --------------------------------------------------
    st.header("🤖 AI Analysis & Study Plan")

    subject_details = []

    for subject in analyzed_subjects:

        if input_method == "📊 Marks":

            detail = (
                f"{subject['name']}: "
                f"{subject['obtained']}/"
                f"{subject['maximum']} "
                f"({subject['percentage']:.1f}%)"
            )

        else:

            detail = (
                f"{subject['name']}: "
                f"Grade {subject['grade']} "
                f"({subject['percentage']}% "
                f"analysis equivalent)"
            )

        subject_details.append(detail)

    subject_text = "\n".join(subject_details)

    prompt = f"""
You are an educational performance analyst.

Analyze the following student's academic performance.

Student Name: {student_name}
Student ID: {student_id}
Education Level: {education_level}
Department/Stream: {department}
Input Method: {input_method}

Overall Percentage: {overall_percentage:.1f}%
Overall Grade: {overall_grade}
Performance Category: {category}
Result: {result}

Strongest Subject:
{strongest['name']} - {strongest['percentage']:.1f}%

Weakest Subject:
{weakest['name']} - {weakest['percentage']:.1f}%

Subject Performance:
{subject_text}

Provide:

1. Overall performance analysis
2. Strong subjects and why they are strong
3. Weak subjects and possible reasons
4. Specific improvement strategies
5. A practical 7-day study plan
6. Recommended daily study priorities
7. Exam preparation tips
8. Motivational advice

Keep the response practical, clear, student-friendly,
and suitable for the student's education level.
"""

    with st.spinner(
        "🤖 AI is analyzing the student's performance..."
    ):

        try:

            response = ollama.chat(
                model="llama3.2:3b",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            ai_response = response["message"]["content"]

            st.markdown(ai_response)

        except Exception as e:

            st.error(
                "Could not connect to Ollama."
            )

            st.info(
                "Make sure Ollama is running and the "
                "llama3.2:3b model is installed."
            )

            st.code(str(e))

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.divider()

st.caption(
    "🎓 EduAnalytics AI | "
    "AI-Powered Academic Performance Analytics System | "
    "Powered by Streamlit + Ollama"
)