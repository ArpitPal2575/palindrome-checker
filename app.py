import streamlit as st
import re # Used for robust cleaning of the string

# --- 1. CORE LOGIC & SETUP ---

# Initialize session state for history log
if 'history' not in st.session_state:
    st.session_state['history'] = []

def is_palindrome(text):
    """
    Checks if a string is a palindrome, ignoring case and non-alphanumeric characters.
    """
    # Step 1: Remove all non-alphanumeric characters (spaces, punctuation, etc.)
    cleaned_text = re.sub(r'[^a-zA-Z0-9]', '', text)
    
    # Step 2: Convert to lowercase
    cleaned_text = cleaned_text.lower()
    
    # Step 3: Compare the cleaned string with its reverse
    is_pal = cleaned_text == cleaned_text[::-1]
    
    return is_pal, cleaned_text

# Function to handle the button click and update history
def check_and_update():
    """Reads input, checks palindrome status, and updates session state."""
    user_input = st.session_state.input_key
    
    if not user_input:
        st.error("🚨 Please enter some text to check!")
        return
        
    is_pal, cleaned_text = is_palindrome(user_input)
    
    if is_pal:
        result_message = f"**'{user_input}' is a Palindrome! 🎉**"
        status = "Palindrome"
        st.success(result_message)
    else:
        result_message = f"**'{user_input}' is NOT a Palindrome. 🙁**"
        status = "Not a Palindrome"
        st.warning(result_message)

    # Display cleaned string for transparency
    with st.expander("🔍 See the Cleaned String"):
        st.code(cleaned_text)

    # Update history log
    st.session_state['history'].insert(0, (user_input, status))
    # Keep the history length manageable (e.g., last 10 checks)
    st.session_state['history'] = st.session_state['history'][:10]

# Function to clear the history log
def clear_history():
    st.session_state['history'] = []

# --- 2. MAIN APP STRUCTURE (BODY) ---

st.title("Palindrome Checker 🔄")

# Use a key to access the text input's value in the callback
st.text_input("Enter a word or phrase to check:", key="input_key")

# The button triggers the check_and_update function
st.button("**Check Palindrome**", on_click=check_and_update)

# --- 3. SIDEBAR & ENHANCEMENTS ---

# Sidebar for explanation
st.sidebar.header("What is a Palindrome? 🤔")
st.sidebar.markdown(
    """
    A **palindrome** is a word, phrase, number, or other sequence of characters that reads the same forwards and backwards.
    
    Examples:
    * `Level`
    * `Madam`
    * `A man, a plan, a canal: Panama` (Ignores spaces and punctuation)
    """
)

st.sidebar.markdown("---")

# Sidebar for History Log
st.sidebar.header("Recent Checks")

if st.session_state['history']:
    # Display recent checks
    for text, status in st.session_state['history']:
        icon = "✅" if status == "Palindrome" else "❌"
        st.sidebar.markdown(f"{icon} **'{text}'** (*{status}*)")
    
    # Clear history button
    st.sidebar.button("Clear History", on_click=clear_history)
else:
    st.sidebar.info("No checks recorded yet.")
