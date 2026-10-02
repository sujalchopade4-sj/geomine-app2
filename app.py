import io
import pandas as pd
import streamlit as st

# -----------------------------------------------------------------
# PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------
st.set_page_config(
    page_title="GeoMine Intelligence | SIH MVP",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for a professional hackathon-ready UI
st.markdown(
    """
    <style>
    .main {
        background-color: #0b1220;
    }
    .stMetric {
        background-color: #111c2e;
        border: 1px solid #293950;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .stMetric label {
        color: #9db0c8 !important;
    }
    .stAlert {
        background-color: #16243a;
        color: #edf3fb;
        border: 1px solid #293950;
    }
    h1, h2, h3 {
        color: #edf3fb;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------------------------------------
if "records" not in st.session_state:
  st.session_state.records = [
      {
          "record_id": "BH-001",
          "location": "East Block",
          "depth_m": 120,
          "rock_type": "Shale",
          "grade_pct": 0.42,
          "notes": "Fractured core noted; assay verified",
      },
      {
          "record_id": "BH-002",
          "location": "East Block",
          "depth_m": 145,
          "rock_type": "Sandstone",
          "grade_pct": None,
          "notes": "Sample assay pending",
      },
      {
          "record_id": "BH-003",
          "location": "North Ridge",
          "depth_m": 98,
          "rock_type": "Limestone",
          "grade_pct": 0.18,
          "notes": "Lithology logged; sample label requires review",
      },
      {
          "record_id": "BH-004",
          "location": "North Ridge",
          "depth_m": None,
          "rock_type": "Shale",
          "grade_pct": 0.31,
          "notes": "Depth value missing in field sheet",
      },
      {
          "record_id": "BH-005",
          "location": "South Extension",
          "depth_m": 172,
          "rock_type": "Coal seam",
          "grade_pct": 0.76,
          "notes": "Observation entered; confirm unit and lab reference",
      },
  ]

if "reports_count" not in st.session_state:
  st.session_state.reports_count = 2


def get_df():
  return pd.DataFrame(st.session_state.records)


# -----------------------------------------------------------------
# SIDEBAR NAVIGATION
# -----------------------------------------------------------------
st.sidebar.markdown(
    """
    <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 20px;'>
        <div style='background: linear-gradient(135deg,#46dbc3,#7db5ff); width: 35px; height: 35px; border-radius: 8px; display: grid; place-items: center; color: #071721; font-weight: bold; font-size: 18px;'>G</div>
        <div>
            <b style='font-size: 15px; color: white;'>GeoMine Intelligence</b><br>
            <span style='font-size: 11px; color: #9db0c8;'>SIH26023 Workspace</span>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Overview",
        "Data & Documents",
        "Report Studio",
        "Ask Your Data",
        "Review & Audit Trail",
    ],
)

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **Hackathon Mode Active**\nLocal-first transparent validation engine"
)

# -----------------------------------------------------------------
# 1. OVERVIEW PAGE
# -----------------------------------------------------------------
if page == "Overview":
  st.caption("MINISTRY OF COAL · SIH26023 PROTOTYPE")
  st.title("Mining reports, from raw data to review-ready.")
  st.write(
      "A unified workspace to structure geological and mining inputs, flag"
      " data-quality issues, draft consistent reports, and keep every finding"
      " traceable to its source."
  )

  df = get_df()
  total_records = len(df)
  missing_cells = df.isna().sum().sum() + (df == "").sum().sum()
  total_cells = df.size if total_records > 0 else 1
  completeness = (
      int((1 - missing_cells / total_cells) * 100) if total_records > 0 else 0
  )

  # Metrics Row
  col1, col2, col3, col4 = st.columns(4)
  col1.metric("Sources loaded", "3", "Demo dataset")
  col2.metric("Records analysed", total_records)
  col3.metric(
      "Items needing review",
      len(df[df.isna().any(axis=1) | (df == "").any(axis=1)]),
  )
  col4.metric("Draft reports", st.session_state.reports_count)

  st.markdown("### Operational Overview")
  st.success(
      "**Project ID:** EB-04 | **Reporting Period:** Q2 2026 | **Block:** East"
      " Block Exploration"
  )

  st.write(f"**Source Validation Coverage: {completeness}%**")
  st.progress(completeness / 100)

  st.markdown("### Priority Review Queue")
  flagged_rows = df[df.isna().any(axis=1) | (df == "").any(axis=1)]
  if not flagged_rows.empty:
    st.dataframe(flagged_rows, use_container_width=True)
  else:
    st.balloons()
    st.success("All loaded records pass baseline checks!")

