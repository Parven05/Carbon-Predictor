from scripts.packages import pd, pickle, QDialog, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QComboBox, QPushButton, QTextEdit, QMessageBox, QIcon
from scripts.textStorage import load_text
from scripts.data import PredictionStore

class FactoryWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transportation to Factory Stage")
        self.setWindowIcon(QIcon("resources/images/A2-favicon.png"))
        self.setFixedSize(400, 520)

        self.materials = [
            'Aluminium', 'Asphalt', 'Bricks', 'Cement', 'Concrete', 'Glass', 
            'Plastics', 'Steel', 'Stone', 'Wood'
        ]
        self.carbon_factors = {
            'Aluminium': 11.0, 'Asphalt': 0.1, 'Bricks': 0.5, 'Cement': 0.9, 
            'Concrete': 0.3, 'Glass': 0.8, 'Plastics': 6.0, 'Steel': 1.8, 
            'Stone': 0.4, 'Wood': 0.2
        }

        self.model = self.load_model()
        self.setup_ui()
        self.update_carbon_factor()  # Set initial carbon factor

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Text for Transportation to Factory Stage page
        transportation_text = QTextEdit(self)
        transportation_text.setReadOnly(True)
        transportation_text.setText(load_text("resources/text/transportationFactory.txt"))
        layout.addWidget(transportation_text)

        form_layout = QFormLayout()

        # Create dropdown and input fields
        self.material_combo = QComboBox()
        self.material_combo.addItems(self.materials)
        self.material_combo.currentIndexChanged.connect(self.update_carbon_factor)

        self.mass_input = QLineEdit()
        self.mass_input.setPlaceholderText('Enter mass used (kg)')

        self.distance_input = QLineEdit()
        self.distance_input.setPlaceholderText('Enter distance traveled (km)')

        self.fuel_consumption_input = QLineEdit()
        self.fuel_consumption_input.setText('0.4')
        self.fuel_consumption_input.setReadOnly(True)

        self.carbon_factor_input = QLineEdit()
        self.carbon_factor_input.setPlaceholderText('Emission factor (kgCO2/l)')
        self.carbon_factor_input.setReadOnly(True)

        # Add form widgets to the form layout
        form_layout.addRow('Material Type:', self.material_combo)
        form_layout.addRow('Mass Used:', self.mass_input)
        form_layout.addRow('Distance Traveled:', self.distance_input)
        form_layout.addRow('Fuel Consumption Rate:', self.fuel_consumption_input)
        form_layout.addRow('Carbon Emission Factor:', self.carbon_factor_input)

        predict_button = QPushButton('Predict Total Carbon Emission')
        predict_button.clicked.connect(self.predict)
        form_layout.addRow(predict_button)

        layout.addLayout(form_layout)

        # Label for displaying results
        self.result_label = QLabel("", self)
        layout.addWidget(self.result_label)

    def load_model(self):
        try:
            with open('models/Gradient-Boosting-A2.pkl', 'rb') as file:
                return pickle.load(file)
        except (FileNotFoundError, pickle.UnpicklingError) as e:
            QMessageBox.critical(self, "Model Error", f"Error loading model: {str(e)}")
            return None

    def update_carbon_factor(self):
        selected_material = self.material_combo.currentText()
        carbon_factor = self.carbon_factors.get(selected_material, "")
        self.carbon_factor_input.setText(str(carbon_factor))

    def predict(self):
        try:
            mass = float(self.mass_input.text())
            distance_traveled = float(self.distance_input.text())
            fuel_consumption = float(self.fuel_consumption_input.text())
            carbon_factor = float(self.carbon_factor_input.text())
        except ValueError:
            QMessageBox.warning(self, "Input Error", "All inputs must be numeric.")
            return

        material_num = self.materials.index(self.material_combo.currentText())

        if self.model:
            features = pd.DataFrame({
                'Raw_material': [material_num],
                'Mass_used': [mass],
                'Distance_traveled': [distance_traveled],
                'Fuel_consumption_rate': [fuel_consumption],
                'Carbon_emission_factor': [carbon_factor]
            })

            try:
                prediction = self.model.predict(features)[0]
                self.result_label.setText(f"Predicted Total Carbon Emission: <b>{prediction:.2f} kgCO2e </b>")

                store = PredictionStore()
                store.set_prediction('transportation_to_factory', prediction)
            except Exception as e:
                QMessageBox.critical(self, "Prediction Error", f"An error occurred during prediction: {str(e)}")
        else:
            QMessageBox.critical(self, "Model Error", "Prediction model is not loaded.")

    def get_prediction(self):
        return getattr(self, 'predicted_emission', 0)
