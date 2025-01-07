import tkinter as tk
from tkinter import PhotoImage

def main():
    # Tkinter 윈도우 생성
    window = tk.Tk()
    window.title("이미지와 텍스트 예제")

    # 이미지 로드
    img1 = PhotoImage(file='entrance.png')

    # Label에 이미지와 텍스트 추가
    label_with_image_and_text = tk.Label(window, compound="top", image=img1, text='1. 프로그램 우측 하단에 총 주차량과 현재 주차량을 입력한다.\n2. 입구 출구 구역설정을 실행한다.')
    label_with_image_and_text.pack(pady=10)  # 여백 추가

    # Tkinter 윈도우 실행
    window.mainloop()

if __name__ == "__main__":
    main()