import streamlit as st
import pandas as pd
from datetime import datetime
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
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

def create_pdf_profile_exact_format(data):
    """Create PDF document exactly like the original PDF format"""
    buffer = io.BytesIO()
    
    # Create PDF with A4 size
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Set font - using standard Helvetica for exact match
    c.setFont("Helvetica", 10)
    
    # Header section (top of page)
    # First line: Address and phone
    c.setFont("Helvetica-Bold", 11)
    c.drawString(30, height - 40, "No.37,32nd Lane Colombo 06. Tel:+94112361793 / +94777365964")
    
    # Second line: Registration number
    c.setFont("Helvetica-Bold", 11)
    c.drawString(30, height - 55, "Reg.No.R/2552/C/238 (MRCA)")
    
    # Title
    c.setFont("Helvetica-Bold", 14)
    c.drawString(width/2 - 100, height - 85, "New Admission Applicant Profile")
    
    # Draw a line under the title
    c.line(30, height - 95, width - 30, height - 95)
    
    # Starting position for content
    y_position = height - 120
    
    # Define field labels exactly as in the PDF
    field_labels = [
        "Full Name",
        "Address",
        "Mobile (WhatsApp)",
        "Mobile",
        "Date of Birth",
        "Place of Birth",
        "NIC No",
        "Languages Spoken",
        "School/College Attended",
        "Last Institute Attended",
        "Medium of Instruction",
        "Last Standard Acquired",
        "Year & Month Last Attended",
        "Completed Memorizing Quran?",
        "If Yes,How Many Juz?",
        "Islamic Institute Last Attended",
        "City/Location",
        "Duration Attended",
        "Reason for Leaving",
        "Parent/Guardian Full Name",
        "Parent/Guardian Address",
        "Father Residing",
        "Occupation",
        "Parent/Guardian Mobile No.",
        "WhatsApp No.",
        "Language(s)Spoken at Home"
    ]
    
    # Define data fields mapping
    data_mapping = {
        "Full Name": data.get('full_name', ''),
        "Address": data.get('address', ''),
        "Mobile (WhatsApp)": data.get('whatsapp_mobile', ''),
        "Mobile": data.get('mobile', ''),
        "Date of Birth": data.get('dob', ''),
        "Place of Birth": data.get('place_of_birth', ''),
        "NIC No": data.get('nic', ''),
        "Languages Spoken": data.get('languages', ''),
        "School/College Attended": data.get('school_attended', ''),
        "Last Institute Attended": data.get('last_institute', ''),
        "Medium of Instruction": data.get('medium', ''),
        "Last Standard Acquired": data.get('last_standard', ''),
        "Year & Month Last Attended": data.get('last_attended', ''),
        "Completed Memorizing Quran?": data.get('quran_memorized', 'No'),
        "If Yes,How Many Juz?": data.get('juz_count', '') if data.get('quran_memorized', '').lower() == 'yes' else '',
        "Islamic Institute Last Attended": data.get('islamic_institute', ''),
        "City/Location": data.get('city_location', ''),
        "Duration Attended": data.get('duration', ''),
        "Reason for Leaving": data.get('reason_leaving', ''),
        "Parent/Guardian Full Name": data.get('parent_name', ''),
        "Parent/Guardian Address": data.get('parent_address', ''),
        "Father Residing": data.get('father_residing', ''),
        "Occupation": data.get('occupation', ''),
        "Parent/Guardian Mobile No.": data.get('parent_mobile', ''),
        "WhatsApp No.": data.get('parent_whatsapp', ''),
        "Language(s)Spoken at Home": data.get('home_languages', '')
    }
    
    # Draw each field and value
    c.setFont("Helvetica", 11)
    
    for i, label in enumerate(field_labels):
        # Skip "If Yes,How Many Juz?" if Quran is not memorized
        if label == "If Yes,How Many Juz?" and data.get('quran_memorized', '').lower() != 'yes':
            continue
            
        # Check if we need a new page
        if y_position < 100:
            c.showPage()
            # Reset font and position for new page
            c.setFont("Helvetica", 11)
            y_position = height - 40
            
        # Draw label
        c.setFont("Helvetica", 11)
        c.drawString(30, y_position, label)
        
        # Draw value (if exists)
        value = data_mapping.get(label, '')
        if value:
            c.setFont("Helvetica", 11)
            # Wrap text if too long
            max_width = width - 60
            value_lines = []
            words = str(value).split()
            current_line = []
            
            for word in words:
                current_line.append(word)
                test_line = ' '.join(current_line)
                if c.stringWidth(test_line, "Helvetica", 11) > max_width:
                    if len(current_line) > 1:
                        value_lines.append(' '.join(current_line[:-1]))
                        current_line = [word]
                    else:
                        value_lines.append(word)
                        current_line = []
            
            if current_line:
                value_lines.append(' '.join(current_line))
            
            # Draw each line of the value
            for line_num, line in enumerate(value_lines):
                c.drawString(30, y_position - (15 * (line_num + 1)), line)
            
            # Adjust y_position based on number of lines
            y_position -= (15 * (len(value_lines) + 1))
        else:
            # Empty line if no value
            y_position -= 30
        
        # Add some space between fields
        y_position -= 5
    
    # Draw "Additional Notes:" at the bottom if space
    if y_position > 100:
        c.setFont("Helvetica", 11)
        c.drawString(30, y_position, "Additional Notes:")
    
    # Save the PDF
    c.save()
    
    # Get PDF bytes
    buffer.seek(0)
    return buffer.getvalue()

