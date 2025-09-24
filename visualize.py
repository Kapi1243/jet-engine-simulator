"""
Advanced visualization and analysis tools for jet engine performance.

Provides comprehensive plotting capabilities including performance maps,
parametric studies, and comparative analysis with publication-quality figures.
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple, Optional
import seaborn as sns
from engine import JetEngine
from config import get_config, CONFIGURATIONS

# Set modern plotting style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class EngineAnalyzer:
    """Advanced analysis and visualization for jet engine performance."""
    
    def __init__(self, save_plots: bool = True, plot_format: str = 'png', dpi: int = 300):
        """Initialize analyzer with output settings."""
        self.save_plots = save_plots
        self.plot_format = plot_format
        self.dpi = dpi
    
    def plot_performance_envelope(self, config_name: str = 'civil_airliner') -> None:
        """Generate comprehensive performance envelope plots."""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle(f'Performance Envelope Analysis - {config_name.replace("_", " ").title()}', 
                    fontsize=16, fontweight='bold')
        
        base_config = get_config(config_name)
        
        # 1. Thrust vs Flight Speed at different altitudes
        speeds = np.linspace(100, 1000, 50)
        altitudes = [0, 5000, 10000, 15000, 20000]
        
        for alt in altitudes:
            thrust_data = []
            for speed in speeds:
                config = base_config
                config.altitude = alt
                config.flight_speed = speed
                engine = JetEngine(**config.__dict__)
                result = engine.simulate()
                thrust_data.append(result['Net Thrust'] / 1000)  # Convert to kN
            
            ax1.plot(speeds, thrust_data, label=f'{alt/1000:.0f} km', linewidth=2)
        
        ax1.set_xlabel('Flight Speed (m/s)', fontsize=12)
        ax1.set_ylabel('Net Thrust (kN)', fontsize=12)
        ax1.set_title('Thrust vs Speed at Various Altitudes', fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. TSFC vs Compression Ratio
        comp_ratios = np.linspace(8, 35, 30)
        tsfc_data = []
        thermal_eff_data = []
        
        for ratio in comp_ratios:
            config = base_config
            config.compression_ratio = ratio
            engine = JetEngine(**config.__dict__)
            result = engine.simulate()
            tsfc_data.append(result['TSFC'] * 1e6)  # Convert to mg/N·s
            thermal_eff_data.append(result['Thermal Efficiency'] * 100)
        
        color = 'tab:red'
        ax2.set_xlabel('Compression Ratio', fontsize=12)
        ax2.set_ylabel('TSFC (mg/N·s)', color=color, fontsize=12)
        ax2.plot(comp_ratios, tsfc_data, color=color, linewidth=2, label='TSFC')
        ax2.tick_params(axis='y', labelcolor=color)
        
        ax2_twin = ax2.twinx()
        color = 'tab:blue'
        ax2_twin.set_ylabel('Thermal Efficiency (%)', color=color, fontsize=12)
        ax2_twin.plot(comp_ratios, thermal_eff_data, color=color, linewidth=2, label='Thermal Eff.')
        ax2_twin.tick_params(axis='y', labelcolor=color)
        
        ax2.set_title('TSFC and Thermal Efficiency vs Compression Ratio', fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        # 3. Propulsive Efficiency vs Flight Speed
        speeds = np.linspace(100, 1200, 50)
        prop_eff_data = []
        overall_eff_data = []
        
        for speed in speeds:
            config = base_config
            config.flight_speed = speed
            engine = JetEngine(**config.__dict__)
            result = engine.simulate()
            prop_eff_data.append(result['Propulsive Efficiency'] * 100)
            overall_eff_data.append(result['Overall Efficiency'] * 100)
        
        ax3.plot(speeds, prop_eff_data, label='Propulsive Efficiency', linewidth=2)
        ax3.plot(speeds, overall_eff_data, label='Overall Efficiency', linewidth=2)
        ax3.set_xlabel('Flight Speed (m/s)', fontsize=12)
        ax3.set_ylabel('Efficiency (%)', fontsize=12)
        ax3.set_title('Efficiency vs Flight Speed', fontweight='bold')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. Temperature Distribution Through Engine
        config = base_config
        engine = JetEngine(**config.__dict__)
        result = engine.simulate()
        
        stations = ['Inlet\n(T0)', 'Compressor\n(T2)', 'Combustor\n(T3)', 'Turbine\n(T4)']
        temperatures = [
            engine.T0,
            result['Compressor Temp (T2)'],
            result['Combustor Temp (T3)'],
            result['Turbine/Exit Temp']
        ]
        
        bars = ax4.bar(stations, temperatures, color=['lightblue', 'orange', 'red', 'green'], alpha=0.7)
        ax4.set_ylabel('Temperature (K)', fontsize=12)
        ax4.set_title('Temperature Distribution Through Engine', fontweight='bold')
        ax4.grid(True, alpha=0.3, axis='y')
        
        # Add temperature values on bars
        for bar, temp in zip(bars, temperatures):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 20,
                    f'{temp:.0f} K', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        if self.save_plots:
            plt.savefig(f'performance_envelope_{config_name}.{self.plot_format}', dpi=self.dpi, bbox_inches='tight')
        plt.show()
    
    def compare_configurations(self) -> None:
        """Compare performance of different engine configurations."""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Engine Configuration Comparison', fontsize=16, fontweight='bold')
        
        config_names = list(CONFIGURATIONS.keys())
        metrics = {name: {} for name in config_names}
        
        # Calculate metrics for each configuration
        for name in config_names:
            config = get_config(name)
            engine = JetEngine(**config.__dict__)
            result = engine.simulate()
            
            metrics[name] = {
                'thrust': result['Net Thrust'] / 1000,  # kN
                'tsfc': result['TSFC'] * 1e6,  # mg/N·s
                'thermal_eff': result['Thermal Efficiency'] * 100,
                'overall_eff': result['Overall Efficiency'] * 100,
                'isp': result['Specific Impulse (Isp)']
            }
        
        # Bar chart comparisons
        x_pos = np.arange(len(config_names))
        labels = [name.replace('_', '\n').title() for name in config_names]
        
        # Thrust comparison
        thrust_values = [metrics[name]['thrust'] for name in config_names]
        bars1 = ax1.bar(x_pos, thrust_values, alpha=0.8)
        ax1.set_xlabel('Engine Configuration', fontsize=12)
        ax1.set_ylabel('Net Thrust (kN)', fontsize=12)
        ax1.set_title('Thrust Comparison', fontweight='bold')
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(labels)
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar, value in zip(bars1, thrust_values):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
        
        # TSFC comparison
        tsfc_values = [metrics[name]['tsfc'] for name in config_names]
        bars2 = ax2.bar(x_pos, tsfc_values, alpha=0.8, color='orange')
        ax2.set_xlabel('Engine Configuration', fontsize=12)
        ax2.set_ylabel('TSFC (mg/N·s)', fontsize=12)
        ax2.set_title('Fuel Efficiency Comparison', fontweight='bold')
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(labels)
        ax2.grid(True, alpha=0.3, axis='y')
        
        for bar, value in zip(bars2, tsfc_values):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
        
        # Efficiency comparison
        thermal_values = [metrics[name]['thermal_eff'] for name in config_names]
        overall_values = [metrics[name]['overall_eff'] for name in config_names]
        
        width = 0.35
        ax3.bar(x_pos - width/2, thermal_values, width, label='Thermal', alpha=0.8)
        ax3.bar(x_pos + width/2, overall_values, width, label='Overall', alpha=0.8)
        ax3.set_xlabel('Engine Configuration', fontsize=12)
        ax3.set_ylabel('Efficiency (%)', fontsize=12)
        ax3.set_title('Efficiency Comparison', fontweight='bold')
        ax3.set_xticks(x_pos)
        ax3.set_xticklabels(labels)
        ax3.legend()
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Specific Impulse comparison
        isp_values = [metrics[name]['isp'] for name in config_names]
        bars4 = ax4.bar(x_pos, isp_values, alpha=0.8, color='green')
        ax4.set_xlabel('Engine Configuration', fontsize=12)
        ax4.set_ylabel('Specific Impulse (s)', fontsize=12)
        ax4.set_title('Specific Impulse Comparison', fontweight='bold')
        ax4.set_xticks(x_pos)
        ax4.set_xticklabels(labels)
        ax4.grid(True, alpha=0.3, axis='y')
        
        for bar, value in zip(bars4, isp_values):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 50,
                    f'{value:.0f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        if self.save_plots:
            plt.savefig(f'configuration_comparison.{self.plot_format}', dpi=self.dpi, bbox_inches='tight')
        plt.show()
    
    def plot_afterburner_analysis(self) -> None:
        """Analyze afterburner impact on performance."""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Afterburner Performance Analysis', fontsize=16, fontweight='bold')
        
        base_config = get_config('military_fighter')
        
        # Thrust augmentation vs afterburner fuel fraction
        ab_fractions = np.linspace(0, 0.08, 30)
        thrust_ratio = []
        tsfc_ratio = []
        
        # Baseline without afterburner
        base_config.use_afterburner = False
        base_engine = JetEngine(**base_config.__dict__)
        base_result = base_engine.simulate()
        base_thrust = base_result['Net Thrust']
        base_tsfc = base_result['TSFC']
        
        for fraction in ab_fractions:
            if fraction == 0:
                thrust_ratio.append(1.0)
                tsfc_ratio.append(1.0)
            else:
                base_config.use_afterburner = True
                base_config.afterburner_fuel_fraction = fraction
                engine = JetEngine(**base_config.__dict__)
                result = engine.simulate()
                thrust_ratio.append(result['Net Thrust'] / base_thrust)
                tsfc_ratio.append(result['TSFC'] / base_tsfc)
        
        ax1.plot(ab_fractions * 100, thrust_ratio, 'b-', linewidth=2, label='Thrust Ratio')
        ax1.set_xlabel('Afterburner Fuel Fraction (%)', fontsize=12)
        ax1.set_ylabel('Thrust Augmentation Ratio', fontsize=12, color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')
        ax1.set_title('Afterburner Performance Trade-offs', fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        ax1_twin = ax1.twinx()
        ax1_twin.plot(ab_fractions * 100, tsfc_ratio, 'r--', linewidth=2, label='TSFC Ratio')
        ax1_twin.set_ylabel('TSFC Ratio', fontsize=12, color='red')
        ax1_twin.tick_params(axis='y', labelcolor='red')
        
        # Performance at different flight speeds
        speeds = np.linspace(300, 800, 20)
        thrust_no_ab = []
        thrust_with_ab = []
        
        for speed in speeds:
            base_config.flight_speed = speed
            
            # Without afterburner
            base_config.use_afterburner = False
            engine = JetEngine(**base_config.__dict__)
            result = engine.simulate()
            thrust_no_ab.append(result['Net Thrust'] / 1000)
            
            # With afterburner
            base_config.use_afterburner = True
            base_config.afterburner_fuel_fraction = 0.04
            engine = JetEngine(**base_config.__dict__)
            result = engine.simulate()
            thrust_with_ab.append(result['Net Thrust'] / 1000)
        
        ax2.plot(speeds, thrust_no_ab, 'b-', linewidth=2, label='No Afterburner')
        ax2.plot(speeds, thrust_with_ab, 'r-', linewidth=2, label='With Afterburner')
        ax2.set_xlabel('Flight Speed (m/s)', fontsize=12)
        ax2.set_ylabel('Net Thrust (kN)', fontsize=12)
        ax2.set_title('Thrust vs Speed: Afterburner Comparison', fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Temperature analysis
        base_config.flight_speed = 500  # Reset to baseline
        base_config.use_afterburner = False
        engine_no_ab = JetEngine(**base_config.__dict__)
        result_no_ab = engine_no_ab.simulate()
        
        base_config.use_afterburner = True
        base_config.afterburner_fuel_fraction = 0.04
        engine_with_ab = JetEngine(**base_config.__dict__)
        result_with_ab = engine_with_ab.simulate()
        
        stations = ['Inlet', 'Compressor', 'Combustor', 'Turbine', 'Nozzle']
        temp_no_ab = [
            engine_no_ab.T0,
            result_no_ab['Compressor Temp (T2)'],
            result_no_ab['Combustor Temp (T3)'],
            result_no_ab['Turbine/Exit Temp'],
            result_no_ab['Turbine/Exit Temp']  # Same as turbine exit for no AB
        ]
        temp_with_ab = [
            engine_with_ab.T0,
            result_with_ab['Compressor Temp (T2)'],
            result_with_ab['Combustor Temp (T3)'],
            result_with_ab['Turbine/Exit Temp'] - 200,  # Before AB
            result_with_ab['Turbine/Exit Temp']  # After AB
        ]
        
        x = np.arange(len(stations))
        width = 0.35
        
        ax3.bar(x - width/2, temp_no_ab, width, label='No Afterburner', alpha=0.8)
        ax3.bar(x + width/2, temp_with_ab, width, label='With Afterburner', alpha=0.8)
        ax3.set_xlabel('Engine Station', fontsize=12)
        ax3.set_ylabel('Temperature (K)', fontsize=12)
        ax3.set_title('Temperature Distribution Comparison', fontweight='bold')
        ax3.set_xticks(x)
        ax3.set_xticklabels(stations)
        ax3.legend()
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Fuel flow analysis
        fuel_flows = np.linspace(0, 0.08, 20)
        thrust_per_fuel = []
        
        for flow in fuel_flows:
            if flow == 0:
                base_config.use_afterburner = False
            else:
                base_config.use_afterburner = True
                base_config.afterburner_fuel_fraction = flow
            
            engine = JetEngine(**base_config.__dict__)
            result = engine.simulate()
            thrust_per_fuel.append(result['Net Thrust'] / result['Fuel Flow Rate'])
        
        ax4.plot(fuel_flows * 100, thrust_per_fuel, 'g-', linewidth=2)
        ax4.set_xlabel('Afterburner Fuel Fraction (%)', fontsize=12)
        ax4.set_ylabel('Thrust per Unit Fuel Flow (N·s/kg)', fontsize=12)
        ax4.set_title('Fuel Efficiency vs Afterburner Usage', fontweight='bold')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        if self.save_plots:
            plt.savefig(f'afterburner_analysis.{self.plot_format}', dpi=self.dpi, bbox_inches='tight')
        plt.show()

def main():
    """Run comprehensive visualization suite."""
    analyzer = EngineAnalyzer()
    
    print("🚀 Generating comprehensive engine performance analysis...")
    
    # Generate all visualizations
    analyzer.plot_performance_envelope('civil_airliner')
    analyzer.plot_performance_envelope('military_fighter')
    analyzer.compare_configurations()
    analyzer.plot_afterburner_analysis()
    
    print("✅ Analysis complete! Check generated plots for detailed insights.")

if __name__ == "__main__":
    main()