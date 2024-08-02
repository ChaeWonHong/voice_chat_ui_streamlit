# Streamlit 패키지 추가
# pip install streamlit
# streamlit 실행 : streamlit run app.py

import streamlit as st

def main():
    # 페이지 타이틀 설정
    st.set_page_config(page_title="음성챗봇", layout="wide")

    st.header("음성 챗봇 프로그램")

    # 구분선 
    st.markdown("---")

    # 기본 설명
    with st.expander("음성 챗봇 프로그램에 관하여", expanded=True):
        st.write(
        """
        - 음성 번역 챗봇 프로그램의 UI는 스트림릿을 활용합니다.
        - STT(Speech-To-Text)는 OpenAI의 Whisper를 활용합니다. 
        - 답변은 OpenAI의 GPT 모델을 활용합니다. 
        - TTS(Text-To-Speech)는 OpenAI의 TTS를 활용합니다.
        """
        )
    st.markdown("")

# main() 함수 실행
if __name__ == "__main__":
    # __name__: 파이썬 내장 변수 -> 정해져있는 문법
    main()