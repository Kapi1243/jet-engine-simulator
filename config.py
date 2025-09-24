"""
Configuration management for jet engine simulation parameters.
"""

from dataclasses import dataclass
from typing import Dict, Any
import json
from pathlib import Path

@dataclass
class EngineConfig:
    """Configuration class for engine parameters with validation."""
    
    # Atmospheric conditions
    altitude: float = 10000.0          # [m]
    
    # Engine geometry and design
    compression_ratio: float = 10.0     # Overall pressure ratio
    frontal_area: float = 0.9          # [m²]
    
    # Thermodynamic properties
    fuel_energy: float = 43e6          # Jet-A fuel energy [J/kg]
    fuel_air_ratio: float = 0.045      # Primary combustion f/a ratio
    
    # Component efficiencies
    eta_comp: float = 0.85             # Compressor isentropic efficiency
    eta_turb: float = 0.85             # Turbine isentropic efficiency
    mechanical_eff: float = 0.9        # Mechanical transmission efficiency
    nozzle_eff: float = 0.9           # Nozzle efficiency
    
    # Flight conditions
    flight_speed: float = 1000.0       # [m/s]
    
    # Afterburner configuration
    use_afterburner: bool = False
    afterburner_fuel_fraction: float = 0.03
    
    # Drag modeling
    drag_coefficient: float = 0.01
    
    def validate(self) -> None:
        """Validate configuration parameters for physical consistency."""
        if self.altitude < -500 or self.altitude > 50000:
            raise ValueError(f"Altitude {self.altitude}m outside realistic range")
        
        if self.compression_ratio < 1.0 or self.compression_ratio > 100:
            raise ValueError(f"Compression ratio {self.compression_ratio} outside realistic range")
        
        if not 0.1 <= self.eta_comp <= 1.0:
            raise ValueError(f"Compressor efficiency {self.eta_comp} outside valid range [0.1, 1.0]")
        
        if not 0.1 <= self.eta_turb <= 1.0:
            raise ValueError(f"Turbine efficiency {self.eta_turb} outside valid range [0.1, 1.0]")
        
        if self.fuel_air_ratio < 0.01 or self.fuel_air_ratio > 0.1:
            raise ValueError(f"Fuel-air ratio {self.fuel_air_ratio} outside combustible range")
        
        if self.flight_speed < 0 or self.flight_speed > 3000:
            raise ValueError(f"Flight speed {self.flight_speed} m/s outside realistic range")
        
        if self.afterburner_fuel_fraction < 0 or self.afterburner_fuel_fraction > 0.2:
            raise ValueError(f"Afterburner fuel fraction {self.afterburner_fuel_fraction} outside realistic range")

    @classmethod
    def from_json(cls, json_path: Path) -> 'EngineConfig':
        """Load configuration from JSON file."""
        with open(json_path, 'r') as f:
            data = json.load(f)
        config = cls(**data)
        config.validate()
        return config
    
    def to_json(self, json_path: Path) -> None:
        """Save configuration to JSON file."""
        data = {
            'altitude': self.altitude,
            'compression_ratio': self.compression_ratio,
            'frontal_area': self.frontal_area,
            'fuel_energy': self.fuel_energy,
            'fuel_air_ratio': self.fuel_air_ratio,
            'eta_comp': self.eta_comp,
            'eta_turb': self.eta_turb,
            'mechanical_eff': self.mechanical_eff,
            'nozzle_eff': self.nozzle_eff,
            'flight_speed': self.flight_speed,
            'use_afterburner': self.use_afterburner,
            'afterburner_fuel_fraction': self.afterburner_fuel_fraction,
            'drag_coefficient': self.drag_coefficient
        }
        
        with open(json_path, 'w') as f:
            json.dump(data, f, indent=2)

# Predefined engine configurations
CONFIGURATIONS: Dict[str, EngineConfig] = {
    'civil_airliner': EngineConfig(
        altitude=35000,
        compression_ratio=25,
        flight_speed=250,  # ~M 0.8 at cruise
        eta_comp=0.90,
        eta_turb=0.88,
        fuel_air_ratio=0.042,
        use_afterburner=False
    ),
    
    'military_fighter': EngineConfig(
        altitude=15000,
        compression_ratio=20,
        flight_speed=600,  # ~M 1.8
        eta_comp=0.85,
        eta_turb=0.85,
        fuel_air_ratio=0.048,
        use_afterburner=True,
        afterburner_fuel_fraction=0.04
    ),
    
    'supersonic_transport': EngineConfig(
        altitude=50000,
        compression_ratio=15,
        flight_speed=650,  # ~M 2.0
        eta_comp=0.82,
        eta_turb=0.84,
        fuel_air_ratio=0.045,
        use_afterburner=True,
        afterburner_fuel_fraction=0.02
    ),
    
    'regional_jet': EngineConfig(
        altitude=25000,
        compression_ratio=18,
        flight_speed=200,  # ~M 0.6
        eta_comp=0.88,
        eta_turb=0.86,
        fuel_air_ratio=0.040,
        use_afterburner=False
    )
}

def get_config(name: str) -> EngineConfig:
    """Get a predefined engine configuration by name."""
    if name not in CONFIGURATIONS:
        available = ', '.join(CONFIGURATIONS.keys())
        raise ValueError(f"Unknown configuration '{name}'. Available: {available}")
    
    return CONFIGURATIONS[name]

def list_configurations() -> list[str]:
    """List all available predefined configurations."""
    return list(CONFIGURATIONS.keys())
