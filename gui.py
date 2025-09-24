from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSlider, QDoubleSpinBox, 
    QPushButton, QCheckBox, QGroupBox, QFormLayout, QFrame, QScrollArea, QGridLayout,
    QTabWidget, QProgressBar, QSplitter, QTextEdit, QMainWindow
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor, QPixmap, QIcon
import sys
from engine import JetEngine

class JetEngineGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚀 Advanced Jet Engine Simulator")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(1000, 700)
        
        # Apply modern styling
        self.setStyleSheet(self.get_modern_stylesheet())
        
        # Create main layout with splitter for resizable panels
        self.create_ui()
        self.update_simulation()
        
    def get_modern_stylesheet(self):
        return """
        QWidget {
            background-color: #f5f5f5;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 10pt;
        }
        
        QMainWindow {
            background-color: #ffffff;
        }
        
        QGroupBox {
            font-weight: bold;
            font-size: 11pt;
            color: #2c3e50;
            border: 2px solid #bdc3c7;
            border-radius: 8px;
            margin-top: 1ex;
            padding-top: 10px;
            background-color: #ffffff;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 8px 0 8px;
            color: #2980b9;
            font-weight: bold;
        }
        
        QDoubleSpinBox, QSpinBox {
            border: 2px solid #bdc3c7;
            border-radius: 4px;
            padding: 5px;
            background-color: #ffffff;
            selection-background-color: #3498db;
            font-size: 10pt;
        }
        
        QDoubleSpinBox:focus, QSpinBox:focus {
            border-color: #3498db;
            background-color: #f8f9fa;
        }
        
        QCheckBox {
            spacing: 8px;
            font-size: 10pt;
            color: #2c3e50;
        }
        
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
        }
        
        QCheckBox::indicator:unchecked {
            border: 2px solid #bdc3c7;
            border-radius: 3px;
            background-color: #ffffff;
        }
        
        QCheckBox::indicator:checked {
            border: 2px solid #27ae60;
            border-radius: 3px;
            background-color: #27ae60;
            image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTQiIGhlaWdodD0iMTQiIHZpZXdCb3g9IjAgMCAxNCAxNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTExLjMzMzMgMy41TDUuMjQ5OTkgOS41ODMzM0wyLjY2NjY2IDciIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=);
        }
        
        QLabel {
            color: #2c3e50;
            font-size: 10pt;
            padding: 2px;
        }
        
        QTabWidget::pane {
            border: 2px solid #bdc3c7;
            border-radius: 4px;
            background-color: #ffffff;
        }
        
        QTabBar::tab {
            background-color: #ecf0f1;
            color: #2c3e50;
            border: 1px solid #bdc3c7;
            padding: 8px 15px;
            margin-right: 2px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }
        
        QTabBar::tab:selected {
            background-color: #3498db;
            color: white;
            font-weight: bold;
        }
        
        QTabBar::tab:hover {
            background-color: #d5dbdb;
        }
        
        QPushButton {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 10pt;
        }
        
        QPushButton:hover {
            background-color: #2980b9;
        }
        
        QPushButton:pressed {
            background-color: #21618c;
        }
        
        QProgressBar {
            border: 2px solid #bdc3c7;
            border-radius: 4px;
            text-align: center;
            font-weight: bold;
            color: #2c3e50;
        }
        
        QProgressBar::chunk {
            background-color: #27ae60;
            border-radius: 2px;
        }
        
        QScrollArea {
            border: 1px solid #bdc3c7;
            border-radius: 4px;
            background-color: #ffffff;
        }
        
        QFrame {
            border: 1px solid #bdc3c7;
            border-radius: 4px;
            background-color: #ffffff;
        }
        
        /* Performance indicators */
        .excellent { color: #27ae60; font-weight: bold; }
        .good { color: #f39c12; font-weight: bold; }
        .poor { color: #e74c3c; font-weight: bold; }
        """

    def create_ui(self):
        # Main horizontal splitter
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel with tabbed controls
        left_panel = self.create_controls_panel()
        
        # Right panel with results
        right_panel = self.create_results_panel()
        
        # Add panels to splitter
        main_splitter.addWidget(left_panel)
        main_splitter.addWidget(right_panel)
        main_splitter.setSizes([400, 800])  # Initial sizes
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Add header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Add splitter
        main_layout.addWidget(main_splitter)
        
        self.setLayout(main_layout)
    
    def create_header(self):
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #3498db, stop: 1 #2980b9);
                border-radius: 8px;
                padding: 10px;
            }
            QLabel {
                color: white;
                font-weight: bold;
            }
        """)
        header_frame.setFixedHeight(60)
        
        layout = QHBoxLayout(header_frame)
        
        title_label = QLabel("🚀 Advanced Jet Engine Performance Simulator")
        title_label.setStyleSheet("font-size: 16pt; font-weight: bold; color: white;")
        
        subtitle_label = QLabel("Real-time thermodynamic analysis with professional visualization")
        subtitle_label.setStyleSheet("font-size: 10pt; color: #ecf0f1;")
        
        title_layout = QVBoxLayout()
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        
        return header_frame
    
    def create_controls_panel(self):
        # Create tabbed widget for organized controls
        tab_widget = QTabWidget()
        tab_widget.setMaximumWidth(400)
        
        # Operating Conditions Tab
        conditions_tab = QWidget()
        conditions_layout = QFormLayout(conditions_tab)
        
        self.altitude = self.create_enhanced_spinbox("Altitude", 0, 50000, 500, 10000, "m", "Operating altitude above sea level")
        self.speed = self.create_enhanced_spinbox("Flight Speed", 0, 2000, 10, 250, "m/s", "Aircraft velocity through air")
        
        conditions_layout.addRow("🌍 Altitude (m):", self.altitude)
        conditions_layout.addRow("✈️ Flight Speed (m/s):", self.speed)
        
        # Add afterburner checkbox with enhanced styling
        self.afterburner_checkbox = QCheckBox("🔥 Enable Afterburner")
        self.afterburner_checkbox.setChecked(False)
        self.afterburner_checkbox.stateChanged.connect(self.update_simulation)
        self.afterburner_checkbox.setStyleSheet("font-weight: bold; color: #e74c3c;")
        conditions_layout.addRow(self.afterburner_checkbox)
        
        tab_widget.addTab(conditions_tab, "🌍 Operating Conditions")
        
        # Engine Design Tab
        design_tab = QWidget()
        design_layout = QFormLayout(design_tab)
        
        self.comp_ratio = self.create_enhanced_spinbox("Compression Ratio", 5, 50, 0.5, 10, "", "Overall pressure ratio across compressor")
        self.fuel_air = self.create_enhanced_spinbox("Fuel-Air Ratio", 0.01, 0.08, 0.001, 0.045, "", "Primary combustion fuel-to-air mass ratio")
        self.afterburner_fraction = self.create_enhanced_spinbox("Afterburner Fuel Fraction", 0, 0.1, 0.001, 0.03, "", "Additional fuel fraction for afterburner")
        
        design_layout.addRow("⚙️ Compression Ratio:", self.comp_ratio)
        design_layout.addRow("🔥 Fuel-Air Ratio:", self.fuel_air)
        design_layout.addRow("🚀 Afterburner Fraction:", self.afterburner_fraction)
        
        tab_widget.addTab(design_tab, "⚙️ Engine Design")
        
        # Component Efficiencies Tab
        efficiency_tab = QWidget()
        efficiency_layout = QFormLayout(efficiency_tab)
        
        self.eta_comp = self.create_enhanced_spinbox("Compressor Efficiency", 0.7, 0.95, 0.01, 0.85, "%", "Compressor isentropic efficiency")
        self.eta_turb = self.create_enhanced_spinbox("Turbine Efficiency", 0.7, 0.95, 0.01, 0.85, "%", "Turbine isentropic efficiency")
        self.mechanical_eff = self.create_enhanced_spinbox("Mechanical Efficiency", 0.8, 0.98, 0.01, 0.9, "%", "Mechanical transmission efficiency")
        self.nozzle_eff = self.create_enhanced_spinbox("Nozzle Efficiency", 0.85, 0.98, 0.01, 0.9, "%", "Nozzle expansion efficiency")
        
        efficiency_layout.addRow("🌪️ Compressor η:", self.eta_comp)
        efficiency_layout.addRow("⚡ Turbine η:", self.eta_turb)
        efficiency_layout.addRow("🔧 Mechanical η:", self.mechanical_eff)
        efficiency_layout.addRow("🚪 Nozzle η:", self.nozzle_eff)
        
        tab_widget.addTab(efficiency_tab, "📊 Efficiencies")
        
        # Preset Configurations Tab
        presets_tab = QWidget()
        presets_layout = QVBoxLayout(presets_tab)
        
        presets_label = QLabel("Quick Configuration Presets:")
        presets_label.setStyleSheet("font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        presets_layout.addWidget(presets_label)
        
        preset_buttons = [
            ("🛫 Civil Airliner", self.load_civil_preset),
            ("🚁 Military Fighter", self.load_military_preset),  
            ("🚀 Supersonic Transport", self.load_supersonic_preset),
            ("✈️ Regional Jet", self.load_regional_preset)
        ]
        
        for name, func in preset_buttons:
            btn = QPushButton(name)
            btn.clicked.connect(func)
            btn.setStyleSheet("text-align: left; padding: 8px;")
            presets_layout.addWidget(btn)
        
        presets_layout.addStretch()
        tab_widget.addTab(presets_tab, "🎛️ Presets")
        
        return tab_widget
    
    def create_enhanced_spinbox(self, name, min_val, max_val, step, default, unit, tooltip):
        spinbox = QDoubleSpinBox()
        spinbox.setRange(min_val, max_val)
        spinbox.setSingleStep(step)
        spinbox.setValue(default)
        spinbox.setDecimals(3 if step < 0.01 else 2)
        spinbox.setSuffix(f" {unit}" if unit else "")
        spinbox.setToolTip(f"{tooltip}\nRange: {min_val} - {max_val} {unit}")
        spinbox.valueChanged.connect(self.update_simulation)
        return spinbox

    def create_results_panel(self):
        results_widget = QWidget()
        layout = QVBoxLayout(results_widget)
        
        # Results header with status indicator
        results_header = QFrame()
        results_header.setStyleSheet("""
            QFrame {
                background-color: #34495e;
                border-radius: 6px;
                padding: 8px;
            }
            QLabel {
                color: white;
                font-weight: bold;
            }
        """)
        
        header_layout = QHBoxLayout(results_header)
        results_title = QLabel("📊 Real-time Performance Analysis")
        results_title.setStyleSheet("font-size: 12pt; color: white;")
        
        self.status_indicator = QLabel("●")
        self.status_indicator.setStyleSheet("color: #2ecc71; font-size: 14pt;")
        self.status_indicator.setToolTip("Simulation Status: Active")
        
        header_layout.addWidget(results_title)
        header_layout.addStretch()
        header_layout.addWidget(QLabel("Status:"))
        header_layout.addWidget(self.status_indicator)
        
        layout.addWidget(results_header)
        
        # Create tabbed results view
        results_tabs = QTabWidget()
        
        # Performance Summary Tab
        summary_tab = QWidget()
        summary_layout = QVBoxLayout(summary_tab)
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setStyleSheet("""
            QTextEdit {
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 10pt;
                background-color: #2c3e50;
                color: #ecf0f1;
                border: 2px solid #34495e;
                border-radius: 6px;
                padding: 10px;
            }
        """)
        summary_layout.addWidget(self.results_text)
        
        results_tabs.addTab(summary_tab, "📈 Performance Summary")
        
        # Detailed Analysis Tab
        analysis_tab = QWidget()
        analysis_layout = QVBoxLayout(analysis_tab)
        
        # Add progress bar for calculation status
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        analysis_layout.addWidget(self.progress_bar)
        
        # Key metrics display
        metrics_frame = QFrame()
        metrics_frame.setStyleSheet("""
            QFrame {
                background-color: #ecf0f1;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        metrics_layout = QGridLayout(metrics_frame)
        
        # Create metric displays
        self.thrust_display = self.create_metric_display("Thrust", "0.0", "kN", "#e74c3c")
        self.sfc_display = self.create_metric_display("SFC", "0.0", "kg/kN·h", "#3498db")
        self.efficiency_display = self.create_metric_display("Efficiency", "0.0", "%", "#2ecc71")
        self.mach_display = self.create_metric_display("Mach Number", "0.0", "", "#f39c12")
        
        metrics_layout.addWidget(self.thrust_display, 0, 0)
        metrics_layout.addWidget(self.sfc_display, 0, 1)
        metrics_layout.addWidget(self.efficiency_display, 1, 0)
        metrics_layout.addWidget(self.mach_display, 1, 1)
        
        analysis_layout.addWidget(metrics_frame)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.plot_button = QPushButton("📊 Generate Performance Plot")
        self.plot_button.clicked.connect(self.plot_performance)
        self.plot_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        
        self.export_button = QPushButton("💾 Export Results")
        self.export_button.clicked.connect(self.export_results)
        self.export_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        
        button_layout.addWidget(self.plot_button)
        button_layout.addWidget(self.export_button)
        button_layout.addStretch()
        
        analysis_layout.addLayout(button_layout)
        analysis_layout.addStretch()
        
        results_tabs.addTab(analysis_tab, "🔬 Detailed Analysis")
        
        layout.addWidget(results_tabs)
        
        return results_widget
    
    def create_metric_display(self, label, value, unit, color):
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-left: 4px solid {color};
                border-radius: 4px;
                padding: 10px;
            }}
        """)
        
        layout = QVBoxLayout(frame)
        
        label_widget = QLabel(label)
        label_widget.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 9pt;")
        
        value_widget = QLabel(f"{value} {unit}")
        value_widget.setStyleSheet("color: #2c3e50; font-size: 14pt; font-weight: bold;")
        
        layout.addWidget(label_widget)
        layout.addWidget(value_widget)
        
        # Store value widget for updates
        setattr(self, f"{label.lower().replace(' ', '_')}_value", value_widget)
        
        return frame
    
    def load_civil_preset(self):
        """Load settings optimized for civil airliner (efficient cruise)"""
        self.altitude.setValue(11000)  # Typical cruise altitude
        self.speed.setValue(250)       # Subsonic cruise speed
        self.comp_ratio.setValue(35)   # High bypass ratio
        self.fuel_air.setValue(0.03)   # Efficient fuel consumption
        self.eta_comp.setValue(0.88)   # High compressor efficiency
        self.eta_turb.setValue(0.9)    # High turbine efficiency
        self.afterburner_checkbox.setChecked(False)
        
    def load_military_preset(self):
        """Load settings for military fighter aircraft (performance)"""
        self.altitude.setValue(15000)  # Combat altitude
        self.speed.setValue(600)       # High-speed capability
        self.comp_ratio.setValue(25)   # Balanced for performance
        self.fuel_air.setValue(0.05)   # Higher fuel flow for power
        self.eta_comp.setValue(0.85)   # Military spec efficiency
        self.eta_turb.setValue(0.87)   # Military spec efficiency
        self.afterburner_checkbox.setChecked(True)
        
    def load_supersonic_preset(self):
        """Load settings for supersonic transport"""
        self.altitude.setValue(18000)  # High altitude cruise
        self.speed.setValue(650)       # Supersonic cruise
        self.comp_ratio.setValue(15)   # Optimized for supersonic
        self.fuel_air.setValue(0.055)  # High specific thrust
        self.eta_comp.setValue(0.82)   # Supersonic optimized
        self.eta_turb.setValue(0.85)   # Supersonic optimized
        self.afterburner_checkbox.setChecked(False)
        
    def load_regional_preset(self):
        """Load settings for regional jet (short-haul efficiency)"""
        self.altitude.setValue(8000)   # Lower cruise altitude
        self.speed.setValue(200)       # Regional jet speed
        self.comp_ratio.setValue(20)   # Moderate compression
        self.fuel_air.setValue(0.035)  # Efficient for short haul
        self.eta_comp.setValue(0.86)   # Good efficiency
        self.eta_turb.setValue(0.88)   # Good efficiency
        self.afterburner_checkbox.setChecked(False)
        
    def export_results(self):
        """Export current simulation results to file"""
        try:
            import json
            from datetime import datetime
            
            # Get current results
            engine = JetEngine(
                altitude=self.altitude.value(),
                compression_ratio=self.comp_ratio.value(),
                flight_speed=self.speed.value(),
                fuel_air_ratio=self.fuel_air.value(),
                eta_comp=self.eta_comp.value(),
                eta_turb=self.eta_turb.value(),
                mechanical_eff=self.mechanical_eff.value(),
                nozzle_eff=self.nozzle_eff.value(),
                afterburner_fuel_fraction=self.afterburner_fraction.value() if self.afterburner_checkbox.isChecked() else 0.0
            )
            
            results = engine.simulate()
            
            # Create export data
            export_data = {
                "timestamp": datetime.now().isoformat(),
                "configuration": {
                    "altitude_m": self.altitude.value(),
                    "flight_speed_ms": self.speed.value(),
                    "compression_ratio": self.comp_ratio.value(),
                    "fuel_air_ratio": self.fuel_air.value(),
                    "compressor_efficiency": self.eta_comp.value(),
                    "turbine_efficiency": self.eta_turb.value(),
                    "mechanical_efficiency": self.mechanical_eff.value(),
                    "nozzle_efficiency": self.nozzle_eff.value(),
                    "afterburner_enabled": self.afterburner_checkbox.isChecked(),
                    "afterburner_fuel_fraction": self.afterburner_fraction.value()
                },
                "results": results
            }
            
            # Save to file
            filename = f"jet_engine_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)
                
            self.status_indicator.setStyleSheet("color: #2ecc71; font-size: 14pt;")
            self.status_indicator.setToolTip(f"Results exported to {filename}")
            
        except Exception as e:
            self.status_indicator.setStyleSheet("color: #e74c3c; font-size: 14pt;")
            self.status_indicator.setToolTip(f"Export failed: {str(e)}")

    def update_simulation(self):
        try:
            # Show progress
            if hasattr(self, 'progress_bar'):
                self.progress_bar.setVisible(True)
                self.progress_bar.setValue(20)
                
            engine = JetEngine(
                altitude=self.altitude.value(),
                compression_ratio=self.comp_ratio.value(),
                flight_speed=self.speed.value(),
                fuel_air_ratio=self.fuel_air.value(),
                eta_comp=self.eta_comp.value(),
                eta_turb=self.eta_turb.value(),
                mechanical_eff=self.mechanical_eff.value(),
                nozzle_eff=self.nozzle_eff.value(),
                use_afterburner=self.afterburner_checkbox.isChecked(),
                afterburner_fuel_fraction=self.afterburner_fraction.value()
            )

            if hasattr(self, 'progress_bar'):
                self.progress_bar.setValue(60)
                
            results = engine.simulate()
            
            if hasattr(self, 'progress_bar'):
                self.progress_bar.setValue(80)

            # Update results text with enhanced formatting
            if hasattr(self, 'results_text'):
                self.update_results_display(results)
            
            # Update metric displays
            self.update_metric_displays(results)
            
            # Update legacy output labels if they exist
            if hasattr(self, 'output_labels'):
                def fmt(value, unit=''):
                    return f"{value:.2f} {unit}" if isinstance(value, float) else str(value)
                
                if 'Net Thrust' in results:
                    self.output_labels['Net Thrust (N)'].setText(fmt(results['Net Thrust'], 'N'))
                if 'Fuel Flow Rate' in results:
                    self.output_labels['Fuel Flow Rate (kg/s)'].setText(fmt(results['Fuel Flow Rate'], 'kg/s'))
                # Add other fields as needed
            
            # Update status
            if hasattr(self, 'status_indicator'):
                self.status_indicator.setStyleSheet("color: #2ecc71; font-size: 14pt;")
                self.status_indicator.setToolTip("Simulation Status: Complete")
                
            if hasattr(self, 'progress_bar'):
                self.progress_bar.setValue(100)
                self.progress_bar.setVisible(False)
                
        except Exception as e:
            if hasattr(self, 'status_indicator'):
                self.status_indicator.setStyleSheet("color: #e74c3c; font-size: 14pt;")
                self.status_indicator.setToolTip(f"Simulation Error: {str(e)}")
            if hasattr(self, 'progress_bar'):
                self.progress_bar.setVisible(False)
    
    def update_results_display(self, results):
        """Update the main results text display with enhanced formatting"""
        output_lines = []
        output_lines.append("=" * 60)
        output_lines.append("🚀 JET ENGINE PERFORMANCE ANALYSIS")
        output_lines.append("=" * 60)
        output_lines.append("")
        
        # Operating Conditions
        output_lines.append("🌍 OPERATING CONDITIONS:")
        output_lines.append(f"   Altitude:           {self.altitude.value():>10.0f} m")
        output_lines.append(f"   Flight Speed:       {self.speed.value():>10.1f} m/s")
        output_lines.append(f"   Afterburner:        {'Enabled' if self.afterburner_checkbox.isChecked() else 'Disabled':>10}")
        output_lines.append("")
        
        # Engine Configuration
        output_lines.append("⚙️ ENGINE CONFIGURATION:")
        output_lines.append(f"   Compression Ratio:  {self.comp_ratio.value():>10.1f}")
        output_lines.append(f"   Fuel-Air Ratio:     {self.fuel_air.value():>10.4f}")
        output_lines.append(f"   Compressor η:       {self.eta_comp.value():>10.1%}")
        output_lines.append(f"   Turbine η:          {self.eta_turb.value():>10.1%}")
        output_lines.append("")
        
        # Performance Results
        output_lines.append("📊 PERFORMANCE RESULTS:")
        if 'Net Thrust' in results:
            output_lines.append(f"   Net Thrust:         {results['Net Thrust']:>10.0f} N")
        if 'Fuel Flow Rate' in results:
            output_lines.append(f"   Fuel Flow Rate:     {results['Fuel Flow Rate']:>10.3f} kg/s")
        if 'TSFC' in results:
            output_lines.append(f"   TSFC:               {results['TSFC']*1e6:>10.2f} mg/N·s")
        if 'Specific Impulse (Isp)' in results:
            output_lines.append(f"   Specific Impulse:   {results['Specific Impulse (Isp)']:>10.1f} s")
        if 'Overall Efficiency' in results:
            output_lines.append(f"   Overall Efficiency: {results['Overall Efficiency']*100:>10.1f} %")
        if 'Exhaust Velocity' in results:
            output_lines.append(f"   Exhaust Velocity:   {results['Exhaust Velocity']:>10.1f} m/s")
        
        output_lines.append("")
        output_lines.append("=" * 60)
        
        self.results_text.setText("\n".join(output_lines))
    
    def update_metric_displays(self, results):
        """Update the key metric display cards"""
        try:
            # Update thrust display
            if hasattr(self, 'thrust_value') and 'Net Thrust' in results:
                thrust_kn = results['Net Thrust'] / 1000  # Convert N to kN
                self.thrust_value.setText(f"{thrust_kn:.1f} kN")
            
            # Update SFC display  
            if hasattr(self, 'sfc_value') and 'TSFC' in results:
                sfc_kg_kn_h = results['TSFC'] * 3.6  # Convert to kg/kN·h
                self.sfc_value.setText(f"{sfc_kg_kn_h:.2f} kg/kN·h")
            
            # Update efficiency display
            if hasattr(self, 'efficiency_value') and 'Overall Efficiency' in results:
                self.efficiency_value.setText(f"{results['Overall Efficiency']*100:.1f}%")
            
            # Update Mach number display
            if hasattr(self, 'mach_number_value'):
                # Calculate Mach number from speed and temperature
                import math
                gamma = 1.4  # Heat capacity ratio for air
                R = 287     # Gas constant for air (J/kg·K)
                # Use ambient temperature from results or calculate from altitude
                if 'Ambient Temperature' in results:
                    temp = results['Ambient Temperature']
                else:
                    # Standard atmosphere approximation: T = 288.15 - 0.0065*h
                    temp = 288.15 - 0.0065 * self.altitude.value()
                    if temp < 216.65:  # Stratosphere temperature
                        temp = 216.65
                        
                a = math.sqrt(gamma * R * temp)  # Speed of sound
                mach = self.speed.value() / a
                self.mach_number_value.setText(f"{mach:.2f}")
                    
        except Exception as e:
            pass  # Silently handle metric update errors

    def plot_performance(self):
        """Generate and display performance plots using the visualize module"""
        try:
            import matplotlib.pyplot as plt
            
            # Get current engine configuration
            current_config = {
                'altitude': self.altitude.value(),
                'compression_ratio': self.comp_ratio.value(), 
                'flight_speed': self.speed.value(),
                'fuel_air_ratio': self.fuel_air.value(),
                'eta_comp': self.eta_comp.value(),
                'eta_turb': self.eta_turb.value(),
                'mechanical_eff': self.mechanical_eff.value(),
                'nozzle_eff': self.nozzle_eff.value(),
                'use_afterburner': self.afterburner_checkbox.isChecked(),
                'afterburner_fuel_fraction': self.afterburner_fraction.value()
            }
            
            # Create performance analysis plots
            fig, axes = plt.subplots(2, 2, figsize=(12, 10))
            fig.suptitle('🚀 Jet Engine Performance Analysis', fontsize=16, fontweight='bold')
            
            # Plot 1: Thrust vs Altitude
            altitudes = range(0, 25001, 2000)
            thrusts = []
            for alt in altitudes:
                engine = JetEngine(
                    altitude=alt,
                    compression_ratio=current_config['compression_ratio'],
                    flight_speed=current_config['flight_speed'],
                    fuel_air_ratio=current_config['fuel_air_ratio'],
                    eta_comp=current_config['eta_comp'],
                    eta_turb=current_config['eta_turb'],
                    mechanical_eff=current_config['mechanical_eff'],
                    nozzle_eff=current_config['nozzle_eff'],
                    use_afterburner=current_config['use_afterburner'],
                    afterburner_fuel_fraction=current_config['afterburner_fuel_fraction']
                )
                result = engine.simulate()
                thrusts.append(result['Net Thrust'] / 1000)  # Convert to kN
            
            axes[0,0].plot(altitudes, thrusts, 'b-', linewidth=2, label='Current Config')
            axes[0,0].axvline(current_config['altitude'], color='r', linestyle='--', alpha=0.7, label='Current Altitude')
            axes[0,0].set_xlabel('Altitude (m)')
            axes[0,0].set_ylabel('Thrust (kN)')
            axes[0,0].set_title('Thrust vs Altitude')
            axes[0,0].grid(True, alpha=0.3)
            axes[0,0].legend()
            
            # Plot 2: Efficiency vs Flight Speed
            speeds = range(100, 801, 50)
            efficiencies = []
            for speed in speeds:
                engine = JetEngine(
                    altitude=current_config['altitude'],
                    compression_ratio=current_config['compression_ratio'],
                    flight_speed=speed,
                    fuel_air_ratio=current_config['fuel_air_ratio'],
                    eta_comp=current_config['eta_comp'],
                    eta_turb=current_config['eta_turb'],
                    mechanical_eff=current_config['mechanical_eff'],
                    nozzle_eff=current_config['nozzle_eff'],
                    use_afterburner=current_config['use_afterburner'],
                    afterburner_fuel_fraction=current_config['afterburner_fuel_fraction']
                )
                result = engine.simulate()
                efficiencies.append(result['Overall Efficiency'] * 100)
            
            axes[0,1].plot(speeds, efficiencies, 'g-', linewidth=2, label='Overall Efficiency')
            axes[0,1].axvline(current_config['flight_speed'], color='r', linestyle='--', alpha=0.7, label='Current Speed')
            axes[0,1].set_xlabel('Flight Speed (m/s)')
            axes[0,1].set_ylabel('Overall Efficiency (%)')
            axes[0,1].set_title('Efficiency vs Flight Speed')
            axes[0,1].grid(True, alpha=0.3)
            axes[0,1].legend()
            
            # Plot 3: TSFC vs Compression Ratio
            comp_ratios = [x for x in range(8, 41, 2)]  # 8 to 40 in steps of 2
            tsfcs = []
            for cr in comp_ratios:
                engine = JetEngine(
                    altitude=current_config['altitude'],
                    compression_ratio=cr,
                    flight_speed=current_config['flight_speed'],
                    fuel_air_ratio=current_config['fuel_air_ratio'],
                    eta_comp=current_config['eta_comp'],
                    eta_turb=current_config['eta_turb'],
                    mechanical_eff=current_config['mechanical_eff'],
                    nozzle_eff=current_config['nozzle_eff'],
                    use_afterburner=current_config['use_afterburner'],
                    afterburner_fuel_fraction=current_config['afterburner_fuel_fraction']
                )
                result = engine.simulate()
                tsfcs.append(result['TSFC'] * 1e6)  # Convert to mg/N·s
            
            axes[1,0].plot(comp_ratios, tsfcs, 'm-', linewidth=2, label='TSFC')
            axes[1,0].axvline(current_config['compression_ratio'], color='r', linestyle='--', alpha=0.7, label='Current CR')
            axes[1,0].set_xlabel('Compression Ratio')
            axes[1,0].set_ylabel('TSFC (mg/N·s)')
            axes[1,0].set_title('Fuel Consumption vs Compression Ratio')
            axes[1,0].grid(True, alpha=0.3)
            axes[1,0].legend()
            
            # Plot 4: Current Engine Performance Summary
            axes[1,1].axis('off')
            
            # Get current performance
            engine = JetEngine(
                altitude=current_config['altitude'],
                compression_ratio=current_config['compression_ratio'],
                flight_speed=current_config['flight_speed'],
                fuel_air_ratio=current_config['fuel_air_ratio'],
                eta_comp=current_config['eta_comp'],
                eta_turb=current_config['eta_turb'],
                mechanical_eff=current_config['mechanical_eff'],
                nozzle_eff=current_config['nozzle_eff'],
                use_afterburner=current_config['use_afterburner'],
                afterburner_fuel_fraction=current_config['afterburner_fuel_fraction']
            )
            result = engine.simulate()
            
            summary_text = f"""Current Performance:
            
