import json
import tkinter
import pyautogui
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk, ImageDraw, ImageGrab
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
import re
from tkinter import PhotoImage

class CaptureWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("메뉴 선택")
        self.root.geometry("500x200")

        self.brif_Istrue = False

        # 버튼 관리
        self.Guide_button = tk.Button(root, text='사용자 가이드', command=self.On_Guide)
        self.Guide_button.config(bg='black', fg='white',width=20, height=1, font=("Arial", 12, "bold"))
        self.Guide_button.pack(pady=20)

        self.Go_To_Manage = tk.Button(root, text='프로그램 시작', command=self.Manage_Progam)
        self.Go_To_Manage.config(bg='black', fg='white', width=20, height=1, font=("Arial", 12, "bold"))
        self.Go_To_Manage.pack(pady=10)

        self.image_selector_windows = []

        # ImageCaptureAndCompare 인스턴스 저장
        self.image_capture_compare = None


    def Manage_Progam(self):
        self.Manage_Window = tk.Toplevel()
        self.Manage_Window.geometry("750x450")
        self.Manage_Window.title("메인 프로그램")

        self.section_button = tk.Button(self.Manage_Window, text='감시구역 구역설정', command=self.Get_Capture)
        self.section_button.configure(bg='black', fg='white', width=20, height=1, font=("Arial", 12, "bold"))
        self.section_button.pack(pady=10)

        self.monitoring_button = tk.Button(self.Manage_Window, text='모니터링 시작', command=self.start_monitoring)
        self.monitoring_button.configure(bg='black', fg='white', width=20, height=1, font=("Arial", 12, "bold"))
        self.monitoring_button.pack(pady=10)

        self.stop_monitoring_button = tk.Button(self.Manage_Window, text='모니터링 종료', command=self.stop_monitoring)
        self.stop_monitoring_button.configure(bg='black', fg='white', width=20, height=1, font=("Arial", 12, "bold"))
        self.stop_monitoring_button.pack(pady=10)

        self.coor_reset_button = tk.Button(self.Manage_Window, text='지정구역 초기화', command=self.reset_coordinates)
        self.coor_reset_button.configure(bg='black', fg='white', width=20, height=1, font=("Arial", 12, "bold"))
        self.coor_reset_button.pack(pady=10)

        # 차량번호 초기화 창이다. 지속적인 차량번호 초기화가 필요 할 때 사용하세요

        # self.park_reset_button = tk.Button(self.Manage_Window, text='차량번호 초기화', command=self.reset_prarking_list)
        # self.park_reset_button.configure(bg='black', fg='white', width=20, height=1, font=("Arial", 12, "bold"))
        # self.park_reset_button.pack(pady=10)

        # 최대 주차량
        self.Max_Parking_Space = tk.StringVar()
        self.load_Max_Park()
        self.Max_Parking_Space.trace_add("write", self.Save_Max_Park)
        self.M_Park_Space()

        # 현재 주차량
        self.Now_Park = tk.StringVar()
        self.load_Now_Park()
        self.Now_Park.trace_add("write", self.Save_Now_Park)
        self.N_Park_Space()

        # 캡처 화면 좌표 저장
        self.Capture_Window_left = 0
        self.Capture_Window_top = 0
        self.Capture_Window_width = 0
        self.Capture_Window_height = 0

    def Get_Capture(self):
        self.Capture_Window = tk.Toplevel()
        self.Capture_Window.title("캡처 윈도우")
        self.Capture_Window.geometry("1000x1000")

        self.Capture_Button = tk.Button(self.Capture_Window, text='화면 캡처', command=self.show_image_selector)
        self.Capture_Button.config(bg='black', fg='white', width=20, height=1, font=("Arial", 12, "bold"))
        self.Capture_Button.pack(anchor="center", pady=20)

        # 투명도를 조절하는 드래그바
        self.create_transparency_slider()

    def On_Guide(self):
        self.Guide_window = tk.Toplevel()
        self.Guide_window.geometry("1000x1000")
        self.Guide_window.title("사용자 가이드")
        self.Guide_window.configure(bg='black')

        self.notebook = ttk.Notebook(self.Guide_window, width=1000, height=950)
        self.notebook.pack(pady=0)

        #1
        frame1 = tkinter.Frame(self.Guide_window)
        self.notebook.add(frame1, text='감시구역 설정 1')

        self.img1 = PhotoImage(file='캡처예시1.png')
        Photo1 = tkinter.Label(frame1, image=self.img1)
        Photo1.pack()

        How_Use_1 = tkinter.Label(frame1, text='1. 감시구역 설정 버튼을 누르면 화면 캡쳐 윈도우가 나타난다.'
                                             '\n\n2. 설정하고 싶은 구역에 윈도우를 올려 놓고 화면 캡처 버튼을 누른다'
                                '\n(윈도우창 좌측 하단 부분의 투명도 설정을 이용하여 화면을 조정할 수 있다.)')
        How_Use_1.pack()

        #2
        frame2 = tkinter.Frame(self.Guide_window)
        self.notebook.add(frame2, text='감시구역 설정 2')

        self.img2 = PhotoImage(file='캡처예시2.png')
        Photo2 = tkinter.Label(frame2, image=self.img2)
        Photo2.pack()

        How_Use_2 = tkinter.Label(frame2, text='1. 마우스로 캡처 된 화면을 드래그 하여 입구와 출구를 선택한다.\n'
                                               '(첫번째 드래그는 입구, 두번째 드래그는 출구를 나타낸다.)'
                                  '\n\n2. 입구와 출구가 지정 됐다면, 모니터링 시작 버튼을 누른다.')
        How_Use_2.pack()

        #3
        frame3 = tkinter.Frame(self.Guide_window)
        self.notebook.add(frame3, text='모니터링 시작, 종료')

        self.img3 = PhotoImage(file='캡처예시3.png')
        Photo3 = tkinter.Label(frame3, image=self.img3)
        Photo3.pack()

        How_Use_3 = tkinter.Label(frame3, text='1. 모니터링 시작 버튼을 누르면 지정된 구역의 좌표와 현재 주차장 현황이 간략하게 나타난다.'
                                  '\n\n2. 모니터링 종료 버튼을 누르면 모니터링 창이 종료된다.')
        How_Use_3.pack()

        #4
        frame4 = tkinter.Frame(self.Guide_window)
        self.notebook.add(frame4, text='지정구역 초기화')

        self.img4 = PhotoImage(file='캡처예시4.png')
        Photo4 = tkinter.Label(frame4, image=self.img4)
        Photo4.pack()

        How_Use_4 = tkinter.Label(frame4, text='1. 만일 지정구역을 잘못 설정하였거나, 변경하고 싶다면 지정구역 초기화 버튼을 누른다.\n'
                                               '\n2. 그 후 다시 감시구역 설정 버튼을 통해 재설정한다.')
        How_Use_4.pack()

        #5
        frame5 = tkinter.Frame(self.Guide_window)
        self.notebook.add(frame5, text='현재, 수용가능 차량')

        self.img5 = PhotoImage(file='캡처예시5.png')
        Photo5 = tkinter.Label(frame5, image=self.img5)
        Photo5.pack()

        How_Use_5 = tkinter.Label(frame5, text='1.현재 주차량에는 현재 주차장에 주차돼있는 추정 주차량을 입력한다.'
                                  '\n\n2.수용가능 차량에는 주차장이 수용할 수 있는 총 수용량을 입력한다.')
        How_Use_5.pack(pady=50)

        #6
        frame6 = tkinter.Frame(self.Guide_window)
        self.notebook.add(frame6, text='설명 끝')
        How_Use_6 = tkinter.Label(frame6, text='사용자 가이드는 끝났습니다. 이제 메뉴 선택창에 있는 \n 프로그램 시작 버튼을 눌러 프로그램을 실행하세요.')
        How_Use_6.config(anchor="center", justify="center", bg="black", fg="white", font=("Arial", 12, "bold"))
        How_Use_6.pack()



        # next,pre button
        next_button = tk.Button(self.Guide_window, text="<--", command=self.show_previous_tab)
        next_button.place(x=20, y=940)

        previous_button = tk.Button(self.Guide_window, text="-->", command=self.show_next_tab)
        previous_button.place(x=930, y=940)

    def show_next_tab(self):
        current_index = self.notebook.index(self.notebook.select())
        next_index = (current_index + 1) % self.notebook.index("end")
        self.notebook.select(next_index)

    def show_previous_tab(self):
        current_index = self.notebook.index(self.notebook.select())
        previous_index = (current_index - 1) % self.notebook.index("end")
        self.notebook.select(previous_index)

    def M_Park_Space(self):
        label = tk.Label(self.Manage_Window, text='수용가능 차량')
        entry = tk.Entry(self.Manage_Window, textvariable=self.Max_Parking_Space)

        entry.pack(side=tk.RIGHT, anchor=tk.SE)
        label.pack(side=tk.RIGHT, anchor=tk.SE)

    def load_Max_Park(self):
        try:
            # JSON 파일에서 에러 범위 읽어오기
            with open('Max_Park.json', 'r') as json_file:
                data = json.load(json_file)
                if 'Max_Park' in data:
                    self.Max_Parking_Space.set(data['Max_Park'])
        except FileNotFoundError:
            print('최대 주차 가능 파일이 존재하지 않습니다.')

    def Save_Max_Park(self, *args):
        data = {"Max_Park": self.Max_Parking_Space.get()}
        with open('Max_Park.json', 'w') as json_file:
            json.dump(data, json_file, indent=2)

    def N_Park_Space(self):
        label = tk.Label(self.Manage_Window, text='현재 주차량')
        entry = tk.Entry(self.Manage_Window, textvariable=self.Now_Park)

        entry.pack(side=tk.RIGHT, anchor=tk.SE)
        label.pack(side=tk.RIGHT, anchor=tk.SE)

    def load_Now_Park(self):
        try:
            # JSON 파일에서 에러 범위 읽어오기
            with open('Now_Park.json', 'r') as json_file:
                data = json.load(json_file)
                if 'Now_Park' in data:
                    self.Now_Park.set(data['Now_Park'])
        except FileNotFoundError:
            print('현재 주차 정보 파일이 존재하지 않습니다.')

    def Save_Now_Park(self, *args):
        data = {"Now_Park": self.Now_Park.get()}
        with open('Now_Park.json', 'w') as json_file:
            json.dump(data, json_file, indent=2)

    def on_slider_change(self, value):
        self.Capture_Window.attributes("-alpha", float(value))

    def reset_coordinates(self):
        # 좌표 초기화
        coordinate_list = []
        with open('coordinate_list.json', 'w') as json_file:
            json.dump(coordinate_list, json_file, indent=2)

    def reset_prarking_list(self):
        # 좌표 초기화
        parking_list = []
        with open('parking_list.json', 'w') as json_file:
            json.dump(parking_list, json_file, indent=2)

    def create_transparency_slider(self):
        # Drag bar 생성
        transparency_label = tk.Label(self.Capture_Window, text='투명도 : ')
        transparency_label.pack(side=tk.LEFT, anchor=tk.SE)

        transparency_slider = tk.Scale(self.Capture_Window, from_=0.2, to=1.0, orient=tk.HORIZONTAL, command=self.on_slider_change, resolution=0.01)
        transparency_slider.pack(side=tk.LEFT, anchor=tk.SE)

        # 초기 투명도 설정
        transparency_slider.set(1.0)

    def capture_1(self):
        # 현재 창의 위치와 크기 정보 가져오기
        window_title = "캡처 윈도우"
        window = pyautogui.getWindowsWithTitle(window_title)

        if window:
            window_left = window[0].left
            window_top = window[0].top
            window_width = window[0].width
            window_height = window[0].height

            # 화면 캡쳐
            screenshot = ImageGrab.grab(
                bbox=(window_left, window_top, window_left + window_width, window_top + window_height))

            # 캡쳐 이미지 저장
            screenshot.save("captured_window.png")
            print("윈도우 창을 성공적으로 캡쳐했습니다.")
        else:
            print(f"윈도우 타이틀 '{window_title}'을 찾을 수 없습니다.")

    def show_image_selector(self):
        self.Capture_Window_left = self.Capture_Window.winfo_x()
        self.Capture_Window_top = self.Capture_Window.winfo_y()
        self.Capture_Window_width = self.Capture_Window.winfo_width()
        self.Capture_Window_height = self.Capture_Window.winfo_height()

        self.brif_window = tk.Toplevel()
        self.brif_Istrue = True
        self.brif_window.title("brif_window")
        self.brif_window.geometry("300x100")

        self.brif_ = tk.Label(self.brif_window, text="첫번째 구역 : 입구\n두번째 구역 : 출구")
        self.brif_.pack(pady=10)

        root_coordinates = {
            'left': self.Capture_Window_left,
            'top': self.Capture_Window_top,
            'width': self.Capture_Window_width,
            'height': self.Capture_Window_height
        }
        with open('root_coordinates.json', 'w') as json_file:
            json.dump(root_coordinates, json_file, indent=2)

        # 투명도를 0으로 설정
        self.Capture_Window.attributes("-alpha", 0.0)

        # 이미지 선택기 창 열기
        Image_Selector_Window = ImageSelectorWindow(self.Capture_Window)
        self.image_selector_windows.append(Image_Selector_Window)

        self.reset_transparency()

    def reset_transparency(self):
        # 투명도 기존 값으로 변경
        self.Capture_Window.attributes("-alpha", 1.0)

    def start_monitoring(self):
        # 이미지 캡처 및 비교기 인스턴스 생성 및 저장
        self.image_capture_compare = ImageCaptureAndCompare(self.Capture_Window, 'coordinate_list.json')
        if self.brif_Istrue is True:
            self.brif_window.destroy()

        # 섹션 윈도우 닫기
        self.close_section_windows()

    def close_section_windows(self):
        # section_button에서 지정된 윈도우 창 닫기
        for window_instance in self.image_selector_windows:
            window_instance.destroy()

    def stop_monitoring(self):
        # 이미지 캡처 및 비교기 인스턴스 종료
        if self.image_capture_compare:
            self.image_capture_compare.stop_monitoring()


