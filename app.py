import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime, date
import os
import uuid
from PIL import Image
import time
from dotenv import load_dotenv

# ==============================================
# LOAD ENVIRONMENT VARIABLES
# ==============================================

load_dotenv()

# ==============================================
# SUPABASE CONNECTION - REST API METHOD
# ==============================================

# Get Supabase credentials from environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Supabase REST API Headers
SUPABASE_HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# Test connection
def test_connection():
    try:
        response = requests.get(f"{SUPABASE_URL}/rest/v1/students?limit=1", headers=SUPABASE_HEADERS)
        return response.status_code == 200
    except:
        return False

DB_CONNECTED = test_connection()

# ==============================================
# LANGUAGE SUPPORT
# ==============================================

TRANSLATIONS = {
    'en': {
        'app_title': '🏫 School Management System',
        'school_name': 'Gangodagama Jayawardhana M.V.',
        'dashboard': '📊 Dashboard',
        'students': '👨‍🎓 Students',
        'teachers': '👨‍🏫 Teachers',
        'development_officers': '👨‍💼 Development Officers',
        'non_academic_officers': '👨‍💼 Non-Academic Officers',
        'search': '🔍 Search',
        'reports': '📄 Reports',
        'total_students': 'Total Students',
        'total_teachers': 'Total Teachers',
        'total_dev': 'Total Development Officers',
        'total_nonacademic': 'Total Non-Academic Officers',
        'grade_distribution': 'Grade Distribution',
        'student_management': 'Student Management',
        'teacher_management': 'Teacher Management',
        'dev_management': 'Development Officer Management',
        'nonacademic_management': 'Non-Academic Officer Management',
        'add_new': 'Add New',
        'view_all': 'View All',
        'edit': '✏️ Edit',
        'delete': '🗑️ Delete',
        'view_details': '📄 View Details',
        'print': '🖨️ Print / Save as PDF',
        'download_html': '📥 Download as HTML',
        'back_to_list': '⬅ Back to List',
        'edit_this': '✏️ Edit This',
        'save': 'Save',
        'save_print': 'Save & Print',
        'update': 'Update',
        'update_print': 'Update & Print',
        'cancel': 'Cancel',
        'full_name': 'Full Name',
        'birthday': 'Birthday',
        'grade': 'Grade',
        'guardian_name': 'Guardian Name',
        'guardian_phone': 'Guardian Phone',
        'guardian_email': 'Guardian Email',
        'school_index': 'School Index Number',
        'address': 'Address',
        'siblings_at_school': 'Siblings at School',
        'mother_occupation': "Mother's Occupation",
        'father_occupation': "Father's Occupation",
        'achievements': 'Achievements',
        'special_needs': 'Special Needs',
        'subject': 'Subject',
        'email': 'Email',
        'phone': 'Phone',
        'qualification': 'Qualification',
        'experience': 'Experience',
        'position': 'Position',
        'date_initial': 'Date of Initial Appointment',
        'date_arrival': 'Date of Arrival at School',
        'nature_appointment': 'Nature of Appointment',
        'vocational_qualifications': 'Vocational/Educational Qualifications',
        'retirement_date': 'Scheduled Date of Retirement',
        'schools_served': 'Schools Served At',
        'designation': 'Designation',
        'department': 'Department',
        'duty_list': 'Duty List',
        'created_at': 'Created At',
        'photo': 'Photo',
        'no_photo': 'No Photo Available',
        'search_by_school_index': 'Search by School Index Number',
        'search_by_grade': 'Filter by Grade',
        'search_by_nic': 'Search by NIC',
        'all_grades': 'All Grades',
        'no_data': 'No data found',
        'success_added': '✅ Added successfully!',
        'success_updated': '✅ Updated successfully!',
        'success_deleted': '✅ Deleted successfully!',
        'error_occurred': '❌ Error occurred: ',
        'confirm_delete': 'Are you sure you want to delete this record?',
        'fill_required': 'Please fill in all required fields (*)',
        'select_record': 'Select Record ID',
        'actions': 'Actions',
        'student_details': 'Student Details Report',
        'teacher_details': 'Teacher Details Report',
        'dev_details': 'Development Officer Details Report',
        'nonacademic_details': 'Non-Academic Officer Details Report',
        'personal_info': '📋 Personal Information',
        'all_rights': 'All Rights Reserved',
        'generated_on': 'Generated on',
        'report_type': 'Report Type'
    },
    'si': {
        'app_title': '🏫 පාසල් කළමනාකරණ පද්ධතිය',
        'school_name': 'ගංගොඩගම ජයවර්ධන ම.වි.',
        'dashboard': '📊 උපකරණ පුවරුව',
        'students': '👨‍🎓 සිසුන්',
        'teachers': '👨‍🏫 ගුරුවරු',
        'development_officers': '👨‍💼 සංවර්ධන නිලධාරීන්',
        'non_academic_officers': '👨‍💼 අධ්‍යාපන නොවන නිලධාරීන්',
        'search': '🔍 සෙවීම',
        'reports': '📄 වාර්තා',
        'total_students': 'මුළු සිසුන්',
        'total_teachers': 'මුළු ගුරුවරු',
        'total_dev': 'මුළු සංවර්ධන නිලධාරීන්',
        'total_nonacademic': 'මුළු අධ්‍යාපන නොවන නිලධාරීන්',
        'grade_distribution': 'ශ්‍රේණි බෙදාහැරීම',
        'student_management': 'සිසුන් කළමනාකරණය',
        'teacher_management': 'ගුරුවරුන් කළමනාකරණය',
        'dev_management': 'සංවර්ධන නිලධාරීන් කළමනාකරණය',
        'nonacademic_management': 'අධ්‍යාපන නොවන නිලධාරීන් කළමනාකරණය',
        'add_new': 'අලුතින් එක් කරන්න',
        'view_all': 'සියල්ල බලන්න',
        'edit': '✏️ සංස්කරණය කරන්න',
        'delete': '🗑️ මකන්න',
        'view_details': '📄 විස්තර බලන්න',
        'print': '🖨️ මුද්‍රණය කරන්න / PDF ලෙස සුරකින්න',
        'download_html': '📥 HTML ලෙස බාගන්න',
        'back_to_list': '⬅ ලැයිස්තුවට ආපසු',
        'edit_this': '✏️ මෙය සංස්කරණය කරන්න',
        'save': 'සුරකින්න',
        'save_print': 'සුරකින්න සහ මුද්‍රණය කරන්න',
        'update': 'යාවත්කාලීන කරන්න',
        'update_print': 'යාවත්කාලීන කරන්න සහ මුද්‍රණය කරන්න',
        'cancel': 'අවලංගු කරන්න',
        'full_name': 'සම්පූර්ණ නම',
        'birthday': 'උපන්දිනය',
        'grade': 'ශ්‍රේණිය',
        'guardian_name': 'භාරකරුගේ නම',
        'guardian_phone': 'භාරකරුගේ දුරකථනය',
        'guardian_email': 'භාරකරුගේ ඊමේල්',
        'school_index': 'පාසල් දර්ශක අංකය',
        'address': 'ලිපිනය',
        'siblings_at_school': 'පාසලේ සහෝදර සහෝදරියන්',
        'mother_occupation': 'මවගේ රැකියාව',
        'father_occupation': 'පියාගේ රැකියාව',
        'achievements': 'ජයග්‍රහණ',
        'special_needs': 'විශේෂ අවශ්‍යතා',
        'subject': 'විෂය',
        'email': 'ඊමේල්',
        'phone': 'දුරකථනය',
        'qualification': 'සුදුසුකම්',
        'experience': 'අත්දැකීම්',
        'position': 'තනතුර',
        'date_initial': 'මූලික පත්වීම් දිනය',
        'date_arrival': 'පාසලට පැමිණි දිනය',
        'nature_appointment': 'පත්වීමේ ස්වභාවය',
        'vocational_qualifications': 'වෘත්තීය/අධ්‍යාපනික සුදුසුකම්',
        'retirement_date': 'විශ්‍රාම යාමට නියමිත දිනය',
        'schools_served': 'සේවය කළ පාසල්',
        'designation': 'නිල නාමය',
        'department': 'දෙපාර්තමේන්තුව',
        'duty_list': 'රාජකාරි ලැයිස්තුව',
        'created_at': 'සාදන ලද දිනය',
        'photo': 'ඡායාරූපය',
        'no_photo': 'ඡායාරූපයක් නොමැත',
        'search_by_school_index': 'පාසල් දර්ශක අංකයෙන් සොයන්න',
        'search_by_grade': 'ශ්‍රේණිය අනුව පෙරන්න',
        'search_by_nic': 'ජාතික හැඳුනුම්පත් අංකයෙන් සොයන්න',
        'all_grades': 'සියලුම ශ්‍රේණි',
        'no_data': 'දත්ත හමු නොවීය',
        'success_added': '✅ සාර්ථකව එකතු කරන ලදී!',
        'success_updated': '✅ සාර්ථකව යාවත්කාලීන කරන ලදී!',
        'success_deleted': '✅ සාර්ථකව මකා දමන ලදී!',
        'error_occurred': '❌ දෝෂයක් සිදු විය: ',
        'confirm_delete': 'ඔබට මෙම වාර්තාව මකා දැමීමට අවශ්‍ය බව ඔබට විශ්වාසද?',
        'fill_required': 'කරුණාකර අවශ්‍ය සියලු ක්ෂේත්‍ර පුරවන්න (*)',
        'select_record': 'වාර්තා අංකය තෝරන්න',
        'actions': 'ක්‍රියාවන්',
        'student_details': 'සිසුන්ගේ විස්තර වාර්තාව',
        'teacher_details': 'ගුරුවරුන්ගේ විස්තර වාර්තාව',
        'dev_details': 'සංවර්ධන නිලධාරීන්ගේ විස්තර වාර්තාව',
        'nonacademic_details': 'අධ්‍යාපන නොවන නිලධාරීන්ගේ විස්තර වාර්තාව',
        'personal_info': '📋 පුද්ගලික තොරතුරු',
        'all_rights': 'සියලුම අයිතිවාසිකම් ඇවිරිණි',
        'generated_on': 'සාදන ලද දිනය',
        'report_type': 'වාර්තා වර්ගය'
    }
}

