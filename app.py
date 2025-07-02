import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Page config
st.set_page_config(page_title="Labeling Process Review Form", layout="wide")
st.title("📋 Labeling Process Review Form")
st.write("Please review each step and provide confirmation or corrections where necessary. Steps with '-' are added diagnostic questions.")

# Define steps
steps = [
    "Planner creates a job order in Oracle.",
    "Serial numbers are assigned to the order.",
    "Job details and serial are recorded in Job Orders.xlsx.",
    "Planner notifies Production Lead to begin label preparation.",
    "Production Lead opens Job Orders.xlsx and retrieves serial information.",
    "Information is copied into Upload File Generator v8.0.xlsm, which outputs a .txt file.",
    "The .txt file is uploaded to the ASML Supplier Portal (https://federation.asml.com/...).",
    "The portal returns one or more barcode strings.",
    "Returned data is copied into ASML Portal Download.xlsx.",
    " Barcode label is printed from the ASML data.",
    " The first barcode scan check is performed by Production Lead.",
    " If passed, the label is given to the Production Operator.",
    " Second scan check is conducted by the Production Team.",
    " Optionally, QA visually verifies the label and captures a photo.",
    " Unit proceeds to shipment if all checks pass.",
    " Was the job order type (standard/non-standard) clearly specified?",
    " Was the 12NC cross-checked before upload?",
    " Was the ASML barcode preview verified before printing?",
    " Were duplicate serial numbers checked before submission?",
    " Was the Upload File Generator .xlsm version verified?",
    " Were any errors or warnings seen during ASML upload?",
    " Was the ASML Portal Download.xlsx file saved immediately after upload?",
    " Did the Production Lead confirm label matches expected format?",
    " Was there a process for label reprint if scan failed?",
    " Were old labels removed from RTF units before relabeling?",
    " Was the QA team notified if label placement looked incorrect?",
    " Was the barcode tested on the final part (not just printed)?",
    " Were photos of labeled parts consistently saved for traceability?",
    " Were rejected barcodes recorded or flagged anywhere?",
    " Was shipment confirmed in Oracle after labeling?"
]

# Collect user responses
responses = []

for i, step in enumerate(steps):
    is_diagnostic = i >= 15
    step_number = f"{i+1}"
    step_desc_clean = step.replace("'- ", "") if is_diagnostic else step

    st.markdown(f"### Step {step_number}: {step_desc_clean}")
    answer = st.radio("Is this step accurate?", ["Yes", "No", "Not Sure"], key=f"answer_{i}")
    comment = st.text_area("Comment or correction (optional):", key=f"comment_{i}")

    responses.append({
        "Step": step_number,
        "Step Description": step_desc_clean,
        "Is this step correct?": answer,
        "Comment": comment
    })

    st.markdown("---")

# Submit and download
if st.button("✅ Submit Review"):
    df = pd.DataFrame(responses)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"label_review_{timestamp}.csv"
    csv = df.to_csv(index=False).encode('utf-8')

    st.success("✅ Review submitted successfully!")

    st.download_button(
        label="📥 Download Your Responses",
        data=csv,
        file_name=filename,
        mime='text/csv',
    )

# Quit
if st.button("🚪 Quit App"):
    st.warning("Shutting down the app...")
    os._exit(0)
