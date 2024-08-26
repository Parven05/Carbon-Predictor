from scripts.packages import QDialog, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QPushButton, QTextEdit, QMessageBox, QIcon
from scripts.textStorage import load_text
from scripts.data import PredictionStore

class TotalWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.update_predictions()

    def setup_ui(self):
        self.setWindowTitle("Total Carbon Emission")
        self.setWindowIcon(QIcon("resources/images/total-favicon.png"))
        self.setFixedSize(400, 480)

        # Main layout
        layout = QVBoxLayout(self)

        # Add instruction text
        self.emission_text = self.create_text_edit("resources/text/total.txt")
        layout.addWidget(self.emission_text)

        # Add form layout
        self.form_layout = self.create_form_layout()
        layout.addLayout(self.form_layout)

        # Result label for total
        self.result_label = QLabel("", self)
        layout.addWidget(self.result_label)

    def create_text_edit(self, file_path):
        text_edit = QTextEdit(self)
        text_edit.setPlainText(load_text(file_path))
        text_edit.setReadOnly(True)
        return text_edit

    def create_form_layout(self):
        form_layout = QFormLayout()

        # Create input fields for various stages
        self.production_input = self.create_read_only_input()
        self.transportation_to_factory_input = self.create_read_only_input()
        self.manufacturing_input = self.create_read_only_input()
        self.transportation_to_site_input = self.create_read_only_input()
        self.construction_input = self.create_read_only_input()

        # Add input fields to the form layout
        form_layout.addRow('Upro:', self.production_input)
        form_layout.addRow('Uttf:', self.transportation_to_factory_input)
        form_layout.addRow('Umat:', self.manufacturing_input)
        form_layout.addRow('Utts:', self.transportation_to_site_input)
        form_layout.addRow('Ucon:', self.construction_input)

        return form_layout

    def create_read_only_input(self):
        input_field = QLineEdit(self)
        input_field.setReadOnly(True)
        return input_field

    def update_predictions(self):
        try:
            store = PredictionStore()
            self.update_field(self.production_input, store.get_prediction('production'))
            self.update_field(self.transportation_to_factory_input, store.get_prediction('transportation_to_factory'))
            self.update_field(self.manufacturing_input, store.get_prediction('manufacturing'))
            self.update_field(self.transportation_to_site_input, store.get_prediction('transportation_to_site'))
            self.update_field(self.construction_input, store.get_prediction('construction'))
            self.update_total_emission()
        except Exception as e:
            QMessageBox.critical(self, "Initialization Error", f"An error occurred while updating predictions: {str(e)}")

    def update_field(self, field, prediction):
        level, color = self.determine_emission_level(prediction / 1000)
        field.setText(f"{prediction:.2f} kgCO2e - {level}")
        field.setStyleSheet(f"background-color: {color}; color: black;")

    def update_total_emission(self):
        store = PredictionStore()
        total_emission = sum([
            store.get_prediction('production'),
            store.get_prediction('transportation_to_factory'),
            store.get_prediction('manufacturing'),
            store.get_prediction('transportation_to_site'),
            store.get_prediction('construction')
        ])
        level, color = self.determine_emission_level(total_emission / 1000)
        self.result_label.setText(f"Calculated Total Carbon Emission: <b>{total_emission:.2f} kgCO2e</b> - <b>{level}</b>")

       # self.result_label.setStyleSheet(f"color: {color};")

    def determine_emission_level(self, emission):
        if emission <= 500:
            return "Safe", "lightgreen"
        elif 501 < emission <= 2000:
            return "Average", "yellow"
        else:
            return "Danger", "red"