• Thrust: {result['Net Thrust']/1000:.1f} kN
• TSFC: {result['TSFC']*1e6:.1f} mg/N·s  
• Overall η: {result['Overall Efficiency']*100:.1f}%
• Isp: {result['Specific Impulse (Isp)']:.0f} s

Operating Point:
• Altitude: {current_config['altitude']:,.0f} m
• Speed: {current_config['flight_speed']:.0f} m/s
• Comp. Ratio: {current_config['compression_ratio']:.1f}
• Afterburner: {'ON' if current_config['use_afterburner'] else 'OFF'}"""
            
            axes[1,1].text(0.05, 0.95, summary_text, transform=axes[1,1].transAxes, 
                          fontsize=11, verticalalignment='top', fontfamily='monospace',
                          bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.8))
            
            plt.tight_layout()
            plt.show()
            
            # Update status
            if hasattr(self, 'status_indicator'):
                self.status_indicator.setStyleSheet("color: #2ecc71; font-size: 14pt;")
                self.status_indicator.setToolTip("Performance plots generated successfully")
                
        except Exception as e:
            if hasattr(self, 'status_indicator'):
                self.status_indicator.setStyleSheet("color: #e74c3c; font-size: 14pt;")
                self.status_indicator.setToolTip(f"Plot generation failed: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JetEngineGUI()
    window.show()
    sys.exit(app.exec())