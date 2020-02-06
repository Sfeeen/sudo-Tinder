import urllib.request

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import tinder_api


class Picture(QWidget):
    def __init__(self, url, width):
        super().__init__()

        layout = QVBoxLayout()

        data = urllib.request.urlopen(url).read()
        pixmap = QPixmap()
        pixmap.loadFromData(data)

        label = QLabel(self)
        label.setPixmap(pixmap.scaledToWidth(width))
        label.setFixedHeight(216)
        # 172 216
        # 320 400
        layout.addWidget(label)

        self.setLayout(layout)


class Swipe(QWidget):
    height = 320
    margin = 7

    def __init__(self, MainWindow, tuple):
        super().__init__()
        self.id, self.url, self.name = tuple
        self.initUI(MainWindow)

    def initUI(self, MainWindow):
        self.mainwindow = MainWindow

        style = """
        background-color: #b8d9a9;
        border: 2px solid black;
        """

        root = QVBoxLayout()
        root.setContentsMargins(Swipe.margin, Swipe.margin, Swipe.margin, Swipe.margin)
        layout = QVBoxLayout()

        pic = Picture(self.url, 172)
        layout.addWidget(pic)

        view_profile_button = QPushButton(self.name)
        view_profile_button.setStyleSheet("background-color: #5a83a3")
        view_profile_button.clicked.connect(self.view_full_profile)
        layout.addWidget(view_profile_button)

        widget = QWidget()
        widget.setLayout(layout)

        root.addWidget(widget)
        self.setLayout(root)
        self.setStyleSheet(style)
        self.setFixedHeight(Swipe.height)

    def view_full_profile(self):
        self.mainwindow.view_person(self.id)


class TeaserRow(QWidget):

    def __init__(self, tuples):
        super().__init__()

        self.initUI(tuples)

    def initUI(self, tuples):
        root = QHBoxLayout()

        for tuple in tuples:
            _, url = tuple
            s = Picture(url, 172)
            root.addWidget(s)

        self.setStyleSheet("background-color:#76c773;border-style: outset;border-style: solid;border-width: 2px;")
        self.setLayout(root)