def get_text(key, lang='en'):
    """Get translated text"""
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)

# ==============================================
# DATABASE FUNCTIONS - REST API
# ==============================================

def get_all_students():
    """Get all students from Supabase"""
    if not DB_CONNECTED:
        return pd.DataFrame()
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/students?order=id.desc",
            headers=SUPABASE_HEADERS
        )
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        else:
            st.error(f"Error fetching students: {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching students: {str(e)}")
        return pd.DataFrame()

def get_student_by_id(id):
    """Get a student by ID"""
    if not DB_CONNECTED:
        return pd.DataFrame()
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/students?id=eq.{id}",
            headers=SUPABASE_HEADERS
        )
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching student: {str(e)}")
        return pd.DataFrame()

def add_student(data):
    """Add a new student to Supabase"""
    if not DB_CONNECTED:
        return None
    try:
        if 'id' in data:
            del data['id']
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/students",
            headers=SUPABASE_HEADERS,
            json=data
        )
        if response.status_code == 201:
            result = response.json()
            return result[0]['id'] if result else None
        else:
            st.error(f"Error adding student: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error adding student: {str(e)}")
        return None

def update_student(id, data):
    """Update a student in Supabase"""
    if not DB_CONNECTED:
        return False
    try:
        if 'id' in data:
            del data['id']
        response = requests.patch(
            f"{SUPABASE_URL}/rest/v1/students?id=eq.{id}",
            headers=SUPABASE_HEADERS,
            json=data
        )
        return response.status_code == 200
    except Exception as e:
        st.error(f"Error updating student: {str(e)}")
        return False

def delete_student(id):
    """Delete a student from Supabase"""
    if not DB_CONNECTED:
        return False
    try:
        response = requests.delete(
            f"{SUPABASE_URL}/rest/v1/students?id=eq.{id}",
            headers=SUPABASE_HEADERS
        )
        return response.status_code == 204
    except Exception as e:
        st.error(f"Error deleting student: {str(e)}")
        return False

def search_student_by_school_index(school_index):
    """Search student by school index number"""
    if not DB_CONNECTED:
        return pd.DataFrame()
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/students?school_index_number=eq.{school_index}",
            headers=SUPABASE_HEADERS
        )
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error searching student: {str(e)}")
        return pd.DataFrame()

def search_students_by_grade(grade):
    """Search students by grade"""
    if not DB_CONNECTED:
        return pd.DataFrame()
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/students?grade=eq.{grade}",
            headers=SUPABASE_HEADERS
        )
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error searching students: {str(e)}")
        return pd.DataFrame()

def get_all_teachers():
    """Get all teachers from Supabase"""
    if not DB_CONNECTED:
        return pd.DataFrame()
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/teachers?order=id.desc",
            headers=SUPABASE_HEADERS
        )
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching teachers: {str(e)}")
        return pd.DataFrame()

def get_teacher_by_id(id):
    """Get a teacher by ID"""
    if not DB_CONNECTED:
        return pd.DataFrame()
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/teachers?id=eq.{id}",
            headers=SUPABASE_HEADERS
        )
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching teacher: {str(e)}")
        return pd.DataFrame()

def add_teacher(data):
    """Add a new teacher to Supabase"""
    if not DB_CONNECTED:
        return None
    try:
        if 'id' in data:
            del data['id']
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/teachers",
            headers=SUPABASE_HEADERS,
            json=data
        )
        if response.status_code == 201:
            result = response.json()
            return result[0]['id'] if result else None
        return None
    except Exception as e:
        st.error(f"Error adding teacher: {str(e)}")
        return None

def update_teacher(id, data):
    """Update a teacher in Supabase"""
    if not DB_CONNECTED:
        return False
    try:
        if 'id' in data:
            del data['id']
        response = requests.patch(
            f"{SUPABASE_URL}/rest/v1/teachers?id=eq.{id}",
            headers=SUPABASE_HEADERS,
            json=data
        )
        return response.status_code == 200
    except Exception as e:
        st.error(f"Error updating teacher: {str(e)}")
        return False

def delete_teacher(id):
    """Delete a teacher from Supabase"""
    if not DB_CONNECTED:
        return False
    try:
        response = requests.delete(
            f"{SUPABASE_URL}/rest/v1/teachers?id=eq.{id}",
            headers=SUPABASE_HEADERS
        )
        return response.status_code == 204
    except Exception as e:
        st.error(f"Error deleting teacher: {str(e)}")
        return False

def search_teacher_by_nic(nic):
    """Search teacher by NIC"""
    if not DB_CONNECTED:
        return pd.DataFrame()
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/teachers?nic_number=eq.{nic}",
            headers=SUPABASE_HEADERS
        )
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error searching teacher: {str(e)}")
        return pd.DataFrame()

def get_all_development_officers():
    """Get all development officers from Supabase"""
    if not DB_CONNECTED:
        return pd.DataFrame()
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/development_officers?order=id.desc",
            headers=SUPABASE_HEADERS
        )
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching development officers: {str(e)}")
        return pd.DataFrame()

def get_development_officer_by_id(id):
    """Get a development officer by ID"""
    if not DB_CONNECTED:
        return pd.DataFrame()
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/development_officers?id=eq.{id}",
            headers=SUPABASE_HEADERS
        )
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching development officer: {str(e)}")
        return pd.DataFrame()

def add_development_officer(data):
    """Add a new development officer to Supabase"""
    if not DB_CONNECTED:
        return None
    try:
        if 'id' in data:
            del data['id']
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/development_officers",
            headers=SUPABASE_HEADERS,
            json=data
        )
        if response.status_code == 201:
            result = response.json()
            return result[0]['id'] if result else None
        return None
    except Exception as e:
        st.error(f"Error adding development officer: {str(e)}")
        return None

def update_development_officer(id, data):
    """Update a development officer in Supabase"""
    if not DB_CONNECTED:
        return False
    try:
        if 'id' in data:
            del data['id']
        response = requests.patch(
            f"{SUPABASE_URL}/rest/v1/development_officers?id=eq.{id}",
            headers=SUPABASE_HEADERS,
            json=data
        )
        return response.status_code == 200
    except Exception as e:
        st.error(f"Error updating development officer: {str(e)}")
        return False

def delete_development_officer(id):
    """Delete a development officer from Supabase"""
    if not DB_CONNECTED:
        return False
    try:
        response = requests.delete(
            f"{SUPABASE_URL}/rest/v1/development_officers?id=eq.{id}",
            headers=SUPABASE_HEADERS
        )
        return response.status_code == 204
    except Exception as e:
        st.error(f"Error deleting development officer: {str(e)}")
        return False

def search_development_officer_by_nic(nic):
    """Search development officer by NIC"""
    if not DB_CONNECTED:
        return pd.DataFrame()
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/development_officers?nic_number=eq.{nic}",
            headers=SUPABASE_HEADERS
        )
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error searching development officer: {str(e)}")
        return pd.DataFrame()

def get_all_non_academic_officers():
    """Get all non-academic officers from Supabase"""
    if not DB_CONNECTED:
        return pd.DataFrame()
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/non_academic_officers?order=id.desc",
            headers=SUPABASE_HEADERS
        )
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching non-academic officers: {str(e)}")
        return pd.DataFrame()

def get_non_academic_officer_by_id(id):
    """Get a non-academic officer by ID"""
    if not DB_CONNECTED:
        return pd.DataFrame()
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/non_academic_officers?id=eq.{id}",
            headers=SUPABASE_HEADERS
        )
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching non-academic officer: {str(e)}")
        return pd.DataFrame()

def add_non_academic_officer(data):
    """Add a new non-academic officer to Supabase"""
    if not DB_CONNECTED:
        return None
    try:
        if 'id' in data:
            del data['id']
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/non_academic_officers",
            headers=SUPABASE_HEADERS,
            json=data
        )
        if response.status_code == 201:
            result = response.json()
            return result[0]['id'] if result else None
        return None
    except Exception as e:
        st.error(f"Error adding non-academic officer: {str(e)}")
        return None

def update_non_academic_officer(id, data):
    """Update a non-academic officer in Supabase"""
    if not DB_CONNECTED:
        return False
    try:
        if 'id' in data:
            del data['id']
        response = requests.patch(
            f"{SUPABASE_URL}/rest/v1/non_academic_officers?id=eq.{id}",
            headers=SUPABASE_HEADERS,
            json=data
        )
        return response.status_code == 200
    except Exception as e:
        st.error(f"Error updating non-academic officer: {str(e)}")
        return False

