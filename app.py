import streamlit as st
import pandas as pd
from datetime import datetime
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import colors
import base64

# Set page config
st.set_page_config(
    page_title="CIT Applicant Profile Generator",
    page_icon="📄",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .section-header {
        background-color: #e6f3ff;
        padding: 10px;
        border-radius: 5px;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .info-label {
        font-weight: bold;
        color: #2c3e50;
    }
    .info-value {
        background-color: #f8f9fa;
        padding: 8px;
        border-radius: 3px;
        border-left: 3px solid #3498db;
    }
    .stDownloadButton button {
        width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

def create_pdf_profile(data):
    """Create PDF document from applicant data"""
    buffer = io.BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Heading1'],
        fontSize=16,
        alignment=TA_CENTER,
        spaceAfter=6
    )
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading2'],
        fontSize=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12
    )
    
    label_style = ParagraphStyle(
        'LabelStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#555555'),
        spaceAfter=2
    )
    
    value_style = ParagraphStyle(
        'ValueStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        spaceAfter=8,
        leftIndent=10
    )
    
    section_style = ParagraphStyle(
        'SectionStyle',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#2c3e50'),
        spaceBefore=12,
        spaceAfter=6,
        underline=True
    )
    
    # Content list
    content = []
    
    # Header with contact info
    header_text = "No.37,32nd Lane Colombo 06. Tel:+94112361793 / +94777365964"
    content.append(Paragraph(header_text, header_style))
    
    reg_text = "Reg.No.R/2552/C/238 (MRCA)"
    content.append(Paragraph(reg_text, header_style))
    
    content.append(Spacer(1, 15))
    
    # Title
    title_text = "New Admission Applicant Profile"
    content.append(Paragraph(title_text, title_style))
    
    content.append(Spacer(1, 20))
    
    # Create table data for applicant information
    table_data = []
    
    # Personal Information
    personal_info = [
        ["<b>Full Name</b>", data.get('full_name', '')],
        ["<b>Address</b>", data.get('address', '')],
        ["<b>Mobile (WhatsApp)</b>", data.get('whatsapp_mobile', '')],
        ["<b>Mobile</b>", data.get('mobile', '')],
        ["<b>Date of Birth</b>", data.get('dob', '')],
        ["<b>Place of Birth</b>", data.get('place_of_birth', '')],
        ["<b>NIC No</b>", data.get('nic', 'Not provided')],
        ["<b>Languages Spoken</b>", data.get('languages', '')],
        ["<b>School/College Attended</b>", data.get('school_attended', '')],
        ["<b>Last Institute Attended</b>", data.get('last_institute', '')],
        ["<b>Medium of Instruction</b>", data.get('medium', '')],
        ["<b>Last Standard Acquired</b>", data.get('last_standard', '')],
        ["<b>Year & Month Last Attended</b>", data.get('last_attended', '')],
        ["<b>Completed Memorizing Quran?</b>", data.get('quran_memorized', 'No')],
    ]
    
    if data.get('quran_memorized', '').lower() == 'yes':
        personal_info.append(["<b>If Yes, How Many Juz?</b>", data.get('juz_count', '')])
    
    personal_info.extend([
        ["<b>Islamic Institute Last Attended</b>", data.get('islamic_institute', '')],
        ["<b>City/Location</b>", data.get('city_location', '')],
        ["<b>Duration Attended</b>", data.get('duration', '')],
        ["<b>Reason for Leaving</b>", data.get('reason_leaving', '')],
        ["<b>Parent/Guardian Full Name</b>", data.get('parent_name', '')],
        ["<b>Parent/Guardian Address</b>", data.get('parent_address', '')],
        ["<b>Father Residing</b>", data.get('father_residing', '')],
        ["<b>Occupation</b>", data.get('occupation', '')],
        ["<b>Parent/Guardian Mobile No.</b>", data.get('parent_mobile', '')],
        ["<b>WhatsApp No.</b>", data.get('parent_whatsapp', '')],
        ["<b>Language(s) spoken at home</b>", data.get('home_languages', '')],
    ])
    
    # Convert to Paragraph objects for proper formatting
    for label, value in personal_info:
        table_data.append([Paragraph(label, label_style), Paragraph(value, value_style)])
    
    # Create table
    table = Table(table_data, colWidths=[2.5*inch, 4*inch])
    
    # Style the table
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
    ]))
    
    content.append(table)
    content.append(Spacer(1, 20))
    
    # Build PDF
    doc.build(content)
    
    # Get PDF bytes
    buffer.seek(0)
    return buffer.getvalue()

