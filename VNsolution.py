# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QGridLayout, QListView, QTextEdit, QMainWindow, QMessageBox, QSizePolicy, QFrame
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtGui import QKeySequence, QStandardItemModel, QStandardItem, QFont, QDesktopServices
# from PyQt5.QtGui import QStandardItemModel, QStandardItem
import mysql.connector
import time
from smsactivate.api import SMSActivateAPI

class LoginScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("로그인")

        # ID Label and LineEdit
        self.id_label = QLabel("아이디:", self)
        self.id_le = QLineEdit(self)

        # Password Label and LineEdit
        password_label = QLabel("비밀번호:", self)
        self.password_le = QLineEdit(self)
        self.password_le.setEchoMode(QLineEdit.Password)

        # Login and Signup Buttons
        login_button = QPushButton("로그인", self)
        signup_button = QPushButton("회원가입", self)

        # Vertical Layout
        v_layout = QVBoxLayout()
        v_layout.addWidget(self.id_label)
        v_layout.addWidget(self.id_le)
        v_layout.addWidget(password_label)
        v_layout.addWidget(self.password_le)
        v_layout.addWidget(login_button)
        v_layout.addWidget(signup_button)

        self.setLayout(v_layout)

        # Apply Stylesheet
        self.setStyleSheet("background-color: lightyellow; color: black; font-family: 'Comic Sans MS'; font-weight: bold;")
        login_button.setStyleSheet("background-color: red; color: white;")
        login_button.clicked.connect(self.login)
        signup_button.setStyleSheet("background-color: red; color: white;")
        signup_button.clicked.connect(self.show_signup_screen)

    def show_signup_screen(self):
        self.signup_screen = SignupScreen()
        # self.signup_screen = SignupScreen()
        self.signup_screen.setGeometry(100,100,400,250)
        self.signup_screen.setFixedSize(400, 250)
        self.signup_screen.show()
    def show_main_screen(self):
        login_screen.hide()
        self.id_text = self.id_le.text()
        self.main_screen = MainScreen('{}'.format(self.id_text))
        # self.setGeometry(300, 300, 500, 500)
    def login(self):
        conn = mysql.connector.connect(
            host="virtualnumber1.cpjzkko9r4hk.ap-northeast-2.rds.amazonaws.com",
            user="admin",
            password="lqp1o2k3",
            database="virtualnumber1"
        )
        cursor = conn.cursor()

        user_id = self.id_le.text()
        sql = "SELECT balance FROM vn_1 WHERE ID=%s AND PW=%s"
        val = (self.id_le.text(), self.password_le.text())
        cursor.execute(sql, val)
        balance = cursor.fetchone() # Example value, replace with the actual balance from the database
        balance = str(balance)
        balance = balance.replace(',','')
        balance = balance.replace('(','')
        balance = balance.replace(')','')
        print(balance) # 잔액 표시

        #사용자 정보 검색 (로그인을 위한것)
        sql = "SELECT * FROM vn_1 WHERE ID=%s AND PW=%s"
        val = (self.id_le.text(), self.password_le.text())
        cursor.execute(sql, val)
        result = cursor.fetchone()
        if result:
            self.close()
            QMessageBox.information(self, "로그인 성공", "로그인에 성공하였습니다 ^^ 즐거운 이용 하세요~")
            self.main_window = MainScreen(user_id)
            
            self.main_window.setGeometry(500, 500, 700, 700)
            self.main_window.setFixedSize(700,700)
            self.main_window.show()
        else:
            #로그인실패
            QMessageBox.warning(self, "Login Failed", "아이디 혹은 비밀번호가 틀렸습니다.")
        cursor.close()
        conn.close()
class SignupScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("회원가입")

        # ID Label and LineEdit
        id_label = QLabel("아이디:", self)
        self.id_le = QLineEdit(self)

        # Password Label and LineEdit
        password_label = QLabel("비밀번호:", self)
        self.password_le = QLineEdit(self)
        self.password_le.setEchoMode(QLineEdit.Password)

        # Referral Code Label and LineEdit
        referral_label = QLabel("추천인코드:", self)
        self.referral_le = QLineEdit(self)

        # Sign Up Button
        signup_button = QPushButton("회원가입하기", self)
        signup_button.clicked.connect(self.signUp)

        # Vertical Layout
        v_layout = QVBoxLayout()
        v_layout.addWidget(id_label)
        v_layout.addWidget(self.id_le)
        v_layout.addWidget(password_label)
        v_layout.addWidget(self.password_le)
        v_layout.addWidget(referral_label)
        v_layout.addWidget(self.referral_le)
        v_layout.addWidget(signup_button)

        self.setLayout(v_layout)

        # Apply Stylesheet
        self.setStyleSheet("background-color: lightyellow; color: black; font-family: 'Comic Sans MS'; font-weight: bold;")
        signup_button.setStyleSheet("background-color: red; color: white;")
    def signUp(self):
            # MySQL 데이터베이스 연결
        conn = mysql.connector.connect(
            host="virtualnumber1.cpjzkko9r4hk.ap-northeast-2.rds.amazonaws.com",
            user="admin",
            password="lqp1o2k3",
            database="virtualnumber1"
        )
        cursor = conn.cursor()

                # 사용자 정보 저장
        sql = "INSERT INTO vn_1 (ID, PW) VALUES (%s, %s)"
        val = (self.id_le.text(), self.password_le.text())
        cursor.execute(sql, val)
        if self.referral_le.text() == '마케팅고트':
            sql = "UPDATE vn_1 SET balance = 5000 WHERE ID ='{}'".format(self.id_le.text())
            cursor.execute(sql)
        else:
            pass
        conn.commit()
        # MySQL 데이터베이스 연결 종료
        cursor.close()
        conn.close()

        # 회원가입 완료 안내창 보여주기
        QMessageBox.information(self, "Sign Up", "회원가입 완료되었습니다 ^^ 즐거운 이용 하세요~\n ※ 꼭 사용법과 주의사항을 읽어주세요 ^^")

        self.close()
