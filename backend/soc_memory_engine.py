class SOCMemoryEngine:

    def __init__(self):
        self.sessions = {}

    # --------------------------------
    # Create investigation session
    # --------------------------------
    def start_session(self, session_id):

        self.sessions[session_id] = []

    # --------------------------------
    # Add message to session
    # --------------------------------
    def add_message(self, session_id, role, message):

        if session_id not in self.sessions:
            self.start_session(session_id)

        self.sessions[session_id].append({
            "role": role,
            "content": message
        })

    # --------------------------------
    # Get conversation history
    # --------------------------------
    def get_history(self, session_id):

        return self.sessions.get(session_id, [])

    # --------------------------------
    # Clear session
    # --------------------------------
    def clear_session(self, session_id):

        if session_id in self.sessions:
            del self.sessions[session_id]