from openai import OpenAI
from rag_engine import RAGEngine
from soc_memory_engine import SOCMemoryEngine

class SOCAIAnalyst:

    def __init__(self, api_key):

        self.client = OpenAI(api_key=api_key)

        self.rag = RAGEngine()

        self.memory = SOCMemoryEngine()
    # --------------------------------
    # Format Logs for LLM Context
    # --------------------------------
    def format_logs(self, logs):

        formatted_logs = []

        for log in logs:

            entry = f"""
            Time: {log.timestamp}
            User: {log.user_id}
            Event: {log.event_type}
            IP: {log.ip_address}
            Resource: {log.resource_accessed}
            Risk: {log.risk_score}
            """

            formatted_logs.append(entry)

        return "\n".join(formatted_logs)

    # --------------------------------
    # Build SOC Investigation Prompt
    # --------------------------------
    def build_prompt(self, query, context):

        prompt = f"""
        You are a professional SOC analyst.

        The following security events were retrieved from system logs.

        Logs:
        {context}

        Analyst Question:
        {query}

        Tasks:
        1. Identify suspicious activity.
        2. Detect possible attack patterns.
        3. Explain the timeline of events.
        4. Assign a security risk level.
        5. Recommend investigation steps.

        Respond like a cybersecurity analyst.
        """

        return prompt

    # --------------------------------
    # Run AI Investigation
    # --------------------------------
    def investigate(self, query):

        # Retrieve relevant logs
        logs = self.rag.search(query)

        context = self.format_logs(logs)

        prompt = self.build_prompt(query, context)

        response = self.client.chat.completions.create(

            model="gpt-4o-mini",

            messages=[
                {"role": "system", "content": "You are an expert SOC analyst."},
                {"role": "user", "content": prompt}
            ],

            temperature=0.2
        )

        answer = response.choices[0].message.content

        return {
            "query": query,
            "analysis": answer,
            "logs_used": len(logs)
        }