def get_download_link(pdf_bytes, filename):
    """Generate a download link for the PDF"""
    b64 = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}" style="display: inline-block; padding: 0.5rem 1rem; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 4px; border: none; cursor: pointer; text-align: center;">📥 Download PDF</a>'
    return href

# Title
st.title("📄 CIT Applicant Profile Generator")
st.markdown("---")

# Sidebar for data input
with st.sidebar:
    st.header("📋 Data Input Options")
    
    input_option = st.radio(
        "Choose input method:",
        ["Manual Entry", "Paste Google Forms Data"]
    )
    
    if input_option == "Paste Google Forms Data":
        st.info("Paste a single row from Google Forms")
        pasted_data = st.text_area(
            "Paste Google Forms row here:",
            height=150,
            placeholder="Paste the tab-separated row here...\nExample: 1/3/2026 18:07:21\tMohammed Aslam Muhammed\t19, Ibrahim Road...",
            help="Copy and paste exactly one row from your Google Forms spreadsheet"
        )
        
        if st.button("Parse Google Forms Data"):
            if pasted_data:
                try:
                    # Split by tab
                    fields = pasted_data.strip().split('\t')
                    
                    # Check if we have enough fields (should be 26)
                    if len(fields) >= 26:
                        # Map to our form fields
                        data = {
                            'timestamp': fields[0],
                            'full_name': fields[1],
                            'address': fields[2],
                            'whatsapp_mobile': fields[3],
                            'mobile': fields[4],
                            'dob': fields[5],
                            'place_of_birth': fields[6],
                            'nic': fields[7],
                            'languages': fields[8],
                            'school_attended': fields[9],
                            'last_institute': fields[10],
                            'medium': fields[11],
                            'last_standard': fields[12],
                            'last_attended': fields[13],
                            'quran_memorized': fields[14],
                            'juz_count': fields[15],
                            'islamic_institute': fields[16],
                            'city_location': fields[17],
                            'duration': fields[18],
                            'reason_leaving': fields[19],
                            'parent_name': fields[20],
                            'parent_address': fields[21],
                            'father_residing': fields[22],
                            'occupation': fields[23],
                            'parent_mobile': fields[24],
                            'parent_whatsapp': fields[25],
                            'home_languages': fields[26] if len(fields) > 26 else fields[25]
                        }
                        
                        # Store in session state
                        for key, value in data.items():
                            st.session_state[key] = value
                        
                        st.success("Data parsed successfully!")
                    else:
                        st.error(f"Expected 26+ fields, got {len(fields)}. Please check your data format.")
                except Exception as e:
                    st.error(f"Error parsing data: {str(e)}")
            else:
                st.warning("Please paste some data first")
        
        st.markdown("---")
        st.markdown("**Sample Google Forms Format:**")
        st.code("""Timestamp\tFull Name\tAddress\tMobile (Whatsapp)\tMobile\tDate of Birth\t...
1/3/2026 18:07:21\tMohammed Aslam Muhammed\t19, Ibrahim Road...""")
    
    st.markdown("---")
    st.info("Fill out all fields in the main form and click 'Generate Profile'")

# Initialize session state
for field in ['full_name', 'address', 'whatsapp_mobile', 'mobile', 'dob', 
              'place_of_birth', 'nic', 'languages', 'school_attended', 
              'last_institute', 'medium', 'last_standard', 'last_attended', 
              'quran_memorized', 'juz_count', 'islamic_institute', 'city_location', 
              'duration', 'reason_leaving', 'parent_name', 'parent_address', 
              'father_residing', 'occupation', 'parent_mobile', 'parent_whatsapp', 
              'home_languages']:
    if field not in st.session_state:
        st.session_state[field] = ""

