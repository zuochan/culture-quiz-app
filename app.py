import streamlit as st
import json
import random

# Load gesture quiz data
with open("data/gestures.json", "r", encoding="utf-8") as f:
    gestures = json.load(f)

st.set_page_config(page_title="Gesture Culture Quiz")
st.title("🧠 Gesture Culture Quiz")
st.write("Can you guess which culture the following gesture is most associated with?")

# Initialize session state
if "used_questions" not in st.session_state:
    st.session_state.used_questions = set()
if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = None
if "answered" not in st.session_state:
    st.session_state.answered = False
if "score" not in st.session_state:
    st.session_state.score = 0
if "total_questions" not in st.session_state:
    st.session_state.total_questions = 0

# Get next question index that hasn't been used
def get_next_question_index():
    remaining_indices = list(set(range(len(gestures))) - st.session_state.used_questions)
    if not remaining_indices:
        return None
    return random.choice(remaining_indices)

# 初回 or Next Question 時に新しいインデックスを設定
if st.session_state.current_question_index is None:
    new_index = get_next_question_index()
    if new_index is not None:
        st.session_state.current_question_index = new_index
        st.session_state.used_questions.add(new_index)

# クイズがすべて出題済みかチェック
if st.session_state.current_question_index is None:
    st.success("🎉 You've completed all the questions!")
    st.markdown(f"**Final Score: {st.session_state.score} / {st.session_state.total_questions}**")
    if st.button("Restart Quiz"):
        st.session_state.used_questions = set()
        st.session_state.current_question_index = None
        st.session_state.answered = False
        st.session_state.score = 0
        st.session_state.total_questions = 0
        st.rerun()
    st.stop()

# 現在の問題を取得
question = gestures[st.session_state.current_question_index]

# 問題表示
st.markdown(f"### Gesture: {question['gesture']}")
st.markdown(f"**{question['question']}**")

option = st.radio("Your answer:", question["options"], key=st.session_state.current_question_index)

# 回答
if st.button("Submit Answer"):
    if not st.session_state.answered:
        st.session_state.answered = True
        st.session_state.total_questions += 1
        if option == question["answer"]:
            st.success("✅ Correct!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Incorrect. The correct answer is: {question['answer']}")
        st.info(f"📝 Explanation: {question['explanation']}")

# 次の問題へ
if st.session_state.answered:
    if st.button("Next Question"):
        new_index = get_next_question_index()
        if new_index is not None:
            st.session_state.current_question_index = new_index
            st.session_state.used_questions.add(new_index)
            st.session_state.answered = False
            st.rerun()
        else:
            st.session_state.current_question_index = None
            st.rerun()

# スコア表示
st.markdown("---")
st.markdown(f"**Score: {st.session_state.score} / {st.session_state.total_questions}**")