class MainScreen(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.countdown_time = 600  # 10 minutes in seconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)
        self.user_id = user_id
        
        self.initUI()
        
    def initUI(self):
        # Create welcome label
        self.welcome_label = QLabel("환영합니다, {} 님".format(self.user_id), self)
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # Create buttons
        self.balance_button = QPushButton("잔액 확인", self)
        self.balance_button.clicked.connect(self.check_balance)
        self.usage_button = QPushButton("사용법", self)
        self.usage_button.clicked.connect(self.how_to_use)
        self.warning_button = QPushButton("주의사항 및 안내", self)
        self.warning_button.clicked.connect(self.caution_info)
        # Create list views
        self.list_view_1 = QListView(self)
        self.list_view_2 = QListView(self)

        self.model = QStandardItemModel(self.list_view_1)
        self.model2 = QStandardItemModel(self.list_view_2)
        self.list_view_1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.list_view_2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        # 리스트안의 아이템에 데이터 넣는방법.
        # item1 = QStandardItem("러시아")
        # item1.setData(0, Qt.UserRole)
        # item2 = QStandardItem("우크라이나")
        # item2.setData(1, Qt.UserRole)
        # item3 = QStandardItem("카자흐스탄")
        

        # model.appendRow(item1)
        # model.appendRow(item2)
        # model.appendRow(item3)
   

        # 국가 코드 넣는 코드
        country_list_code = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 111, 112, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 
131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 183, 184, 185, 186, 187, 189, 196]
        country_list_name = ['러시아', '우크라이나', '카자흐스탄', '중국', '필리핀 제도', '미얀마', '인도네시아', '말레이시아', '케냐', '탄자니아', '베트남', '키르기스스탄', '미국(가상)', '이스라엘', '홍콩', '폴란드', '영국', '마다가스카르', '디콩고', '나이지리아', '마카오', '이집트', '인도', '아일랜드', '캄보디아', '라오스', '아이티', '상아', '감비아', '세르비아', '예멘', '남아프리카', '루마니아', '콜롬비아', '에스토니아', '캐나다', '모로코', '가나', '아르헨티나', '우즈베키스탄', '카메룬', '차드', '독일', '리투아니아', '크로아티아', '스웨덴', '이라크', '네덜란드', '라트비아', '오스트리아', '벨라루스', '태국', '사우디 아라비아', '멕시코', '대만', '스페인', '알제리', '슬로베니아', '방글라데시', '세네갈', '칠면조', '체코 사람', '스리랑카', '페루', '파키스탄', '뉴질랜드', '기니', '말리', '베네수엘라', '에티오피아', '몽골리아', '브라질', '아프가니스탄', '우간다', '앙골라', '키프로스', '프랑스', '파푸아', '모잠비크', '네팔', '벨기에', '불가리아', '헝가리', '몰도바', '이탈리아', '파라과이', '온두라스', '튀니지', '니카라과', '동티모르', '볼리비아', '코스타리카', '과테말라', 'Uae', '짐바브웨', '푸에르토 리코', '토고', '쿠웨이트', '살바도르', '리비아 사람', '자메이카', '트리니다드', '에콰도르', '스와질란드', '오만', '보스니아', '도미니카 공화국', '카타르', '파나마', '모리타니', '시에라리온', '요르단', '포르투갈', '바베이도스', '부룬디', '베냉', '브루나이', '바하마', '보츠와나', '벨리즈', '카페', '도미니카', '그레나다', '그루지야', '그리스', '기니비사우', '가이아나', '아이슬란드', '코모로', '세인트키츠', '라이베리아', '레소토', '말라위', '나미비아', '니제르', '르완다', '슬로바키아', '수리남', '타지키스탄', '모나코', '바레인', '재결합', '잠비아', '아르메니아', '소말리아', '콩고', '칠레', '부키 나 파소', '레바논', '가봉', '알바니아', '우루과이', '모리셔스', '부탄', '몰디브', '과들루프', '투르크메니스탄', '프랑스령 기아나', '핀란드', '세인트 루시아', '룩셈부르크', '세인트빈센트그레나딘', '적도기니', '지부티', '안티구아바르부다', '케이맨 제도', '몬테네그로', '덴마크', '스위스', '노르웨이', '호주', '에리트레아', '남 수단', '사오토메안프린시페', '아루바', '몬세라트', '앵귈라', '북 마케도니아', '세이셸', '뉴 칼레도니아', '카베르데', '미국', '피지', '싱가포르']
        
        for code,name in zip(country_list_code, country_list_name):
            name1 = QStandardItem(name)
            name1.setData(code, Qt.UserRole)
            self.model.appendRow(name1)
        
        self.list_view_1.setModel(self.model)
        
        # 서비스 코드 넣는 코드
        service_list_code = ['nv', 'go', 'fb', 'ig', 'tg', 'tw', 'kt', 'dr', 'mb', 'lf', 'oi', 'rc', 'ds', 'hb', 'am', 'wb']
        service_list_name = ['네이버', '구글(유튜브)', '페이스북', '인스타그램', '텔레그램', '트위터', '카카오톡', 'OpenAI', '야후', '틱톡', '틴더', '스카이프', '디스코드', '트위치', '아마존', '위챗']

        for code,name in zip(service_list_code, service_list_name):
            name2 = QStandardItem(name)
            name2.setData(code, Qt.UserRole)
            self.model2.appendRow(name2)

        self.list_view_2.setModel(self.model2)
        # print(item1)
        # print(item1.data)
        # print(item1.data(Qt.UserRole))
        # print(item2.data(Qt.UserRole))
        # print(item1.data())
        
        


        # Create create button
        self.create_button = QPushButton("생성", self)
        self.create_button.setFixedSize(100,150)
        self.create_button.clicked.connect(self.get_virtual_number)
        # Create result text
        self.result_text = QTextEdit(self)
        self.result_text.setFixedSize(400,150)
        # self.result_text.setLineWidth(3)
        # self.result_text.setFrameShape(QFrame.StyledPanel)
        # self.result_text.setFrameShadow(QFrame.Sunken)
        # Create copy button
        self.copy_button = QPushButton("발급 번호\n복사하기", self)
        self.copy_button.setFixedSize(100,150)
        self.copy_button.clicked.connect(self.copy_number)
        # Create cancle button
        self.cancel_button = QPushButton("주문 취소", self)
        self.cancel_button.setFixedSize(100,150)
        self.cancel_button.clicked.connect(self.cancel_order)
        # Create 번호 창
        self.auth_label = QLabel("▼▼▼▼▼ 인증 번호 ▼▼▼▼▼", self)
        # self.auth_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.auth_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # Create authentication number text
        self.auth_text = QLineEdit(self)

        # Create copy auth number button
        self.copy_auth_button = QPushButton("인증 번호 복사하기", self)
        self.copy_auth_button.clicked.connect(self.copy_auth_number)
         # Create remaining time label
        self.remaining_time_label = QLabel("남은 시간: {}".format(self.format_time(self.countdown_time)), self)
        self.remaining_time_label.setAlignment(Qt.AlignCenter)
        self.remaining_time_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)



        self.bye_label = QLabel("제작자 : 마케팅고트 | 텔레그램 : @GOAT82 \n 프로그램에 추가할 기능, 혹은 가입가능한 많은 사이트 있습니다.\n 현재는 서비스에 국내에서 이용자가 많은 네이버, 구글 등등만 있습니다.\n 추가하시고 싶은 '서비스'는 언제든 문의주세요. 행복한하루되세요 ^^", self)
        self.bye_label.setAlignment(Qt.AlignCenter)
        self.bye_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.marketing_info_button = QPushButton("마케팅 품목 보러가기", self)
        self.marketing_info_button.clicked.connect(self.show_market)
        self.marketing_info_button.setFixedSize(150,50)
        # Create grid layout
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.welcome_label, 0, 0, 1, 2)
        grid.addWidget(self.balance_button, 1, 0)
        grid.addWidget(self.usage_button, 1, 1)
        grid.addWidget(self.warning_button, 1, 2)
        grid.addWidget(self.list_view_1, 2, 0)
        grid.addWidget(self.list_view_2, 2, 1)
        grid.addWidget(self.create_button, 2, 2)
        grid.addWidget(self.result_text, 3, 0, 1, 2)
        grid.addWidget(self.copy_button, 3, 1, Qt.AlignRight)
        grid.addWidget(self.cancel_button, 3, 2)
        grid.addWidget(self.auth_label, 5, 0, Qt.AlignHCenter | Qt.AlignVCenter)
        grid.addWidget(self.remaining_time_label, 5, 1)
        grid.addWidget(self.auth_text, 6, 0)
        grid.addWidget(self.copy_auth_button, 6, 1)
        grid.addWidget(self.bye_label, 7, 0, 1, 2, Qt.AlignHCenter | Qt.AlignVCenter)
        grid.addWidget(self.marketing_info_button, 7, 2, Qt.AlignHCenter | Qt.AlignVCenter)
        # Set central widget and layout
        central_widget = QWidget()
        central_widget.setLayout(grid)
        self.setCentralWidget(central_widget)

        #디자인
        self.setStyleSheet("background-color: lightyellow; color: black; font-family: 'Comic Sans MS'; font-weight: bold;")
        self.balance_button.setStyleSheet("background-color: red; color: white;")
        self.usage_button.setStyleSheet("background-color: red; color: white;")
        self.warning_button.setStyleSheet("background-color: red; color: white;")
        self.create_button.setStyleSheet("background-color: balck; color: white;")
        self.copy_button.setStyleSheet("background-color: black; color: white;")
        self.cancel_button.setStyleSheet("background-color: red; color: white;")
        self.copy_auth_button.setStyleSheet("background-color: black; color: white;")
        # Set window properties
        # self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle("메인화면 0.1 ver")
        self.show()
    def start_countdown(self):
        self.timer.start(1000)
    def update_countdown(self):
        self.countdown_time -= 1
        self.remaining_time_label.setText("남은 시간: {}".format(self.format_time(self.countdown_time)))
        if self.countdown_time == 0:
            self.timer.stop()
            self.countdown_time = 600
            self.remaining_time_label.setText("남은 시간: {}".format(self.format_time(self.countdown_time)))
            # Add code to generate authentication code and display it in the result text
            self.auth_text.setText("인증번호가 도착하지 않았습니다.")
    def format_time(self, secs):
        mins, secs = divmod(secs, 60)
        return "{:02d}:{:02d}".format(mins, secs)
        
    def get_virtual_number(self):
    # 가상번호 발급 함수
        conn = mysql.connector.connect(
            host="virtualnumber1.cpjzkko9r4hk.ap-northeast-2.rds.amazonaws.com",
            user="admin",
            password="lqp1o2k3",
            database="virtualnumber1"
        )
        cursor = conn.cursor()
        sql = "SELECT balance FROM vn_1 WHERE ID='{}'".format(self.user_id)
        # val = (self.greeting.text())
        cursor.execute(sql)
        balance = cursor.fetchone() # Example value, replace with the actual balance from the database
        balance = str(balance)
        balance = balance.replace(',','')
        balance = balance.replace('(','')
        balance = balance.replace(')','')
        # self.balance_amount = QLabel("포인트 잔액 : " + balance)
        
        balance = int(balance)
        if balance > 999:
            api_key = 'e2094e3de4f60fe5e6962634184de2e0'
            self.sa = SMSActivateAPI(api_key)
            # 국가코드 서비스코드 발급.
            print(self.get_country_code())
            print(self.get_service_code())
            self.number = self.sa.getNumber(service=self.get_service_code(), country=self.get_country_code()) # {'activation_id': 000000000, 'phone': 79999999999}
            try:
                # print(self.number) # 79999999999
                self.result_text.setText(' 주문번호 :'+ str(self.number['activation_id']) + '\n 발급번호 :' + '+'+str(self.number['phone'])+'\n 국가 :'+self.get_country_name()+'\n 서비스 :'+self.get_service_name())
                conn = mysql.connector.connect(
                    host="virtualnumber1.cpjzkko9r4hk.ap-northeast-2.rds.amazonaws.com",
                    user="admin",
                    password="lqp1o2k3",
                    database="virtualnumber1"
                )
                cursor = conn.cursor()
                sql = "UPDATE vn_1 SET balance = balance - 1000 WHERE ID = '{}'".format(self.user_id)
                cursor.execute(sql)
                conn.commit()
                cursor.close()
                conn.close()
                # 타임 셋팅 시작.
                self.start_countdown()
                self.get_code()
            except:
                print(self.number['message']) # Error tex
                if self.number['message'] == 'Not enough funds':
                    QMessageBox.information(self, "오류", "개발자에게 문의해주세요 . 문의내용 = 1")

            

            
            
        else:
            QMessageBox.information(self, "잔액 부족", "잔액이 부족합니다. 충전은 개발자에게 문의주십시요. 충전은 '크몽결제'로 진행됩니다.")

    # 인증코드 받는 함수
    def get_code(self):
        self.count = 0
        #인증코드를 받는함수를 적자. 아마 무한루프 10초 무한루프.
        self.auth_text.clear()
        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.check_code)
        self.timer2.start(10000)
        # while True:
        #     activations = self.sa.getActiveActivations()
        #     try:
        #         b = activations['activeActivations'][0]['smsCode']
        #         print(b)
        #         self.auth_text.setText(str(b))
        #     except:
        #         print(activations['error']) # Error
        #     time.sleep(10)
        #     if b is not None:
        #         break
        # self.reset_countdown()
    def check_code(self):
        activations = self.sa.getActiveActivations()
        
        try:
            b = activations['activeActivations'][0]['smsCode']
            if b is None:
                print(b)
                print(self.count)
                self.count += 1 # 10초마다 check_code 가 실행되는데 none 일경우 변수에 1씩추가.
                if self.count == 60:# 60 도달 = 10분 지났다는 소리
                    self.timer2.stop()

                pass
                
            
            elif b is not None:
                print(b[0])
                self.auth_text.setText(b[0])
                self.timer.stop()
                self.timer2.stop()
                self.reset_countdown()
                self.success_order()
        except:
            print(activations['error']) # Error
        
    # 주문 성공했으니 완료 함수
    def success_order(self):
        status = self.sa.setStatus(id=self.number['activation_id'], status=6)
        try:
            QMessageBox.information(self, "코드 도착", "코드가 도착했습니다.")
        except Exception as ex:
            print(ex)
   
    # 번호 취소 함수
    def cancel_order(self):
        # status = self.sa.setStatus(id=self.number['activation_id'], status=8) # ACCESS_READY
        try:
            status = self.sa.setStatus(id=self.number['activation_id'], status=8) # ACCESS_READY

            print(status) # ACCESS_READY
            
            conn = mysql.connector.connect(
                host="virtualnumber1.cpjzkko9r4hk.ap-northeast-2.rds.amazonaws.com",
                user="admin",
                password="lqp1o2k3",
                database="virtualnumber1"
            )
            cursor = conn.cursor()
            sql = "UPDATE vn_1 SET balance = balance + 1000 WHERE ID = '{}'".format(self.user_id)
            cursor.execute(sql)
            conn.commit()
            self.timer.stop()
            self.timer2.stop()
            self.reset_countdown()
            QMessageBox.information(self, "취소 완료", "주문 취소 되었습니다.")
        except:
            print(status['message']) # Error tex
            QMessageBox.information(self, "취소 실패", "취소된 이유는 콘솔창에 나옵니다. 판매자에게 문의해주세요.")

    # 가상번호 복사
    def copy_number(self):
        clipboard = QApplication.clipboard()
        clipboard.setText('+{}'.format(str(self.number['phone'])))

    def reset_countdown(self):
    # Check if the authentication code is correct
        self.result_text.clear()
        if  self.auth_text.text():
            self.countdown_time = 600
            self.remaining_time_label.setText("남은시간: {}".format(self.format_time(self.countdown_time)))
            # self.auth_text.setText("")
            self.timer.stop()
            self.timer2.stop()
        else:
            self.countdown_time = 600
            self.remaining_time_label.setText("남은시간: {}".format(self.format_time(self.countdown_time)))
            self.timer.stop()
            self.timer2.stop()
    # 인증번호 복사
    def copy_auth_number(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.auth_text.text())

    # 잔액확인 함수
    def check_balance(self):
        conn = mysql.connector.connect(
            host="virtualnumber1.cpjzkko9r4hk.ap-northeast-2.rds.amazonaws.com",
            user="admin",
            password="lqp1o2k3",
            database="virtualnumber1"
        )
        cursor = conn.cursor()
        sql = "SELECT balance FROM vn_1 WHERE ID='{}'".format(self.user_id)
        cursor.execute(sql)
        balance = cursor.fetchone()
        balance = str(balance)
        balance = balance.replace(',','')
        balance = balance.replace('(','')
        balance = balance.replace(')','')
        conn.commit()
        
        # MySQL 데이터베이스 연결 종료
        cursor.close()
        conn.close()
        QMessageBox.information(self, "잔액 확인", "{} 원 입니다 \n 충전 = '크몽결제' 문의주세요.".format(balance))
    # 사용방법
    def how_to_use(self):
        font = QFont()
        font.setPointSize(18)
        QMessageBox.information(self, "사용법", "---------------- 사용법 ----------------\n\n 1. 먼저 발급받을 가상번호의 '국가'를 선택합니다.\n 2. 가상번호를 사용할 '서비스'를 선택합니다.\n 3. 생성 버튼을 누르면 텍스트창에 가상번호와 정보가 나옵니다. \n 4. 발급받은 번호를 '서비스'에 입력 후 인증번호를 기다립니다. \n 5. 약 2분안에 인증번호가 도착합니다. \n\n ※ 제한시간은 10분이지만, 약 2~3분안에 인증번호가 도착하지 않을시 '주문 취소' 버튼을 누르시면 시간을 아끼실수 있습니다.")
        QMessageBox.setFont(self, font)
    
    # 주의사항 및 안내
    def caution_info(self):
        font = QFont()
        font.setPointSize(18)
        QMessageBox.information(self, "주의사항 및 안내", "---------------- 주의사항 및 안내 ----------------\n\n 개발자 텔레그램 아이디 = @GOAT82 \n------------------------------------------------\n\n ◆ 각 서비스(포털사이트)마다 가입 로직은 알려드리지 않습니다. \n ◆ 직접 가상번호를 이용하여 가입해보시길 바랍니다. \n ◆ 선택하신 '국가'에 맞는 IP를 이용하시는것을 추천드립니다. \n ◆ 테스트 해본 결과 가입 잘됩니다 ! ! !")
        QMessageBox.setFont(self, font)

    # URL 테스트
    def open_url(self):
        url = QUrl("https://google.com")
        QDesktopServices.openUrl(url)

    # 마케팅 품목
    def show_market(self):
        font = QFont()
        font.setPointSize(18)
        QMessageBox.information(self, "마케팅 품목", "---------------- 마케팅 품목 ----------------\n\n 개발자 텔레그램 아이디 = @GOAT82 \n------------------------------------------------\n\n 1. 구글상위노출 (백링크 7년차) 추천도 : ★★★★★ \n 2. 트위터 무한 게시(인기탭,최신탭,구글이미지) 추천도 : ★★★★\n 3. 맘카페 바이럴 마케팅 - 추천도 : ★★★\n 4. 각종 계정 판매 - 추천도 : ★★★★\n 5. 그외 필요하신것들 문의만주세요")
        QMessageBox.setFont(self, font)

        # 국가 선택한 data 가져오기
    def get_country_code(self):
        selection_model = self.list_view_1.selectionModel()
        selected_indexes = selection_model.selectedIndexes()
        # 선택된 항목이 있는 경우
        if selected_indexes:
    # 첫 번째 선택된 항목을 가져옵니다.
            selected_item = self.model.itemFromIndex(selected_indexes[0])

    # 항목에서 Qt.UserRole 역할에 대한 데이터를 가져옵니다.
            selected_data = selected_item.data(Qt.UserRole)
            print("Selected data:", selected_data)

            return selected_data
        
        # 서비스 선택한 data 가져오기
    def get_service_code(self):
        selection_model2 = self.list_view_2.selectionModel()
        selected_indexes = selection_model2.selectedIndexes()
        # 선택된 항목이 있는 경우
        if selected_indexes:
    # 첫 번째 선택된 항목을 가져옵니다.
            selected_item = self.model2.itemFromIndex(selected_indexes[0])

    # 항목에서 Qt.UserRole 역할에 대한 데이터를 가져옵니다.
            selected_data = selected_item.data(Qt.UserRole)
            print("Selected data:", selected_data)

            return selected_data
    def get_country_name(self):
        selected_item = self.list_view_1.currentIndex()
        selected_text = self.list_view_1.model().data(selected_item, Qt.DisplayRole)
        return selected_text
    def get_service_name(self):
        selected_item = self.list_view_2.currentIndex()
        selected_text = self.list_view_2.model().data(selected_item, Qt.DisplayRole)
        return selected_text
if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_screen = LoginScreen()
    login_screen.setGeometry(500, 500, 400, 250)
    login_screen.setFixedSize(400, 250)
    
    login_screen.show()
    sys.exit(app.exec_())