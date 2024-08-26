from scripts.packages import pd, pickle, QDialog, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QComboBox, QPushButton, QTextEdit, QMessageBox, QIcon
from scripts.textStorage import load_text
from scripts.data import PredictionStore

class ManufacturingWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.model = self.load_model()
        self.setup_ui()
        self.update_fuel_consumption()

    def setup_ui(self):
        self.setWindowTitle("Manufacturing Stage")
        self.setWindowIcon(QIcon("resources/images/A3-favicon.png"))
        self.setFixedSize(400, 520)

        layout = QVBoxLayout(self)

        # Add text edit widget
        self.manufacturing_text = self.create_text_edit("resources/text/manufacturing.txt")
        layout.addWidget(self.manufacturing_text)

        # Add form layout
        self.form_layout = self.create_form_layout()
        layout.addLayout(self.form_layout)

        # Add result label
        self.result_label = QLabel("", self)
        layout.addWidget(self.result_label)

    def create_text_edit(self, file_path):
        text_edit = QTextEdit(self)
        text_edit.setPlainText(load_text(file_path))
        text_edit.setReadOnly(True)
        return text_edit

    def create_form_layout(self):
        form_layout = QFormLayout()

        # Equipment selection
        self.equipment_combo = self.create_combo_box()
        self.equipment_combo.currentIndexChanged.connect(self.update_fuel_consumption)

        # Quantity input
        self.quantity_input = self.create_input('Enter quantity')

        # Fuel consumption input (read-only)
        self.fuel_consumption_input = self.create_input('Fuel consumption (litres/h)', read_only=True)

        # Hours input
        self.hours_input = self.create_input('Enter hours of operation')

        # Carbon factor input (read-only), default value set to 0.5
        self.carbon_factor_input = self.create_input(read_only=True)
        self.carbon_factor_input.setText('0.5')  # Set default value

        # Add widgets to form layout
        form_layout.addRow('Manufacturing Equipment:', self.equipment_combo)
        form_layout.addRow('Quantity:', self.quantity_input)
        form_layout.addRow('Fuel Consumption Rate:', self.fuel_consumption_input)
        form_layout.addRow('Hours of Operation:', self.hours_input)
        form_layout.addRow('Carbon Emission Factor:', self.carbon_factor_input)

        # Predict button
        predict_button = QPushButton('Predict Total Carbon Emission')
        predict_button.clicked.connect(self.predict)
        form_layout.addRow(predict_button)

        return form_layout

    def create_input(self, placeholder_text='', read_only=False):
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder_text)
        input_field.setReadOnly(read_only)
        return input_field

    def create_combo_box(self):
        combo_box = QComboBox()
        equipment_types = {
            'Bending machine': 7,
            'Drill press': 2,
            'Electric furnace': 50,
            'Extruder': 25,
            'Forklift': 4,
            'Generator': 10,
            'Hydraulic press': 10,
            'Laser cutter': 8,
            'Sandblaster': 10,
            'Welding machine': 15
        }
        combo_box.addItems(equipment_types.keys())
        self.equipment_types = equipment_types
        return combo_box

    def load_model(self):
        try:
            with open('models/Gradient-Boosting-A3.pkl', 'rb') as file:
                return pickle.load(file)
        except (FileNotFoundError, pickle.UnpicklingError) as e:
            QMessageBox.critical(self, "Model Error", f"Error loading model: {str(e)}")
            return None

    def update_fuel_consumption(self):
        selected_equipment = self.equipment_combo.currentText()
        fuel_consumption = self.equipment_types.get(selected_equipment, "")
        self.fuel_consumption_input.setText(str(fuel_consumption))

    def predict(self):
        try:
            quantity, fuel_consumption, hours, carbon_factor = self.get_numeric_inputs()
            equipment_num = self.get_equipment_num()

            features = pd.DataFrame({
                'Manufacturing_equipment': [equipment_num],
                'Quantity': [quantity],
                'Fuel_consumption_rate': [fuel_consumption],
                'Hours_of_operation': [hours],
                'Carbon_emission_factor': [carbon_factor]
            })

            if self.model:
                prediction = self.model.predict(features)[0]
                self.store_prediction(prediction)
                self.result_label.setText(f"Predicted Total Carbon Emission: <b>{prediction:.2f} kgCO2e </b>")
            else:
                QMessageBox.critical(self, "Model Error", "Prediction model is not loaded.")
        except ValueError as e:
            QMessageBox.warning(self, "Input Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Prediction Error", f"An error occurred during prediction: {str(e)}")

    def get_numeric_inputs(self):
        try:
            quantity = float(self.quantity_input.text())
            fuel_consumption = float(self.fuel_consumption_input.text())
            hours = float(self.hours_input.text())
            carbon_factor = float(self.carbon_factor_input.text())
            return quantity, fuel_consumption, hours, carbon_factor
        except ValueError:
            raise ValueError("Quantity, Fuel Consumption, Hours of Operation, and Carbon Emission Factor must be numeric.")

    def get_equipment_num(self):
        equipment_mapping = {equip: idx for idx, equip in enumerate(self.equipment_types.keys())}
        equipment_num = equipment_mapping.get(self.equipment_combo.currentText(), -1)
        if equipment_num == -1:
            raise ValueError("Invalid equipment type selected.")
        return equipment_num

    def store_prediction(self, prediction):
        store = PredictionStore()
        store.set_prediction('manufacturing', prediction)
        self.predicted_emission = prediction

    def get_prediction(self):
        return getattr(self, 'predicted_emission', 0)
