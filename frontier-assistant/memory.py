class ConversationMemory:
    def __init__(self, system_prompt: str, max_turns: int = 10):
        self.system_prompt = system_prompt
        self.max_turns = max_turns
        self.history = []

    def add_turn(self, user_msg: str, assistant_msg: str):
        self.history.append((user_msg, assistant_msg))
        if len(self.history) > self.max_turns:
            self.history = self.history[-self.max_turns:]

    def build_messages(self, current_user_msg: str) -> list:
        messages = [{"role": "system", "content": self.system_prompt}]
        for user, assistant in self.history:
            messages.append({"role": "user",      "content": user})
            messages.append({"role": "assistant", "content": assistant})
        messages.append({"role": "user", "content": current_user_msg})
        return messages

    def clear(self):
        self.history = []