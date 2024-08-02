import os
import streamlit as st                      # Streamlit 패키지 추가
import openai                               # OpenAI 패키지 추가
from dotenv import load_dotenv
from audiorecorder import audiorecorder     # audiorecorder 패키지 추가 :  Streamlit 애플리케이션에서 오디오를 녹음할 수 있는 컴포넌트를 제공
from datetime import datetime               # 시간정보 패키지 추가

# .env 파일 경로 지정
load_dotenv()

# Open AI의 API 키 설정
api_key = os.environ.get('OPEN_API_KEY')
client = openai.OpenAI(api_key=api_key)

##### 기능 구현 함수 #####
def STT(speech):
    # 파일 저장
    filename = 'input.mp3'
    speech.export(filename, format = "mp3")

    # 음원 파일 열기
    with open(filename, "rb") as audio_file:
        # Whisper 모델을 활용해 텍스트 얻기
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

    # 파일 삭제
    os.remove(filename)

    return transcription.text

# ask_gpt 함수 정의
def ask_gpt(prompt, model):
     response = client.chat.completions.create(
          model=model,
          messages=prompt
     )
     return response.choices[0].message.content

##### 메인함수 #####
def main():
    # 기본 설정
    st.set_page_config(
        page_title="음성 챗봇 프로그램",
        layout="wide")

    # 제목 
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
    
    system_content = "You are a thoungtful assistant. Respond to all input in 25 words and answer in Korea"

    # session state 초기화
    if "chat" not in st.session_state:
        st.session_state["chat"] = []

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role":"system", "content":system_content}]

    if "check_rest" not in st.session_state:
        st.session_state["check_reset"] = False

    # 사이드바 생성
    with st.sidebar:

        # GPT 모델을 선택하기 위한 라디오 버튼
        model = st.radio(label="GPT모델", options=["gpt-3.5-turbo", "gpt-4o", "gpt-4-turbo"])
        st.markdown("---")

        # 리셋 버튼 생성
        if st.button(label="초기화"):
            # 리셋 코드
            st.session_state["chat"]=[]
            st.session_state["messages"]=[{"role":"system", "content": system_content}]
            st.session_state["check_reset"]=True
            

    # 기능 구현 공간
    col1, col2 = st.columns(2)
    with col1:
        # 왼쪽 영역 작성
        st.subheader("질문하기")
        # 음성 녹음 아이콘 추가
        audio = audiorecorder()
        if (audio.duration_seconds > 0) and (st.session_state["check_reset"]==False):
            # 음성 재생
            st.audio(audio.export().read())

            # 음원 파일에서 텍스트 추출
            question = STT(audio)

            # 채팅을 시각화하기 위한 질문 내용 저장
            now = datetime.now().strftime("%H:%M")
            st.session_state["chat"] = st.session_state["messages"] + [{"role":"user", "content": question}]

            # GPT 모델에 넣을 프롬프트를 위한 질문 내용 저장
            st.session_state["messages"] = st.session_state["messages"] + [{"role":"user", "content":question}]


    with col2:

        # 오른쪽 영역 작성
        st.subheader("질문/답변")

        if (audio.duration_seconds > 0) and (st.session_state["check_reset"]==False):
                    # GPT에게 답변 얻기
                    response = ask_gpt(st.session_state["messages"], model)

                    # GPT 모델에 넣을 프롬프트를 위한 질문 내용 저장
                    st.session_state["messages"] = st.session_state["messages"] + [{"role":"user", "content":question}]

                    # 채팅 시각화를 위한 답변 내용 저장
                    now = datetime.now().strftime("%H:%M")
                    st.session_state["chat"] = st.session_state["chat"] + [("bot", now, response)]



# main() 함수 실행
if __name__ == "__main__":
    # __name__: 파이썬 내장 변수 -> 정해져있는 문법
    main()