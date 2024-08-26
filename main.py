from scripts.packages import sys, QIcon, QMenuBar, QAction, QWidget, QVBoxLayout, Qt, QLabel, QTextEdit, QPixmap, QApplication, QMainWindow
from scripts.textStorage import load_text
from scripts.production import ProductionWindow
from scripts.transportationFactory import FactoryWindow
from scripts.manufacturing import ManufacturingWindow
from scripts.transportationSite import SiteWindow 
from scripts.construction import ConstructionWindow
from scripts.total import TotalWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Smart Carbon Predictor")
        self.setWindowIcon(QIcon("resources/images/favicon.png"))
        self.setFixedSize(680, 560)

        self.setup_menu()
        self.setup_ui()

    def setup_menu(self):
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        buttons = [
            "Production",
            "Transportation to Factory",
            "Manufacturing",
            "Transportation to Site",
            "Construction",
            "Total Carbon Emission"
        ]

        for btn_text in buttons:
            action = QAction(btn_text, self)
            action.triggered.connect(lambda _, text=btn_text: self.on_button_clicked(text))
            menu_bar.addAction(action)

    def setup_ui(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(Qt.AlignCenter)

        self.image_label = QLabel(self)
        self.layout.addWidget(self.image_label)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.text_edit.setText(load_text("resources/text/welcome.txt"))
        self.layout.addWidget(self.text_edit)

        self.show_welcome_screen()

    def show_welcome_screen(self):
        pixmap = QPixmap("resources/images/logo.png")
        self.image_label.setPixmap(pixmap.scaled(
            300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.show()
        self.text_edit.show()

    def on_button_clicked(self, button_name):
        if button_name == "Production":
            self.open_window(ProductionWindow())
        elif button_name == "Transportation to Factory": 
            self.open_window(FactoryWindow())
        elif button_name == "Manufacturing":
            self.open_window(ManufacturingWindow())
        elif button_name == "Transportation to Site":
            self.open_window(SiteWindow())
        elif button_name == "Construction":
            self.open_window(ConstructionWindow())
        elif button_name == "Total Carbon Emission":
            self.open_window(TotalWindow())

    def open_window(self, window):
        window.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("styles.qss", "r") as file:
        app.setStyleSheet(file.read())

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
