class ConversationMemory:
    def __init__(self, system_prompt: str, max_turns: int = 10):
        """
        system_prompt : tells the AI how to behave
        max_turns     : how many past messages to remember
        """
        self.system_prompt = system_prompt
        self.max_turns = max_turns
        self.history = []  # stores (user_message, assistant_message) pairs

    def add_turn(self, user_msg: str, assistant_msg: str):
        """Save one round of conversation."""
        self.history.append((user_msg, assistant_msg))

        # If history gets too long, drop the oldest messages
        # This prevents the model from running out of memory
        if len(self.history) > self.max_turns:
            self.history = self.history[-self.max_turns:]

    def build_messages(self, current_user_msg: str) -> list:
        """
        Build the full message list the model needs.
        Format: system prompt + all past turns + current message
        """
        messages = [{"role": "system", "content": self.system_prompt}]

        for user, assistant in self.history:
            messages.append({"role": "user",      "content": user})
            messages.append({"role": "assistant", "content": assistant})

        # Add the new message at the end
        messages.append({"role": "user", "content": current_user_msg})

        return messages

    def clear(self):
        """Reset conversation — used when user clicks Clear Chat."""
        self.history = []