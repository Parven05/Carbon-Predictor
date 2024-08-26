from scripts.packages import pd, pickle, QDialog, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QComboBox, QPushButton, QTextEdit, QMessageBox, QIcon
from scripts.textStorage import load_text
from scripts.data import PredictionStore

class SiteWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.material_factors = {
            'AAC blocks': 0.6, 'Aluminium studs': 11, 'Cement board': 0.7,
            'Door frame': 0.6, 'Duct tape': 0.3, 'Fiberboard': 0.6,
            'Metal siding': 2.5, 'Resins': 7.5, 'Stainless steel': 4, 'Stone wool': 3
        }
        self.materials = list(self.material_factors.keys())
        self.setup_ui()
        self.model = self.load_model()
        self.update_carbon_factor()  # Set initial carbon factor based on default selection

    def setup_ui(self):
        self.setWindowTitle("Transportation to Site Stage")
        self.setWindowIcon(QIcon("resources/images/A4-favicon.png"))
        self.setFixedSize(400, 520)

        layout = QVBoxLayout(self)

        # Instructional text
        self.transportation_text = self.create_text_edit("resources/text/transportationSite.txt")
        layout.addWidget(self.transportation_text)

        # Form Layout
        self.form_layout = self.create_form_layout()
        layout.addLayout(self.form_layout)

        # Result Label
        self.result_label = QLabel("", self)
        layout.addWidget(self.result_label)

    def create_text_edit(self, file_path):
        text_edit = QTextEdit(self)
        text_edit.setPlainText(load_text(file_path))
        text_edit.setReadOnly(True)
        return text_edit

    def create_form_layout(self):
        form_layout = QFormLayout()

        # Material combo box
        self.material_combo = self.create_combo_box()
        self.material_combo.currentIndexChanged.connect(self.update_carbon_factor)

        # Input fields
        self.mass_input = self.create_input('Enter mass used (kg)')
        self.distance_input = self.create_input('Enter distance traveled (km)')
        
        # Fuel consumption input (fixed value set directly)
        self.fuel_consumption_input = self.create_input(read_only=True)
        self.fuel_consumption_input.setText('0.4')  # Set default value

        # Carbon factor input (set value based on selection)
        self.carbon_factor_input = self.create_input('', read_only=True)

        # Add widgets to form layout
        form_layout.addRow('Material Type:', self.material_combo)
        form_layout.addRow('Mass Used:', self.mass_input)
        form_layout.addRow('Distance Traveled:', self.distance_input)
        form_layout.addRow('Fuel Consumption Rate:', self.fuel_consumption_input)
        form_layout.addRow('Carbon Emission Factor:', self.carbon_factor_input)

        # Predict button
        predict_button = QPushButton('Predict Total Carbon Emission')
        predict_button.clicked.connect(self.predict)
        form_layout.addRow(predict_button)

        return form_layout

    def create_combo_box(self):
        combo_box = QComboBox()
        combo_box.addItems(self.materials)
        return combo_box

    def create_input(self, placeholder_text='', read_only=False):
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder_text)
        input_field.setReadOnly(read_only)
        return input_field

    def load_model(self):
        model_path = 'models/Gradient-Boosting-A4.pkl'
        try:
            with open(model_path, 'rb') as file:
                return pickle.load(file)
        except (FileNotFoundError, pickle.UnpicklingError) as e:
            QMessageBox.critical(self, "Model Error", f"Error loading model: {str(e)}")
            return None

    def update_carbon_factor(self):
        selected_material = self.material_combo.currentText()
        carbon_factor = self.material_factors.get(selected_material, "")
        self.carbon_factor_input.setText(str(carbon_factor))

    def predict(self):
        try:
            material = self.material_combo.currentText()
            mass = float(self.mass_input.text())
            distance_traveled = float(self.distance_input.text())
            fuel_consumption = float(self.fuel_consumption_input.text())
            carbon_factor = float(self.carbon_factor_input.text())

            material_num = self.materials.index(material)
            features = pd.DataFrame({
                'Materials': [material_num],
                'Mass_used': [mass],
                'Distance_traveled': [distance_traveled],
                'Fuel_consumption_rate': [fuel_consumption],
                'Carbon_emission_factor': [carbon_factor]
            })

            if self.model:
                prediction = self.model.predict(features)[0]
                self.store_prediction(prediction)
                self.result_label.setText(f"Predicted Total Carbon Emission: <b>{prediction:.2f} kgCO2e </b>")
            else:
                QMessageBox.critical(self, "Model Error", "Prediction model is not loaded.")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "All inputs must be numeric.")
        except Exception as e:
            QMessageBox.critical(self, "Prediction Error", f"An error occurred during prediction: {str(e)}")

    def store_prediction(self, prediction):
        store = PredictionStore()
        store.set_prediction('transportation_to_site', prediction)
        self.predicted_emission = prediction

    def get_prediction(self):
        return getattr(self, 'predicted_emission', 0)