def create_pdf_profile(data):
    """Alternative PDF creation with table format"""
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
    
    # Custom styles matching original PDF
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        alignment=TA_LEFT,
        spaceAfter=6
    )
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        alignment=TA_CENTER,
        spaceAfter=12
    )
    
    label_style = ParagraphStyle(
        'LabelStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        spaceAfter=2
    )
    
    value_style = ParagraphStyle(
        'ValueStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        spaceAfter=8,
        leftIndent=0
    )
    
    # Content list
    content = []
    
    # Header with contact info (exactly like PDF)
    header_text = "No.37,32nd Lane Colombo 06. Tel:+94112361793 / +94777365964"
    content.append(Paragraph(header_text, header_style))
    
    reg_text = "Reg.No.R/2552/C/238 (MRCA)"
    content.append(Paragraph(reg_text, header_style))
    
    content.append(Spacer(1, 10))
    
    # Title
    title_text = "New Admission Applicant Profile"
    content.append(Paragraph(title_text, title_style))
    
    content.append(Spacer(1, 20))
    
    # Prepare data in exact PDF format
    field_data = [
        ("Full Name", data.get('full_name', '')),
        ("Address", data.get('address', '')),
        ("Mobile (WhatsApp)", data.get('whatsapp_mobile', '')),
        ("Mobile", data.get('mobile', '')),
        ("Date of Birth", data.get('dob', '')),
        ("Place of Birth", data.get('place_of_birth', '')),
        ("NIC No", data.get('nic', '')),
        ("Languages Spoken", data.get('languages', '')),
        ("School/College Attended", data.get('school_attended', '')),
        ("Last Institute Attended", data.get('last_institute', '')),
        ("Medium of Instruction", data.get('medium', '')),
        ("Last Standard Acquired", data.get('last_standard', '')),
        ("Year & Month Last Attended", data.get('last_attended', '')),
        ("Completed Memorizing Quran?", data.get('quran_memorized', 'No')),
    ]
    
    if data.get('quran_memorized', '').lower() == 'yes':
        field_data.append(("If Yes,How Many Juz?", data.get('juz_count', '')))
    
    field_data.extend([
        ("Islamic Institute Last Attended", data.get('islamic_institute', '')),
        ("City/Location", data.get('city_location', '')),
        ("Duration Attended", data.get('duration', '')),
        ("Reason for Leaving", data.get('reason_leaving', '')),
        ("Parent/Guardian Full Name", data.get('parent_name', '')),
        ("Parent/Guardian Address", data.get('parent_address', '')),
        ("Father Residing", data.get('father_residing', '')),
        ("Occupation", data.get('occupation', '')),
        ("Parent/Guardian Mobile No.", data.get('parent_mobile', '')),
        ("WhatsApp No.", data.get('parent_whatsapp', '')),
        ("Language(s)Spoken at Home", data.get('home_languages', '')),
    ])
    
    # Create content with label and value on separate lines
    for label, value in field_data:
        # Skip empty Juz field if Quran not memorized
        if label == "If Yes,How Many Juz?" and not value:
            continue
            
        content.append(Paragraph(label, label_style))
        if value:
            content.append(Paragraph(value, value_style))
        else:
            content.append(Paragraph(" ", value_style))  # Empty line
        content.append(Spacer(1, 5))
    
    # Add Additional Notes at the end
    content.append(Spacer(1, 10))
    content.append(Paragraph("Additional Notes:", label_style))
    
    # Build PDF
    doc.build(content)
    
    # Get PDF bytes
    buffer.seek(0)
    return buffer.getvalue()

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
        
        # Generate PDF using exact format function
        pdf_bytes = create_pdf_profile_exact_format(pdf_data)
        
        # Create download buttons
        col_dl1, col_dl2, col_dl3 = st.columns(3)
        
        with col_dl1:
            # Generate filename
            name_part = st.session_state.full_name.replace(" ", "_") if st.session_state.full_name else "Applicant"
            filename = f"CIT_Application_{name_part}.pdf"
            
            # Use Streamlit's download button
            st.download_button(
                label="📥 Download as PDF (Exact Format)",
                data=pdf_bytes,
                file_name=filename,
                mime="application/pdf",
                use_container_width=True,
                help="Downloads PDF in exact format matching the original template"
            )
        
        with col_dl2:
            # Generate alternative PDF format
            alt_pdf_bytes = create_pdf_profile(pdf_data)
            st.download_button(
                label="📥 Download as PDF (Table Format)",
                data=alt_pdf_bytes,
                file_name=f"CIT_Application_Table_{name_part}.pdf",
                mime="application/pdf",
                use_container_width=True,
                help="Downloads PDF with table formatting"
            )
        
        with col_dl3:
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
        
        # Clear form button
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