# Main form
with st.form("applicant_form"):
    # Header
    st.markdown('<div class="main-header"><h3>New Admission Applicant Profile</h3></div>', unsafe_allow_html=True)
    
    # Personal Information Section
    st.markdown('<div class="section-header"><h4>Personal Information</h4></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.session_state.full_name = st.text_input("Full Name*", value=st.session_state.full_name, placeholder="Mohammed Shifas Ahamadh")
        st.session_state.address = st.text_area("Address*", value=st.session_state.address, placeholder="38/C Kawdana Road, Dehiwala", height=60)
        
        col1a, col1b = st.columns(2)
        with col1a:
            st.session_state.whatsapp_mobile = st.text_input("Mobile (WhatsApp)*", value=st.session_state.whatsapp_mobile, placeholder="0772226866")
        with col1b:
            st.session_state.mobile = st.text_input("Mobile*", value=st.session_state.mobile, placeholder="0772226866")
        
        st.session_state.dob = st.text_input("Date of Birth*", value=st.session_state.dob, placeholder="19 February 2009")
        st.session_state.place_of_birth = st.text_input("Place of Birth*", value=st.session_state.place_of_birth, placeholder="Akurana")
    
    with col2:
        st.session_state.nic = st.text_input("NIC No", value=st.session_state.nic, placeholder="Leave blank if not available")
        st.session_state.languages = st.text_input("Languages Spoken*", value=st.session_state.languages, placeholder="English, Tamil")
        st.session_state.school_attended = st.text_input("School/College Attended*", value=st.session_state.school_attended, placeholder="Hejazz International, Al Haqqaniyah Arabic College")
        st.session_state.last_institute = st.text_input("Last Institute Attended*", value=st.session_state.last_institute, placeholder="Al Haqqaniyyah Arabic College")
        st.session_state.medium = st.text_input("Medium of Instruction*", value=st.session_state.medium, placeholder="English")
    
    # Educational Information
    st.markdown('<div class="section-header"><h4>Educational Information</h4></div>', unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.session_state.last_standard = st.text_input("Last Standard Acquired*", value=st.session_state.last_standard, placeholder="GCE (O/L)")
        st.session_state.last_attended = st.text_input("Year & Month Last Attended*", value=st.session_state.last_attended, placeholder="2023, June")
        
        quran_options = ["No", "Yes"]
        quran_index = 0 if st.session_state.quran_memorized == "No" else 1
        st.session_state.quran_memorized = st.selectbox("Completed Memorizing Quran?", quran_options, index=quran_index)
        
        if st.session_state.quran_memorized == "Yes":
            st.session_state.juz_count = st.text_input("If Yes, How Many Juz?", value=st.session_state.juz_count, placeholder="30")
        else:
            st.session_state.juz_count = ""
    
    with col4:
        st.session_state.islamic_institute = st.text_input("Islamic Institute Last Attended*", value=st.session_state.islamic_institute, placeholder="Al Haqqaniyyah Arabic College")
        st.session_state.city_location = st.text_input("City/Location*", value=st.session_state.city_location, placeholder="Kandy")
        st.session_state.duration = st.text_input("Duration Attended*", value=st.session_state.duration, placeholder="3 years")
        st.session_state.reason_leaving = st.text_area("Reason for Leaving*", value=st.session_state.reason_leaving, placeholder="Wants to be with parents and continue studies", height=60)
    
    # Parent/Guardian Information
    st.markdown('<div class="section-header"><h4>Parent/Guardian Information</h4></div>', unsafe_allow_html=True)
    
    col5, col6 = st.columns(2)
    
    with col5:
        st.session_state.parent_name = st.text_input("Parent/Guardian Full Name*", value=st.session_state.parent_name, placeholder="Ahamad Farook Mohammed Shifas")
        st.session_state.parent_address = st.text_area("Parent/Guardian Address*", value=st.session_state.parent_address, placeholder="38/C Kawdana Road, Dehiwala", height=60)
        
        residing_options = ["Inland", "Overseas"]
        residing_index = 0 if st.session_state.father_residing in ["", "Inland"] else 1
        st.session_state.father_residing = st.selectbox("Father Residing", residing_options, index=residing_index)
    
    with col6:
        st.session_state.occupation = st.text_input("Occupation*", value=st.session_state.occupation, placeholder="Business")
        
        col6a, col6b = st.columns(2)
        with col6a:
            st.session_state.parent_mobile = st.text_input("Parent/Guardian Mobile No.*", value=st.session_state.parent_mobile, placeholder="0772226866")
        with col6b:
            st.session_state.parent_whatsapp = st.text_input("WhatsApp No.*", value=st.session_state.parent_whatsapp, placeholder="0772226866")
        
        st.session_state.home_languages = st.text_input("Language(s) spoken at home*", value=st.session_state.home_languages, placeholder="English, Tamil")
    
    # Submit button
    submitted = st.form_submit_button("Generate Profile", type="primary")

# Display generated profile
if submitted or any(st.session_state.get(field, '') for field in ['full_name', 'address']):
    st.markdown("---")
    st.markdown("## 📋 Generated Applicant Profile")
    st.markdown("---")
    
    # Create the profile display similar to PDF
    with st.container():
        # Header with contact info (similar to PDF)
        st.markdown(f"""
        <div style='background-color: #f8f9fa; padding: 20px; border-radius: 5px; border-left: 5px solid #3498db; margin-bottom: 20px;'>
            <div style='text-align: center; font-weight: bold; font-size: 16px;'>
                No.37,32nd Lane Colombo 06. Tel:+94112361793 / +94777365964
            </div>
            <div style='text-align: center; margin-top: 10px;'>
                <strong>Reg.No.R/2552/C/238 (MRCA)</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h2 style='text-align: center; color: #2c3e50;'>New Admission Applicant Profile</h2>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Profile content in two columns
        col_left, col_right = st.columns([1, 2])
        
        with col_left:
            st.markdown("#### Applicant Details")
            
            # Create a clean display
            profile_data = [
                ("Full Name", st.session_state.full_name),
                ("Address", st.session_state.address),
                ("Mobile (WhatsApp)", st.session_state.whatsapp_mobile),
                ("Mobile", st.session_state.mobile),
                ("Date of Birth", st.session_state.dob),
                ("Place of Birth", st.session_state.place_of_birth),
                ("NIC No", st.session_state.nic or "Not provided"),
                ("Languages Spoken", st.session_state.languages),
                ("School/College Attended", st.session_state.school_attended),
                ("Last Institute Attended", st.session_state.last_institute),
                ("Medium of Instruction", st.session_state.medium),
                ("Last Standard Acquired", st.session_state.last_standard),
                ("Year & Month Last Attended", st.session_state.last_attended),
                ("Completed Memorizing Quran?", st.session_state.quran_memorized),
            ]
            
            if st.session_state.quran_memorized == "Yes":
                profile_data.append(("If Yes, How Many Juz?", st.session_state.juz_count))
            
            profile_data.extend([
                ("Islamic Institute Last Attended", st.session_state.islamic_institute),
                ("City/Location", st.session_state.city_location),
                ("Duration Attended", st.session_state.duration),
                ("Reason for Leaving", st.session_state.reason_leaving),
                ("Parent/Guardian Full Name", st.session_state.parent_name),
                ("Parent/Guardian Address", st.session_state.parent_address),
                ("Father Residing", st.session_state.father_residing),
                ("Occupation", st.session_state.occupation),
                ("Parent/Guardian Mobile No.", st.session_state.parent_mobile),
                ("WhatsApp No.", st.session_state.parent_whatsapp),
                ("Language(s) spoken at home", st.session_state.home_languages),
            ])
            
            # Display all fields
            for label, value in profile_data:
                if value:  # Only show if there's a value
                    st.markdown(f"""
                    <div style='margin-bottom: 15px;'>
                        <div class='info-label'>{label}</div>
                        <div class='info-value'>{value}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        with col_right:
            st.markdown("#### Additional Information")
            st.info("""
            **Instructions:**
            1. Review all information carefully
            2. Ensure all required fields (*) are filled
            3. Contact information must be accurate
            4. Parent/Guardian details must match supporting documents
            """)
            
            # Summary section
            st.markdown("##### Profile Summary")
            
            summary_data = {
                "Applicant Name": st.session_state.full_name,
                "Date of Birth": st.session_state.dob,
                "Last Education": f"{st.session_state.last_standard} ({st.session_state.last_attended})",
                "Current Status": f"Studied at {st.session_state.last_institute} for {st.session_state.duration}",
                "Parent Contact": st.session_state.parent_mobile,
            }
            
            for key, value in summary_data.items():
                if value:
                    st.markdown(f"**{key}:** {value}")
            
            st.markdown("---")
            
            # Validation status
            required_fields = ['full_name', 'address', 'whatsapp_mobile', 'mobile', 'dob', 
                             'place_of_birth', 'languages', 'school_attended', 'last_institute',
                             'medium', 'last_standard', 'last_attended', 'parent_name',
                             'parent_address', 'occupation', 'parent_mobile', 'parent_whatsapp',
                             'home_languages']
            
            missing_fields = [field for field in required_fields if not st.session_state.get(field, '')]
            
            if missing_fields:
                st.error(f"⚠️ Missing {len(missing_fields)} required field(s)")
                for field in missing_fields:
                    field_name = field.replace('_', ' ').title()
                    st.caption(f"• {field_name}")
            else:
                st.success("✅ All required fields are complete!")
    
    # Download buttons
    st.markdown("---")
    st.markdown("### 📥 Export Options")
    
    # Create PDF if all required fields are filled
    if not missing_fields:
        # Prepare data for PDF
        pdf_data = {}
        for field in ['full_name', 'address', 'whatsapp_mobile', 'mobile', 'dob', 
                     'place_of_birth', 'nic', 'languages', 'school_attended', 
                     'last_institute', 'medium', 'last_standard', 'last_attended', 
                     'quran_memorized', 'juz_count', 'islamic_institute', 'city_location', 
                     'duration', 'reason_leaving', 'parent_name', 'parent_address', 
                     'father_residing', 'occupation', 'parent_mobile', 'parent_whatsapp', 
                     'home_languages']:
            pdf_data[field] = st.session_state.get(field, '')
        
        # Generate PDF
        pdf_bytes = create_pdf_profile(pdf_data)
        
        # Create download buttons
        col_dl1, col_dl2, col_dl3 = st.columns(3)
        
        with col_dl1:
            # Generate filename
            name_part = st.session_state.full_name.replace(" ", "_") if st.session_state.full_name else "Applicant"
            filename = f"CIT_Application_{name_part}.pdf"
            
            # Use Streamlit's download button
            st.download_button(
                label="📥 Download as PDF",
                data=pdf_bytes,
                file_name=filename,
                mime="application/pdf",
                use_container_width=True
            )
        
        with col_dl2:
            # Create formatted text for copying
            profile_text = f"""CIT APPLICANT PROFILE
=============================

APPLICANT INFORMATION:
---------------------
Full Name: {st.session_state.full_name}
Address: {st.session_state.address}
Mobile: {st.session_state.mobile} (WhatsApp: {st.session_state.whatsapp_mobile})
Date of Birth: {st.session_state.dob}
Place of Birth: {st.session_state.place_of_birth}
NIC No: {st.session_state.nic or 'Not provided'}
Languages Spoken: {st.session_state.languages}

EDUCATIONAL BACKGROUND:
----------------------
School/College Attended: {st.session_state.school_attended}
Last Institute Attended: {st.session_state.last_institute}
Medium of Instruction: {st.session_state.medium}
Last Standard Acquired: {st.session_state.last_standard}
Year & Month Last Attended: {st.session_state.last_attended}

Quran Memorization: {st.session_state.quran_memorized}
{f'Juz Count: {st.session_state.juz_count}' if st.session_state.quran_memorized == 'Yes' else ''}

Islamic Institute: {st.session_state.islamic_institute}
City/Location: {st.session_state.city_location}
Duration Attended: {st.session_state.duration}
Reason for Leaving: {st.session_state.reason_leaving}

PARENT/GUARDIAN INFORMATION:
---------------------------
Parent/Guardian Name: {st.session_state.parent_name}
Parent/Guardian Address: {st.session_state.parent_address}
Father Residing: {st.session_state.father_residing}
Occupation: {st.session_state.occupation}
Parent Mobile: {st.session_state.parent_mobile}
Parent WhatsApp: {st.session_state.parent_whatsapp}
Languages at Home: {st.session_state.home_languages}

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            
            st.download_button(
                label="📋 Download as Text",
                data=profile_text,
                file_name=f"CIT_Application_{name_part}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col_dl3:
            if st.button("🔄 Clear Form", use_container_width=True):
                for key in list(st.session_state.keys()):
                    if key not in ['_']:  # Don't clear internal streamlit keys
                        st.session_state[key] = ""
                st.rerun()
    else:
        st.warning("Please fill all required fields (marked with *) before downloading PDF")

# Instructions in sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📝 Instructions")
    st.markdown("""
    1. **Choose input method** above
    2. **Fill all required fields** (*)
    3. **Click 'Generate Profile'**
    4. **Review** the generated profile
    5. **Download** or copy as needed
    """)
    
    st.markdown("---")
    st.markdown("### 📊 Field Guide")
    st.markdown("""
    - **Timestamp**: From Google Forms
    - **NIC No**: Optional
    - **Juz Count**: Only if memorized Quran
    - **All other fields**: Required
    """)

# Footer
st.markdown("---")
st.caption("CIT Applicant Profile Generator v1.0 | Automatically formats data to match official PDF template")
