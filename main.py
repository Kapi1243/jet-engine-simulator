from engine import JetEngine, print_results

def main():
    print("Running Jet Engine Simulations...\n")

    # Baseline engine without afterburner
    base_engine = JetEngine(use_afterburner=False)
    base_results = base_engine.simulate()
    print_results("Jet Engine (No Afterburner)", base_results)

    # Engine with afterburner
    ab_engine = JetEngine(use_afterburner=True, afterburner_fuel_fraction=0.03)
    ab_results = ab_engine.simulate()
    print_results("Jet Engine (With Afterburner)", ab_results)

if __name__ == "__main__":
    main()
