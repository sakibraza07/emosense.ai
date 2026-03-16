feedback_map = {
    "neutral": "You sound calm and composed. That's a great state to be in for focused work or clear communication.",
    "calm": "You seem very relaxed. Use this energy to tackle something meaningful today.",
    "happy": "You sound genuinely happy! That positive energy is contagious — keep it up.",
    "sad": "It sounds like you might be feeling a bit low. That's okay. Take it one step at a time, and be kind to yourself.",
    "angry": "It seems like something is bothering you. Try taking a few deep breaths to reset before responding.",
    "fearful": "You sound a little anxious. Remember that most fears shrink when faced directly. You've got this.",
    "disgust": "Something seems to be unsettling you. Try stepping away briefly and coming back with fresh eyes.",
    "surprised": "You sound surprised! Whether it's good or unexpected news, take a moment to process before reacting."
}

def generate_feedback(emotion):
    return feedback_map.get(emotion, "Emotion detected. Stay mindful of how you're feeling.")
