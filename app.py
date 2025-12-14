import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO, StringIO
import base64
from datetime import datetime
import re
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import colors
from reportlab.lib.units import inch
import tempfile
import zipfile
import os

# Page configuration
st.set_page_config(
    page_title="CIT Applicant Profile Generator",
    page_icon="📋",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .section-header {
        font-size: 1.5rem;
        color: #1E3A8A;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #1E3A8A;
        padding-bottom: 0.5rem;
    }
    .input-area {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 2px dashed #1E3A8A;
        margin-bottom: 20px;
    }
    .preview-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #ddd;
        font-family: monospace;
        white-space: pre-wrap;
        overflow-x: auto;
        max-height: 300px;
        overflow-y: auto;
    }
    .stButton>button {
        width: 100%;
        background-color: #1E3A8A;
        color: white;
        font-weight: bold;
    }
    .success-msg {
        background-color: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<div class="main-header">📋 CIT Applicant Profile Generator</div>', unsafe_allow_html=True)

# Sidebar for instructions
with st.sidebar:
    st.markdown("## 📋 Instructions")
    st.markdown("""
    ### How to use:
    1. **Copy data from Google Sheets** - Select and copy the entire table including headers
    2. **Paste in the text area** - Use Ctrl+V or right-click to paste
    3. **Configure settings** - Adjust column mappings if needed
    4. **Generate PDFs** - Create individual PDFs or a zip file

    ### Expected Data Format:
    - The first row should contain column headers
    - Each row represents one applicant
    - Data should be tab-separated (default from Google Sheets)

    ### Required Columns:
    - Full Name
    - Address
    - Mobile (WhatsApp)
    - Date of Birth
    - Place of Birth
    - Languages Spoken
    - School/College Attended
    - Last Institute Attended
    - And other fields from the sample PDF

    ### Tip:
    Copy the exact format from Google Sheets including all columns.
    """)
    
    st.markdown("---")
    st.markdown("#### Sample Data Format")
    st.code("""Full Name\tAddress\tMobile (WhatsApp)\tDate of Birth
John Doe\t123 Main St\t0771234567\t2009-02-19
Jane Smith\t456 Oak Ave\t0787654321\t2008-05-15""")
    
    st.markdown("---")
    st.markdown("#### About")
    st.markdown("""
    **Version:** 2.0
    **Features:**
    - Batch PDF generation
    - Custom column mapping
    - Exact PDF formatting
    - Zip file download
    """)

# Function to create PDF for a single applicant
def create_applicant_pdf(data_dict, output_filename):
    """Create a PDF in the exact format of the provided sample"""
    
    # Create a BytesIO buffer for the PDF
    buffer = BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    address_style = ParagraphStyle(
        'AddressStyle',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_RIGHT
    )
    
    reg_style = ParagraphStyle(
        'RegStyle',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_RIGHT,
        spaceAfter=20
    )
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=14,
        alignment=TA_CENTER,
        spaceAfter=30,
        spaceBefore=20
    )
    
    label_style = ParagraphStyle(
        'LabelStyle',
        parent=styles['Normal'],
        fontSize=11,
        fontName='Helvetica-Bold',
        spaceAfter=5
    )
    
    value_style = ParagraphStyle(
        'ValueStyle',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=10
    )
    
    # Build the story (content)
    story = []
    
    # Page 1 content
    # Top right address and telephone
    address_text = f"{data_dict.get('address_line', 'No.37,32nd Lane Colombo 06.')} Tel:{data_dict.get('telephone', '+94112361793 / +94777365964')}"
    story.append(Paragraph(address_text, address_style))
    
    # Registration number
    reg_text = f"Reg.No.{data_dict.get('reg_no', 'R/2552/C/238 (MRCA)')}"
    story.append(Paragraph(reg_text, reg_style))
    
    # Title
    story.append(Paragraph("New Admission Applicant Profile", title_style))
    
    # Create a table for the form-like layout
    form_data = []
    
    # Function to add field to form
    def add_field(label, value):
        if pd.isna(value) or str(value).strip() == '':
            value = ''
        form_data.append([Paragraph(label, label_style), Paragraph(str(value), value_style)])
    
    # Add all fields in order
    add_field("Full Name", data_dict.get('Full Name', ''))
    add_field("Address", data_dict.get('Address', ''))
    add_field("Mobile (WhatsApp)", data_dict.get('Mobile (WhatsApp)', data_dict.get('Mobile', '')))
    add_field("Mobile", data_dict.get('Mobile', ''))
    
    # Format date
    dob = data_dict.get('Date of Birth', '')
    if dob:
        try:
            if isinstance(dob, str):
                # Try to parse the date
                for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y', '%Y.%m.%d'):
                    try:
                        dob_date = datetime.strptime(str(dob), fmt)
                        dob = dob_date.strftime('%d %B %Y')
                        break
                    except:
                        continue
        except:
            pass
    
    add_field("Date of Birth", dob)
    add_field("Place of Birth", data_dict.get('Place of Birth', ''))
    add_field("NIC No", data_dict.get('NIC No', ''))
    add_field("Languages Spoken", data_dict.get('Languages Spoken', ''))
    add_field("School/College Attended", data_dict.get('School/College Attended', ''))
    add_field("Last Institute Attended", data_dict.get('Last Institute Attended', ''))
    add_field("Medium of Instruction", data_dict.get('Medium of Instruction', ''))
    add_field("Last Standard Acquired", data_dict.get('Last Standard Acquired', ''))
    add_field("Year & Month Last Attended", data_dict.get('Year & Month Last Attended', ''))
    
    # Quran memorization
    quran_mem = data_dict.get('Completed Memorizing Quran?', 'No')
    add_field("Completed Memorizing Quran?", quran_mem)
    
    if quran_mem == 'Yes':
        add_field("If Yes,How Many Juz?", data_dict.get('If Yes,How Many Juz?', ''))
    
    add_field("Islamic Institute Last Attended", data_dict.get('Islamic Institute Last Attended', ''))
    add_field("City/Location", data_dict.get('City/Location', ''))
    add_field("Duration Attended", data_dict.get('Duration Attended', ''))
    add_field("Reason for Leaving", data_dict.get('Reason for Leaving', ''))
    add_field("Parent/Guardian Full Name", data_dict.get('Parent/Guardian Full Name', ''))
    add_field("Parent/Guardian Address", data_dict.get('Parent/Guardian Address', ''))
    add_field("Father Residing", data_dict.get('Father Residing', ''))
    add_field("Occupation", data_dict.get('Occupation', ''))
    add_field("Parent/Guardian Mobile No.", data_dict.get('Parent/Guardian Mobile No.', ''))
    add_field("WhatsApp No.", data_dict.get('WhatsApp No.', ''))
    add_field("Language(s)Spoken at Home", data_dict.get('Language(s)Spoken at Home', ''))
    
    # Additional Notes
    add_field("Additional Notes:", data_dict.get('Additional Notes', ''))
    
    # Create table for the form
    table = Table(form_data, colWidths=[2.5*inch, 4*inch])
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    
    story.append(table)
    
    # Add page break for second page
    story.append(PageBreak())
    
    # Page 2 - Empty (but we need to add something to create the page)
    story.append(Spacer(1, 12*inch))
    
    # Build PDF
    doc.build(story)
    
    # Get PDF bytes
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes

