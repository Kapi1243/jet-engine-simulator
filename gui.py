from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSlider, QDoubleSpinBox, QPushButton, QCheckBox, QGroupBox, QFormLayout
)
from PyQt6.QtCore import Qt
import sys
from engine import JetEngine

class JetEngineGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jet Engine Simulator")
        self.setGeometry(100, 100, 900, 600)

        self.create_controls()
        self.create_output()

        layout = QHBoxLayout()
        layout.addWidget(self.controls_box)
        layout.addWidget(self.output_box)

        self.setLayout(layout)
        self.update_simulation()

    def create_controls(self):
        self.controls_box = QGroupBox("Engine Parameters")
        layout = QFormLayout()

        def add_spinbox(label, min_, max_, step, default):
            box = QDoubleSpinBox()
            box.setRange(min_, max_)
            box.setSingleStep(step)
            box.setValue(default)
            box.valueChanged.connect(self.update_simulation)
            layout.addRow(label, box)
            return box
        
        self.altitude = add_spinbox("Altitude (m)", 0, 30000, 100, 20000)
        self.Speed = add_spinbox("Initial Velocity (m/s)", 0, 2000, 10, 1050)
        self.comp_ratio = add_spinbox("Compression Ratio", 1, 50, 0.5, 10)
        self.fuel_air = add_spinbox("Fuel-Air Ratio", 0.01, 0.1, 0.001, 0.045)
        self.afterburner_fraction = add_spinbox("Afterburner Fuel Fraction", 0, 0.1, 0.001, 0.03)

        self.eta_comp = add_spinbox("Compressor Efficiency", 0.1, 1.0, 0.01, 0.85)
        self.eta_turb = add_spinbox("Turbine Efficiency", 0.1, 1.0, 0.01, 0.85)
        self.mechanical_eff = add_spinbox("Mechanical Efficiency", 0.1, 1.0, 0.01, 0.9)
        self.nozzle_eff = add_spinbox("Nozzle Efficiency", 0.1, 1.0, 0.01, 0.9)

        self.afterburner_checkbox = QCheckBox("Use Afterburner")
        self.afterburner_checkbox.setChecked(False)
        self.afterburner_checkbox.stateChanged.connect(self.update_simulation)
        layout.addRow(self.afterburner_checkbox)

        self.controls_box.setLayout(layout)

    def create_output(self):
        self.output_box = QGroupBox("Engine Output")
        layout = QVBoxLayout()
        self.output_labels = {}

        output_fields = [
            'Net Thrust (N)', 'Fuel Flow Rate (kg/s)', 'TSFC (mg/N·s)', 'Specific Impulse (s)', 'Thermal Efficiency (%)', 'Propulsive Efficiency (%)', 'Overall Efficiency (%)',
            'Exhaust Velocity (m/s)', 'Compressor Temp (K)', 'Combustor Temp (K)', 'Turbine/Exit Temp (K)'
        ]

        for field in output_fields:
            label = QLabel()
            layout.addWidget(label)
            self.output_labels[field] = label

        self.output_box.setLayout(layout)

    def update_simulation(self):
        engine = JetEngine(
            altitude=self.altitude.value(),
            compression_ratio=self.comp_ratio.value(),
            flight_speed=self.Speed.value(),
            fuel_air_ratio=self.fuel_air.value(),
            eta_comp=self.eta_comp.value(),
            eta_turb=self.eta_turb.value(),
            mechanical_eff=self.mechanical_eff.value(),
            nozzle_eff=self.nozzle_eff.value(),
            use_afterburner=self.afterburner_checkbox.isChecked(),
            afterburner_fuel_fraction=self.afterburner_fraction.value()
        )

        results = engine.simulate()

        def fmt(value, unit=''):
            return f"{value:.2f} {unit}" if isinstance(value, float) else str(value)
        
        self.output_labels['Net Thrust (N)'].setText(fmt(results['Net Thrust'], 'N'))
        self.output_labels['Fuel Flow Rate (kg/s)'].setText(fmt(results['Fuel Flow Rate'], 'kg/s'))
        self.output_labels['TSFC (mg/N·s)'].setText(fmt(results['TSFC'] * 1e6, 'mg/N·s'))
        self.output_labels['Specific Impulse (s)'].setText(fmt(results['Specific Impulse (Isp)'], 's'))
        self.output_labels['Thermal Efficiency (%)'].setText(fmt(results['Thermal Efficiency'] * 100, '%'))
        self.output_labels['Propulsive Efficiency (%)'].setText(fmt(results['Propulsive Efficiency'] * 100, '%'))
        self.output_labels['Overall Efficiency (%)'].setText(fmt(results['Overall Efficiency'] * 100, '%'))
        self.output_labels['Exhaust Velocity (m/s)'].setText(fmt(results['Exhaust Velocity'], 'm/s'))
        self.output_labels['Compressor Temp (K)'].setText(fmt(results['Compressor Temp (T2)'], 'K'))
        self.output_labels['Combustor Temp (K)'].setText(fmt(results['Combustor Temp (T3)'], 'K'))
        self.output_labels['Turbine/Exit Temp (K)'].setText(fmt(results['Turbine/Exit Temp'], 'K'))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JetEngineGUI()
    window.show()
    sys.exit(app.exec())