# -----------------------------------------------------------------
# 2. DATA & DOCUMENTS PAGE
# -----------------------------------------------------------------
elif page == "Data & Documents":
  st.title("Data Intake & Management")
  st.write(
      "Upload tabular field sheets (CSV or Excel) to update session records"
      " instantly."
  )

  uploaded_file = st.file_uploader(
      "Upload source file (.csv, .xlsx)", type=["csv", "xlsx"]
  )

  if uploaded_file is not None:
    try:
      if uploaded_file.name.endswith(".csv"):
        new_df = pd.read_csv(uploaded_file)
      else:
        new_df = pd.read_excel(uploaded_file)

      st.session_state.records = new_df.to_dict(orient="records")
      st.success(f"Successfully loaded {len(new_df)} records from file!")
      st.rerun()
    except Exception as e:
      st.error(f"Error parsing file: {e}")

  st.subheader("Current Loaded Records Table")
  df = get_df()
  if not df.empty:
    st.dataframe(df, use_container_width=True)
    if st.button("🗑️ Clear Imported Records", type="secondary"):
      st.session_state.records = []
      st.rerun()
  else:
    st.warning("No records loaded. Upload a file above.")

# -----------------------------------------------------------------
# 3. REPORT STUDIO PAGE
# -----------------------------------------------------------------
elif page == "Report Studio":
  st.title("Report Studio")
  st.write(
      "Generate review-ready geological report drafts with built-in data"
      " quality caveats."
  )

  col1, col2 = st.columns([1, 1])
  with col1:
    report_title = st.text_input(
        "Report Title", "Geological Observation and Data Quality Report"
    )
    project_name = st.text_input("Project / Block", "East Block Exploration")
    period = st.text_input("Reporting period", "Q2 2026")
    prepared_by = st.text_input("Prepared by", "SIH26023 Autonomous Team")

  df = get_df()
  total_records = len(df)
  columns = list(df.columns) if not df.empty else []

  report_text = f"""{report_title.upper()}
{'='*len(report_title)}

Project / Block: {project_name}
Reporting Period: {period}
Prepared By: {prepared_by}
Status: DRAFT FOR TECHNICAL REVIEW

1. EXECUTIVE SUMMARY
This report compiles {total_records} active geological records across fields: {', '.join(columns)}. 
Automated transparent validation checks have been applied. Results are preliminary and require authorized engineering verification.

2. OBSERVATION STATISTICS
- Total Borehole/Sample Entries: {total_records}
- Data Schema Columns: {len(columns)}

3. COMPLIANCE & GOVERNANCE CAVEATS
- This tool assists with extraction, consistency checking, and drafting.
- Does not replace certified geological resource calculations or safety audits.
- All flags must be independently verified by a licensed specialist.

Generated by GeoMine Intelligence | SIH26023 Prototype Workspace
"""

  with col2:
    st.subheader("Generated Draft Output")
    st.text_area("Report Preview", report_text, height=300)
    st.download_button(
        "📥 Download Report (.txt)",
        report_text,
        file_name="geomine_report.txt",
        mime="text/plain",
    )
    if st.button("🔄 Refresh Draft Count"):
      st.session_state.reports_count += 1
      st.success("Draft report counter updated!")

# ----------------------------------------------------
# 4. ASK YOUR DATA PAGE
# ----------------------------------------------------
elif page == "Ask Your Data":
  st.title("Evidence Search Engine")
  st.write(
      "Query loaded records and notes using deterministic keyword matching."
  )

  query = st.text_input(
      "Search query",
      placeholder="e.g., shale, pending, fractured core, East Block",
  )

  if query:
    df = get_df()
    if not df.empty:
      # Filter rows where any column contains the query string
      mask = (
          df.astype(str)
          .apply(lambda col: col.str.contains(query, case=False, na=False))
          .any(axis=1)
      )
      results = df[mask]
      st.write(
          f"Found **{len(results)}** matching record(s) for query: `{query}`"
      )
      if not results.empty:
        st.dataframe(results, use_container_width=True)
      else:
        st.info("No matching records found. Try broader keywords.")
    else:
      st.warning("No data available to search.")

# -----------------------------------------------------------------
# 5. REVIEW & AUDIT TRAIL PAGE
# -----------------------------------------------------------------
elif page == "Review & Audit Trail":
  st.title("Review & Audit Trail")
  st.write(
      "Inspect rule-based flags generated from data inconsistencies or pending"
      " status notes."
  )

  df = get_df()
  flags = []

  if not df.empty:
    for idx, row in df.iterrows():
      rid = row.get("record_id", f"Row {idx+1}")
      # Check for missing values
      for col, val in row.items():
        if pd.isna(val) or str(val).strip() == "":
          flags.append({
              "Priority": "Medium",
              "Record": rid,
              "Issue": f"Missing value in '{col}'",
              "Suggested Action": (
                  f"Verify field sheet entry for column {col}."
              ),
          })
      # Check notes for keywords
      notes = str(row.get("notes", ""))
      if any(
          kw in notes.lower()
          for kw in ["pending", "unverified", "review", "missing"]
      ):
        flags.append({
            "Priority": "High",
            "Record": rid,
            "Issue": f"Review flag in notes: {notes}",
            "Suggested Action": (
                "Confirm lab reference or update field status."
            ),
        })

  if flags:
    flags_df = pd.DataFrame(flags)
    st.dataframe(flags_df, use_container_width=True)
  else:
    st.success("No active review flags detected.")