class LicensePlateExtractor:
    def __init__(self, image_path):
        plt.style.use('dark_background')
        self.num_list = []
        self.image_path = image_path
        self.possible_contours = []
        self.matched_result = []
        self.plate_imgs = []
        self.plate_infos = []

    def preprocess_image(self):
        img = cv2.imread(self.image_path)
        height, width, channel = img.shape
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        structuringElement = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        imgTopHat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, structuringElement)
        imgBlackHat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, structuringElement)

        imgGrayscalePlusTopHat = cv2.add(gray, imgTopHat)
        gray = cv2.subtract(imgGrayscalePlusTopHat, imgBlackHat)
        img_blurred = cv2.GaussianBlur(gray, ksize=(5, 5), sigmaX=0)

        img_thresh = cv2.adaptiveThreshold(
            img_blurred,
            maxValue=255.0,
            adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            thresholdType=cv2.THRESH_BINARY_INV,
            blockSize=19,
            C=9
        )

        contours, _ = cv2.findContours(img_thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)
        temp_result = np.zeros((height, width, channel), dtype=np.uint8)
        cv2.drawContours(temp_result, contours=contours, contourIdx=-1, color=(255, 255, 255))
        temp_result = np.zeros((height, width, channel), dtype=np.uint8)

        contours_dict = []

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(temp_result, pt1=(x, y), pt2=(x + w, y + h), color=(255, 255, 255), thickness=2)

            contours_dict.append({
                'contour': contour,
                'x': x,
                'y': y,
                'w': w,
                'h': h,
                'cx': x + (w / 2),
                'cy': y + (h / 2)
            })

        MIN_AREA = 80
        MIN_WIDTH, MIN_HEIGHT = 2, 8
        MIN_RATIO, MAX_RATIO = 0.25, 1.0

        possible_contours = []

        cnt = 0
        for d in contours_dict:
            area = d['w'] * d['h']
            ratio = d['w'] / d['h']

            if area > MIN_AREA \
                    and d['w'] > MIN_WIDTH and d['h'] > MIN_HEIGHT \
                    and MIN_RATIO < ratio < MAX_RATIO:
                d['idx'] = cnt
                cnt += 1
                possible_contours.append(d)

        temp_result = np.zeros((height, width, channel), dtype=np.uint8)

        for d in possible_contours:
            cv2.rectangle(temp_result, pt1=(d['x'], d['y']), pt2=(d['x'] + d['w'], d['y'] + d['h']),
                          color=(255, 255, 255), thickness=2)

        MAX_DIAG_MULTIPLIER = 5
        MAX_ANGLE_DIFF = 12.0
        MAX_AREA_DIFF = 0.5
        MAX_WIDTH_DIFF = 0.8
        MAX_HEIGHT_DIFF = 0.2
        MIN_N_MATCHED = 3

        def find_chars(contour_list):
            matched_result_idx = []

            for d1 in contour_list:
                matched_contours_idx = []
                for d2 in contour_list:
                    if d1['idx'] == d2['idx']:
                        continue

                    dx = abs(d1['cx'] - d2['cx'])
                    dy = abs(d1['cy'] - d2['cy'])

                    diagonal_length1 = np.sqrt(d1['w'] ** 2 + d1['h'] ** 2)

                    distance = np.linalg.norm(np.array([d1['cx'], d1['cy']]) - np.array([d2['cx'], d2['cy']]))
                    if dx == 0:
                        angle_diff = 90
                    else:
                        angle_diff = np.degrees(np.arctan(dy / dx))
                    area_diff = abs(d1['w'] * d1['h'] - d2['w'] * d2['h']) / (d1['w'] * d1['h'])
                    width_diff = abs(d1['w'] - d2['w']) / d1['w']
                    height_diff = abs(d1['h'] - d2['h']) / d1['h']

                    if distance < diagonal_length1 * MAX_DIAG_MULTIPLIER \
                            and angle_diff < MAX_ANGLE_DIFF and area_diff < MAX_AREA_DIFF \
                            and width_diff < MAX_WIDTH_DIFF and height_diff < MAX_HEIGHT_DIFF:
                        matched_contours_idx.append(d2['idx'])

                matched_contours_idx.append(d1['idx'])

                if len(matched_contours_idx) < MIN_N_MATCHED:
                    continue

                matched_result_idx.append(matched_contours_idx)

                unmatched_contour_idx = []
                for d4 in contour_list:
                    if d4['idx'] not in matched_contours_idx:
                        unmatched_contour_idx.append(d4['idx'])

                unmatched_contour = np.take(possible_contours, unmatched_contour_idx)

                recursive_contour_list = find_chars(unmatched_contour)

                for idx in recursive_contour_list:
                    matched_result_idx.append(idx)

                break

            return matched_result_idx

        result_idx = find_chars(possible_contours)

        matched_result = []
        for idx_list in result_idx:
            matched_result.append(np.take(possible_contours, idx_list))

        temp_result = np.zeros((height, width, channel), dtype=np.uint8)

        for r in matched_result:
            for d in r:
                cv2.rectangle(temp_result, pt1=(d['x'], d['y']),
                              pt2=(d['x'] + d['w'], d['y'] + d['h']),
                              color=(255, 255, 255), thickness=2)

        PLATE_WIDTH_PADDING = 1.3
        PLATE_HEIGHT_PADDING = 1.5
        MIN_PLATE_RATIO = 3
        MAX_PLATE_RATIO = 10

        plate_imgs = []
        plate_infos = []

        for i, matched_chars in enumerate(matched_result):
            sorted_chars = sorted(matched_chars, key=lambda x: x['cx'])

            plate_cx = (sorted_chars[0]['cx'] + sorted_chars[-1]['cx']) / 2
            plate_cy = (sorted_chars[0]['cy'] + sorted_chars[-1]['cy']) / 2

            plate_width = (sorted_chars[-1]['x'] + sorted_chars[-1]['w'] - sorted_chars[0]['x']) * PLATE_WIDTH_PADDING

            sum_height = 0
            for d in sorted_chars:
                sum_height += d['h']

            plate_height = int(sum_height / len(sorted_chars) * PLATE_HEIGHT_PADDING)

            triangle_height = sorted_chars[-1]['cy'] - sorted_chars[0]['cy']
            triangle_hypotenuse = np.linalg.norm(
                np.array([sorted_chars[0]['cx'], sorted_chars[0]['cy']]) -
                np.array([sorted_chars[-1]['cx'], sorted_chars[-1]['cy']])
            )

            angle = np.degrees(np.arcsin(triangle_height / triangle_hypotenuse))

            rotation_matrix = cv2.getRotationMatrix2D(center=(plate_cx, plate_cy), angle=angle, scale=1.0)

            img_rotated = cv2.warpAffine(img_thresh, M=rotation_matrix, dsize=(width, height))

            img_cropped = cv2.getRectSubPix(
                img_rotated,
                patchSize=(int(plate_width), int(plate_height)),
                center=(int(plate_cx), int(plate_cy))
            )

            if img_cropped.shape[1] / img_cropped.shape[0] < MIN_PLATE_RATIO or \
                    img_cropped.shape[1] / img_cropped.shape[0] > MAX_PLATE_RATIO:
                continue

            plate_imgs.append(img_cropped)
            plate_infos.append({
                'x': int(plate_cx - plate_width / 2),
                'y': int(plate_cy - plate_height / 2),
                'w': int(plate_width),
                'h': int(plate_height)
            })

        self.possible_contours = possible_contours
        self.matched_result = matched_result
        self.plate_imgs = plate_imgs
        self.plate_infos = plate_infos

    def recognize_and_process_text(self):
        with open('parking_list.json', 'r') as json_file:
            data = json.load(json_file)

        if self.image_path == "entrance.png":
            for img_cropped in self.plate_imgs:
                text = pytesseract.image_to_string(img_cropped, lang='kor', config='--psm 7 --oem 3')
                sub_text = re.sub(r"[^0-9]", "", text)
                replace_text = sub_text.replace("\n\x0c", "")
                # if len(replace_text) == 6 or len(replace_text) == 7:
                #     if replace_text not in self.num_list:
                #         self.num_list.append(replace_text)
                if replace_text not in data and len(replace_text) > 0:
                    data.append(replace_text)
                    with open('parking_list.json', 'w') as json_file:
                        json.dump(data, json_file, indent=2)

        else:
            for img_cropped in self.plate_imgs:
                text = pytesseract.image_to_string(img_cropped, lang='kor', config='--psm 7 --oem 3')
                sub_text = re.sub(r"[^0-9]", "", text)
                replace_text = sub_text.replace("\n\x0c", "")
                # if len(replace_text) == 6 or len(replace_text) == 7:
                #     if replace_text not in self.num_list:
                #         self.num_list.append(replace_text)
                if replace_text in data:
                    data.remove(replace_text)
                    with open('parking_list.json', 'w') as json_file:
                        json.dump(data, json_file, indent=2)

            print(data)

    def run_extraction_process(self):
        self.preprocess_image()
        self.recognize_and_process_text()


class ImageSelectorWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("입구와 출구를 드래그 해주세요")

        # 이미지 선택기 창 열 때 이미지 캡처
        CaptureWindow.capture_1(self)

        # 이미지 선택기 생성
        self.image_selector = ImageSelector(self, "captured_window.png", 'coordinate_list.json')


class ImageSelector:
    def __init__(self, master, image_path, coordinate_file):
        self.master = master
        self.image_path = image_path

        # 이미지 열기
        self.image = Image.open(self.image_path)
        self.tk_image = ImageTk.PhotoImage(self.image)

        # Canvas 생성 및 이미지 표시
        self.canvas = tk.Canvas(self.master, width=self.image.width, height=self.image.height)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

        # 선택한 영역을 표시할 Draw 객체 초기화
        self.draw = ImageDraw.Draw(self.image)

        # 좌표 저장 리스트 초기화
        self.load_coordinate(coordinate_file)

        # 사용자가 선택한 영역의 좌표 초기화
        self.start_x = None
        self.start_y = None

        # 마우스 이벤트 바인딩
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        # 마우스 버튼이 눌렸을 때의 이벤트 핸들러
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

    def on_drag(self, event):
        # 마우스 드래그 중일 때의 이벤트 핸들러
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)

        # 이전에 그린 영역 삭제 및 새로운 영역 그리기
        self.canvas.delete("rect")
        self.canvas.create_rectangle(self.start_x, self.start_y, cur_x, cur_y, outline="red", tags="rect")

    def on_release(self, event):
        # 마우스 버튼이 떼어졌을 때의 이벤트 핸들러
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)

        start = (self.start_x, self.start_y)
        end = (end_x, end_y)

        self.draw.rectangle([start, end], outline='red')
        self.coordinate_list.append([start, end])

        with open('coordinate_list.json', 'w') as json_file:
            json.dump(self.coordinate_list, json_file, indent=2)
        print('구역이 정해졌습니다.')

        Image.open(self.image_path)

        # 이미지를 따로 띄우기
        captured_image = self.image.crop((start[0]+1, start[1]+1, end[0]-0.5, end[1]-0.5))
        self.show_captured_image(captured_image)

        # 지정된 좌표 사진 저장
        with open('coordinate_list.json', 'r') as json_file:
            data = json.load(json_file)

        if len(data) == 1:
            capture_image_path_entrance = "Entrance.png"
            captured_image.save(capture_image_path_entrance)
        else:
            captured_image_path_exit = "Exit.png"
            captured_image.save(captured_image_path_exit)

        # 좌표 값 가져오기
        self.load_coordinate('coordinate_list.json')

    def show_captured_image(self, image):
        top_level = tk.Toplevel(self.master)
        tk_image = ImageTk.PhotoImage(image)
        label = tk.Label(top_level, image=tk_image)
        label.image = tk_image
        label.pack()
        top_level.geometry("500x500")

    def load_coordinate(self, coordinate_file):
        try:
            with open('coordinate_list.json', 'r') as json_file:
                self.coordinate_list = json.load(json_file)

            for start, end in self.coordinate_list:
                self.canvas.create_rectangle(start[0], start[1], end[0], end[1], outline='red')

        except FileNotFoundError:
            print(f'좌표파일 {coordinate_file}이(가) 없습니다.')


