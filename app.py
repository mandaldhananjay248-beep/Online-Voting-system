import streamlit as st
import auth
import voting
import leaderboard
import json

# Page configuration
st.set_page_config(
    page_title="Online Voting System",
    page_icon="🗳️",
    layout="wide"
)

# Initialize systems
auth_system = auth.AuthSystem()
voting_system = voting.VotingSystem()
leaderboard_system = leaderboard.Leaderboard()

def main():
    st.title("🗳️ Online Voting System")
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    
    if not st.session_state.logged_in:
        show_login_register()
    else:
        show_voting_interface()

def show_login_register():
    st.sidebar.subheader("Authentication")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login to Vote")
        login_username = st.text_input("Username", key="login_user")
        login_password = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Login"):
            if login_username and login_password:
                success, message = auth_system.login_user(login_username, login_password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.username = login_username
                    st.success(f"Welcome {login_username}!")
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Please fill all fields")
    
    with tab2:
        st.subheader("Register New Account")
        reg_username = st.text_input("Username", key="reg_user")
        reg_password = st.text_input("Password", type="password", key="reg_pass")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_pass")
        
        if st.button("Register"):
            if reg_username and reg_password and confirm_password:
                if reg_password == confirm_password:
                    success, message = auth_system.register_user(reg_username, reg_password)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                else:
                    st.error("Passwords don't match")
            else:
                st.error("Please fill all fields")

def show_voting_interface():
    st.sidebar.subheader(f"Welcome, {st.session_state.username}!")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()
    
    # Check if user has already voted
    if auth_system.has_voted(st.session_state.username):
        show_results()
    else:
        show_voting_booth()

def show_voting_booth():
    st.header("Cast Your Vote")
    st.info("Please select your preferred candidate. You can only vote once!")
    
    candidates = voting_system.get_candidates()
    
    selected_candidate = st.radio(
        "Select Candidate:",
        options=list(candidates.keys()),
        format_func=lambda x: f"{x} - {candidates[x]}"
    )
    
    if st.button("Submit Vote"):
        if voting_system.validate_candidate(selected_candidate):
            # Record vote
            leaderboard_system.add_vote(selected_candidate)
            # Mark user as voted
            auth_system.mark_voted(st.session_state.username)
            st.success(f"Thank you for voting for {selected_candidate}!")
            st.balloons()
            st.rerun()
        else:
            st.error("Invalid candidate selected")

def show_results():
    st.header("Voting Results")
    
    # Show leaderboard
    st.subheader("🏆 Current Leaderboard")
    top_candidates = leaderboard_system.get_leaderboard()
    
    for i, (candidate, votes) in enumerate(top_candidates, 1):
        emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "📊"
        st.write(f"{emoji} **{i}. {candidate}**: {votes} votes")
    
    # Show detailed results
    st.subheader("Detailed Results")
    col1, col2, col3 = st.columns(3)
    
    all_candidates = list(voting_system.get_candidates().keys())
    for i, candidate in enumerate(all_candidates):
        with [col1, col2, col3][i % 3]:
            votes = leaderboard_system.get_candidate_votes(candidate)
            st.metric(
                label=candidate,
                value=f"{votes} votes",
                delta=None
            )
    
    # Show vote distribution chart
    st.subheader("Vote Distribution")
    chart_data = {
        "Candidate": all_candidates,
        "Votes": [leaderboard_system.get_candidate_votes(c) for c in all_candidates]
    }
    st.bar_chart(chart_data, x="Candidate", y="Votes")

if __name__ == "__main__":
    main()