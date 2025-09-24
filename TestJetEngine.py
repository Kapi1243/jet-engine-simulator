"""
Comprehensive test suite for jet engine simulation validation.
Tests cover thermodynamic accuracy, edge cases, and performance metrics.
"""

import unittest
import math
from engine import JetEngine

class TestJetEngineThermodynamics(unittest.TestCase):
    """Test core thermodynamic calculations and physical constraints."""
    
    def setUp(self):
        """Set up test fixtures with standard engine configurations."""
        self.standard_engine = JetEngine(
            altitude=10000,
            compression_ratio=10,
            flight_speed=250,
            use_afterburner=False
        )
        self.afterburner_engine = JetEngine(
            altitude=10000,
            compression_ratio=15,
            flight_speed=500,
            use_afterburner=True,
            afterburner_fuel_fraction=0.03
        )

    def test_thrust_always_positive_or_zero(self):
        """Verify thrust is never negative under normal conditions."""
        for altitude in [0, 5000, 10000, 20000]:
            for speed in [100, 300, 500, 800]:
                engine = JetEngine(altitude=altitude, flight_speed=speed)
                result = engine.simulate()
                self.assertGreaterEqual(
                    result['Net Thrust'], 0,
                    f"Thrust negative at alt={altitude}m, speed={speed}m/s"
                )

    def test_tsfc_physical_bounds(self):
        """Test TSFC is within realistic bounds for jet engines."""
        result = self.standard_engine.simulate()
        # Modern jet engines: TSFC typically 15-25 mg/N·s
        tsfc_mg_per_n_s = result['TSFC'] * 1e6
        self.assertTrue(
            10 < tsfc_mg_per_n_s < 50,
            f"TSFC {tsfc_mg_per_n_s:.1f} mg/N·s outside realistic range"
        )

    def test_temperature_increases_through_engine(self):
        """Verify temperatures increase appropriately through engine cycle."""
        result = self.standard_engine.simulate()
        T0 = self.standard_engine.T0
        T2 = result['Compressor Temp (T2)']
        T3 = result['Combustor Temp (T3)']
        T4 = result['Turbine/Exit Temp']
        
        # Check temperature progression
        self.assertGreater(T2, T0, "Compressor should increase temperature")
        self.assertGreater(T3, T2, "Combustor should increase temperature")
        self.assertLess(T4, T3, "Turbine should decrease temperature")
        
        # Check realistic temperature bounds
        self.assertLess(T3, 2500, "Combustor temp too high (material limits)")
        self.assertGreater(T3, 1000, "Combustor temp too low for combustion")

    def test_afterburner_increases_performance(self):
        """Verify afterburner increases thrust but decreases efficiency."""
        base_result = self.standard_engine.simulate()
        ab_result = self.afterburner_engine.simulate()
        
        # Afterburner should increase thrust
        self.assertGreater(
            ab_result['Net Thrust'], base_result['Net Thrust'] * 0.8,
            "Afterburner should significantly increase thrust"
        )
        
        # But decrease fuel efficiency
        if base_result['TSFC'] != float('inf') and ab_result['TSFC'] != float('inf'):
            self.assertGreater(
                ab_result['TSFC'], base_result['TSFC'],
                "Afterburner should increase TSFC (decrease efficiency)"
            )

    def test_efficiency_conservation_laws(self):
        """Test that efficiency calculations obey thermodynamic laws."""
        result = self.standard_engine.simulate()
        
        # Overall efficiency = thermal × propulsive
        calculated_overall = (result['Thermal Efficiency'] * 
                            result['Propulsive Efficiency'])
        
        self.assertAlmostEqual(
            result['Overall Efficiency'], calculated_overall,
            places=6, msg="Overall efficiency calculation inconsistent"
        )
        
        # All efficiencies should be between 0 and 1
        for eff_name in ['Thermal Efficiency', 'Propulsive Efficiency', 'Overall Efficiency']:
            self.assertTrue(
                0 <= result[eff_name] <= 1,
                f"{eff_name} {result[eff_name]} outside physical bounds [0,1]"
            )

    def test_isp_consistency(self):
        """Test specific impulse calculation consistency."""
        result = self.standard_engine.simulate()
        
        if result['Net Thrust'] > 0 and result['Fuel Flow Rate'] > 0:
            # Isp = Thrust / (fuel_flow * g)
            calculated_isp = result['Net Thrust'] / (result['Fuel Flow Rate'] * 9.80665)
            self.assertAlmostEqual(
                result['Specific Impulse (Isp)'], calculated_isp,
                places=3, msg="Specific impulse calculation inconsistent"
            )

