from scripts.packages import pd, pickle, QDialog, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QComboBox, QPushButton, QTextEdit, QMessageBox, QIcon
from scripts.textStorage import load_text
from scripts.data import PredictionStore

class ConstructionWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.model = self.load_model('models/Gradient-Boosting-A5.pkl')
        self.machinery_factors = self.get_machinery_factors()
        self.update_factors()  # Set initial values based on default selection

    def setup_ui(self):
        self.setWindowTitle("Construction Stage")
        self.setWindowIcon(QIcon("resources/images/A5-favicon.png"))
        self.setFixedSize(400, 520)

        layout = QVBoxLayout(self)

        # Instruction text
        self.construction_text = self.create_text_edit("resources/text/construction.txt")
        layout.addWidget(self.construction_text)

        # Form layout
        self.form_layout = self.create_form_layout()
        layout.addLayout(self.form_layout)

        # Result label
        self.result_label = QLabel("", self)
        layout.addWidget(self.result_label)

    def create_text_edit(self, file_path):
        text_edit = QTextEdit(self)
        text_edit.setPlainText(load_text(file_path))
        text_edit.setReadOnly(True)
        return text_edit

    def create_form_layout(self):
        form_layout = QFormLayout()

        # Machinery combo box
        self.machinery_combo = self.create_combo_box()
        self.machinery_combo.currentIndexChanged.connect(self.update_factors)

        # Input fields
        self.quantity_input = self.create_input('Enter quantity')
        self.fuel_consumption_input = self.create_input('', read_only=True)
        self.hours_input = self.create_input('Enter hours of operation')
        self.carbon_factor_input = self.create_input('', read_only=True)

        # Add widgets to form layout
        form_layout.addRow('Machinery:', self.machinery_combo)
        form_layout.addRow('Quantity:', self.quantity_input)
        form_layout.addRow('Fuel Consumption Rate:', self.fuel_consumption_input)
        form_layout.addRow('Hours of Operation:', self.hours_input)
        form_layout.addRow('Carbon Emission Factor:', self.carbon_factor_input)

        # Predict button
        predict_button = QPushButton('Predict Total Carbon Emission')
        predict_button.clicked.connect(self.predict)
        form_layout.addRow(predict_button)

        return form_layout

    def create_combo_box(self):
        combo_box = QComboBox()
        combo_box.addItems(self.get_machinery_list())
        return combo_box

    def create_input(self, placeholder_text, read_only=False):
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder_text)
        input_field.setReadOnly(read_only)
        return input_field

    def load_model(self, model_path):
        """Load the pickled model."""
        try:
            with open(model_path, 'rb') as file:
                return pickle.load(file)
        except (FileNotFoundError, pickle.UnpicklingError) as e:
            QMessageBox.critical(self, "Model Error", f"Error loading model: {str(e)}")
            return None

    def get_machinery_list(self):
        return [
            'Air compressor', 'Bulldozer', 'Concrete mixer', 'Concrete pump',
            'Crane', 'Crusher', 'Floor grinder', 'Power buggy', 'Road roller', 'Rock crusher'
        ]

    def get_machinery_factors(self):
        return {
            'Air compressor': (18, 1.6),
            'Bulldozer': (20, 1.5),
            'Concrete mixer': (18, 1.6),
            'Concrete pump': (32, 2.3),
            'Crane': (30, 2),
            'Crusher': (50, 2.8),
            'Floor grinder': (40, 2.5),
            'Power buggy': (15, 1.4),
            'Road roller': (25, 1.9),
            'Rock crusher': (40, 2.5)
        }

    def update_factors(self):
        selected_machinery = self.machinery_combo.currentText()
        fuel_consumption, carbon_factor = self.machinery_factors.get(selected_machinery, ("", ""))
        self.fuel_consumption_input.setText(str(fuel_consumption))
        self.carbon_factor_input.setText(str(carbon_factor))

    def predict(self):
        if not self.validate_inputs():
            return

        features = self.prepare_features()
        if self.model:
            try:
                prediction = self.model.predict(features)[0]
                self.store_and_display_prediction(prediction)
            except Exception as e:
                QMessageBox.critical(self, "Prediction Error", f"An error occurred during prediction: {str(e)}")
        else:
            QMessageBox.critical(self, "Model Error", "Prediction model is not loaded.")

    def validate_inputs(self):
        """Validate user inputs."""
        try:
            float(self.quantity_input.text())
            float(self.hours_input.text())
            return True
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Quantity and Hours of Operation must be numeric.")
            return False

    def prepare_features(self):
        machinery_mapping = {mach: idx for idx, mach in enumerate(self.get_machinery_list())}
        machinery_num = machinery_mapping[self.machinery_combo.currentText()]

        features = pd.DataFrame({
            'Machinery': [machinery_num],
            'Quantity': [float(self.quantity_input.text())],
            'Fuel_consumption_rate': [float(self.fuel_consumption_input.text())],
            'Hours_of_operation': [float(self.hours_input.text())],
            'Carbon_emission_factor': [float(self.carbon_factor_input.text())]
        })
        return features

    def store_and_display_prediction(self, prediction):
        self.predicted_emission = prediction
        PredictionStore().set_prediction('construction', prediction)
        self.result_label.setText(f"Predicted Total Carbon Emission: <b>{prediction:.2f} kgCO2e </b>")

    def get_prediction(self):
        return getattr(self, 'predicted_emission', 0)