# Main application
st.markdown('<div class="section-header">Step 1: Paste Data from Google Sheets</div>', unsafe_allow_html=True)

# Input area for pasting data
st.markdown("### 📋 Paste your data here:")
st.markdown("""
<div class="input-area">
Copy your data from Google Sheets (including headers) and paste it below.
The app will automatically detect the format.
</div>
""", unsafe_allow_html=True)

# Text area for pasting data
pasted_data = st.text_area(
    "Paste your data here (Ctrl+V):",
    height=200,
    help="Paste the entire table from Google Sheets. Include headers in the first row."
)

# Delimiter selection
col1, col2, col3 = st.columns(3)
with col1:
    delimiter = st.selectbox(
        "Select delimiter:",
        ["Tab (\\t)", "Comma (,)", "Semicolon (;)", "Pipe (|)"],
        index=0
    )
    
    # Map delimiter selection
    delimiter_map = {
        "Tab (\\t)": "\t",
        "Comma (,)": ",",
        "Semicolon (;)": ";",
        "Pipe (|)": "|"
    }
    selected_delimiter = delimiter_map[delimiter]

with col2:
    header_option = st.radio(
        "First row contains headers?",
        ["Yes", "No"],
        index=0
    )
    has_header = header_option == "Yes"

with col3:
    encoding_option = st.selectbox(
        "Text encoding:",
        ["UTF-8", "ISO-8859-1", "Windows-1252"],
        index=0
    )

