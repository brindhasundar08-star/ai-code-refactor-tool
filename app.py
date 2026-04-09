import streamlit as st
from analyzer import analyze_code
from refactor import refactor_code
from tester import test_code
import difflib

st.set_page_config(page_title="AI Code Refactoring Tool", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for green button
st.markdown("""
    <style>
        .stButton > button {
            border-radius: 5px;
            font-weight: bold;
        }
        .refactor-btn > button {
            background-color: #28a745 !important;
            color: white !important;
        }
        .refactor-btn > button:hover {
            background-color: #218838 !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 AI Code Refactoring Tool")
st.markdown("Analyze, refactor, and validate your Python code with AI-powered suggestions")

# Sidebar settings
with st.sidebar:
    st.header("⚙️ Settings")
    show_diff = st.checkbox("Show differences", value=True)
    show_metrics = st.checkbox("Show statistics", value=True)
    st.markdown("---")
    st.markdown("📌 **How it works:**\n1. Upload a Python file or paste code\n2. View issues found\n3. Click refactor button\n4. View refactored code\n5. Download result")

# Initialize session state
if 'code' not in st.session_state:
    st.session_state.code = None
if 'refactored_code' not in st.session_state:
    st.session_state.refactored_code = None
if 'file_name' not in st.session_state:
    st.session_state.file_name = 'refactored_code.py'

# Tabs for input method
tab1, tab2 = st.tabs(["📤 Upload File", "📝 Paste Code"])

with tab1:
    st.subheader("📤 Upload Python File")
    uploaded_file = st.file_uploader("Choose a .py file", type=["py"], key="file_uploader")
    
    if uploaded_file is not None:
        code_content = uploaded_file.read().decode("utf-8")
        st.session_state.code = code_content
        st.session_state.file_name = f"refactored_{uploaded_file.name}"
        st.success(f"✅ Loaded: {uploaded_file.name}")
        st.info(f"📊 File size: {len(code_content)} characters")
        
        if st.button("🔄 Refactor Code", key="upload_refactor", use_container_width=True):
            st.session_state.refactor_triggered = True

with tab2:
    st.subheader("📝 Paste Python Code")
    code_input = st.text_area(
        "Paste your code here:",
        height=300,
        placeholder="def calc(x, y):\n    return x + y",
        key="code_input"
    )
    
    if code_input:
        st.session_state.code = code_input
        st.session_state.file_name = 'refactored_code.py'
        st.success("✅ Code ready to refactor")
        
        if st.button("🔄 Refactor Code", key="paste_refactor", use_container_width=True):
            st.session_state.refactor_triggered = True

# Process code
if st.session_state.code:
    st.markdown("---")
    
    # Analyze
    issues = analyze_code(st.session_state.code)
    
    # Display original code
    with st.expander("📌 Original Code", expanded=True):
        st.code(st.session_state.code, language='python')
    
    # Display analysis
    col1, col2 = st.columns(2)
    with col1:
        if issues:
            st.warning(f"🔍 **Issues Found:** {len(issues)}")
            with st.expander("View Issues"):
                for i, issue in enumerate(issues, 1):
                    st.write(f"{i}. {issue}")
        else:
            st.success("✅ No issues found!")
    
    # Refactor trigger
    if st.session_state.get('refactor_triggered', False):
        st.session_state.refactor_triggered = False
        
        with col2:
            st.info("⏳ Refactoring...")
        
        new_code = refactor_code(st.session_state.code, issues)
        st.session_state.refactored_code = new_code
        
        # Validate syntax
        is_valid = test_code(st.session_state.code, new_code)
        
        # Display refactored code
        st.subheader("✅ Refactored Code")
        st.code(new_code, language='python')
        
        # Validation status
        if is_valid:
            st.success("✅ Syntax validation passed!")
        else:
            st.error("❌ Syntax validation failed!")
        
        # Show differences
        if show_diff and st.session_state.code != new_code:
            st.subheader("📊 Changes Made")
            diff = list(difflib.unified_diff(
                st.session_state.code.splitlines(keepends=True),
                new_code.splitlines(keepends=True),
                fromfile='Original',
                tofile='Refactored'
            ))
            if diff:
                st.code("".join(diff), language='diff')
        
        # Statistics
        if show_metrics:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Lines (Original)", len(st.session_state.code.splitlines()))
            with col2:
                st.metric("Lines (Refactored)", len(new_code.splitlines()))
            with col3:
                st.metric("Issues Found", len(issues))
            with col4:
                st.metric("Syntax Valid", "✅ Yes" if is_valid else "❌ No")
        
        # Download button
        st.download_button(
            label="💾 Download Refactored Code",
            data=new_code,
            file_name=st.session_state.file_name,
            mime="text/plain",
            use_container_width=True
        )
        
        # Clear button
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.code = None
            st.session_state.refactored_code = None
            st.session_state.file_name = 'refactored_code.py'
            st.rerun()

        # Download button
        file_name = "refactored_code.py"
        if hasattr(st.session_state, 'uploaded_file_name'):
            file_name = f"refactored_{st.session_state.uploaded_file_name}"
        
        st.download_button(
            label="💾 Download Refactored Code",
            data=new_code,
            file_name=file_name,
            mime="text/plain"
        )

