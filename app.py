import streamlit as st
import pandas as pd

from cleaner import DataCleaner
from analyzer import analyze_dataset
from validator import validate_dataset


# ==================================================
# PAGE SETTINGS
# ==================================================

st.set_page_config(
    page_title="Data Cleaner Agent",
    page_icon="🧹",
    layout="wide"
)


# ==================================================
# CUSTOM FRONTEND DESIGN
# ==================================================

st.markdown("""
<style>

    /* ==============================================
       MAIN PAGE
    ============================================== */

    .stApp {
        background:
            radial-gradient(
                circle at top left,
                #eef2ff 0%,
                transparent 35%
            ),
            radial-gradient(
                circle at top right,
                #f3e8ff 0%,
                transparent 35%
            ),
            linear-gradient(
                135deg,
                #f8fafc 0%,
                #eef2ff 50%,
                #f8f7ff 100%
            );
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
    }


    /* ==============================================
       HIDE STREAMLIT DEFAULT ELEMENTS
    ============================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    /* ==============================================
       HEADER
    ============================================== */

    .main-title {
        font-size: 52px;
        font-weight: 800;
        line-height: 1.1;

        background: linear-gradient(
            90deg,
            #4f46e5,
            #7c3aed,
            #2563eb
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;

        margin-bottom: 8px;

        animation: slideDown 0.8s ease;
    }

    .subtitle {
        font-size: 18px;
        color: #64748b;
        margin-bottom: 35px;

        animation: fadeUp 1s ease;
    }


    /* ==============================================
       SECTION TITLES
    ============================================== */

    .section-title {
        font-size: 25px;
        font-weight: 750;
        color: #172033;

        margin-top: 30px;
        margin-bottom: 5px;

        animation: fadeUp 0.6s ease;
    }

    .section-description {
        font-size: 14px;
        color: #64748b;

        margin-bottom: 16px;
    }


    /* ==============================================
       UPLOAD BOX
    ============================================== */

    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.95);

        border: 2px dashed #818cf8;
        border-radius: 20px;

        padding: 20px;

        box-shadow:
            0 10px 30px rgba(79, 70, 229, 0.10);

        transition: all 0.3s ease;

        animation: fadeUp 0.7s ease;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: #4f46e5;

        transform: translateY(-4px);

        box-shadow:
            0 16px 35px rgba(79, 70, 229, 0.18);
    }


    /* ==============================================
       FILE INFORMATION
    ============================================== */

    .file-info {
        background: linear-gradient(
            135deg,
            #eef2ff,
            #f5f3ff
        );

        border-left: 5px solid #6366f1;

        border-radius: 14px;

        padding: 16px 20px;

        margin-top: 18px;
        margin-bottom: 25px;

        color: #334155;

        box-shadow:
            0 6px 20px rgba(79, 70, 229, 0.08);

        animation: fadeUp 0.5s ease;
    }


    /* ==============================================
       METRIC CARDS
    ============================================== */

    [data-testid="stMetric"] {

        background: rgba(255, 255, 255, 0.96);

        border: 1px solid #e0e7ff;

        border-radius: 18px;

        padding: 20px;

        box-shadow:
            0 8px 22px rgba(15, 23, 42, 0.07);

        transition: all 0.3s ease;

        animation: fadeUp 0.6s ease;
    }

    [data-testid="stMetric"]:hover {

        transform: translateY(-6px);

        box-shadow:
            0 16px 32px rgba(79, 70, 229, 0.16);
    }

    [data-testid="stMetricLabel"] {
        color: #64748b;
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: #312e81;
        font-weight: 800;
    }


    /* ==============================================
       CLEAN BUTTON
    ============================================== */

    .stButton > button {

        width: 100%;
        height: 58px;

        border: none;
        border-radius: 15px;

        background: linear-gradient(
            90deg,
            #4f46e5,
            #7c3aed
        );

        color: white;

        font-size: 17px;
        font-weight: 700;

        box-shadow:
            0 8px 20px rgba(79, 70, 229, 0.25);

        transition: all 0.3s ease;
    }

    .stButton > button:hover {

        background: linear-gradient(
            90deg,
            #4338ca,
            #6d28d9
        );

        transform: translateY(-4px);

        box-shadow:
            0 14px 28px rgba(79, 70, 229, 0.35);
    }


    /* ==============================================
       DOWNLOAD BUTTON
    ============================================== */

    .stDownloadButton > button {

        width: 100%;
        height: 55px;

        border-radius: 15px;

        border: 2px solid #6366f1;

        background: white;

        color: #4338ca;

        font-size: 16px;
        font-weight: 700;

        transition: all 0.3s ease;
    }

    .stDownloadButton > button:hover {

        background: #eef2ff;

        transform: translateY(-3px);

        box-shadow:
            0 10px 25px rgba(79, 70, 229, 0.15);
    }


    /* ==============================================
       DATA TABLE
    ============================================== */

    [data-testid="stDataFrame"] {

        border-radius: 16px;

        overflow: hidden;

        box-shadow:
            0 8px 24px rgba(15, 23, 42, 0.08);

        animation: fadeUp 0.7s ease;
    }


    /* ==============================================
       SUCCESS MESSAGE
    ============================================== */

    [data-testid="stAlert"] {

        border-radius: 14px;

        animation: fadeUp 0.5s ease;
    }


    /* ==============================================
       DIVIDER
    ============================================== */

    .custom-divider {

        height: 2px;

        background: linear-gradient(
            90deg,
            transparent,
            #c7d2fe,
            #a78bfa,
            #c7d2fe,
            transparent
        );

        margin: 35px 0;
    }


    /* ==============================================
       EMPTY STATE
    ============================================== */

    .empty-state {

        background: rgba(255, 255, 255, 0.85);

        border: 1px solid #e0e7ff;

        border-radius: 22px;

        padding: 55px 30px;

        text-align: center;

        margin-top: 35px;

        box-shadow:
            0 12px 30px rgba(15, 23, 42, 0.06);

        animation: fadeUp 0.8s ease;
    }

    .empty-icon {

        font-size: 55px;

        margin-bottom: 12px;

        animation: floatIcon 2.5s ease-in-out infinite;
    }

    .empty-title {

        font-size: 24px;

        font-weight: 750;

        color: #172033;

        margin-bottom: 8px;
    }

    .empty-text {

        font-size: 15px;

        color: #64748b;
    }


    /* ==============================================
       ANIMATIONS
    ============================================== */

    @keyframes slideDown {

        from {
            opacity: 0;
            transform: translateY(-30px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }

    }


    @keyframes fadeUp {

        from {
            opacity: 0;
            transform: translateY(20px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }

    }


    @keyframes floatIcon {

        0% {
            transform: translateY(0);
        }

        50% {
            transform: translateY(-8px);
        }

        100% {
            transform: translateY(0);
        }

    }

</style>
""", unsafe_allow_html=True)