# Process the pasted data
df = None
if pasted_data:
    try:
        # Read the pasted data
        df = pd.read_csv(
            StringIO(pasted_data),
            delimiter=selected_delimiter,
            header=0 if has_header else None,
            encoding=encoding_option,
            dtype=str,
            keep_default_na=False
        )
        
        st.success(f"✅ Successfully parsed {len(df)} rows with {len(df.columns)} columns!")
        
        # Display preview
        st.markdown("### 👁️ Data Preview:")
        st.dataframe(df.head(), use_container_width=True)
        
        # Show column statistics
        st.markdown("#### 📊 Column Information:")
        col_info = pd.DataFrame({
            'Column Name': df.columns,
            'Non-Empty Values': df.notna().sum(),
            'Data Type': df.dtypes.astype(str)
        })
        st.dataframe(col_info, use_container_width=True, hide_index=True)
        
    except Exception as e:
        st.error(f"❌ Error parsing data: {str(e)}")
        st.info("""
        **Troubleshooting tips:**
        1. Make sure you selected the correct delimiter
        2. Check if the first row contains column headers
        3. Try copying the data again from Google Sheets
        4. Ensure there are no merged cells in your Google Sheet
        """)

# Step 2: Column mapping and configuration
if df is not None and not df.empty:
    st.markdown('<div class="section-header">Step 2: Configure PDF Settings</div>', unsafe_allow_html=True)
    
    # Required fields from the PDF
    pdf_fields = [
        'Full Name',
        'Address',
        'Mobile (WhatsApp)',
        'Mobile',
        'Date of Birth',
        'Place of Birth',
        'NIC No',
        'Languages Spoken',
        'School/College Attended',
        'Last Institute Attended',
        'Medium of Instruction',
        'Last Standard Acquired',
        'Year & Month Last Attended',
        'Completed Memorizing Quran?',
        'If Yes,How Many Juz?',
        'Islamic Institute Last Attended',
        'City/Location',
        'Duration Attended',
        'Reason for Leaving',
        'Parent/Guardian Full Name',
        'Parent/Guardian Address',
        'Father Residing',
        'Occupation',
        'Parent/Guardian Mobile No.',
        'WhatsApp No.',
        'Language(s)Spoken at Home',
        'Additional Notes'
    ]
    
    # Default values
    default_values = {
        'address_line': 'No.37,32nd Lane Colombo 06.',
        'telephone': '+94112361793 / +94777365964',
        'reg_no': 'R/2552/C/238 (MRCA)'
    }
    
    # Create column mapping interface
    st.markdown("### 🗺️ Column Mapping (Optional)")
    st.markdown("If your column names don't match exactly, you can map them here:")
    
    # Create a simple mapping interface
    mapping_cols = st.columns(3)
    field_mapping = {}
    
    for i, field in enumerate(pdf_fields):
        col_idx = i % 3
        with mapping_cols[col_idx]:
            available_columns = ['(Not Mapped)'] + list(df.columns)
            selected_col = st.selectbox(
                f"{field}:",
                available_columns,
                index=0
            )
            if selected_col != '(Not Mapped)':
                field_mapping[field] = selected_col
    
    # PDF header settings
    st.markdown("### 📄 PDF Header Settings")
    header_col1, header_col2, header_col3 = st.columns(3)
    
    with header_col1:
        address_line = st.text_input("Address Line:", value=default_values['address_line'])
    
    with header_col2:
        telephone = st.text_input("Telephone:", value=default_values['telephone'])
    
    with header_col3:
        reg_no_template = st.text_input("Registration No. Template:", value=default_values['reg_no'])
    
    # Step 3: Generate PDFs
    st.markdown('<div class="section-header">Step 3: Generate PDFs</div>', unsafe_allow_html=True)
    
    # Generation options
    gen_col1, gen_col2 = st.columns(2)
    
    with gen_col1:
        generate_all = st.button("📄 Generate All PDFs (as ZIP)", type="primary")
    
    with gen_col2:
        # For single PDF generation, let user select a row
        selected_index = st.selectbox(
            "Select applicant to generate single PDF:",
            range(len(df)),
            format_func=lambda x: f"Row {x+1}: {df.iloc[x].get('Full Name', 'Unknown') if 'Full Name' in df.columns else 'Unknown'}"
        )
        generate_single = st.button("📄 Generate Single PDF")
    
    # Function to process row data
    def prepare_row_data(row):
        data_dict = {}
        
        # Add mapped fields
        for pdf_field, sheet_field in field_mapping.items():
            if sheet_field in row:
                data_dict[pdf_field] = row[sheet_field]
        
        # Add unmapped fields (direct match)
        for pdf_field in pdf_fields:
            if pdf_field not in data_dict and pdf_field in row:
                data_dict[pdf_field] = row[pdf_field]
        
        # Add PDF header info
        data_dict['address_line'] = address_line
        data_dict['telephone'] = telephone
        
        # Customize reg number if needed
        reg_num = reg_no_template
        if 'Full Name' in data_dict and data_dict['Full Name']:
            # Create a simple ID from name
            name_id = ''.join([c for c in data_dict['Full Name'] if c.isalpha()])[:5].upper()
            reg_num = f"R/{name_id}/{datetime.now().strftime('%y%m')}"
        
        data_dict['reg_no'] = reg_num
        
        return data_dict
    
    # Generate single PDF
    if generate_single and df is not None:
        try:
            row = df.iloc[selected_index]
            data_dict = prepare_row_data(row)
            
            # Generate PDF
            pdf_bytes = create_applicant_pdf(data_dict, f"applicant_{selected_index + 1}")
            
            # Create download button
            applicant_name = data_dict.get('Full Name', f"applicant_{selected_index + 1}")
            safe_name = "".join([c for c in applicant_name if c.isalnum() or c in (' ', '-', '_')]).rstrip()
            
            st.markdown(f'<div class="success-msg">✅ PDF generated for: {applicant_name}</div>', unsafe_allow_html=True)
            
            st.download_button(
                label=f"📥 Download {safe_name}.pdf",
                data=pdf_bytes,
                file_name=f"CIT_Applicant_{safe_name}.pdf",
                mime="application/pdf"
            )
            
        except Exception as e:
            st.error(f"Error generating PDF: {str(e)}")
    
    # Generate all PDFs as ZIP
    if generate_all and df is not None:
        try:
            with st.spinner(f"Generating {len(df)} PDFs... This may take a moment."):
                # Create a temporary directory for PDFs
                with tempfile.TemporaryDirectory() as tmpdir:
                    zip_buffer = BytesIO()
                    
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                        for idx, row in df.iterrows():
                            try:
                                data_dict = prepare_row_data(row)
                                applicant_name = data_dict.get('Full Name', f"applicant_{idx + 1}")
                                safe_name = "".join([c for c in applicant_name if c.isalnum() or c in (' ', '-', '_')]).rstrip()
                                
                                # Generate PDF
                                pdf_bytes = create_applicant_pdf(data_dict, f"applicant_{idx + 1}")
                                
                                # Add to ZIP
                                zip_file.writestr(f"CIT_Applicant_{safe_name}.pdf", pdf_bytes)
                                
                            except Exception as e:
                                st.warning(f"Could not generate PDF for row {idx + 1}: {str(e)}")
                    
                    zip_buffer.seek(0)
                    
                    st.markdown(f'<div class="success-msg">✅ Successfully generated {len(df)} PDFs!</div>', unsafe_allow_html=True)
                    
                    st.download_button(
                        label="📦 Download All PDFs (ZIP)",
                        data=zip_buffer,
                        file_name="CIT_Applicant_Profiles.zip",
                        mime="application/zip"
                    )
                    
        except Exception as e:
            st.error(f"Error generating ZIP file: {str(e)}")

