"""
CodeAlpha Internship — Task 4: Basic Chatbot
============================================
A rule-based chatbot that responds to common user inputs.
Key Concepts: if-elif, functions, loops, input/output.
"""

import random
import re
from datetime import datetime

# ─────────────────────────────────────────────────────────
#  Response rules: each entry is (list_of_patterns, list_of_replies)
#  The chatbot picks a random reply from the matched list.
# ─────────────────────────────────────────────────────────
RULES = [
    # ── Greetings
    (
        [r"\bhello\b", r"\bhi\b", r"\bhey\b", r"\bgreetings\b", r"\bwhat'?s up\b"],
        ["Hi there! 😊", "Hello! How can I help you?", "Hey! What's on your mind?"]
    ),
    # ── How are you
    (
        [r"how are you", r"how('re| are) you doing", r"are you (ok|okay|good|fine)"],
        ["I'm doing great, thanks for asking! 😄", "All good here! How about you?",
         "Running smoothly! How can I assist you?"]
    ),
    # ── User is fine / good
    (
        [r"\bi('?m| am) (fine|good|great|okay|ok|well|doing well)\b"],
        ["Glad to hear that! 😊", "That's wonderful!", "Great! Is there anything I can help you with?"]
    ),
    # ── Name query
    (
        [r"what('?s| is) your name", r"who are you", r"tell me about yourself"],
        ["I'm CodeBot, your friendly assistant! 🤖",
         "My name is CodeBot — built for CodeAlpha's Python internship!"]
    ),
    # ── Creator / maker
    (
        [r"who (made|created|built|developed) you", r"who('?s| is) your (creator|developer|maker)"],
        ["I was built by a CodeAlpha intern as part of Task 4! 🛠️"]
    ),
    # ── Time / date
    (
        [r"\btime\b", r"what time is it"],
        [f"The current time is {datetime.now().strftime('%I:%M %p')}."]
    ),
    (
        [r"\bdate\b", r"what('?s| is) (today'?s? date|the date)"],
        [f"Today is {datetime.now().strftime('%A, %B %d, %Y')}."]
    ),
    # ── Jokes
    (
        [r"\bjoke\b", r"tell me a joke", r"make me (laugh|smile)"],
        [
            "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
            "Why did the Python programmer break up with Java? Too much class! 😂",
            "I told my computer I needed a break... now it won't stop sending me vacation ads! 😅"
        ]
    ),
    # ── Help
    (
        [r"\bhelp\b", r"what can you do", r"what do you (know|support)"],
        [
            "I can chat with you! Try asking me:\n"
            "  • 'hello' / 'hi'\n"
            "  • 'how are you'\n"
            "  • 'what's the time / date'\n"
            "  • 'tell me a joke'\n"
            "  • 'bye' to exit"
        ]
    ),
    # ── Thanks
    (
        [r"\bthank(s| you)\b", r"\bthx\b", r"\bthanks a lot\b"],
        ["You're welcome! 😊", "Happy to help!", "Anytime! 🙌"]
    ),
    # ── Goodbye
    (
        [r"\bbye\b", r"\bgoodbye\b", r"\bsee you\b", r"\btake care\b", r"\bexit\b", r"\bquit\b"],
        ["Goodbye! Have a great day! 👋", "See you later! 😊", "Take care! Bye! 👋"]
    ),
]

# Words that trigger the exit condition
EXIT_WORDS = {"bye", "goodbye", "exit", "quit", "see you", "take care"}

# ─────────────────────────────────────────────────────────
#  Core: match input to a rule and return a reply
# ─────────────────────────────────────────────────────────
def get_response(user_input: str) -> tuple[str, bool]:
    """
    Returns (reply_text, should_exit).
    should_exit is True when the user says goodbye.
    """
    text  = user_input.strip().lower()
    flags = re.IGNORECASE

    for patterns, replies in RULES:
        for pattern in patterns:
            if re.search(pattern, text, flags):
                reply      = random.choice(replies)
                should_exit = any(word in text for word in EXIT_WORDS)
                return reply, should_exit

    # Default fallback
    fallbacks = [
        "Hmm, I'm not sure about that. 🤔 Type 'help' to see what I can do!",
        "I didn't quite catch that. Could you rephrase?",
        "Interesting! Tell me more, or type 'help' for options.",
    ]
    return random.choice(fallbacks), False

# ─────────────────────────────────────────────────────────
#  Main chat loop
# ─────────────────────────────────────────────────────────
def main():
    print("\n" + "=" * 50)
    print("   🤖  CODEBOT  —  CodeAlpha Task 4")
    print("=" * 50)
    print("  Hi! I'm CodeBot. Type 'help' to see what I can do.")
    print("  Type 'bye' to exit.\n")

    while True:
        try:
            user_input = input("  You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  CodeBot: Goodbye! 👋\n")
            break

        if not user_input:
            print("  CodeBot: (waiting for your message...)\n")
            continue

        reply, should_exit = get_response(user_input)
        print(f"  CodeBot: {reply}\n")

        if should_exit:
            break


if __name__ == "__main__":
    main()