def delete_non_academic_officer(id):
    """Delete a non-academic officer from Supabase"""
    if not DB_CONNECTED:
        return False
    try:
        response = requests.delete(
            f"{SUPABASE_URL}/rest/v1/non_academic_officers?id=eq.{id}",
            headers=SUPABASE_HEADERS
        )
        return response.status_code == 204
    except Exception as e:
        st.error(f"Error deleting non-academic officer: {str(e)}")
        return False

def search_non_academic_officer_by_nic(nic):
    """Search non-academic officer by NIC"""
    if not DB_CONNECTED:
        return pd.DataFrame()
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/non_academic_officers?nic_number=eq.{nic}",
            headers=SUPABASE_HEADERS
        )
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error searching non-academic officer: {str(e)}")
        return pd.DataFrame()

# ==============================================
# STATS FUNCTIONS
# ==============================================

def get_stats():
    """Get statistics from Supabase"""
    if not DB_CONNECTED:
        return {
            'total_students': 0,
            'total_teachers': 0,
            'total_development_officers': 0,
            'total_non_academic_officers': 0,
            'grade_distribution': []
        }
    try:
        stats = {}
        
        # Get counts
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/students?select=id",
            headers=SUPABASE_HEADERS
        )
        stats['total_students'] = len(response.json()) if response.status_code == 200 else 0
        
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/teachers?select=id",
            headers=SUPABASE_HEADERS
        )
        stats['total_teachers'] = len(response.json()) if response.status_code == 200 else 0
        
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/development_officers?select=id",
            headers=SUPABASE_HEADERS
        )
        stats['total_development_officers'] = len(response.json()) if response.status_code == 200 else 0
        
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/non_academic_officers?select=id",
            headers=SUPABASE_HEADERS
        )
        stats['total_non_academic_officers'] = len(response.json()) if response.status_code == 200 else 0
        
        # Get grade distribution
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/students?select=grade",
            headers=SUPABASE_HEADERS
        )
        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            if not df.empty:
                grade_dist = df['grade'].value_counts().reset_index()
                grade_dist.columns = ['grade', 'count']
                stats['grade_distribution'] = grade_dist.sort_values('grade').to_dict('records')
            else:
                stats['grade_distribution'] = []
        else:
            stats['grade_distribution'] = []
        
        return stats
    except Exception as e:
        st.error(f"Error getting stats: {str(e)}")
        return {
            'total_students': 0,
            'total_teachers': 0,
            'total_development_officers': 0,
            'total_non_academic_officers': 0,
            'grade_distribution': []
        }

# ==============================================
# PHOTO FUNCTIONS
# ==============================================

def save_photo(uploaded_file):
    """Save uploaded photo and return URL"""
    if uploaded_file is not None:
        try:
            os.makedirs('uploads', exist_ok=True)
            
            file_extension = uploaded_file.name.split('.')[-1]
            unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
            file_path = os.path.join('uploads', unique_filename)
            
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            
            return f'uploads/{unique_filename}'
        except Exception as e:
            st.error(f"Error saving photo: {str(e)}")
            return None
    return None

def display_photo_in_streamlit(image_path, size=150, lang='en'):
    """Display photo in Streamlit with proper styling - UI ONLY"""
    if image_path and os.path.exists(image_path):
        try:
            img = Image.open(image_path)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(img, width=size, caption=get_text('photo', lang))
        except Exception as e:
            st.warning(f"{get_text('error_occurred', lang)} {str(e)}")
    else:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
            <div style="text-align:center; padding:20px;">
                <div style="width:{size}px;height:{size}px;border-radius:50%;background:linear-gradient(135deg, #4F46E5, #7C3AED);color:white;display:flex;align-items:center;justify-content:center;font-size:40px;font-weight:bold;margin:0 auto;border:3px solid #4F46E5;">
                    👤
                </div>
                <p style="margin-top:10px;color:#6b7280;">{get_text('no_photo', lang)}</p>
            </div>
            """, unsafe_allow_html=True)

# ==============================================
# PRINT/VIEW FUNCTIONS
# ==============================================

def create_html_report(data, report_type, person_name, lang='en'):
    """Create HTML report for printing - NO PHOTO"""
    
    school_name = get_text('school_name', lang)
    
    details_html = ""
    for label, value in data.items():
        if value is None or value == '':
            value = 'N/A'
        details_html += f"""
        <div class="detail-item">
            <span class="label">{label}</span>
            <span class="value">{value}</span>
        </div>
        """
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{person_name} - {report_type}</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: 'Segoe UI', Arial, sans-serif;
                background: #f0f2f5;
                padding: 20px;
            }}
            .print-container {{
                max-width: 210mm;
                margin: 0 auto;
                background: white;
                border-radius: 12px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            .print-header {{
                background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
                padding: 30px 40px;
                color: white;
                text-align: center;
            }}
            .print-header h1 {{
                font-size: 28px;
                font-weight: 700;
                margin-bottom: 5px;
            }}
            .print-header .school-name {{
                font-size: 16px;
                opacity: 0.9;
            }}
            .print-header .report-type {{
                font-size: 14px;
                opacity: 0.8;
                margin-top: 5px;
                background: rgba(255,255,255,0.2);
                display: inline-block;
                padding: 4px 20px;
                border-radius: 20px;
            }}
            .print-body {{
                padding: 30px 40px;
            }}
            .print-section-title {{
                font-size: 18px;
                font-weight: 600;
                color: #1a237e;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 2px solid #e8eaf6;
            }}
            .details-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 15px;
                margin-bottom: 30px;
            }}
            .detail-item {{
                background: #f8f9fa;
                border-radius: 10px;
                padding: 15px 20px;
                border-left: 4px solid #4F46E5;
                page-break-inside: avoid;
            }}
            .detail-item .label {{
                font-size: 11px;
                font-weight: 600;
                color: #78909c;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                display: block;
                margin-bottom: 4px;
            }}
            .detail-item .value {{
                font-size: 15px;
                color: #1a237e;
                font-weight: 500;
            }}
            .print-footer {{
                background: #f8f9fa;
                padding: 20px 40px;
                text-align: center;
                border-top: 2px solid #e8eaf6;
                font-size: 12px;
                color: #78909c;
            }}
            .print-footer .school-name {{
                font-weight: 600;
                color: #4F46E5;
            }}
            .print-actions {{
                padding: 20px 40px;
                background: white;
                border-top: 1px solid #e8eaf6;
                text-align: center;
            }}
            .btn-print {{
                background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
                color: white;
                border: none;
                padding: 14px 50px;
                border-radius: 10px;
                font-size: 18px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 20px rgba(79, 70, 229, 0.3);
            }}
            .btn-print:hover {{
                transform: translateY(-3px);
                box-shadow: 0 8px 30px rgba(79, 70, 229, 0.4);
            }}
            .btn-back {{
                background: #6c757d;
                color: white;
                border: none;
                padding: 14px 30px;
                border-radius: 10px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                margin-right: 15px;
            }}
            .btn-back:hover {{
                background: #5a6268;
                transform: translateY(-2px);
            }}
            @media print {{
                body {{ background: white !important; padding: 0 !important; }}
                .print-container {{ box-shadow: none !important; border-radius: 0 !important; max-width: 100% !important; }}
                .print-actions {{ display: none !important; }}
                .print-header {{ -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }}
                .detail-item {{ -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }}
                .print-footer {{ -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }}
            }}
            @media (max-width: 600px) {{
                .print-header {{ padding: 20px; }}
                .print-header h1 {{ font-size: 20px; }}
                .print-body {{ padding: 20px; }}
                .details-grid {{ grid-template-columns: 1fr; }}
                .print-actions {{ padding: 15px 20px; }}
                .btn-print {{ padding: 12px 30px; font-size: 16px; width: 100%; }}
                .btn-back {{ width: 100%; margin-right: 0; margin-bottom: 10px; }}
            }}
        </style>
    </head>
    <body>
        <div class="print-container">
            <div class="print-header">
                <h1>{person_name}</h1>
                <div class="school-name">{school_name}</div>
                <div class="report-type">{report_type}</div>
            </div>
            <div class="print-body">
                <div class="print-section-title">{get_text('personal_info', lang)}</div>
                <div class="details-grid">
                    {details_html}
                </div>
            </div>
            <div class="print-footer">
                <span class="school-name">© {school_name}</span>
                <span> - {get_text('generated_on', lang)} {datetime.now().strftime('%Y-%m-%d %H:%M')} | {get_text('all_rights', lang)}</span>
            </div>
            <div class="print-actions">
                <button class="btn-back" onclick="history.back()">⬅ {get_text('back_to_list', lang)}</button>
                <button class="btn-print" onclick="window.print()">🖨️ {get_text('print', lang)}</button>
            </div>
        </div>
    </body>
    </html>
    """
    return html

