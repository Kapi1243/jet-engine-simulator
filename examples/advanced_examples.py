"""
Advanced Examples - Jet Engine Performance Optimization

This module demonstrates advanced usage patterns and optimization techniques
for the jet engine simulator, showcasing professional software engineering practices.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional
from scipy.optimize import minimize, differential_evolution
from engine import JetEngine
from config import EngineConfig, get_config

class EngineOptimizer:
    """Advanced optimization framework for jet engine design parameters."""
    
    def __init__(self, base_config: EngineConfig):
        self.base_config = base_config
        self.optimization_history: List[Dict] = []
    
    def objective_function(self, params: np.ndarray, objective: str = 'fuel_efficiency') -> float:
        """
        Multi-objective optimization function.
        
        Args:
            params: Array of optimization parameters [compression_ratio, fuel_air_ratio, ...]
            objective: Optimization target ('fuel_efficiency', 'thrust', 'overall_efficiency')
        """
        try:
            # Update configuration with optimization parameters
            config = self.base_config
            config.compression_ratio = params[0]
            config.fuel_air_ratio = params[1]
            config.eta_comp = params[2]
            config.eta_turb = params[3]
            
            # Validate parameters are within bounds
            config.validate()
            
            # Run simulation
            engine = JetEngine(**config.__dict__)
            result = engine.simulate()
            
            # Calculate objective based on target
            if objective == 'fuel_efficiency':
                # Minimize TSFC (lower is better)
                obj_value = result['TSFC']
            elif objective == 'thrust':
                # Maximize thrust (minimize negative thrust)
                obj_value = -result['Net Thrust']
            elif objective == 'overall_efficiency':
                # Maximize overall efficiency
                obj_value = -result['Overall Efficiency']
            else:
                raise ValueError(f"Unknown objective: {objective}")
            
            # Store optimization history
            self.optimization_history.append({
                'params': params.copy(),
                'objective_value': obj_value,
                'result': result
            })
            
            return obj_value
            
        except (ValueError, Exception) as e:
            # Return high penalty for invalid configurations
            return 1e6
    
    def optimize_engine(self, objective: str = 'fuel_efficiency', 
                       method: str = 'differential_evolution') -> Dict:
        """
        Perform multi-parameter optimization of engine design.
        
        Args:
            objective: Optimization target
            method: Optimization algorithm ('minimize', 'differential_evolution')
        """
        # Define parameter bounds [min, max]
        bounds = [
            (5.0, 40.0),    # compression_ratio
            (0.020, 0.070), # fuel_air_ratio  
            (0.70, 0.95),   # eta_comp
            (0.70, 0.95),   # eta_turb
        ]
        
        # Initial guess
        x0 = [
            self.base_config.compression_ratio,
            self.base_config.fuel_air_ratio,
            self.base_config.eta_comp,
            self.base_config.eta_turb
        ]
        
        print(f"🎯 Optimizing for {objective}...")
        print(f"Initial parameters: CR={x0[0]:.1f}, F/A={x0[1]:.3f}, η_c={x0[2]:.2f}, η_t={x0[3]:.2f}")
        
        if method == 'differential_evolution':
            # Global optimization - better for multi-modal problems
            result = differential_evolution(
                lambda x: self.objective_function(x, objective),
                bounds,
                maxiter=100,
                popsize=15,
                seed=42
            )
        else:
            # Local optimization - faster but may find local minima
            result = minimize(
                lambda x: self.objective_function(x, objective),
                x0,
                method='L-BFGS-B',
                bounds=bounds
            )
        
        # Extract optimized configuration
        optimal_params = result.x
        optimal_config = self.base_config
        optimal_config.compression_ratio = optimal_params[0]
        optimal_config.fuel_air_ratio = optimal_params[1]
        optimal_config.eta_comp = optimal_params[2]
        optimal_config.eta_turb = optimal_params[3]
        
        # Run final simulation with optimal parameters
        optimal_engine = JetEngine(**optimal_config.__dict__)
        optimal_result = optimal_engine.simulate()
        
        optimization_summary = {
            'success': result.success,
            'optimal_params': optimal_params,
            'optimal_config': optimal_config,
            'optimal_result': optimal_result,
            'optimization_result': result,
            'improvement_metrics': self._calculate_improvements(optimal_result, objective)
        }
        
        print(f"✅ Optimization complete!")
        print(f"Optimal parameters: CR={optimal_params[0]:.1f}, F/A={optimal_params[1]:.3f}, η_c={optimal_params[2]:.2f}, η_t={optimal_params[3]:.2f}")
        
        return optimization_summary
    
    def _calculate_improvements(self, optimal_result: Dict, objective: str) -> Dict:
        """Calculate performance improvements from optimization."""
        # Run baseline simulation
        baseline_engine = JetEngine(**self.base_config.__dict__)
        baseline_result = baseline_engine.simulate()
        
        improvements = {}
        for metric in ['Net Thrust', 'TSFC', 'Overall Efficiency', 'Thermal Efficiency']:
            baseline_value = baseline_result[metric]
            optimal_value = optimal_result[metric]
            
            if metric == 'TSFC':
                # Lower TSFC is better
                improvement = (baseline_value - optimal_value) / baseline_value * 100
            else:
                # Higher values are better
                improvement = (optimal_value - baseline_value) / baseline_value * 100
            
            improvements[metric] = improvement
        
        return improvements
    
    def plot_optimization_history(self) -> None:
        """Visualize optimization convergence history."""
        if not self.optimization_history:
            print("No optimization history available")
            return
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Engine Optimization Convergence History', fontsize=16, fontweight='bold')
        
        iterations = range(len(self.optimization_history))
        
        # Objective function convergence
        obj_values = [entry['objective_value'] for entry in self.optimization_history]
        ax1.plot(iterations, obj_values, 'b-', linewidth=2)
        ax1.set_xlabel('Iteration')
        ax1.set_ylabel('Objective Function Value')
        ax1.set_title('Convergence History')
        ax1.grid(True, alpha=0.3)
        
        # Parameter evolution
        compression_ratios = [entry['params'][0] for entry in self.optimization_history]
        fuel_air_ratios = [entry['params'][1] for entry in self.optimization_history]
        
        ax2.plot(iterations, compression_ratios, 'r-', linewidth=2, label='Compression Ratio')
        ax2.set_xlabel('Iteration')
        ax2.set_ylabel('Compression Ratio')
        ax2.set_title('Parameter Evolution - Compression Ratio')
        ax2.grid(True, alpha=0.3)
        
        ax3.plot(iterations, fuel_air_ratios, 'g-', linewidth=2, label='Fuel-Air Ratio')
        ax3.set_xlabel('Iteration')
        ax3.set_ylabel('Fuel-Air Ratio')
        ax3.set_title('Parameter Evolution - Fuel-Air Ratio')
        ax3.grid(True, alpha=0.3)
        
        # Performance metrics evolution
        thrust_values = [entry['result']['Net Thrust'] / 1000 for entry in self.optimization_history]
        tsfc_values = [entry['result']['TSFC'] * 1e6 for entry in self.optimization_history]
        
        ax4_twin = ax4.twinx()
        line1 = ax4.plot(iterations, thrust_values, 'b-', linewidth=2, label='Thrust (kN)')
        line2 = ax4_twin.plot(iterations, tsfc_values, 'r--', linewidth=2, label='TSFC (mg/N·s)')
        
        ax4.set_xlabel('Iteration')
        ax4.set_ylabel('Net Thrust (kN)', color='blue')
        ax4_twin.set_ylabel('TSFC (mg/N·s)', color='red')
        ax4.set_title('Performance Metrics Evolution')
        
        # Combine legends
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax4.legend(lines, labels, loc='best')
        
        plt.tight_layout()
        plt.savefig('optimization_history.png', dpi=300, bbox_inches='tight')
        plt.show()

def demonstrate_multi_objective_optimization():
    """Demonstrate advanced multi-objective optimization techniques."""
    print("🚀 Advanced Multi-Objective Engine Optimization Demo")
    print("=" * 60)
    
    # Start with a baseline configuration
    base_config = get_config('civil_airliner')
    optimizer = EngineOptimizer(base_config)
    
    # Optimize for different objectives
    objectives = ['fuel_efficiency', 'thrust', 'overall_efficiency']
    results = {}
    
    for objective in objectives:
        print(f"\n🎯 Optimizing for {objective}...")
        result = optimizer.optimize_engine(objective, method='differential_evolution')
        results[objective] = result
        
        # Print improvement summary
        improvements = result['improvement_metrics']
        print(f"Performance improvements:")
        for metric, improvement in improvements.items():
            print(f"  • {metric}: {improvement:+.1f}%")
    
    # Plot optimization history for the last run
    optimizer.plot_optimization_history()
    
    # Generate comparison plot
    plot_optimization_comparison(results)
    
    return results

def plot_optimization_comparison(results: Dict) -> None:
    """Generate comparison plot of different optimization objectives."""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Multi-Objective Optimization Comparison', fontsize=16, fontweight='bold')
    
    objectives = list(results.keys())
    metrics = ['Net Thrust', 'TSFC', 'Thermal Efficiency', 'Overall Efficiency']
    
    # Extract data for plotting
    plot_data = {metric: [] for metric in metrics}
    
    for objective in objectives:
        result = results[objective]['optimal_result']
        plot_data['Net Thrust'].append(result['Net Thrust'] / 1000)  # kN
        plot_data['TSFC'].append(result['TSFC'] * 1e6)  # mg/N·s
        plot_data['Thermal Efficiency'].append(result['Thermal Efficiency'] * 100)  # %
        plot_data['Overall Efficiency'].append(result['Overall Efficiency'] * 100)  # %
    
    # Create bar plots
    x_pos = np.arange(len(objectives))
    obj_labels = [obj.replace('_', '\n').title() for obj in objectives]
    
    # Thrust comparison
    ax1.bar(x_pos, plot_data['Net Thrust'], alpha=0.8, color='blue')
    ax1.set_ylabel('Net Thrust (kN)')
    ax1.set_title('Optimized Thrust Performance')
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(obj_labels)
    
    # TSFC comparison
    ax2.bar(x_pos, plot_data['TSFC'], alpha=0.8, color='red')
    ax2.set_ylabel('TSFC (mg/N·s)')
    ax2.set_title('Optimized Fuel Consumption')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(obj_labels)
    
    # Efficiency comparisons
    width = 0.35
    ax3.bar(x_pos - width/2, plot_data['Thermal Efficiency'], width, 
           label='Thermal', alpha=0.8)
    ax3.bar(x_pos + width/2, plot_data['Overall Efficiency'], width,
           label='Overall', alpha=0.8)
    ax3.set_ylabel('Efficiency (%)')
    ax3.set_title('Optimized Efficiency Performance')
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels(obj_labels)
    ax3.legend()
    
    # Pareto frontier approximation (simplified)
    tsfc_vals = plot_data['TSFC']
    thrust_vals = plot_data['Net Thrust']
    
    ax4.scatter(tsfc_vals, thrust_vals, s=100, alpha=0.8, c=['blue', 'red', 'green'])
    for i, obj in enumerate(obj_labels):
        ax4.annotate(obj, (tsfc_vals[i], thrust_vals[i]), 
                    xytext=(5, 5), textcoords='offset points')
    
    ax4.set_xlabel('TSFC (mg/N·s)')
    ax4.set_ylabel('Net Thrust (kN)')
    ax4.set_title('Performance Trade-off Space')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('optimization_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()

def sensitivity_analysis_example():
    """Demonstrate parameter sensitivity analysis."""
    print("\n🔍 Parameter Sensitivity Analysis")
    print("=" * 40)
    
    base_config = get_config('military_fighter')
    engine = JetEngine(**base_config.__dict__)
    baseline_result = engine.simulate()
    
    # Parameters to analyze
    sensitivity_params = {
        'compression_ratio': (base_config.compression_ratio, np.linspace(10, 30, 21)),
        'fuel_air_ratio': (base_config.fuel_air_ratio, np.linspace(0.035, 0.055, 21)),
        'eta_comp': (base_config.eta_comp, np.linspace(0.75, 0.95, 21)),
        'altitude': (base_config.altitude, np.linspace(5000, 25000, 21))
    }
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.flatten()
    fig.suptitle('Parameter Sensitivity Analysis', fontsize=16, fontweight='bold')
    
    for idx, (param_name, (baseline_val, param_range)) in enumerate(sensitivity_params.items()):
        thrust_sensitivity = []
        tsfc_sensitivity = []
        
        for param_val in param_range:
            # Create modified configuration
            config = base_config
            setattr(config, param_name, param_val)
            
            # Run simulation
            engine = JetEngine(**config.__dict__)
            result = engine.simulate()
            
            # Calculate relative change from baseline
            thrust_change = (result['Net Thrust'] - baseline_result['Net Thrust']) / baseline_result['Net Thrust'] * 100
            tsfc_change = (result['TSFC'] - baseline_result['TSFC']) / baseline_result['TSFC'] * 100
            
            thrust_sensitivity.append(thrust_change)
            tsfc_sensitivity.append(tsfc_change)
        
        # Plot sensitivity curves
        ax = axes[idx]
        ax.plot(param_range, thrust_sensitivity, 'b-', linewidth=2, label='Thrust')
        ax.plot(param_range, tsfc_sensitivity, 'r--', linewidth=2, label='TSFC')
        
        # Mark baseline point
        ax.axvline(baseline_val, color='gray', linestyle=':', alpha=0.7, label='Baseline')
        ax.axhline(0, color='black', linewidth=0.5)
        
        ax.set_xlabel(param_name.replace('_', ' ').title())
        ax.set_ylabel('Change from Baseline (%)')
        ax.set_title(f'Sensitivity to {param_name.replace("_", " ").title()}')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('sensitivity_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    # Run comprehensive examples
    optimization_results = demonstrate_multi_objective_optimization()
    sensitivity_analysis_example()
    
    print("\n🎉 Advanced examples complete!")
    print("Generated files: optimization_history.png, optimization_comparison.png, sensitivity_analysis.png")