class ImageCaptureAndCompare:
    def __init__(self, root, coordinate_list):
        self.Capture_Window = root
        self.Capture_Window.title("메인프로그램")
        self.Capture_Window.attributes("-alpha", 1.0)

        self.coordinate_list = coordinate_list

        self.main_image_path = "captured_window.png"
        self.load_main_image()

        self.label = tk.Label(self.Capture_Window, image=self.tk_image)
        self.label.pack()

        self.top_levels = []

        self.capture_and_compare()

    def load_main_image(self):
        self.main_image = Image.open(self.main_image_path)
        self.tk_image = ImageTk.PhotoImage(self.main_image)

    def read_coordinates_from_json(self, json_file):
        with open(json_file, 'r') as file:
            coordinates = json.load(file)
        return coordinates
    def compare_average_rgb(self):
        coordinates = self.read_coordinates_from_json(self.coordinate_list)

        for i, coord in enumerate(coordinates, 1):
            start, end = coord
            cropped_image = self.main_image.crop((start[0], start[1], end[0], end[1]))

            # 구역의 사진 및 정보
            tk_image = ImageTk.PhotoImage(cropped_image)

            # 지정된 좌표 사진 저장
            with open('coordinate_list.json', 'r') as json_file:
                data = json.load(json_file)

            if i == 1:
                capture_image_path_entrance = "Entrance.png"
                cropped_image.save(capture_image_path_entrance)
            else:
                captured_image_path_exit = "Exit.png"
                cropped_image.save(captured_image_path_exit)

            if i <= len(self.top_levels):
                top_level = self.top_levels[i - 1]
                label = top_level.children["!label"]  # 라벨의 이름을 확인하고 수정
                label.config(image=tk_image)
                label.image = tk_image

            else:
                top_level = tk.Toplevel(self.Capture_Window)
                if i == 1:
                    top_level.title("입구")
                else:
                    top_level.title("출구")

                label = tk.Label(top_level, image=tk_image)
                label.pack()

                top_level.geometry("500x500")

                top_level.tk_image = tk_image

                self.top_levels.append(top_level)
        self.show_parking_info()

    def capture_and_compare(self):
        window_title = "메인프로그램"
        window = pyautogui.getWindowsWithTitle(window_title)

        root_cordinates = self.read_coordinates_from_json('./root_coordinates.json')

        if window:
            window_left = root_cordinates['left']
            window_top = root_cordinates['top']
            window_width = root_cordinates['width']
            window_height = root_cordinates['height']

            try:
                screenshot = ImageGrab.grab(
                    bbox=(window_left, window_top, window_left + window_width, window_top + window_height))
                screenshot.save("captured_window.png")

                # Reload the main image
                self.load_main_image()

                # Compare the new screenshot with the initial image
                self.compare_average_rgb()
            except Exception as e:
                print("")

        else:
            print(f"Window title '{window_title}' not found.")

        # 이미지 파일 경로 지정
        En_path = 'entrance.png'
        Ex_path = 'Exit.png'
        pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"


        lp_extractor_En = LicensePlateExtractor(En_path)
        lp_extractor_En.run_extraction_process()

        lp_extractor_EX = LicensePlateExtractor(Ex_path)
        lp_extractor_EX.run_extraction_process()


        # Schedule the next capture after 5 seconds
        self.Capture_Window.after(3000, self.capture_and_compare)

    def stop_monitoring(self):
        # 종료 시 리소스 정리 및 윈도우 종료
        for top_level in self.top_levels:
            top_level.destroy()
        self.Capture_Window.destroy()

    def show_parking_info(self):
        with open('Max_Park.json', 'r') as json_file:
            data_M = json.load(json_file)
        Max = int(data_M["Max_Park"])

        with open('Now_Park.json', 'r') as json_file:
            data_N = json.load(json_file)
        F_Now = int(data_N["Now_Park"])

        with open('parking_list.json', 'r') as json_file:
            parking_list = json.load(json_file)

        Now = F_Now + len(parking_list)

        # 창이 열려있는지 확인 후 업데이트
        if hasattr(self, 'info_window') and self.info_window.winfo_exists():
            # 기존에 있는 정보 라벨들 삭제
            for widget in self.info_window.winfo_children():
                widget.destroy()
            self.info_window.geometry("500x100")

            if (Now/Max) * 100 <= 30:
                Parking_free_space = tk.Label(self.info_window, text="여유")
                Now_park = tk.Label(self.info_window, text=f"현재 주차 비율 : {Now}/{Max} , {int((Now / Max) * 100)}%")

                Parking_free_space.pack()
                Now_park.pack()
            elif (Now/Max) * 100 > 30 and (Now/Max) * 100 <= 60:
                Parking_free_space = tk.Label(self.info_window, text="원활")
                Now_park = tk.Label(self.info_window, text=f"현재 주차 비율 : {Now}/{Max} , {int((Now / Max) * 100)}%")

                Parking_free_space.pack()
                Now_park.pack()
            elif (Now/Max) * 100 > 60 and (Now/Max) * 100 <= 99:
                Parking_free_space = tk.Label(self.info_window, text="혼잡")
                Now_park = tk.Label(self.info_window, text=f"현재 주차 비율 : {Now}/{Max} , {int((Now / Max) * 100)}%")

                Parking_free_space.pack()
                Now_park.pack()
            else:
                Parking_free_space = tk.Label(self.info_window, text="만석")
                Now_park = tk.Label(self.info_window, text=f"현재 주차 비율 : {Now}/{Max} , {int((Now / Max) * 100)}%")

                Parking_free_space.pack()
                Now_park.pack()

            # 창을 업데이트
            self.info_window.update()
        else:
            # 창이 닫혀있으면 새로 열기
            self.info_window = tk.Toplevel(self.Capture_Window)
            self.info_window.title("주차감시 프로그램")
            self.info_window.geometry("500x100")

            if (Now/Max) * 100 <= 30:
                Parking_free_space = tk.Label(self.info_window, text="여유")
                Now_park = tk.Label(self.info_window, text=f"현재 주차 비율 : {Now}/{Max} , {int((Now / Max) * 100)}%")

                Parking_free_space.pack()
                Now_park.pack()
            elif (Now/Max) * 100 > 30 or (Now/Max) * 100 <= 60:
                Parking_free_space = tk.Label(self.info_window, text="원활")
                Now_park = tk.Label(self.info_window, text=f"현재 주차 비율 : {Now}/{Max} , {int((Now / Max) * 100)}%")

                Parking_free_space.pack()
                Now_park.pack()
            elif (Now/Max) * 100 > 60 or (Now/Max) * 100 <= 99:
                Parking_free_space = tk.Label(self.info_window, text="혼잡")
                Now_park = tk.Label(self.info_window, text=f"현재 주차 비율 : {Now}/{Max} , {int((Now / Max) * 100)}")

                Parking_free_space.pack()
                Now_park.pack()
            else:
                Parking_free_space = tk.Label(self.info_window, text="만석")
                Now_park = tk.Label(self.info_window, text=f"현재 주차 비율 : {Now}/{Max} , {int((Now / Max) * 100)}")

                Parking_free_space.pack()
                Now_park.pack()

def main():

    root = tk.Tk()
    CaptureWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()