def display_print_view(data, report_type, person_name, lang='en'):
    """Display print view using HTML - NO PHOTO"""
    
    html_content = create_html_report(data, report_type, person_name, lang)
    
    st.components.v1.html(html_content, height=800, scrolling=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button(
            label=f"📥 {get_text('download_html', lang)}",
            data=html_content,
            file_name=f"{report_type.replace(' ', '_')}_{person_name.replace(' ', '_')}.html",
            mime="text/html"
        )
    with col2:
        if st.button(f"⬅ {get_text('back_to_list', lang)}"):
            st.session_state.show_print = False
            st.session_state.print_data = None
            st.session_state.print_type = None
            st.rerun()
    with col3:
        if st.button(f"✏️ {get_text('edit_this', lang)}"):
            st.session_state.edit_id = st.session_state.print_data.get('id')
            st.session_state.edit_type = st.session_state.print_type
            st.session_state.show_print = False
            st.rerun()

# ==============================================
# STUDENT DETAILS FUNCTIONS
# ==============================================

def get_student_details_dict(student, lang='en'):
    """Get student details as dictionary for display (without NIC)"""
    return {
        get_text('full_name', lang): student.get('name', 'N/A'),
        get_text('birthday', lang): student.get('birthday', 'N/A'),
        get_text('grade', lang): student.get('grade', 'N/A'),
        get_text('guardian_name', lang): student.get('guardian_name', 'N/A'),
        get_text('guardian_phone', lang): student.get('guardian_phone', 'N/A'),
        get_text('guardian_email', lang): student.get('guardian_email', 'N/A'),
        get_text('school_index', lang): student.get('school_index_number', 'N/A'),
        get_text('address', lang): student.get('address', 'N/A'),
        get_text('siblings_at_school', lang): student.get('siblings_at_school', 'N/A'),
        get_text('mother_occupation', lang): student.get('mother_occupation', 'N/A'),
        get_text('father_occupation', lang): student.get('father_occupation', 'N/A'),
        get_text('achievements', lang): student.get('achievements', 'N/A'),
        get_text('special_needs', lang): student.get('is_special_needs', 'N/A'),
        get_text('created_at', lang): student.get('created_at', 'N/A')
    }

def get_teacher_details_dict(teacher, lang='en'):
    """Get teacher details as dictionary for display"""
    return {
        get_text('full_name', lang): teacher.get('name', 'N/A'),
        get_text('birthday', lang): teacher.get('birthday', 'N/A'),
        get_text('subject', lang): teacher.get('subject', 'N/A'),
        get_text('email', lang): teacher.get('email', 'N/A'),
        get_text('phone', lang): teacher.get('phone', 'N/A'),
        get_text('nic_number', lang): teacher.get('nic_number', 'N/A'),
        get_text('qualification', lang): teacher.get('qualification', 'N/A'),
        get_text('experience', lang): teacher.get('experience', 'N/A'),
        get_text('address', lang): teacher.get('address', 'N/A'),
        get_text('date_initial', lang): teacher.get('date_of_initial_appointment', 'N/A'),
        get_text('date_arrival', lang): teacher.get('date_of_arrival_at_school', 'N/A'),
        get_text('nature_appointment', lang): teacher.get('nature_of_appointment', 'N/A'),
        get_text('vocational_qualifications', lang): teacher.get('vocational_educational_qualifications', 'N/A'),
        get_text('retirement_date', lang): teacher.get('scheduled_date_of_retirement', 'N/A'),
        get_text('schools_served', lang): teacher.get('schools_served_at', 'N/A'),
        get_text('position', lang): teacher.get('position', 'N/A'),
        get_text('created_at', lang): teacher.get('created_at', 'N/A')
    }

def get_development_officer_details_dict(officer, lang='en'):
    """Get development officer details as dictionary for display"""
    return {
        get_text('full_name', lang): officer.get('name', 'N/A'),
        get_text('birthday', lang): officer.get('birthday', 'N/A'),
        get_text('designation', lang): officer.get('designation', 'N/A'),
        get_text('department', lang): officer.get('department', 'N/A'),
        get_text('email', lang): officer.get('email', 'N/A'),
        get_text('phone', lang): officer.get('phone', 'N/A'),
        get_text('nic_number', lang): officer.get('nic_number', 'N/A'),
        get_text('qualification', lang): officer.get('qualification', 'N/A'),
        get_text('experience', lang): officer.get('experience', 'N/A'),
        get_text('address', lang): officer.get('address', 'N/A'),
        get_text('date_initial', lang): officer.get('date_of_initial_appointment', 'N/A'),
        get_text('date_arrival', lang): officer.get('date_of_arrival_at_school', 'N/A'),
        get_text('nature_appointment', lang): officer.get('nature_of_appointment', 'N/A'),
        get_text('vocational_qualifications', lang): officer.get('vocational_educational_qualifications', 'N/A'),
        get_text('retirement_date', lang): officer.get('scheduled_date_of_retirement', 'N/A'),
        get_text('schools_served', lang): officer.get('schools_served_at', 'N/A'),
        get_text('position', lang): officer.get('position', 'N/A'),
        get_text('duty_list', lang): officer.get('duty_list', 'N/A'),
        get_text('created_at', lang): officer.get('created_at', 'N/A')
    }

def get_non_academic_officer_details_dict(officer, lang='en'):
    """Get non-academic officer details as dictionary for display"""
    return {
        get_text('full_name', lang): officer.get('name', 'N/A'),
        get_text('birthday', lang): officer.get('birthday', 'N/A'),
        get_text('designation', lang): officer.get('designation', 'N/A'),
        get_text('department', lang): officer.get('department', 'N/A'),
        get_text('email', lang): officer.get('email', 'N/A'),
        get_text('phone', lang): officer.get('phone', 'N/A'),
        get_text('nic_number', lang): officer.get('nic_number', 'N/A'),
        get_text('qualification', lang): officer.get('qualification', 'N/A'),
        get_text('experience', lang): officer.get('experience', 'N/A'),
        get_text('address', lang): officer.get('address', 'N/A'),
        get_text('date_initial', lang): officer.get('date_of_initial_appointment', 'N/A'),
        get_text('date_arrival', lang): officer.get('date_of_arrival_at_school', 'N/A'),
        get_text('nature_appointment', lang): officer.get('nature_of_appointment', 'N/A'),
        get_text('vocational_qualifications', lang): officer.get('vocational_educational_qualifications', 'N/A'),
        get_text('retirement_date', lang): officer.get('scheduled_date_of_retirement', 'N/A'),
        get_text('schools_served', lang): officer.get('schools_served_at', 'N/A'),
        get_text('position', lang): officer.get('position', 'N/A'),
        get_text('created_at', lang): officer.get('created_at', 'N/A')
    }

# ==============================================
# STUDENT FORM FUNCTIONS
# ==============================================

def show_student_form(edit_data=None, lang='en'):
    """Show student form for add/edit - NO NIC"""
    
    if edit_data is not None:
        st.markdown(f"### ✏️ {get_text('edit', lang)} {get_text('students', lang)}")
        if edit_data and edit_data.get('photo_url'):
            st.markdown(f"#### {get_text('photo', lang)}")
            display_photo_in_streamlit(edit_data.get('photo_url'), 150, lang)
    else:
        st.markdown(f"### ➕ {get_text('add_new', lang)} {get_text('students', lang)}")
    
    with st.form(f"student_form_{'edit' if edit_data else 'add'}"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(f"{get_text('full_name', lang)} *", value=edit_data.get('name', '') if edit_data else '')
            birthday = st.date_input(f"{get_text('birthday', lang)} *", 
                                    value=datetime.strptime(edit_data['birthday'], '%Y-%m-%d').date() if edit_data and edit_data.get('birthday') else date.today())
            grade = st.selectbox(f"{get_text('grade', lang)} *", list(range(1, 14)), 
                               index=list(range(1, 14)).index(edit_data['grade']) if edit_data and edit_data.get('grade') else 0)
            guardian_name = st.text_input(f"{get_text('guardian_name', lang)} *", value=edit_data.get('guardian_name', '') if edit_data else '')
            guardian_phone = st.text_input(get_text('guardian_phone', lang), value=edit_data.get('guardian_phone', '') if edit_data else '')
            guardian_email = st.text_input(get_text('guardian_email', lang), value=edit_data.get('guardian_email', '') if edit_data else '')
        
        with col2:
            school_index = st.text_input(get_text('school_index', lang), value=edit_data.get('school_index_number', '') if edit_data else '')
            address = st.text_area(get_text('address', lang), value=edit_data.get('address', '') if edit_data else '')
            siblings = st.text_input(get_text('siblings_at_school', lang), value=edit_data.get('siblings_at_school', '') if edit_data else '')
            mother_occupation = st.text_input(get_text('mother_occupation', lang), value=edit_data.get('mother_occupation', '') if edit_data else '')
            father_occupation = st.text_input(get_text('father_occupation', lang), value=edit_data.get('father_occupation', '') if edit_data else '')
            achievements = st.text_area(get_text('achievements', lang), value=edit_data.get('achievements', '') if edit_data else '')
            special_needs = st.selectbox(get_text('special_needs', lang), ["No", "Yes"], 
                                       index=0 if edit_data is None or edit_data.get('is_special_needs') != 'Yes' else 1)
        
        photo = st.file_uploader(f"📷 {get_text('upload_photo', lang)}", type=['jpg', 'jpeg', 'png'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            submitted = st.form_submit_button(f"💾 {get_text('save' if not edit_data else 'update', lang)}")
        with col2:
            submitted_and_print = st.form_submit_button(f"💾 {get_text('save_print' if not edit_data else 'update_print', lang)}")
        with col3:
            if edit_data:
                submitted_delete = st.form_submit_button(f"🗑️ {get_text('delete', lang)}", type="secondary")
            else:
                submitted_delete = None
        
        if submitted or submitted_and_print or submitted_delete:
            photo_url = edit_data.get('photo_url') if edit_data else None
            if photo:
                photo_url = save_photo(photo)
            
            return {
                'action': 'save' if submitted else 'save_print' if submitted_and_print else 'delete' if submitted_delete else None,
                'data': {
                    'name': name,
                    'birthday': birthday.strftime('%Y-%m-%d'),
                    'grade': grade,
                    'guardian_name': guardian_name,
                    'guardian_phone': guardian_phone,
                    'guardian_email': guardian_email,
                    'photo_url': photo_url,
                    'school_index_number': school_index.upper() if school_index else None,
                    'address': address,
                    'siblings_at_school': siblings,
                    'mother_occupation': mother_occupation,
                    'father_occupation': father_occupation,
                    'achievements': achievements,
                    'is_special_needs': special_needs
                }
            }
    return None

# ==============================================
# TEACHER FORM FUNCTIONS
# ==============================================

def show_teacher_edit_form(teacher, lang='en'):
    """Show teacher edit form"""
    
    st.markdown(f"### ✏️ {get_text('edit', lang)} {get_text('teachers', lang)}")
    
    if teacher.get('photo_url'):
        st.markdown(f"#### {get_text('photo', lang)}")
        display_photo_in_streamlit(teacher.get('photo_url'), 150, lang)
    
    with st.form("teacher_edit_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(f"{get_text('full_name', lang)} *", value=teacher.get('name', ''))
            birthday = st.date_input(f"{get_text('birthday', lang)}", value=datetime.strptime(teacher['birthday'], '%Y-%m-%d').date() if teacher.get('birthday') else date.today())
            subject = st.text_input(f"{get_text('subject', lang)} *", value=teacher.get('subject', ''))
            email = st.text_input(get_text('email', lang), value=teacher.get('email', ''))
            phone = st.text_input(get_text('phone', lang), value=teacher.get('phone', ''))
            nic_number = st.text_input(get_text('nic_number', lang), value=teacher.get('nic_number', ''))
        
        with col2:
            qualification = st.text_input(get_text('qualification', lang), value=teacher.get('qualification', ''))
            experience = st.number_input(get_text('experience', lang), min_value=0, step=1, value=teacher.get('experience', 0))
            address = st.text_area(get_text('address', lang), value=teacher.get('address', ''))
            date_initial = st.date_input(get_text('date_initial', lang), value=datetime.strptime(teacher['date_of_initial_appointment'], '%Y-%m-%d').date() if teacher.get('date_of_initial_appointment') else date.today())
            date_arrival = st.date_input(get_text('date_arrival', lang), value=datetime.strptime(teacher['date_of_arrival_at_school'], '%Y-%m-%d').date() if teacher.get('date_of_arrival_at_school') else date.today())
            nature_appointment = st.text_input(get_text('nature_appointment', lang), value=teacher.get('nature_of_appointment', ''))
            retirement_date = st.date_input(get_text('retirement_date', lang), value=datetime.strptime(teacher['scheduled_date_of_retirement'], '%Y-%m-%d').date() if teacher.get('scheduled_date_of_retirement') else date.today())
            schools_served = st.text_area(get_text('schools_served', lang), value=teacher.get('schools_served_at', ''))
            position = st.text_input(get_text('position', lang), value=teacher.get('position', ''))
        
        photo = st.file_uploader(f"📷 {get_text('upload_photo', lang)}", type=['jpg', 'jpeg', 'png'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            submitted = st.form_submit_button(f"💾 {get_text('update', lang)}")
        with col2:
            submitted_and_print = st.form_submit_button(f"💾 {get_text('update_print', lang)}")
        with col3:
            submitted_delete = st.form_submit_button(f"🗑️ {get_text('delete', lang)}", type="secondary")
        
        if submitted or submitted_and_print or submitted_delete:
            photo_url = teacher.get('photo_url')
            if photo:
                photo_url = save_photo(photo)
            
            return {
                'action': 'save' if submitted else 'save_print' if submitted_and_print else 'delete' if submitted_delete else None,
                'data': {
                    'name': name,
                    'birthday': birthday.strftime('%Y-%m-%d'),
                    'subject': subject,
                    'email': email,
                    'phone': phone,
                    'photo_url': photo_url,
                    'nic_number': nic_number,
                    'qualification': qualification,
                    'experience': experience,
                    'address': address,
                    'date_of_initial_appointment': date_initial.strftime('%Y-%m-%d'),
                    'date_of_arrival_at_school': date_arrival.strftime('%Y-%m-%d'),
                    'nature_of_appointment': nature_appointment,
                    'vocational_educational_qualifications': '',
                    'scheduled_date_of_retirement': retirement_date.strftime('%Y-%m-%d'),
                    'schools_served_at': schools_served,
                    'position': position
                }
            }
    return None

# ==============================================
# MAIN FUNCTION
# ==============================================

def main():
    # Page configuration
    st.set_page_config(
        page_title="School Management System",
        page_icon="🏫",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem;
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4F46E5;
    }
    .stat-label {
        font-size: 1rem;
        color: #6b7280;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Language selector
    st.sidebar.markdown("## 🌐 Language / භාෂාව")
    lang = st.sidebar.selectbox(
        "Select Language",
        options=['en', 'si'],
        format_func=lambda x: 'English' if x == 'en' else 'සිංහල'
    )
    
    # Check database connection
    if not DB_CONNECTED:
        st.error("""
        ❌ **Failed to connect to Supabase!**
        
        Please check:
        1. Your `.env` file has correct SUPABASE_URL and SUPABASE_KEY
        2. You have an active internet connection
        3. Your Supabase project is active
        """)
        return
    
    # Initialize session state
    if 'show_print' not in st.session_state:
        st.session_state.show_print = False
    if 'print_data' not in st.session_state:
        st.session_state.print_data = None
    if 'print_type' not in st.session_state:
        st.session_state.print_type = None
    if 'edit_id' not in st.session_state:
        st.session_state.edit_id = None
    if 'edit_type' not in st.session_state:
        st.session_state.edit_type = None
    if 'last_menu' not in st.session_state:
        st.session_state.last_menu = None
    
    # Sidebar navigation
    st.sidebar.markdown("## 🏫 Navigation")
    menu = st.sidebar.radio(
        "Select Section",
        [get_text('dashboard', lang), get_text('students', lang), get_text('teachers', lang), 
         get_text('development_officers', lang), get_text('non_academic_officers', lang), 
         get_text('search', lang), get_text('reports', lang)]
    )
    
    # Map menu to English keys
    menu_map = {
        get_text('dashboard', lang): 'dashboard',
        get_text('students', lang): 'students',
        get_text('teachers', lang): 'teachers',
        get_text('development_officers', lang): 'development',
        get_text('non_academic_officers', lang): 'nonacademic',
        get_text('search', lang): 'search',
        get_text('reports', lang): 'reports'
    }
    menu_key = menu_map.get(menu, 'dashboard')
    
    # Reset edit state when changing menu
    if menu_key != st.session_state.get('last_menu'):
        st.session_state.edit_id = None
        st.session_state.edit_type = None
        st.session_state.last_menu = menu_key
        if not st.session_state.show_print:
            st.rerun()
    
    # Header
    st.markdown(f"""
    <div class="main-header">
        <h1>{get_text('app_title', lang)}</h1>
        <p>{get_text('school_name', lang)}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ==========================================
    # DASHBOARD
    # ==========================================
    if menu_key == "dashboard":
        st.markdown(f"## {get_text('dashboard', lang)}")
        
        stats = get_stats()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{stats['total_students']}</div>
                <div class="stat-label">{get_text('total_students', lang)}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{stats['total_teachers']}</div>
                <div class="stat-label">{get_text('total_teachers', lang)}</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{stats['total_development_officers']}</div>
                <div class="stat-label">{get_text('total_dev', lang)}</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{stats['total_non_academic_officers']}</div>
                <div class="stat-label">{get_text('total_nonacademic', lang)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        if stats['grade_distribution']:
            st.markdown(f"### {get_text('grade_distribution', lang)}")
            df = pd.DataFrame(stats['grade_distribution'])
            st.bar_chart(df.set_index('grade'))
    
    # ==========================================
    # STUDENTS
    # ==========================================
    elif menu_key == "students":
        st.markdown(f"## {get_text('student_management', lang)}")
        
        if st.session_state.show_print and st.session_state.print_type == 'student':
            st.markdown(f"### 📄 {get_text('student_details', lang)}")
            student_data = st.session_state.print_data
            details_dict = get_student_details_dict(student_data, lang)
            display_print_view(details_dict, get_text('student_details', lang), student_data.get('name', 'Student'), lang)
            return
        
        if st.session_state.edit_id and st.session_state.edit_type == 'student':
            student_data = get_student_by_id(st.session_state.edit_id)
            if not student_data.empty:
                student = student_data.iloc[0].to_dict()
                result = show_student_form(student, lang)
                if result:
                    if result['action'] == 'delete':
                        try:
                            if delete_student(st.session_state.edit_id):
                                st.success(get_text('success_deleted', lang))
                            else:
                                st.error("Failed to delete student")
                            st.session_state.edit_id = None
                            st.session_state.edit_type = None
                            st.rerun()
                        except Exception as e:
                            st.error(f"{get_text('error_occurred', lang)} {str(e)}")
                    elif result['action'] in ['save', 'save_print']:
                        try:
                            if update_student(st.session_state.edit_id, result['data']):
                                st.success(get_text('success_updated', lang))
                            else:
                                st.error("Failed to update student")
                            
                            if result['action'] == 'save_print':
                                updated_data = get_student_by_id(st.session_state.edit_id).iloc[0].to_dict()
                                st.session_state.print_data = updated_data
                                st.session_state.print_type = 'student'
                                st.session_state.show_print = True
                                st.session_state.edit_id = None
                                st.session_state.edit_type = None
                                st.rerun()
                            else:
                                st.session_state.edit_id = None
                                st.session_state.edit_type = None
                                st.rerun()
                        except Exception as e:
                            st.error(f"{get_text('error_occurred', lang)} {str(e)}")
            else:
                st.warning("Student not found")
                st.session_state.edit_id = None
                st.session_state.edit_type = None
            return
        
        tab1, tab2 = st.tabs([get_text('view_all', lang), get_text('add_new', lang)])
        
        with tab1:
            df = get_all_students()
            if not df.empty:
                st.dataframe(df[['id', 'name', 'grade', 'guardian_name', 'school_index_number']], use_container_width=True)
                
                st.markdown(f"#### {get_text('actions', lang)}")
                selected_id = st.selectbox(f"{get_text('select_record', lang)}", df['id'].tolist(), key="student_select")
                
                selected_student = df[df['id'] == selected_id].iloc[0].to_dict()
                st.markdown("---")
                col_img, col_info = st.columns([1, 3])
                with col_img:
                    display_photo_in_streamlit(selected_student.get('photo_url'), 150, lang)
                with col_info:
                    st.markdown(f"**{get_text('full_name', lang)}:** {selected_student.get('name')}")
                    st.markdown(f"**{get_text('grade', lang)}:** {selected_student.get('grade')}")
                    st.markdown(f"**{get_text('guardian_name', lang)}:** {selected_student.get('guardian_name')}")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button(f"📄 {get_text('view_details', lang)}", key="view_student"):
                        st.session_state.print_data = selected_student
                        st.session_state.print_type = 'student'
                        st.session_state.show_print = True
                        st.rerun()
                with col2:
                    if st.button(f"✏️ {get_text('edit', lang)}", key="edit_student"):
                        st.session_state.edit_id = selected_id
                        st.session_state.edit_type = 'student'
                        st.rerun()
                with col3:
                    if st.button(f"🗑️ {get_text('delete', lang)}", key="delete_student"):
                        if st.warning(get_text('confirm_delete', lang)):
                            try:
                                if delete_student(selected_id):
                                    st.success(get_text('success_deleted', lang))
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.error("Failed to delete student")
                            except Exception as e:
                                st.error(f"{get_text('error_occurred', lang)} {str(e)}")
            else:
                st.info(get_text('no_data', lang))
        
        with tab2:
            result = show_student_form(None, lang)
            if result:
                if result['action'] in ['save', 'save_print']:
                    if not result['data']['name'] or not result['data']['guardian_name']:
                        st.error(get_text('fill_required', lang))
                    else:
                        try:
                            student_id = add_student(result['data'])
                            if student_id:
                                st.success(f"✅ {get_text('success_added', lang)} ID: {student_id}")
                                st.balloons()
                                
                                if result['action'] == 'save_print':
                                    time.sleep(1)
                                    student_data = get_student_by_id(student_id).iloc[0].to_dict()
                                    st.session_state.print_data = student_data
                                    st.session_state.print_type = 'student'
                                    st.session_state.show_print = True
                                    st.rerun()
                                else:
                                    time.sleep(1)
                                    st.rerun()
                            else:
                                st.error("Failed to add student")
                        except Exception as e:
                            st.error(f"{get_text('error_occurred', lang)} {str(e)}")
    
    # ==========================================
    # TEACHERS
    # ==========================================
    elif menu_key == "teachers":
        st.markdown(f"## {get_text('teacher_management', lang)}")
        
        if st.session_state.show_print and st.session_state.print_type == 'teacher':
            st.markdown(f"### 📄 {get_text('teacher_details', lang)}")
            teacher_data = st.session_state.print_data
            details_dict = get_teacher_details_dict(teacher_data, lang)
            display_print_view(details_dict, get_text('teacher_details', lang), teacher_data.get('name', 'Teacher'), lang)
            return
        
        if st.session_state.edit_id and st.session_state.edit_type == 'teacher':
            teacher_data = get_teacher_by_id(st.session_state.edit_id)
            if not teacher_data.empty:
                teacher = teacher_data.iloc[0].to_dict()
                result = show_teacher_edit_form(teacher, lang)
                if result:
                    if result['action'] == 'delete':
                        try:
                            if delete_teacher(st.session_state.edit_id):
                                st.success(get_text('success_deleted', lang))
                            st.session_state.edit_id = None
                            st.session_state.edit_type = None
                            st.rerun()
                        except Exception as e:
                            st.error(f"{get_text('error_occurred', lang)} {str(e)}")
                    elif result['action'] in ['save', 'save_print']:
                        try:
                            if update_teacher(st.session_state.edit_id, result['data']):
                                st.success(get_text('success_updated', lang))
                            
                            if result['action'] == 'save_print':
                                updated_data = get_teacher_by_id(st.session_state.edit_id).iloc[0].to_dict()
                                st.session_state.print_data = updated_data
                                st.session_state.print_type = 'teacher'
                                st.session_state.show_print = True
                                st.session_state.edit_id = None
                                st.session_state.edit_type = None
                                st.rerun()
                            else:
                                st.session_state.edit_id = None
                                st.session_state.edit_type = None
                                st.rerun()
                        except Exception as e:
                            st.error(f"{get_text('error_occurred', lang)} {str(e)}")
            else:
                st.warning("Teacher not found")
                st.session_state.edit_id = None
                st.session_state.edit_type = None
            return
        
        tab1, tab2 = st.tabs([get_text('view_all', lang), get_text('add_new', lang)])
        
        with tab1:
            df = get_all_teachers()
            if not df.empty:
                st.dataframe(df[['id', 'name', 'subject', 'email', 'phone', 'nic_number', 'position']], use_container_width=True)
                
                st.markdown(f"#### {get_text('actions', lang)}")
                selected_id = st.selectbox(f"{get_text('select_record', lang)}", df['id'].tolist(), key="teacher_select")
                
                selected_teacher = df[df['id'] == selected_id].iloc[0].to_dict()
                st.markdown("---")
                col_img, col_info = st.columns([1, 3])
                with col_img:
                    display_photo_in_streamlit(selected_teacher.get('photo_url'), 150, lang)
                with col_info:
                    st.markdown(f"**{get_text('full_name', lang)}:** {selected_teacher.get('name')}")
                    st.markdown(f"**{get_text('subject', lang)}:** {selected_teacher.get('subject')}")
                    st.markdown(f"**{get_text('position', lang)}:** {selected_teacher.get('position')}")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button(f"📄 {get_text('view_details', lang)}", key="view_teacher"):
                        st.session_state.print_data = selected_teacher
                        st.session_state.print_type = 'teacher'
                        st.session_state.show_print = True
                        st.rerun()
                with col2:
                    if st.button(f"✏️ {get_text('edit', lang)}", key="edit_teacher"):
                        st.session_state.edit_id = selected_id
                        st.session_state.edit_type = 'teacher'
                        st.rerun()
                with col3:
                    if st.button(f"🗑️ {get_text('delete', lang)}", key="delete_teacher"):
                        if st.warning(get_text('confirm_delete', lang)):
                            try:
                                if delete_teacher(selected_id):
                                    st.success(get_text('success_deleted', lang))
                                    time.sleep(1)
                                    st.rerun()
                            except Exception as e:
                                st.error(f"{get_text('error_occurred', lang)} {str(e)}")
            else:
                st.info(get_text('no_data', lang))
        
        with tab2:
            st.markdown(f"### ➕ {get_text('add_new', lang)} {get_text('teachers', lang)}")
            with st.form("teacher_add_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input(f"{get_text('full_name', lang)} *")
                    birthday = st.date_input(get_text('birthday', lang), value=date.today())
                    subject = st.text_input(f"{get_text('subject', lang)} *")
                    email = st.text_input(get_text('email', lang))
                    phone = st.text_input(get_text('phone', lang))
                    nic_number = st.text_input(get_text('nic_number', lang))
                
                with col2:
                    qualification = st.text_input(get_text('qualification', lang))
                    experience = st.number_input(get_text('experience', lang), min_value=0, step=1)
                    address = st.text_area(get_text('address', lang))
                    date_initial = st.date_input(get_text('date_initial', lang))
                    date_arrival = st.date_input(get_text('date_arrival', lang))
                    nature_appointment = st.text_input(get_text('nature_appointment', lang))
                    retirement_date = st.date_input(get_text('retirement_date', lang))
                    schools_served = st.text_area(get_text('schools_served', lang))
                    position = st.text_input(get_text('position', lang))
                
                photo = st.file_uploader(f"📷 {get_text('upload_photo', lang)}", type=['jpg', 'jpeg', 'png'])
                
                col1, col2 = st.columns(2)
                with col1:
                    submitted = st.form_submit_button(f"💾 {get_text('save', lang)}")
                with col2:
                    submitted_and_print = st.form_submit_button(f"💾 {get_text('save_print', lang)}")
                
                if submitted or submitted_and_print:
                    if not name or not subject:
                        st.error(get_text('fill_required', lang))
                    else:
                        photo_url = save_photo(photo) if photo else None
                        teacher_data = {
                            'name': name,
                            'birthday': birthday.strftime('%Y-%m-%d'),
                            'subject': subject,
                            'email': email,
                            'phone': phone,
                            'photo_url': photo_url,
                            'nic_number': nic_number,
                            'qualification': qualification,
                            'experience': experience,
                            'address': address,
                            'date_of_initial_appointment': date_initial.strftime('%Y-%m-%d'),
                            'date_of_arrival_at_school': date_arrival.strftime('%Y-%m-%d'),
                            'nature_of_appointment': nature_appointment,
                            'vocational_educational_qualifications': '',
                            'scheduled_date_of_retirement': retirement_date.strftime('%Y-%m-%d'),
                            'schools_served_at': schools_served,
                            'position': position
                        }
                        try:
                            teacher_id = add_teacher(teacher_data)
                            if teacher_id:
                                st.success(f"✅ {get_text('success_added', lang)} ID: {teacher_id}")
                                st.balloons()
                                
                                if submitted_and_print:
                                    time.sleep(1)
                                    teacher_data = get_teacher_by_id(teacher_id).iloc[0].to_dict()
                                    st.session_state.print_data = teacher_data
                                    st.session_state.print_type = 'teacher'
                                    st.session_state.show_print = True
                                    st.rerun()
                                else:
                                    time.sleep(1)
                                    st.rerun()
                            else:
                                st.error("Failed to add teacher")
                        except Exception as e:
                            st.error(f"{get_text('error_occurred', lang)} {str(e)}")
    
    # ==========================================
    # DEVELOPMENT OFFICERS
    # ==========================================
    elif menu_key == "development":
        st.markdown(f"## {get_text('dev_management', lang)}")
        
        if st.session_state.show_print and st.session_state.print_type == 'development':
            st.markdown(f"### 📄 {get_text('dev_details', lang)}")
            officer_data = st.session_state.print_data
            details_dict = get_development_officer_details_dict(officer_data, lang)
            display_print_view(details_dict, get_text('dev_details', lang), officer_data.get('name', 'Officer'), lang)
            return
        
        tab1, tab2 = st.tabs([get_text('view_all', lang), get_text('add_new', lang)])
        
        with tab1:
            df = get_all_development_officers()
            if not df.empty:
                st.dataframe(df[['id', 'name', 'designation', 'department', 'email', 'phone', 'nic_number', 'position']], use_container_width=True)
                
                st.markdown(f"#### {get_text('actions', lang)}")
                selected_id = st.selectbox(f"{get_text('select_record', lang)}", df['id'].tolist(), key="dev_select")
                
                selected_officer = df[df['id'] == selected_id].iloc[0].to_dict()
                st.markdown("---")
                col_img, col_info = st.columns([1, 3])
                with col_img:
                    display_photo_in_streamlit(selected_officer.get('photo_url'), 150, lang)
                with col_info:
                    st.markdown(f"**{get_text('full_name', lang)}:** {selected_officer.get('name')}")
                    st.markdown(f"**{get_text('designation', lang)}:** {selected_officer.get('designation')}")
                    st.markdown(f"**{get_text('department', lang)}:** {selected_officer.get('department')}")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button(f"📄 {get_text('view_details', lang)}", key="view_dev"):
                        st.session_state.print_data = selected_officer
                        st.session_state.print_type = 'development'
                        st.session_state.show_print = True
                        st.rerun()
                with col2:
                    if st.button(f"✏️ {get_text('edit', lang)}", key="edit_dev"):
                        st.session_state.edit_id = selected_id
                        st.session_state.edit_type = 'development'
                        st.rerun()
                with col3:
                    if st.button(f"🗑️ {get_text('delete', lang)}", key="delete_dev"):
                        if st.warning(get_text('confirm_delete', lang)):
                            try:
                                if delete_development_officer(selected_id):
                                    st.success(get_text('success_deleted', lang))
                                    time.sleep(1)
                                    st.rerun()
                            except Exception as e:
                                st.error(f"{get_text('error_occurred', lang)} {str(e)}")
            else:
                st.info(get_text('no_data', lang))
        
        with tab2:
            st.markdown(f"### ➕ {get_text('add_new', lang)} {get_text('development_officers', lang)}")
            with st.form("dev_add_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input(f"{get_text('full_name', lang)} *")
                    birthday = st.date_input(get_text('birthday', lang), value=date.today())
                    designation = st.text_input(f"{get_text('designation', lang)} *")
                    department = st.text_input(get_text('department', lang))
                    email = st.text_input(get_text('email', lang))
                    phone = st.text_input(get_text('phone', lang))
                    nic_number = st.text_input(get_text('nic_number', lang))
                
                with col2:
                    qualification = st.text_input(get_text('qualification', lang))
                    experience = st.number_input(get_text('experience', lang), min_value=0, step=1)
                    address = st.text_area(get_text('address', lang))
                    date_initial = st.date_input(get_text('date_initial', lang))
                    date_arrival = st.date_input(get_text('date_arrival', lang))
                    nature_appointment = st.text_input(get_text('nature_appointment', lang))
                    retirement_date = st.date_input(get_text('retirement_date', lang))
                    schools_served = st.text_area(get_text('schools_served', lang))
                    position = st.text_input(get_text('position', lang))
                    duty_list = st.text_area(get_text('duty_list', lang))
                
                photo = st.file_uploader(f"📷 {get_text('upload_photo', lang)}", type=['jpg', 'jpeg', 'png'])
                
                col1, col2 = st.columns(2)
                with col1:
                    submitted = st.form_submit_button(f"💾 {get_text('save', lang)}")
                with col2:
                    submitted_and_print = st.form_submit_button(f"💾 {get_text('save_print', lang)}")
                
                if submitted or submitted_and_print:
                    if not name or not designation:
                        st.error(get_text('fill_required', lang))
                    else:
                        photo_url = save_photo(photo) if photo else None
                        dev_data = {
                            'name': name,
                            'birthday': birthday.strftime('%Y-%m-%d'),
                            'designation': designation,
                            'department': department,
                            'email': email,
                            'phone': phone,
                            'photo_url': photo_url,
                            'nic_number': nic_number,
                            'qualification': qualification,
                            'experience': experience,
                            'address': address,
                            'date_of_initial_appointment': date_initial.strftime('%Y-%m-%d'),
                            'date_of_arrival_at_school': date_arrival.strftime('%Y-%m-%d'),
                            'nature_of_appointment': nature_appointment,
                            'vocational_educational_qualifications': '',
                            'scheduled_date_of_retirement': retirement_date.strftime('%Y-%m-%d'),
                            'schools_served_at': schools_served,
                            'position': position,
                            'duty_list': duty_list
                        }
                        try:
                            officer_id = add_development_officer(dev_data)
                            if officer_id:
                                st.success(f"✅ {get_text('success_added', lang)} ID: {officer_id}")
                                st.balloons()
                                
                                if submitted_and_print:
                                    time.sleep(1)
                                    officer_data = get_development_officer_by_id(officer_id).iloc[0].to_dict()
                                    st.session_state.print_data = officer_data
                                    st.session_state.print_type = 'development'
                                    st.session_state.show_print = True
                                    st.rerun()
                                else:
                                    time.sleep(1)
                                    st.rerun()
                            else:
                                st.error("Failed to add development officer")
                        except Exception as e:
                            st.error(f"{get_text('error_occurred', lang)} {str(e)}")
    
    # ==========================================
    # NON-ACADEMIC OFFICERS
    # ==========================================
    elif menu_key == "nonacademic":
        st.markdown(f"## {get_text('nonacademic_management', lang)}")
        
        if st.session_state.show_print and st.session_state.print_type == 'nonacademic':
            st.markdown(f"### 📄 {get_text('nonacademic_details', lang)}")
            officer_data = st.session_state.print_data
            details_dict = get_non_academic_officer_details_dict(officer_data, lang)
            display_print_view(details_dict, get_text('nonacademic_details', lang), officer_data.get('name', 'Officer'), lang)
            return
        
        tab1, tab2 = st.tabs([get_text('view_all', lang), get_text('add_new', lang)])
        
        with tab1:
            df = get_all_non_academic_officers()
            if not df.empty:
                st.dataframe(df[['id', 'name', 'designation', 'department', 'email', 'phone', 'nic_number', 'position']], use_container_width=True)
                
                st.markdown(f"#### {get_text('actions', lang)}")
                selected_id = st.selectbox(f"{get_text('select_record', lang)}", df['id'].tolist(), key="nonacad_select")
                
                selected_officer = df[df['id'] == selected_id].iloc[0].to_dict()
                st.markdown("---")
                col_img, col_info = st.columns([1, 3])
                with col_img:
                    display_photo_in_streamlit(selected_officer.get('photo_url'), 150, lang)
                with col_info:
                    st.markdown(f"**{get_text('full_name', lang)}:** {selected_officer.get('name')}")
                    st.markdown(f"**{get_text('designation', lang)}:** {selected_officer.get('designation')}")
                    st.markdown(f"**{get_text('department', lang)}:** {selected_officer.get('department')}")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button(f"📄 {get_text('view_details', lang)}", key="view_nonacad"):
                        st.session_state.print_data = selected_officer
                        st.session_state.print_type = 'nonacademic'
                        st.session_state.show_print = True
                        st.rerun()
                with col2:
                    if st.button(f"✏️ {get_text('edit', lang)}", key="edit_nonacad"):
                        st.session_state.edit_id = selected_id
                        st.session_state.edit_type = 'nonacademic'
                        st.rerun()
                with col3:
                    if st.button(f"🗑️ {get_text('delete', lang)}", key="delete_nonacad"):
                        if st.warning(get_text('confirm_delete', lang)):
                            try:
                                if delete_non_academic_officer(selected_id):
                                    st.success(get_text('success_deleted', lang))
                                    time.sleep(1)
                                    st.rerun()
                            except Exception as e:
                                st.error(f"{get_text('error_occurred', lang)} {str(e)}")
            else:
                st.info(get_text('no_data', lang))
        
        with tab2:
            st.markdown(f"### ➕ {get_text('add_new', lang)} {get_text('non_academic_officers', lang)}")
            with st.form("nonacad_add_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input(f"{get_text('full_name', lang)} *")
                    birthday = st.date_input(get_text('birthday', lang), value=date.today())
                    designation = st.text_input(f"{get_text('designation', lang)} *")
                    department = st.text_input(get_text('department', lang))
                    email = st.text_input(get_text('email', lang))
                    phone = st.text_input(get_text('phone', lang))
                    nic_number = st.text_input(get_text('nic_number', lang))
                
                with col2:
                    qualification = st.text_input(get_text('qualification', lang))
                    experience = st.number_input(get_text('experience', lang), min_value=0, step=1)
                    address = st.text_area(get_text('address', lang))
                    date_initial = st.date_input(get_text('date_initial', lang))
                    date_arrival = st.date_input(get_text('date_arrival', lang))
                    nature_appointment = st.text_input(get_text('nature_appointment', lang))
                    retirement_date = st.date_input(get_text('retirement_date', lang))
                    schools_served = st.text_area(get_text('schools_served', lang))
                    position = st.text_input(get_text('position', lang))
                
                photo = st.file_uploader(f"📷 {get_text('upload_photo', lang)}", type=['jpg', 'jpeg', 'png'])
                
                col1, col2 = st.columns(2)
                with col1:
                    submitted = st.form_submit_button(f"💾 {get_text('save', lang)}")
                with col2:
                    submitted_and_print = st.form_submit_button(f"💾 {get_text('save_print', lang)}")
                
                if submitted or submitted_and_print:
                    if not name or not designation:
                        st.error(get_text('fill_required', lang))
                    else:
                        photo_url = save_photo(photo) if photo else None
                        officer_data = {
                            'name': name,
                            'birthday': birthday.strftime('%Y-%m-%d'),
                            'designation': designation,
                            'department': department,
                            'email': email,
                            'phone': phone,
                            'photo_url': photo_url,
                            'nic_number': nic_number,
                            'qualification': qualification,
                            'experience': experience,
                            'address': address,
                            'date_of_initial_appointment': date_initial.strftime('%Y-%m-%d'),
                            'date_of_arrival_at_school': date_arrival.strftime('%Y-%m-%d'),
                            'nature_of_appointment': nature_appointment,
                            'vocational_educational_qualifications': '',
                            'scheduled_date_of_retirement': retirement_date.strftime('%Y-%m-%d'),
                            'schools_served_at': schools_served,
                            'position': position
                        }
                        try:
                            officer_id = add_non_academic_officer(officer_data)
                            if officer_id:
                                st.success(f"✅ {get_text('success_added', lang)} ID: {officer_id}")
                                st.balloons()
                                
                                if submitted_and_print:
                                    time.sleep(1)
                                    officer_data = get_non_academic_officer_by_id(officer_id).iloc[0].to_dict()
                                    st.session_state.print_data = officer_data
                                    st.session_state.print_type = 'nonacademic'
                                    st.session_state.show_print = True
                                    st.rerun()
                                else:
                                    time.sleep(1)
                                    st.rerun()
                            else:
                                st.error("Failed to add non-academic officer")
                        except Exception as e:
                            st.error(f"{get_text('error_occurred', lang)} {str(e)}")
    
    # ==========================================
    # SEARCH
    # ==========================================
    elif menu_key == "search":
        st.markdown(f"## {get_text('search', lang)}")
        
        search_type = st.selectbox(
            f"{get_text('search', lang)}",
            [f"{get_text('students', lang)} by {get_text('school_index', lang)}", 
             f"{get_text('teachers', lang)} by {get_text('nic_number', lang)}", 
             f"{get_text('development_officers', lang)} by {get_text('nic_number', lang)}", 
             f"{get_text('non_academic_officers', lang)} by {get_text('nic_number', lang)}"]
        )
        
        if "School Index" in search_type or "දර්ශක" in search_type:
            school_index = st.text_input(f"{get_text('search_by_school_index', lang)}")
            if st.button(f"🔍 {get_text('search', lang)}"):
                if school_index:
                    df = search_student_by_school_index(school_index.upper())
                    if not df.empty:
                        st.success("✅ Student found!")
                        student_data = df.iloc[0].to_dict()
                        st.session_state.print_data = student_data
                        st.session_state.print_type = 'student'
                        st.session_state.show_print = True
                        st.rerun()
                    else:
                        st.warning(get_text('no_data', lang))
                else:
                    st.warning("Please enter a value")
        
        elif "Teacher" in search_type or "ගුරු" in search_type:
            nic = st.text_input(f"{get_text('search_by_nic', lang)}")
            if st.button(f"🔍 {get_text('search', lang)}"):
                if nic:
                    df = search_teacher_by_nic(nic.upper())
                    if not df.empty:
                        st.success("✅ Teacher found!")
                        teacher_data = df.iloc[0].to_dict()
                        st.session_state.print_data = teacher_data
                        st.session_state.print_type = 'teacher'
                        st.session_state.show_print = True
                        st.rerun()
                    else:
                        st.warning(get_text('no_data', lang))
                else:
                    st.warning("Please enter a NIC number")
        
        elif "Development" in search_type or "සංවර්ධන" in search_type:
            nic = st.text_input(f"{get_text('search_by_nic', lang)}")
            if st.button(f"🔍 {get_text('search', lang)}"):
                if nic:
                    df = search_development_officer_by_nic(nic.upper())
                    if not df.empty:
                        st.success("✅ Development Officer found!")
                        officer_data = df.iloc[0].to_dict()
                        st.session_state.print_data = officer_data
                        st.session_state.print_type = 'development'
                        st.session_state.show_print = True
                        st.rerun()
                    else:
                        st.warning(get_text('no_data', lang))
                else:
                    st.warning("Please enter a NIC number")
        
        elif "Non-Academic" in search_type or "අධ්‍යාපන නොවන" in search_type:
            nic = st.text_input(f"{get_text('search_by_nic', lang)}")
            if st.button(f"🔍 {get_text('search', lang)}"):
                if nic:
                    df = search_non_academic_officer_by_nic(nic.upper())
                    if not df.empty:
                        st.success("✅ Non-Academic Officer found!")
                        officer_data = df.iloc[0].to_dict()
                        st.session_state.print_data = officer_data
                        st.session_state.print_type = 'nonacademic'
                        st.session_state.show_print = True
                        st.rerun()
                    else:
                        st.warning(get_text('no_data', lang))
                else:
                    st.warning("Please enter a NIC number")
    
    # ==========================================
    # REPORTS
    # ==========================================
    elif menu_key == "reports":
        st.markdown(f"## {get_text('reports', lang)}")
        
        report_type = st.selectbox(
            f"{get_text('reports', lang)}",
            [get_text('students', lang), get_text('teachers', lang), 
             get_text('development_officers', lang), get_text('non_academic_officers', lang)]
        )
        
        if report_type == get_text('students', lang):
            st.markdown(f"### 📊 {get_text('students', lang)} {get_text('reports', lang)}")
            df = get_all_students()
            if not df.empty:
                st.dataframe(df, use_container_width=True)
                csv = df.to_csv(index=False)
                st.download_button(
                    label=f"📥 {get_text('download_html', lang)}",
                    data=csv,
                    file_name="students_report.csv",
                    mime="text/csv"
                )
            else:
                st.info(get_text('no_data', lang))
        
        elif report_type == get_text('teachers', lang):
            st.markdown(f"### 📊 {get_text('teachers', lang)} {get_text('reports', lang)}")
            df = get_all_teachers()
            if not df.empty:
                st.dataframe(df, use_container_width=True)
                csv = df.to_csv(index=False)
                st.download_button(
                    label=f"📥 {get_text('download_html', lang)}",
                    data=csv,
                    file_name="teachers_report.csv",
                    mime="text/csv"
                )
            else:
                st.info(get_text('no_data', lang))
        
        elif report_type == get_text('development_officers', lang):
            st.markdown(f"### 📊 {get_text('development_officers', lang)} {get_text('reports', lang)}")
            df = get_all_development_officers()
            if not df.empty:
                st.dataframe(df, use_container_width=True)
                csv = df.to_csv(index=False)
                st.download_button(
                    label=f"📥 {get_text('download_html', lang)}",
                    data=csv,
                    file_name="development_officers_report.csv",
                    mime="text/csv"
                )
            else:
                st.info(get_text('no_data', lang))
        
        elif report_type == get_text('non_academic_officers', lang):
            st.markdown(f"### 📊 {get_text('non_academic_officers', lang)} {get_text('reports', lang)}")
            df = get_all_non_academic_officers()
            if not df.empty:
                st.dataframe(df, use_container_width=True)
                csv = df.to_csv(index=False)
                st.download_button(
                    label=f"📥 {get_text('download_html', lang)}",
                    data=csv,
                    file_name="non_academic_officers_report.csv",
                    mime="text/csv"
                )
            else:
                st.info(get_text('no_data', lang))
    
    # Footer
    st.markdown("---")
    st.markdown(f"© 2024 {get_text('school_name', lang)} - {get_text('app_title', lang)}")

if __name__ == "__main__":
    main()