# ==================================================
# HEADER
# ==================================================

st.markdown(
    '<div class="main-title">🧹 Data Cleaner Agent</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Clean • Validate • Prepare your datasets in seconds'
    '</div>',
    unsafe_allow_html=True
)


# ==================================================
# UPLOAD SECTION
# ==================================================

st.markdown(
    '<div class="section-title">📂 Upload Your Dataset</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Upload a CSV or Excel file to analyze and clean your data.'
    '</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Drag and drop your file here or browse",
    type=["csv", "xlsx"]
)


# ==================================================
# WHEN FILE IS UPLOADED
# ==================================================

if uploaded_file:

    # ----------------------------------------------
    # READ DATASET
    # ----------------------------------------------

    if uploaded_file.name.endswith(".csv"):

        df = pd.read_csv(uploaded_file)

    else:

        df = pd.read_excel(uploaded_file)


    # ----------------------------------------------
    # FILE INFORMATION
    # ----------------------------------------------

    file_size = uploaded_file.size / 1024

    file_type = uploaded_file.name.split(".")[-1].upper()

    st.markdown(
        f"""
        <div class="file-info">
            <b>📄 {uploaded_file.name}</b>
            &nbsp;&nbsp; | &nbsp;&nbsp;
            {file_type} File
            &nbsp;&nbsp; | &nbsp;&nbsp;
            {file_size:.1f} KB
        </div>
        """,
        unsafe_allow_html=True
    )


    # ----------------------------------------------
    # DATASET PREVIEW
    # ----------------------------------------------

    st.markdown(
        '<div class="section-title">👀 Dataset Preview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Preview of the uploaded dataset.'
        '</div>',
        unsafe_allow_html=True
    )

    st.dataframe(
        df.head(100),
        use_container_width=True
    )


    # ==================================================
    # ANALYZE DATASET
    # ==================================================

    report = analyze_dataset(df)


    # ----------------------------------------------
    # DATASET OVERVIEW
    # ----------------------------------------------

    st.markdown(
        '<div class="section-title">📊 Dataset Overview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Quick summary of your dataset before cleaning.'
        '</div>',
        unsafe_allow_html=True
    )


    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Rows",
        report["rows"]
    )

    col2.metric("Missing Values", int(report["missing_values"]))

    col3.metric(
        "Missing Values",
        report["missing_values"]
    )

    col4.metric(
        "Duplicates",
        report["duplicate_rows"]
    )


    # ----------------------------------------------
    # DIVIDER
    # ----------------------------------------------

    st.markdown(
        '<div class="custom-divider"></div>',
        unsafe_allow_html=True
    )


    # ==================================================
    # CLEAN DATASET
    # ==================================================

    st.markdown(
        '<div class="section-title">🧹 Clean Your Dataset</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Remove duplicate records and handle missing values automatically.'
        '</div>',
        unsafe_allow_html=True
    )


    if st.button("✨ Clean My Dataset"):

        # ------------------------------------------
        # CLEANING PROCESS
        # ------------------------------------------

        with st.spinner("Cleaning your dataset..."):

            cleaner = DataCleaner(df)

            cleaned_df = cleaner.run()

            validation = validate_dataset(cleaned_df)


        # ------------------------------------------
        # CLEANING CALCULATIONS
        # ------------------------------------------

        duplicates_removed = int(
            df.duplicated().sum()
        )

        missing_before = int(
            df.isnull().sum().sum()
        )

        remaining_nulls = int(
            cleaned_df.isnull().sum().sum()
        )

        remaining_duplicates = int(
            cleaned_df.duplicated().sum()
        )

        missing_handled = (
            missing_before - remaining_nulls
        )


        # ------------------------------------------
        # SUCCESS MESSAGE
        # ------------------------------------------

        st.success(
            "Dataset cleaned successfully!"
        )


        # ==================================================
        # CLEANING REPORT
        # ==================================================

        st.markdown(
            '<div class="section-title">📋 Cleaning Report</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-description">'
            'Summary of the cleaning operations performed.'
            '</div>',
            unsafe_allow_html=True
        )


        col1, col2, col3, col4 = st.columns(4)


        col1.metric(
            "Duplicates Removed",
            duplicates_removed
        )

        col2.metric(
            "Missing Values Handled",
            missing_handled
        )

        col3.metric(
            "Remaining Nulls",
            remaining_nulls
        )

        col4.metric(
            "Remaining Duplicates",
            remaining_duplicates
        )


        # ==================================================
        # CLEANED DATASET
        # ==================================================

        st.markdown(
            '<div class="section-title">✨ Cleaned Dataset</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-description">'
            'Your dataset after cleaning and validation.'
            '</div>',
            unsafe_allow_html=True
        )


        st.dataframe(
            cleaned_df.head(100),
            use_container_width=True
        )


        # ==================================================
        # DOWNLOAD
        # ==================================================

        csv = cleaned_df.to_csv(
            index=False
        )


        st.markdown(
            '<div style="height:15px;"></div>',
            unsafe_allow_html=True
        )


        st.download_button(
            label="⬇️ Download Clean Dataset",
            data=csv,
            file_name="cleaned_data.csv",
            mime="text/csv"
        )


# ==================================================
# EMPTY STATE
# ==================================================

if uploaded_file is None:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">📊</div>
        <div class="empty-title">Ready to clean your data?</div>
        <div class="empty-text">
            Upload a CSV or Excel dataset above to get started.
        </div>
    </div>
    """, unsafe_allow_html=True)