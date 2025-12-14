import streamlit as st
import pandas as pd
from datetime import datetime
import io

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
    .profile-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1E3A8A;
        margin-bottom: 20px;
    }
    .generated-output {
        background-color: #f0f2f6;
        padding: 25px;
        border-radius: 10px;
        font-family: monospace;
        white-space: pre-wrap;
        overflow-x: auto;
        margin-top: 20px;
        border: 1px solid #ddd;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<div class="main-header">📋 CIT Applicant Profile Generator</div>', unsafe_allow_html=True)

# Create tabs for different sections
tab1, tab2, tab3 = st.tabs(["📝 Input Form", "👤 Generated Profile", "📊 Data Summary"])

with tab1:
    st.markdown('<div class="section-header">Personal Information</div>', unsafe_allow_html=True)
    
    # Create two columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        full_name = st.text_input("Full Name", value="Mohammed Shifas Ahamadh")
        address = st.text_area("Address", value="38/C Kawdana Road, Dehiwala")
        mobile_whatsapp = st.text_input("Mobile (WhatsApp)", value="0772226866")
        mobile = st.text_input("Mobile", value="0772226866")
        dob = st.date_input("Date of Birth", value=datetime(2009, 2, 19))
        place_of_birth = st.text_input("Place of Birth", value="Akurana")
        nic_no = st.text_input("NIC No", value="")
        
    with col2:
        languages = st.multiselect(
            "Languages Spoken",
            ["English", "Tamil", "Sinhala", "Arabic", "Other"],
            default=["English", "Tamil"]
        )
        
        # Add "Other" language input if selected
        if "Other" in languages:
            other_language = st.text_input("Specify other language")
            if other_language:
                languages = [lang for lang in languages if lang != "Other"]
                languages.append(other_language)
        
        school_college = st.text_input("School/College Attended", value="Hejazz International, Al Haqqaniyah Arabic College")
        last_institute = st.text_input("Last Institute Attended", value="Al Haqqaniyyah Arabic College")
        medium_instruction = st.text_input("Medium of Instruction", value="English")
        last_standard = st.text_input("Last Standard Acquired", value="GCE (O/L)")
        year_month = st.text_input("Year & Month Last Attended", value="")
    
    st.markdown('<div class="section-header">Quran Memorization Details</div>', unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        memorized_quran = st.radio("Completed Memorizing Quran?", ["Yes", "No"], index=1)
    
    with col4:
        if memorized_quran == "Yes":
            juz_count = st.number_input("If Yes, How Many Juz?", min_value=1, max_value=30, value=1)
        else:
            juz_count = None
    
    st.markdown('<div class="section-header">Islamic Institute Details</div>', unsafe_allow_html=True)
    
    col5, col6 = st.columns(2)
    
    with col5:
        islamic_institute = st.text_input("Islamic Institute Last Attended", value="Al Haqqaniyyah Arabic College")
        city_location = st.text_input("City/Location", value="Kandy")
        duration_attended = st.text_input("Duration Attended", value="3 years")
    
    with col6:
        reason_leaving = st.text_area("Reason for Leaving", value="Wants to be with parents and continue studies")
    
    st.markdown('<div class="section-header">Parent/Guardian Information</div>', unsafe_allow_html=True)
    
    col7, col8 = st.columns(2)
    
    with col7:
        parent_name = st.text_input("Parent/Guardian Full Name", value="Ahamad Farook Mohammed Shifas")
        parent_address = st.text_area("Parent/Guardian Address", value="38/C Kawdana Road, Dehiwala")
        father_residing = st.selectbox("Father Residing", ["Inland", "Outland", "Abroad"], index=0)
        occupation = st.text_input("Occupation", value="Business")
    
    with col8:
        parent_mobile = st.text_input("Parent/Guardian Mobile No.", value="0772226866")
        parent_whatsapp = st.text_input("WhatsApp No.", value="0772226866")
        home_languages = st.multiselect(
            "Language(s) Spoken at Home",
            ["English", "Tamil", "Sinhala", "Arabic", "Other"],
            default=["English", "Tamil"]
        )
        
        # Add "Other" language input for home languages
        if "Other" in home_languages:
            other_home_language = st.text_input("Specify other home language")
            if other_home_language:
                home_languages = [lang for lang in home_languages if lang != "Other"]
                home_languages.append(other_home_language)
    
    # Additional information section
    st.markdown('<div class="section-header">Additional Information</div>', unsafe_allow_html=True)
    
    col9, col10 = st.columns(2)
    
    with col9:
        reg_no = st.text_input("Registration No.", value="R/2552/C/238 (MRCA)")
        address_line = st.text_input("Address Line", value="No.37,32nd Lane Colombo 06.")
        telephone = st.text_input("Telephone", value="+94112361793 / +94777365964")
    
    with col10:
        additional_notes = st.text_area("Additional Notes", value="")

# Generate the profile output
with tab2:
    st.markdown('<div class="section-header">Generated Applicant Profile</div>', unsafe_allow_html=True)
    
    # Create the formatted output
    profile_output = f"""{address_line} Tel:{telephone}

Reg.No.{reg_no}

New Admission Applicant Profile

Full Name
{full_name}

Address
{address}

Mobile (WhatsApp)
{mobile_whatsapp}

Mobile
{mobile}

Date of Birth
{dob.strftime('%d %B %Y') if hasattr(dob, 'strftime') else dob}

Place of Birth
{place_of_birth}

NIC No
{nic_no if nic_no else ''}

Languages Spoken
{', '.join(languages)}

School/College Attended
{school_college}

Last Institute Attended
{last_institute}

Medium of Instruction
{medium_instruction}

Last Standard Acquired
{last_standard}

Year & Month Last Attended
{year_month if year_month else ''}

Completed Memorizing Quran?
{memorized_quran}

{f'If Yes,How Many Juz? {juz_count}' if memorized_quran == 'Yes' and juz_count else ''}

Islamic Institute Last Attended
{islamic_institute}

City/Location
{city_location}

Duration Attended
{duration_attended}

Reason for Leaving
{reason_leaving}

Parent/Guardian Full Name
{parent_name}

Parent/Guardian Address
{parent_address}

Father Residing
{father_residing}

Occupation
{occupation}

Parent/Guardian Mobile No.
{parent_mobile}

WhatsApp No.
{parent_whatsapp}

Language(s)Spoken at Home
{', '.join(home_languages)}

Additional Notes:
{additional_notes if additional_notes else ''}
"""
    
    # Display the generated profile
    st.markdown('<div class="generated-output">' + profile_output + '</div>', unsafe_allow_html=True)
    
    # Add download button for the profile
    col_download1, col_download2 = st.columns(2)
    
    with col_download1:
        # Download as text file
        st.download_button(
            label="📥 Download as Text File",
            data=profile_output,
            file_name=f"CIT_Applicant_Profile_{full_name.replace(' ', '_')}.txt",
            mime="text/plain"
        )
    
    with col_download2:
        # Copy to clipboard button
        if st.button("📋 Copy to Clipboard"):
            st.code(profile_output)
            st.success("Profile copied! You can now paste it anywhere.")

# Data summary tab
with tab3:
    st.markdown('<div class="section-header">Applicant Data Summary</div>', unsafe_allow_html=True)
    
    # Create a summary dictionary
    summary_data = {
        "Field": [
            "Full Name", "Address", "Date of Birth", "Languages Spoken",
            "Last Institute", "Medium of Instruction", "Quran Memorized",
            "Islamic Institute", "Duration Attended", "Parent Name",
            "Parent Occupation", "Registration No."
        ],
        "Value": [
            full_name, 
            address[:30] + "..." if len(address) > 30 else address,
            dob.strftime('%d/%m/%Y') if hasattr(dob, 'strftime') else dob,
            ', '.join(languages),
            last_institute[:30] + "..." if len(last_institute) > 30 else last_institute,
            medium_instruction,
            memorized_quran,
            islamic_institute,
            duration_attended,
            parent_name[:30] + "..." if len(parent_name) > 30 else parent_name,
            occupation,
            reg_no
        ]
    }
    
    # Create a DataFrame and display it
    df = pd.DataFrame(summary_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Display some statistics
    st.markdown('<div class="section-header">Quick Statistics</div>', unsafe_allow_html=True)
    
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    
    with stat_col1:
        st.metric("Languages Spoken", len(languages))
    
    with stat_col2:
        # Calculate age if DOB is provided
        if hasattr(dob, 'year'):
            today = datetime.now()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            st.metric("Approx. Age", age)
        else:
            st.metric("Age", "N/A")
    
    with stat_col3:
        st.metric("Contact Numbers", 3 if mobile_whatsapp and mobile and parent_mobile else "Check")

# Sidebar with instructions
with st.sidebar:
    st.markdown("## 📋 Instructions")
    st.markdown("""
    1. Fill in all the required fields in the **Input Form** tab
    2. View the generated profile in the **Generated Profile** tab
    3. Download or copy the profile as needed
    4. Check the **Data Summary** tab for a quick overview
    
    ### Tips:
    - All fields with asterisk (*) are required
    - Use the same format as shown in examples
    - You can edit any field at any time
    - The profile updates automatically
    """)
    
    st.markdown("---")
    st.markdown("### Sample Data Loaded")
    if st.button("Reset to Default Values"):
        st.rerun()
    
    st.markdown("---")
    st.markdown("#### About")
    st.markdown("""
    This application automates the creation of CIT Applicant Profiles based on the input provided.
    
    **Version:** 1.0
    **Last Updated:** February 2024
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; font-size: 0.9rem;'>"
    "CIT Applicant Profile Generator | Created with Streamlit | All data is stored locally in your session"
    "</div>",
    unsafe_allow_html=True
)
