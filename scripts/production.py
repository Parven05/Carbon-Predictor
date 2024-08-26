
from scripts.packages import pd, pickle, QDialog, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QComboBox, QPushButton, QTextEdit, QMessageBox, QIcon
from scripts.textStorage import load_text
from scripts.data import PredictionStore

class ProductionWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Production Stage")
        self.setWindowIcon(QIcon("resources/images/A1-favicon.png"))
        self.setFixedSize(400, 378)

        self.model = self.load_model()
        self.carbon_factors = {
            'Aluminium': 11.0, 'Asphalt': 0.1, 'Bricks': 0.5, 'Cement': 0.9, 
            'Concrete': 0.3, 'Glass': 0.8, 'Plastics': 6.0, 'Steel': 1.8, 
            'Stone': 0.4, 'Wood': 0.2
        }

        self.setup_ui()
        self.update_carbon_factor()  # Set initial carbon factor

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Text for Production Stage page
        production_stage_text = QTextEdit(self)
        production_stage_text.setReadOnly(True)
        production_stage_text.setText(load_text("resources/text/production.txt"))
        layout.addWidget(production_stage_text)

        # Form layout for input fields
        form_layout = QFormLayout()

        self.material_combo = QComboBox()
        self.material_combo.addItems(self.carbon_factors.keys())
        self.material_combo.currentIndexChanged.connect(self.update_carbon_factor)

        self.mass_input = QLineEdit()
        self.mass_input.setPlaceholderText('Enter mass used (kg)')

        self.carbon_factor_input = QLineEdit()
        self.carbon_factor_input.setPlaceholderText('Emission factor (kgCO2/kg)')
        self.carbon_factor_input.setReadOnly(True)

        form_layout.addRow('Raw Material Type:', self.material_combo)
        form_layout.addRow('Mass Used:', self.mass_input)
        form_layout.addRow('Carbon Emission Factor:', self.carbon_factor_input)

        predict_button = QPushButton('Predict Total Carbon Emission')
        predict_button.clicked.connect(self.predict)
        form_layout.addRow(predict_button)

        layout.addLayout(form_layout)

        self.result_label = QLabel("", self)
        layout.addWidget(self.result_label)

    def load_model(self):
        try:
            with open('models/Gradient-Boosting-A1.pkl', 'rb') as file:
                return pickle.load(file)
        except (FileNotFoundError, pickle.PickleError) as e:
            QMessageBox.critical(self, "Model Load Error", f"Could not load model: {str(e)}")
            return None

    def update_carbon_factor(self):
        selected_material = self.material_combo.currentText()
        carbon_factor = self.carbon_factors.get(selected_material, "")
        self.carbon_factor_input.setText(str(carbon_factor))

    def predict(self):
        material = self.material_combo.currentText()
        mass = self.mass_input.text()
        carbon_factor = self.carbon_factor_input.text()

        if not mass or not carbon_factor:
            QMessageBox.warning(self, "Input Error", "Please provide all numeric inputs.")
            return

        try:
            mass = float(mass)
            carbon_factor = float(carbon_factor)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Mass and Carbon Emission Factor must be numeric.")
            return

        material_mapping = {mat: idx for idx, mat in enumerate(self.carbon_factors.keys())}
        material_num = material_mapping.get(material, -1)

        if material_num == -1:
            QMessageBox.warning(self, "Input Error", "Invalid material type selected.")
            return

        features = pd.DataFrame({
            'Raw_material': [material_num],
            'Mass_used': [mass],
            'Carbon_emission_factor': [carbon_factor]
        })

        if self.model:
            try:
                prediction = self.model.predict(features)[0]
                self.predicted_emission = prediction

                store = PredictionStore()
                store.set_prediction('production', prediction)

                self.result_label.setText(f"Predicted Total Carbon Emission: <b>{prediction:.2f} kgCO2e </b>")
            except Exception as e:
                QMessageBox.critical(self, "Prediction Error", f"An error occurred during prediction: {str(e)}")

    def get_prediction(self):
        return getattr(self, 'predicted_emission', 0)