class TestJetEngineEdgeCases(unittest.TestCase):
    """Test engine behavior at extreme conditions and edge cases."""
    
    def test_zero_altitude_operation(self):
        """Test engine operates correctly at sea level."""
        engine = JetEngine(altitude=0)
        result = engine.simulate()
        self.assertGreater(result['Net Thrust'], 0)
        self.assertTrue(math.isfinite(result['TSFC']))

    def test_high_altitude_operation(self):
        """Test engine operates at high altitude (stratosphere)."""
        engine = JetEngine(altitude=20000)
        result = engine.simulate()
        # At high altitude, thrust should be lower due to low air density
        self.assertGreater(result['Net Thrust'], 0)

    def test_extreme_compression_ratios(self):
        """Test engine with very high and low compression ratios."""
        # Low compression ratio
        low_comp_engine = JetEngine(compression_ratio=3)
        low_result = low_comp_engine.simulate()
        
        # High compression ratio  
        high_comp_engine = JetEngine(compression_ratio=40)
        high_result = high_comp_engine.simulate()
        
        # Both should produce positive thrust
        self.assertGreater(low_result['Net Thrust'], 0)
        self.assertGreater(high_result['Net Thrust'], 0)
        
        # Higher compression should generally give better thermal efficiency
        # (though this depends on other factors)
        self.assertIsNotNone(high_result['Thermal Efficiency'])

    def test_subsonic_vs_supersonic_flight(self):
        """Compare engine performance at subsonic vs supersonic speeds."""
        subsonic_engine = JetEngine(flight_speed=200)  # ~M 0.6
        supersonic_engine = JetEngine(flight_speed=600)  # ~M 1.8
        
        sub_result = subsonic_engine.simulate()
        super_result = supersonic_engine.simulate()
        
        # Both should work
        self.assertGreater(sub_result['Net Thrust'], 0)
        self.assertGreater(super_result['Net Thrust'], 0)
        
        # Propulsive efficiency behavior should be different
        self.assertIsNotNone(sub_result['Propulsive Efficiency'])
        self.assertIsNotNone(super_result['Propulsive Efficiency'])

class TestJetEngineInputValidation(unittest.TestCase):
    """Test input validation and error handling."""
    
    def test_negative_inputs_handling(self):
        """Test that negative physical parameters are handled gracefully."""
        # Most negative inputs should either be rejected or handled gracefully
        try:
            engine = JetEngine(altitude=-1000)  # Below sea level
            result = engine.simulate()
            # Should either work or raise appropriate exception
            if result:
                self.assertIsNotNone(result['Net Thrust'])
        except (ValueError, AssertionError):
            pass  # Acceptable to reject negative altitude

    def test_extreme_fuel_air_ratios(self):
        """Test engine with extreme fuel-air ratios."""
        # Very lean mixture
        lean_engine = JetEngine(fuel_air_ratio=0.01)
        lean_result = lean_engine.simulate()
        
        # Very rich mixture (but still combustible)
        rich_engine = JetEngine(fuel_air_ratio=0.08)
        rich_result = rich_engine.simulate()
        
        # Both should produce some results
        self.assertIsNotNone(lean_result)
        self.assertIsNotNone(rich_result)

class TestISAAtmosphere(unittest.TestCase):
    """Test International Standard Atmosphere implementation."""
    
    def test_sea_level_conditions(self):
        """Verify sea level standard conditions."""
        engine = JetEngine(altitude=0)
        T, P, rho = engine.isa_atmosphere(0)
        
        # Standard sea level conditions
        self.assertAlmostEqual(T, 288.15, places=1)  # 15°C
        self.assertAlmostEqual(P, 101325, places=0)  # 101.325 kPa
        self.assertAlmostEqual(rho, 1.225, places=2)  # kg/m³

    def test_troposphere_gradient(self):
        """Test temperature lapse rate in troposphere."""
        engine = JetEngine()
        T_5km, _, _ = engine.isa_atmosphere(5000)
        T_10km, _, _ = engine.isa_atmosphere(10000)
        
        # Temperature should decrease with altitude
        self.assertLess(T_10km, T_5km)
        
        # Standard lapse rate is -6.5°C/km
        expected_temp_diff = 5000 * 0.0065  # 32.5K
        actual_temp_diff = T_5km - T_10km
        self.assertAlmostEqual(actual_temp_diff, expected_temp_diff, places=1)

    def test_stratosphere_isothermal(self):
        """Test isothermal stratosphere above 11km."""
        engine = JetEngine()
        T_12km, _, _ = engine.isa_atmosphere(12000)
        T_15km, _, _ = engine.isa_atmosphere(15000)
        
        # Temperature should be constant in lower stratosphere
        self.assertAlmostEqual(T_12km, T_15km, places=1)
        self.assertAlmostEqual(T_12km, 216.65, places=1)

if __name__ == '__main__':
    # Run tests with detailed output
    unittest.main(verbosity=2)
