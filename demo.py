"""
Quick demonstration of your enhanced jet engine simulator capabilities.
"""

from config import get_config, list_configurations
from engine import JetEngine

def main():
    print("🚀 Enhanced Jet Engine Simulator - Quick Demo")
    print("=" * 50)
    
    print("\n📋 Available Engine Configurations:")
    for config_name in list_configurations():
        config = get_config(config_name)
        engine = JetEngine(**config.__dict__)
        result = engine.simulate()
        
        name_display = config_name.replace('_', ' ').title()
        afterburner = "Yes" if config.use_afterburner else "No"
        
        print(f"\n{name_display}:")
        print(f"  • Altitude: {config.altitude:,} m")
        print(f"  • Compression Ratio: {config.compression_ratio}")
        print(f"  • Afterburner: {afterburner}")
        print(f"  • Net Thrust: {result['Net Thrust']/1000:.1f} kN")
        print(f"  • TSFC: {result['TSFC']*1e6:.1f} mg/N·s")
        print(f"  • Overall Efficiency: {result['Overall Efficiency']*100:.1f}%")

    print("\n🎯 How to Use Your Simulator:")
    print("1. Basic CLI:        python main.py")
    print("2. Interactive GUI:  python gui.py") 
    print("3. Visualizations:   python visualize.py")
    print("4. Run Tests:        python TestJetEngine.py")
    print("5. Benchmarking:     python benchmark.py")
    print("6. Advanced Examples: python examples/advanced_examples.py")
    
    print("\n📊 Key Features Added:")
    print("• Professional configuration management")
    print("• Comprehensive test suite (15+ test cases)")
    print("• Advanced visualization with publication-quality plots")
    print("• Performance benchmarking and optimization")
    print("• Multi-objective parameter optimization")
    print("• Type annotations and error handling")
    print("• CI/CD pipeline with GitHub Actions")
    print("• Complete package setup for distribution")

if __name__ == "__main__":
    main()
