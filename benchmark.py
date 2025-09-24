"""
Performance benchmarking and optimization analysis for jet engine simulation.

This module provides tools to benchmark simulation performance, identify
bottlenecks, and demonstrate computational efficiency.
"""

import time
import cProfile
import pstats
from typing import Dict, List, Callable, Any
import numpy as np
import matplotlib.pyplot as plt
from functools import wraps
from engine import JetEngine
from config import get_config, CONFIGURATIONS

class PerformanceBenchmark:
    """Comprehensive performance benchmarking suite."""
    
    def __init__(self):
        self.results: Dict[str, Dict[str, float]] = {}
    
    def time_function(self, func: Callable, *args, **kwargs) -> tuple[Any, float]:
        """Time a function execution and return result with execution time."""
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        return result, end_time - start_time
    
    def benchmark_single_simulation(self, config_name: str = 'civil_airliner', iterations: int = 1000) -> Dict[str, float]:
        """Benchmark single engine simulation performance."""
        config = get_config(config_name)
        engine = JetEngine(**config.__dict__)
        
        times = []
        for _ in range(iterations):
            _, exec_time = self.time_function(engine.simulate)
            times.append(exec_time)
        
        times_array = np.array(times)
        
        stats = {
            'mean_time': np.mean(times_array) * 1000,  # Convert to ms
            'std_time': np.std(times_array) * 1000,
            'min_time': np.min(times_array) * 1000,
            'max_time': np.max(times_array) * 1000,
            'median_time': np.median(times_array) * 1000,
            'simulations_per_second': 1.0 / np.mean(times_array),
            'total_time': np.sum(times_array),
            'iterations': iterations
        }
        
        self.results[f'{config_name}_single'] = stats
        return stats
    
    def benchmark_parameter_sweep(self, param_name: str, param_range: np.ndarray, 
                                config_name: str = 'civil_airliner') -> Dict[str, float]:
        """Benchmark parameter sweep performance."""
        config = get_config(config_name)
        
        start_time = time.perf_counter()
        
        results = []
        for param_value in param_range:
            # Update the parameter
            setattr(config, param_name, param_value)
            engine = JetEngine(**config.__dict__)
            result = engine.simulate()
            results.append(result)
        
        end_time = time.perf_counter()
        total_time = end_time - start_time
        
        stats = {
            'total_time': total_time,
            'time_per_simulation': total_time / len(param_range) * 1000,  # ms
            'simulations_per_second': len(param_range) / total_time,
            'parameter_points': len(param_range),
            'parameter_name': param_name
        }
        
        self.results[f'{config_name}_{param_name}_sweep'] = stats
        return stats
    
    def benchmark_all_configurations(self, iterations: int = 100) -> Dict[str, Dict[str, float]]:
        """Benchmark all predefined engine configurations."""
        config_results = {}
        
        for config_name in CONFIGURATIONS.keys():
            print(f"Benchmarking {config_name}...")
            stats = self.benchmark_single_simulation(config_name, iterations)
            config_results[config_name] = stats
        
        return config_results
    
    def profile_simulation(self, config_name: str = 'civil_airliner', 
                          output_file: str = 'profile_results.prof') -> None:
        """Profile a simulation to identify performance bottlenecks."""
        config = get_config(config_name)
        engine = JetEngine(**config.__dict__)
        
        # Run profiler
        profiler = cProfile.Profile()
        profiler.enable()
        
        # Run multiple simulations for better profiling data
        for _ in range(100):
            engine.simulate()
        
        profiler.disable()
        
        # Save and analyze results
        profiler.dump_stats(output_file)
        
        # Print top functions by cumulative time
        stats = pstats.Stats(output_file)
        stats.sort_stats('cumulative')
        print("\n=== Top Functions by Cumulative Time ===")
        stats.print_stats(10)
        
        stats.sort_stats('tottime')
        print("\n=== Top Functions by Total Time ===")
        stats.print_stats(10)
    
    def memory_usage_analysis(self, config_name: str = 'civil_airliner') -> Dict[str, Any]:
        """Analyze memory usage patterns (requires psutil)."""
        try:
            import psutil
            import os
            
            process = psutil.Process(os.getpid())
            initial_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            config = get_config(config_name)
            engines = []
            
            # Create multiple engine instances
            for i in range(100):
                engine = JetEngine(**config.__dict__)
                engines.append(engine)
                
                if i % 10 == 0:
                    current_memory = process.memory_info().rss / 1024 / 1024
                    print(f"Engines created: {i+1}, Memory: {current_memory:.1f} MB")
            
            peak_memory = process.memory_info().rss / 1024 / 1024
            
            # Run simulations
            for engine in engines:
                engine.simulate()
            
            final_memory = process.memory_info().rss / 1024 / 1024
            
            return {
                'initial_memory_mb': initial_memory,
                'peak_memory_mb': peak_memory,
                'final_memory_mb': final_memory,
                'memory_per_engine_mb': (peak_memory - initial_memory) / 100,
                'memory_after_simulation_mb': final_memory - peak_memory
            }
            
        except ImportError:
            print("psutil not available, skipping memory analysis")
            return {}
    
    def generate_performance_report(self) -> None:
        """Generate comprehensive performance report."""
        print("🚀 Jet Engine Simulator - Performance Benchmark Report")
        print("=" * 60)
        
        # Single simulation benchmarks
        if hasattr(self, 'results') and self.results:
            print("\n📊 Single Simulation Performance:")
            for test_name, stats in self.results.items():
                if 'single' in test_name:
                    config_name = test_name.replace('_single', '')
                    print(f"\n{config_name.replace('_', ' ').title()}:")
                    print(f"  • Mean execution time: {stats['mean_time']:.3f} ± {stats['std_time']:.3f} ms")
                    print(f"  • Simulations per second: {stats['simulations_per_second']:.0f}")
                    print(f"  • Min/Max time: {stats['min_time']:.3f}/{stats['max_time']:.3f} ms")
        
        # Parameter sweep benchmarks
        print("\n📈 Parameter Sweep Performance:")
        for test_name, stats in self.results.items():
            if 'sweep' in test_name:
                print(f"\n{test_name}:")
                print(f"  • Time per simulation: {stats['time_per_simulation']:.3f} ms")
                print(f"  • Simulations per second: {stats['simulations_per_second']:.0f}")
                print(f"  • Total parameter points: {stats['parameter_points']}")
        
        # System performance info
        try:
            import psutil
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            memory = psutil.virtual_memory()
            
            print(f"\n💻 System Information:")
            print(f"  • CPU Cores: {cpu_count}")
            if cpu_freq:
                print(f"  • CPU Frequency: {cpu_freq.current:.0f} MHz")
            print(f"  • Available Memory: {memory.available / 1024**3:.1f} GB")
            
        except ImportError:
            print("\n💻 System Information: (psutil not available)")
    
    def plot_performance_comparison(self) -> None:
        """Generate performance comparison plots."""
        if not self.results:
            print("No benchmark results available for plotting")
            return
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Jet Engine Simulator - Performance Analysis', fontsize=16, fontweight='bold')
        
        # Extract single simulation results
        single_results = {k.replace('_single', ''): v for k, v in self.results.items() if 'single' in k}
        
        if single_results:
            configs = list(single_results.keys())
            mean_times = [single_results[config]['mean_time'] for config in configs]
            std_times = [single_results[config]['std_time'] for config in configs]
            
            # Execution time comparison
            ax1.bar(configs, mean_times, yerr=std_times, capsize=5, alpha=0.7)
            ax1.set_ylabel('Execution Time (ms)', fontsize=12)
            ax1.set_title('Simulation Execution Time by Configuration', fontweight='bold')
            ax1.tick_params(axis='x', rotation=45)
            
            # Throughput comparison
            throughput = [single_results[config]['simulations_per_second'] for config in configs]
            ax2.bar(configs, throughput, alpha=0.7, color='green')
            ax2.set_ylabel('Simulations per Second', fontsize=12)
            ax2.set_title('Simulation Throughput by Configuration', fontweight='bold')
            ax2.tick_params(axis='x', rotation=45)
        
        # Performance distribution (if we have detailed timing data)
        # This would require storing individual timing measurements
        ax3.text(0.5, 0.5, 'Performance Distribution\n(Requires detailed timing data)', 
                ha='center', va='center', transform=ax3.transAxes, fontsize=12)
        ax3.set_title('Execution Time Distribution', fontweight='bold')
        
        # Parameter sweep performance
        sweep_results = {k: v for k, v in self.results.items() if 'sweep' in k}
        if sweep_results:
            sweep_names = list(sweep_results.keys())
            sweep_throughput = [sweep_results[name]['simulations_per_second'] for name in sweep_names]
            
            ax4.bar(range(len(sweep_names)), sweep_throughput, alpha=0.7, color='orange')
            ax4.set_ylabel('Simulations per Second', fontsize=12)
            ax4.set_title('Parameter Sweep Performance', fontweight='bold')
            ax4.set_xticks(range(len(sweep_names)))
            ax4.set_xticklabels([name.split('_')[-2] for name in sweep_names], rotation=45)
        
        plt.tight_layout()
        plt.savefig('performance_benchmark.png', dpi=300, bbox_inches='tight')
        plt.show()

