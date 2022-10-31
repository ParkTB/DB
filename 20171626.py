import pymysql
from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
import sys, datetime
import csv
import xml.etree.ElementTree as ET
import json

class DB_Utils:

    def queryExecutor(self, db, sql, params):
        conn = pymysql.connect(host='localhost', user='guest', password='bemyguest', db=db, charset='utf8')

        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:     # dictionary based cursor
                cursor.execute(sql, params)
                tuples = cursor.fetchall()
                return tuples
        except Exception as e:
            print(e)
            print(type(e))
        finally:
            conn.close()

class DB_Queries:
    # 모든 검색문은 여기에 각각 하나의 메소드로 정의

    def selectPlayerPosition(self):
        sql = "SELECT DISTINCT position FROM player"
        params = ()

        util = DB_Utils()
        tuples = util.queryExecutor(db="kleague", sql=sql, params=params)
        return tuples

    def selectPlayerTeamname(self):
        sql = "SELECT DISTINCT team_name FROM team"
        params = ()

        util = DB_Utils()
        tuples = util.queryExecutor(db="kleague", sql=sql, params=params)
        return tuples

    def selectPlayerCountry(self):
        sql = "SELECT DISTINCT nation FROM player"
        params = ()

        util = DB_Utils()
        tuples = util.queryExecutor(db="kleague", sql=sql, params=params)
        return tuples

    def selectPlayer(self, val):
        print(val)
        sql2 = " WHERE"
        a = [0, 0, 0, 0, 0]
        if(val[0] == "ALL"):
            print("ALL")
        else:
            a[0] = 1
            sql2 += " team_id = (SELECT team_id FROM team WHERE TEAM_NAME = %s)"
        if (val[1] == "ALL"):
            print("ALL2")
        elif (val[1] == "미정"):

            if 1 in a or 2 in a:
                sql2 += " and position IS NULL"
            else:
                sql2 += " position IS NULL"

            a[1] = 2
        else:
            if 1 in a or 2 in a:
                sql2 += " and position = %s"
            else:
                sql2 += " position = %s"

            a[1] = 1
        if (val[2] == "ALL"):
            print("ALL3")
        elif (val[2] == "대한민국"):

            if 1 in a or 2 in a:
                sql2 += " and nation IS NULL"
            else:
                sql2 += " nation IS NULL"
            a[2] = 2
        else:

            if 1 in a or 2 in a:
                sql2 += " and nation = %s"
            else:
                sql2 += " nation = %s"
            a[2] = 1
        if (val[3] == ''):
            print("ALL4")
        else:

            if (val[5] == 'up'):
                if 1 in a or 2 in a:
                    sql2 += " and height >= %s"
                else:
                    sql2 += " height >= %s"
            if (val[5] == 'down'):
                if 1 in a or 2 in a:
                    sql2 += " and height <= %s"
                else:
                    sql2 += " height <= %s"
            a[3] = 1
        if (val[4] == ''):
            print("ALL5")
        else:

            if (val[6] == 'up'):
                if 1 in a or 2 in a:
                    sql2 += " and weight >= %s"
                else:
                    sql2 += " weight >= %s"
            if (val[6] == 'down'):
                if 1 in a or 2 in a:
                    sql2 += " and weight <= %s"
                else:
                    sql2 += " weight <= %s"
            a[4] = 1

        if 1 not in a and 2 not in a:
            sql2 = ""

        sql = "SELECT * FROM player" + sql2
        print(sql)


        tmp = []
        for i in range(len(a)):
            if a[i] == 1:
                tmp.append(val[i])
        params = tuple(tmp)
        print("vkfka")
        print(params)
        print(":ㅍㅇㅁㄴ")

        util = DB_Utils()
        tuples = util.queryExecutor(db="kleague", sql=sql, params=params)
        print("xxx")
        print(tuples)
        for i in range(len(tuples)):
            if tuples[i]['POSITION'] == None:
                tuples[i]['POSITION'] = "미정"
            if tuples[i]['NATION'] == None:
                tuples[i]['NATION'] = "대한민국"


        return tuples

