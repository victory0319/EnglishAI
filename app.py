import streamlit as st
import google.generativeai as genai
import pandas as pd
import json

# 1. 설정
genai.configure(api_key="AQ.Ab8RN6I-Q_K58fRfku1Sl-MjwmzoLVtF6IkfpKeJY4zIpWqsPA")

# 2. 분석 프롬프트
ANALYSIS_PROMPT = """
당신은 영어독해와작문 전문 튜터입니다. 사용자의 영어 답변을 분석하여 아래 JSON 포맷으로만 응답하세요.
다른 말은 절대 하지 말고 오직 JSON만 출력하세요.

{
  "grammar_score": 0,
  "vocab_score": 0,
  "logic_score": 0,
  "feedback": "피드백 내용",
  "recommended_focus": "문법/어휘/논리 중 하나"
}
"""

st.title("English AI Tutor 🎓")

# 3. 사용자 입력
user_input = st.text_area("영어 문장을 입력하세요:", height=150)

if st.button("분석 시작"):
    if user_input:
        try:
            model_name = 'gemini-3.5-flash'
model = genai.GenerativeModel(model_name)
            response = model.generate_content(f"{ANALYSIS_PROMPT} \n 사용자 답변: {user_input}")
            
            # JSON 정제 로직
            clean_text = response.text.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_text)
            
            # 결과 표시
            st.subheader("분석 결과")
            col1, col2, col3 = st.columns(3)
            col1.metric("문법", data['grammar_score'])
            col2.metric("어휘", data['vocab_score'])
            col3.metric("논리", data['logic_score'])
            
            st.info(f"💡 피드백: {data['feedback']}")
            st.warning(f"🎯 추천 학습 포인트: {data['recommended_focus']}")
            
        except Exception as e:
            st.error(f"분석 중 오류가 발생했습니다: {e}")
    else:
        st.warning("분석할 문장을 입력해 주세요.")