style = """
.QWidget#root {
background-color :#56B8D0;
}


.QLabel#app_titel {
background-color: #ba0f34; 
padding: 10px;border: 
5px solid black;
margin-bottom: 30 px;
font-family: "Quicksand Light";
font-size: 25pt;
}

.QPushButton {
background-color: #334A70; 
font-family: "Quicksand Light";
font-size: 13pt;
}

.QPushButton#approve {
background-color: #7D9B00; 
}

.QPushButton#decline {
background-color: #ba0f34; 
}

.QLabel {
font-family: "Quicksand Light";
font-size: 13pt;
}
"""


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.logged_in = False
        self.setWindowTitle("Sudo Tinder")
        self.setWindowIcon(QIcon("tinder.png"))
        # width = get_monitors()[0].width
        # height = get_monitors()[0].height - 200
        width = 1920
        height = 880 - 200
        self.setGeometry(0, 0, width, height)

        root = QHBoxLayout()

        # LEFT PANEL
        left_panel = QVBoxLayout()

        title_label = QLabel("Sudo Tinder")
        title_label.setObjectName("app_titel")
        title_label.setFixedHeight(100)
        left_panel.addWidget(title_label)

        login_button = QPushButton("Log in")
        login_button.clicked.connect(self.login)
        left_panel.addWidget(login_button)

        fetch_rec_button = QPushButton("Fetch Swipes")
        fetch_rec_button.clicked.connect(self.fetch_recs)
        left_panel.addWidget(fetch_rec_button)

        fetch_more_button = QPushButton("Fetch more")
        fetch_more_button.clicked.connect(self.fetch_more)
        left_panel.addWidget(fetch_more_button)

        location_button = QPushButton("Set new location")
        location_button.clicked.connect(self.set_new_location)
        left_panel.addWidget(location_button)

        teaser_button = QPushButton("Get teasers")
        teaser_button.clicked.connect(self.get_teasers)
        left_panel.addWidget(teaser_button)

        space = QLabel()
        space.setFixedHeight(300)
        left_panel.addWidget(space)

        fb_label = QLabel("Feedback:")
        left_panel.addWidget(fb_label)

        self.feedback_text = QPlainTextEdit()
        self.feedback_text.setFixedHeight(200)
        left_panel.addWidget(self.feedback_text)

        left_widget = QWidget()
        left_widget.setLayout(left_panel)
        left_widget.setFixedWidth(300)

        root.addWidget(left_widget)

        # MIDDLE PANEL
        self.scroll = QScrollArea()
        self.scroll.setFixedWidth(925)
        self.scroll.setStyleSheet("background-color:#bab6b8")
        self.columns = 4
        root.addWidget(self.scroll)
        self.fetch_am = 0

        ### VIEW PANEL
        vbox = QVBoxLayout()

        self.id = ""
        self.name_label = QLabel("naam")
        vbox.addWidget(self.name_label)

        self.bday_label = QLabel("fuzzy bday")
        vbox.addWidget(self.bday_label)

        self.ping_label = QLabel("ping")
        vbox.addWidget(self.ping_label)

        self.city_label = QLabel("city")
        vbox.addWidget(self.city_label)

        self.distance_label = QLabel("distance")
        vbox.addWidget(self.distance_label)

        self.bio_label = QLabel("Bio")
        vbox.addWidget(self.bio_label)

        hbox = QHBoxLayout()

        self.like_button = QPushButton("Approve")
        self.like_button.setObjectName("approve")
        self.like_button.clicked.connect(self.like_person)
        hbox.addWidget(self.like_button)

        self.dislike_button = QPushButton("Decline")
        self.dislike_button.setObjectName("decline")
        self.dislike_button.clicked.connect(self.dislike_person)
        hbox.addWidget(self.dislike_button)

        vbox.addLayout(hbox)

        self.superlike_button = QPushButton("Superlike")
        self.superlike_button.clicked.connect(self.superlike_person)
        vbox.addWidget(self.superlike_button)

        self.view_scroll = QScrollArea()
        self.view_scroll.setFixedHeight(500)
        self.view_scroll.setStyleSheet("background-color: white")
        vbox.addWidget(self.view_scroll)

        wid = QWidget()
        wid.setFixedWidth(600)
        wid.setLayout(vbox)

        root.addWidget(wid)

        #####################

        widget = QWidget()
        widget.setObjectName("root")
        widget.setStyleSheet(style)
        widget.setLayout(root)
        self.setCentralWidget(widget)

    def feedback_append_line(self, text):
        text = str(text)
        self.feedback_text.setPlainText(text + "\n" + self.feedback_text.toPlainText())

    def view_person(self, id):
        if not self.logged_in:
            self.feedback_append_line("Please login first!")
            return
        self.id = id
        self.feedback_append_line("** Viewing: " + str(id))
        person = tinder_api.get_person(id)["results"]

        pics = person["photos"]

        pic_urls = []

        for pic in range(len(pics)):
            pic_urls.append(pics[pic]["processedFiles"][1]["url"])

        layout = QGridLayout()
        for number, pic in enumerate(pic_urls):
            layout.addWidget(Picture(pic, 275), number / 2, number % 2)
        self.view_scroll.setLayout(layout)

        widget = QWidget()
        widget.setLayout(layout)

        self.view_scroll.setWidget(widget)
        name = person["name"]
        bio = "no bio"
        birthday = "no birthday"
        ping = "no ping"
        city = "no city"
        dist = "no distance"

        if "bio" in person:
            bio = person["bio"]

        if "birth_date" in person:
            birthday = person["birth_date"]

        if "ping_time" in person:
            ping = person["ping_time"]

        if "city" in person:
            city = person["city"]["name"] + " -- " + person["city"]["region"]

        if "distance_mi" in person:
            dist = person["distance_mi"]

        self.name_label.setText(name)
        self.bio_label.setText("bio: " + bio)
        self.distance_label.setText("distance (mi): " + str(dist))
        self.bday_label.setText("fuzzy birthday: " + birthday)
        self.ping_label.setText("ping: " + ping)
        self.city_label.setText("city: " + city)

    def fetch_recs(self):
        if not self.logged_in:
            self.feedback_append_line("Please login first!")
            return

        tuples = tinder_api.get_LQ_rec()
        # tuples = rec_tuples

        amount = len(tuples)
        self.feedback_append_line("Found " + str(amount) + " new Swipes")
        QGuiApplication.processEvents()

        self.gridlayout = QGridLayout()

        self.swipe_container_widget = QWidget()
        self.swipe_container_widget.setObjectName("swipe_container")
        self.swipe_container_widget.setLayout(self.gridlayout)
        self.swipe_container_widget.setFixedWidth(900)

        for number in range(amount):
            self.gridlayout.addWidget(Swipe(self, tuples[number]), number / self.columns, number % self.columns)
            self.scroll.setWidget(self.swipe_container_widget)
            self.swipe_container_widget.setFixedHeight(
                (int(number / self.columns) + 1) * (Swipe.height + 2 * Swipe.margin))
            QGuiApplication.processEvents()

    def fetch_more(self):
        tuples = rec_tuples[:2]

        amount = len(tuples)
        self.feedback_append_line("Not implemented")

    def get_teasers(self):
        if not self.logged_in:
            self.feedback_append_line("Please login first!")
            return

        resp = tinder_api.get_teasers()["data"]["results"]
        # resp = teaser_tuples

        amount = len(resp)
        self.feedback_append_line("Found " + str(amount) + " Teasers")
        QGuiApplication.processEvents()

        person_data = []
        for number in range(amount):
            id = resp[number]["user"]["_id"]
            url = resp[number]["user"]["photos"][0]["processedFiles"][1]["url"]
            person_data.append((id, url))

        vbox = QGridLayout()

        self.swipe_container_widget = QWidget()
        self.swipe_container_widget.setFixedWidth(900)
        self.swipe_container_widget.setLayout(vbox)

        for number in range(amount):
            person = person_data[number]
            _, url = person
            vbox.addWidget(Picture(url, 200), number / self.columns, number % self.columns)
            QGuiApplication.processEvents()

        self.scroll.setWidget(self.swipe_container_widget)

    def like_person(self):
        if not self.logged_in:
            self.feedback_append_line("Please login first!")
            return
        self.feedback_append_line("Liking: " + self.id)
        resp = tinder_api.like(self.id)
        if resp["match"]:
            self.feedback_append_line("It seems like she likes you to! <3")
        else:
            self.feedback_append_line("No match ... yet!")

    def superlike_person(self):
        if not self.logged_in:
            self.feedback_append_line("Please login first!")
            return
        self.feedback_append_line("Superliking: " + self.id)
        resp = tinder_api.superlike(self.id)
        if "limit_exceeded" in resp:
            self.feedback_append_line("You already used your superlike")
            return

        if resp["match"]:
            self.feedback_append_line("It seems like she likes you to! <3")
        else:
            self.feedback_append_line("No match ... yet!")
        print(resp)

    def dislike_person(self):
        if not self.logged_in:
            self.feedback_append_line("Please login first!")
            return
        self.feedback_append_line("Disliking: " + self.id)
        resp = tinder_api.dislike(self.id)
        print(resp)

    def set_new_location(self):
        if not self.logged_in:
            self.feedback_append_line("Please login first!")
            return

        lat, okPressed = QInputDialog.getText(self, "Change Location", "Latitude:")
        if okPressed:
            lon, okPressed = QInputDialog.getText(self, "Change Location", "Longitude:")
            if okPressed:
                resp = tinder_api.set_location(lat, lon)
                if resp["meta"]["status"] == 200:
                    self.feedback_append_line("Location succesfully changed!")
                else:
                    self.feedback_append_line("Location not changed (error)")

                self.fetch_recs()

    def login(self):

        email, okPressed = QInputDialog.getText(self, "Login", "fb-emailadres:")
        if okPressed:
            password, okPressed = QInputDialog.getText(self, "Login", "fb-password:", QLineEdit.Password)
            if okPressed:
                resp, code = tinder_api.get_tinder_token(email, password)
                if not resp:
                    self.feedback_append_line("Credentials are incorrect! Code: " + code)
                else:
                    self.feedback_append_line("Logged in succesfully!")
                    self.logged_in = True

                    # self.fetch_recs()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