#########################################

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):

        # 윈도우 설정
        self.setWindowTitle("20171626 박태범 중간과제")
        self.setGeometry(0, 0, 1100, 620)

        # 라벨 설정
        self.label2 = QLabel("팀명:", self)
        self.label = QLabel("포지션:", self)
        self.label3 = QLabel("출신국:", self)
        self.label4 = QLabel("키:", self)
        self.label5 = QLabel("몸무게:", self)
        

        # 콤보박스 설정
        self.comboBox = QComboBox(self)
        self.comboBox2 = QComboBox(self)
        self.comboBox3 = QComboBox(self)



        self.btngroup1 = QButtonGroup()
        self.btngroup2 = QButtonGroup()
        self.btngroup3 = QButtonGroup()
        self.rbtn1 = QRadioButton("이상",self)
        self.rbtn2 = QRadioButton("이하",self)


        self.rbtn3 = QRadioButton("이상",self)
        self.rbtn4 = QRadioButton("이하",self)

        self.rbtn5 = QRadioButton("CSV", self)
        self.rbtn6 = QRadioButton("JSON", self)
        self.rbtn7 = QRadioButton("XML", self)

        self.btngroup1.addButton(self.rbtn1)
        self.btngroup1.addButton(self.rbtn2)
        self.btngroup2.addButton(self.rbtn3)
        self.btngroup2.addButton(self.rbtn4)
        self.btngroup3.addButton(self.rbtn5)
        self.btngroup3.addButton(self.rbtn6)
        self.btngroup3.addButton(self.rbtn7)

        self.rbtn1.setChecked(True)
        self.rbtn3.setChecked(True)
        self.rbtn5.setChecked(True)

        self.line1 = QLineEdit("", self)
        self.line2 = QLineEdit("", self)
        self.line1.textChanged.connect(self.line1EditChanged)
        self.line2.textChanged.connect(self.line2EditChanged)
        # self.line1.setValidator(QIntValidator(self))
        # self.line2.setValidator(QIntValidator(self))

        # DB 검색문 실행
        query = DB_Queries()
        rows = query.selectPlayerPosition()        # 딕셔너리의 리스트
        print(rows)
        print()

        columnName = list(rows[0].keys())[0]
        items = ['미정' if row[columnName] == None else row[columnName] for row in rows]
        items.insert(0, "ALL")
        self.comboBox.addItems(items)

        rows2 = query.selectPlayerTeamname()
        print(rows2)
        columnName2 = list(rows2[0].keys())[0]
        items2 = ['없음' if row2[columnName2] == None else row2[columnName2] for row2 in rows2]
        items2.insert(0, "ALL")
        self.comboBox2.addItems(items2)

        rows3 = query.selectPlayerCountry()
        print(rows3)
        columnName3 = list(rows3[0].keys())[0]
        items3 = ['대한민국' if row3[columnName3] == None else row3[columnName3] for row3 in rows3]
        items3.insert(0, "ALL")
        self.comboBox3.addItems(items3)


        self.comboBox.move(300, 50)
        self.comboBox.resize(100, 20)
        self.comboBox.activated.connect(self.comboBox_Activated)
        self.comboBox2.activated.connect(self.comboBox2_Activated)
        self.comboBox3.activated.connect(self.comboBox3_Activated)

        # 푸쉬버튼 설정
        self.pushButton = QPushButton("검색", self)
        self.pushButton.move(600, 50)
        self.pushButton.resize(100, 20)
        self.pushButton.clicked.connect(self.pushButton_Clicked)
        self.pushButton2 = QPushButton("초기화", self)
        self.pushButton3 = QPushButton("저장", self)

        self.pushButton2.clicked.connect(self.pushButton2_Clicked)
        self.pushButton3.clicked.connect(self.pushButton3_Clicked)

        self.rbtn1.clicked.connect(self.rbtn1Click)
        self.rbtn2.clicked.connect(self.rbtn2Click)
        self.rbtn3.clicked.connect(self.rbtn3Click)
        self.rbtn4.clicked.connect(self.rbtn4Click)
        self.rbtn5.clicked.connect(self.rbtn5Click)
        self.rbtn6.clicked.connect(self.rbtn6Click)
        self.rbtn7.clicked.connect(self.rbtn7Click)


        # 테이블위젯 설정
        self.tableWidget = QTableWidget(self)   # QTableWidget 객체 생성
        self.tableWidget.move(50, 100)
        self.tableWidget.resize(1000, 500)


        upInnerLayout = QGridLayout()
        groupBox = QGroupBox("선수검색")

        groupBox5 = QGroupBox()
        tall = QHBoxLayout()
        tall.addWidget(self.label4)
        tall.addWidget(self.line1)
        tall.addWidget(self.rbtn1)
        tall.addWidget(self.rbtn2)
        groupBox5.setLayout(tall)

        groupBox3 = QGroupBox()
        name = QHBoxLayout()
        name.addWidget(self.label2)
        name.addWidget(self.comboBox2)
        groupBox3.setLayout(name)

        groupBox2 = QGroupBox()
        pos = QHBoxLayout()
        pos.addWidget(self.label)
        pos.addWidget(self.comboBox)
        groupBox2.setLayout(pos)

        groupBox4 = QGroupBox()
        weight = QHBoxLayout()
        weight.addWidget(self.label5)
        weight.addWidget(self.line2)
        weight.addWidget(self.rbtn3)
        weight.addWidget(self.rbtn4)
        groupBox4.setLayout(weight)

        groupBox6 = QGroupBox()
        coun = QHBoxLayout()
        coun.addWidget(self.label3)
        coun.addWidget(self.comboBox3)
        groupBox6.setLayout(coun)


        groupBox7 = QGroupBox("파일 출력")
        save = QHBoxLayout()
        save.addWidget(self.rbtn5)
        save.addWidget(self.rbtn6)
        save.addWidget(self.rbtn7)
        save.addWidget(self.pushButton3)
        groupBox7.setLayout(save)

        upInnerLayout.addWidget(groupBox3, 0, 0)
        upInnerLayout.addWidget(groupBox2, 0, 3)
        upInnerLayout.addWidget(groupBox6, 0, 5)
        upInnerLayout.addWidget(self.pushButton2, 0, 7)


        upInnerLayout.addWidget(groupBox5, 1, 0)
        upInnerLayout.addWidget(groupBox4, 1, 3)
        upInnerLayout.addWidget(self.pushButton, 1, 7)


        groupBox.setLayout(upInnerLayout)
        upLayout = QVBoxLayout()
        upLayout.addWidget(groupBox)

        downLayout = QVBoxLayout()
        downLayout.addWidget(self.tableWidget)

        layout = QGridLayout()
        layout.addLayout(upLayout,0,0)
        layout.addLayout(downLayout,1,0)
        layout.addWidget(groupBox7, 2, 0)

        #첫 실행시 초기값
        self.positionValue = "ALL"
        self.teamnameValue = "ALL"
        self.countryValue = "ALL"
        self.line1Value = ""
        self.updown1 = "up"
        self.line2Value = ""
        self.updown2 = "up"
        self.fileType = "csv"


        self.setLayout(layout)

    def comboBox_Activated(self):

        self.positionValue = self.comboBox.currentText()  # positionValue를 통해 선택한 포지션 값을 전달

    def comboBox2_Activated(self):

        self.teamnameValue = self.comboBox2.currentText()

    def comboBox3_Activated(self):

        self.countryValue = self.comboBox3.currentText()

    def line1EditChanged(self):
        self.line1Value = self.line1.text()

    def line2EditChanged(self):
        self.line2Value = self.line2.text()

    def rbtn1Click(self):
        self.updown1 = "up"

    def rbtn2Click(self):
        self.updown1 = "down"

    def rbtn3Click(self):
        self.updown2 = "up"

    def rbtn4Click(self):
        self.updown2 = "down"

    def rbtn5Click(self):
        self.fileType = "csv"

    def rbtn6Click(self):
        self.fileType = "json"

    def rbtn7Click(self):
        self.fileType = "xml"

    #초기화
    def pushButton2_Clicked(self):
        self.comboBox.setCurrentText("ALL")
        self.comboBox2.setCurrentText("ALL")
        self.comboBox3.setCurrentText("ALL")
        self.positionValue = "ALL"
        self.teamnameValue = "ALL"
        self.countryValue = "ALL"

        self.line1.setText("")
        self.line2.setText("")
        self.rbtn1.setChecked(True)
        self.rbtn3.setChecked(True)
        self.rbtn5.setChecked(True)
        self.line1Value = ""
        self.updown1 = "up"
        self.line2Value = ""
        self.updown2 = "up"
        self.fileType = "csv"

        self.pushButton_Clicked()

    #저장
    def pushButton3_Clicked(self):
        query = DB_Queries()
        vallist = [self.teamnameValue, self.positionValue, self.countryValue, self.line1Value, self.line2Value,
                   self.updown1, self.updown2]

        if vallist[3] == "":
            k = -1
        else:
            k = vallist[3]
        if vallist[4] == "":
            q = -1
        else:
            q = vallist[4]

        try:
            int(k) and int(q)

            players = query.selectPlayer(vallist)

            if self.fileType == "csv":
                with open('player.csv', 'w', encoding='utf-8-sig', newline='') as f:

                    wr = csv.writer(f)
                    columnNames = list(players[0].keys())
                    wr.writerow(columnNames)
                    for player in players:
                        row = list(player.values())
                        wr.writerow(row)

                    self.pushButton_Clicked()
                    print("csv file saved")
                    QMessageBox.about(self, "csv 저장", "파일이 저장되었습니다.")

            if self.fileType == "xml":
                for player in players:
                    for k, v in player.items():
                        if isinstance(v, datetime.date):
                            player[k] = v.strftime('%Y-%m-%d')  # 키가 k인 item의 값 v를 수정

                newDict = dict(player=players)
                print(newDict)

                # XDM 트리 생성
                tableName = list(newDict.keys())[0]
                tableRows = list(newDict.values())[0]

                rootElement = ET.Element('Table')
                rootElement.attrib['name'] = tableName

                for row in tableRows:
                    rowElement = ET.Element('Row')
                    rootElement.append(rowElement)

                    for columnName in list(row.keys()):
                        if row[columnName] == None:  # NICKNAME, JOIN_YYYY, NATION 처리
                            rowElement.attrib[columnName] = ''
                        else:
                            rowElement.attrib[columnName] = row[columnName]

                        if type(row[columnName]) == int:  # BACK_NO, HEIGHT, WEIGHT 처리
                            rowElement.attrib[columnName] = str(row[columnName])

                # XDM 트리를 화일에 출력
                ET.ElementTree(rootElement).write('player.xml', encoding='utf-8', xml_declaration=True)
                self.pushButton_Clicked()
                print("xml file saved")
                QMessageBox.about(self, "xml 저장", "파일이 저장되었습니다.")
            elif self.fileType == "json":
                for player in players:
                    for k, v in player.items():
                        if isinstance(v, datetime.date):
                            player[k] = v.strftime('%Y-%m-%d')  # 키가 k인 item의 값 v를 수정

                newDict = dict(playerGK=players)
                print(newDict)
                with open('playerGK_indent.json', 'w', encoding='utf-8') as f:
                    json.dump(newDict, f, indent=4, ensure_ascii=False)

                self.pushButton_Clicked()
                print("json file saved")
                QMessageBox.about(self, "json 저장", "파일이 저장되었습니다.")



        except ValueError:
            QMessageBox.about(self, "정수 입력", "정수를 입력하세요")


    def pushButton_Clicked(self):

        # DB 검색문 실행
        query = DB_Queries()
        vallist = [self.teamnameValue, self.positionValue, self.countryValue, self.line1Value, self.line2Value, self.updown1, self.updown2]

        if vallist[3] == "":
            k = -1
        else:
            k = vallist[3]
        if vallist[4] == "":
            q = -1
        else:
            q = vallist[4]

        try:
            int(k) and int(q)

            players = query.selectPlayer(vallist)

            self.tableWidget.clearContents()
            if len(players) != 0:

                self.tableWidget.setRowCount(len(players))
                self.tableWidget.setColumnCount(len(players[0]))
                columnNames = list(players[0].keys())
                self.tableWidget.setHorizontalHeaderLabels(columnNames)
                self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

                for player in players:                              # player는 딕셔너리임.
                    rowIDX = players.index(player)                  # 테이블 위젯의 row index 할당

                    for k, v in player.items():
                        columnIDX = list(player.keys()).index(k)    # 테이블 위젯의 column index 할당

                        if v == None:                               # 파이썬이 DB의 널값을 None으로 변환함.
                            continue                                # QTableWidgetItem 객체를 생성하지 않음
                        elif isinstance(v, datetime.date):          # QTableWidgetItem 객체 생성
                            item = QTableWidgetItem(v.strftime('%Y-%m-%d'))
                        else:
                            item = QTableWidgetItem(str(v))


                        self.tableWidget.setItem(rowIDX, columnIDX, item)

                self.tableWidget.resizeColumnsToContents()
                self.tableWidget.resizeRowsToContents()
            else:
                self.tableWidget.setRowCount(len(players))
                QMessageBox.about(self, "검색 결과", "검색 결과가 없습니다.")


        except ValueError:
            QMessageBox.about(self, "정수 입력", "정수를 입력하세요")


#########################################

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

main()