def run_comprehensive_benchmark() -> None:
    """Run complete performance benchmark suite."""
    benchmark = PerformanceBenchmark()
    
    print("🚀 Starting comprehensive performance benchmark...")
    
    # 1. Single simulation benchmarks
    print("\n1️⃣ Single Simulation Benchmarks")
    benchmark.benchmark_all_configurations(iterations=500)
    
    # 2. Parameter sweep benchmarks
    print("\n2️⃣ Parameter Sweep Benchmarks")
    benchmark.benchmark_parameter_sweep(
        'compression_ratio', 
        np.linspace(8, 25, 50), 
        'civil_airliner'
    )
    
    benchmark.benchmark_parameter_sweep(
        'flight_speed', 
        np.linspace(200, 800, 30), 
        'military_fighter'
    )
    
    # 3. Memory usage analysis
    print("\n3️⃣ Memory Usage Analysis")
    memory_stats = benchmark.memory_usage_analysis()
    if memory_stats:
        print(f"Memory per engine instance: {memory_stats['memory_per_engine_mb']:.2f} MB")
        print(f"Peak memory usage: {memory_stats['peak_memory_mb']:.1f} MB")
    
    # 4. Generate reports
    print("\n4️⃣ Generating Performance Report")
    benchmark.generate_performance_report()
    benchmark.plot_performance_comparison()
    
    # 5. Detailed profiling
    print("\n5️⃣ Detailed Performance Profiling")
    benchmark.profile_simulation('civil_airliner', 'engine_profile.prof')
    
    print("\n✅ Benchmark complete! Check generated reports and plots.")

if __name__ == "__main__":
    run_comprehensive_benchmark()