# Sample data for testing
if not pasted_data:
    st.markdown('<div class="section-header">💡 Need Sample Data?</div>', unsafe_allow_html=True)
    
    if st.button("Load Sample Data for Testing"):
        sample_data = """Full Name	Address	Mobile (WhatsApp)	Mobile	Date of Birth	Place of Birth	NIC No	Languages Spoken	School/College Attended	Last Institute Attended	Medium of Instruction	Last Standard Acquired	Year & Month Last Attended	Completed Memorizing Quran?	If Yes,How Many Juz?	Islamic Institute Last Attended	City/Location	Duration Attended	Reason for Leaving	Parent/Guardian Full Name	Parent/Guardian Address	Father Residing	Occupation	Parent/Guardian Mobile No.	WhatsApp No.	Language(s)Spoken at Home	Additional Notes
Mohammed Shifas Ahamadh	38/C Kawdana Road,Dehiwala	0772226866	0772226866	2009-02-19	Akurana			English,Tamil	Hejazz International,Al Haqqaniyah Arabic College	Al Haqqaniyyah Arabic College	English	GCE (O/L)		No		Al Haqqaniyyah Arabic College	Kandy	3 years	Wants to be with parents and continue studies	Ahamad Farook Mohammed Shifas	38/C Kawdana Road,Dehiwala	Inland	Business	0772226866	0772226866	English,Tamil	
Ali Raza Khan	45/D Marine Drive,Colombo 03	0771112222	0771112222	2008-05-15	Colombo			English,Sinhala,Tamil	Colombo International School	Colombo International School	English	GCE (O/L)	2023-06	Yes	15	Al-Azhar College	Colombo	2 years	Higher education	Raza Ahmed Khan	45/D Marine Drive,Colombo 03	Inland	Doctor	0773334444	0773334444	English,Sinhala	Excellent academic record"""
        
        st.code(sample_data, language="text")
        st.info("Copy this sample data and paste it above to test the application.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; font-size: 0.9rem;'>"
    "CIT Applicant Profile Generator v2.0 | Google Sheets to PDF Converter"
    "</div>",
    unsafe_allow_html=True
)
