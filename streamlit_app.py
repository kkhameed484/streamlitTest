import streamlit as st
# Import the function module directly from your local file directory
from pdf_generator import create_report_pdf

st.set_page_config(page_title="PDF Engine Client", layout="centered")

st.title("💼 Enterprise PDF Generator")
st.write("Fill out the configuration dashboard settings to dynamically construct a personalized ReportLab download binary file.")

# Collect dynamic properties using Streamlit UI components
form_user = st.text_input("Author Name", value="Jane Doe")
form_title = st.text_input("Report Subject Header", value="Q3 Cloud Infrastructure Metrics Summary")

# Setup a clean mockup grid array dataset
mock_dataset = [
    ["Target Platform Server", "Regional Zone", "System Load Balance"],
    ["AWS Cloud Infrastructure Instance 01", "us-east-1", "Operational - 42% Capacity"],
    ["Google Cloud Engine Storage Cluster", "us-central1", "Operational - 18% Capacity"],
    ["Microsoft Azure Active Directory Node", "eu-west-2", "Degraded - 89% Capacity Request Surge"]
]

st.divider()
st.subheader("Preview Dataset Matrix")
st.table(mock_dataset)

# Trigger calculation call when the download button is invoked by the browser client
if st.button("🚀 Compile and Prepare Document Stream"):
    with st.spinner("Processing vector graphics layout assets..."):
        # Compile document through the standalone layout engine backend file
        processed_pdf_stream = create_report_pdf(
            user_name=form_user,
            report_title=form_title,
            table_data=mock_dataset
        )
        
        # Present the generated buffer to the client via native browser download mechanics
        st.download_button(
            label="💾 Download Generated PDF File",
            data=processed_pdf_stream,
            file_name="enterprise_system_report.pdf",
            mime="application/pdf"
        )
        st.success("PDF compilation successfully written into memory channel stream!")
