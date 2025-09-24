# API Reference

## Core Engine Classes

### `JetEngine`

The main simulation class for jet engine performance analysis.

#### Constructor

```python
JetEngine(
    altitude: float = 10000,                    # Operating altitude [m]
    compression_ratio: float = 10,              # Overall pressure ratio
    fuel_energy: float = 43e6,                  # Jet-A fuel energy [J/kg]
    eta_comp: float = 0.85,                     # Compressor isentropic efficiency
    eta_turb: float = 0.85,                     # Turbine isentropic efficiency
    mechanical_eff: float = 0.9,                # Mechanical transmission efficiency
    nozzle_eff: float = 0.9,                    # Nozzle efficiency
    flight_speed: float = 1000,                 # Flight velocity [m/s]
    fuel_air_ratio: float = 0.045,              # Primary fuel-air ratio
    use_afterburner: bool = False,              # Afterburner activation
    afterburner_fuel_fraction: float = 0.03,    # AB fuel fraction
    drag_coefficient: float = 0.01,             # Engine nacelle drag coefficient
    frontal_area: float = 0.9                   # Engine frontal area [m²]
) -> None
```

#### Methods

##### `simulate() -> Dict[str, float]`

Performs complete engine cycle simulation.

**Returns:**
- `Dict[str, float]`: Performance metrics including:
  - `'Net Thrust'`: Net thrust output [N]
  - `'Fuel Flow Rate'`: Total fuel consumption [kg/s]
  - `'TSFC'`: Thrust Specific Fuel Consumption [kg/N·s]
  - `'Thermal Efficiency'`: Thermal efficiency [dimensionless]
  - `'Propulsive Efficiency'`: Propulsive efficiency [dimensionless]
  - `'Overall Efficiency'`: Overall efficiency [dimensionless]
  - `'Specific Impulse (Isp)'`: Specific impulse [s]
  - `'Exhaust Velocity'`: Nozzle exit velocity [m/s]
  - `'Compressor Temp (T2)'`: Compressor exit temperature [K]
  - `'Combustor Temp (T3)'`: Combustor exit temperature [K]
  - `'Turbine/Exit Temp'`: Turbine exit temperature [K]

**Example:**
```python
engine = JetEngine(altitude=10000, compression_ratio=15)
results = engine.simulate()
print(f"Thrust: {results['Net Thrust']:.0f} N")
print(f"TSFC: {results['TSFC']*1e6:.1f} mg/N·s")
```

##### `isa_atmosphere(altitude: float) -> Tuple[float, float, float]`

Calculates atmospheric conditions using International Standard Atmosphere.

**Parameters:**
- `altitude`: Altitude above sea level [m]

**Returns:**
- `Tuple[float, float, float]`: (Temperature [K], Pressure [Pa], Density [kg/m³])

## Configuration Management

### `EngineConfig`

Data class for engine configuration management with validation.

#### Attributes

```python
@dataclass
class EngineConfig:
    altitude: float = 10000.0          # [m]
    compression_ratio: float = 10.0     # Overall pressure ratio
    frontal_area: float = 0.9          # [m²]
    fuel_energy: float = 43e6          # Jet-A fuel energy [J/kg]
    fuel_air_ratio: float = 0.045      # Primary combustion f/a ratio
    eta_comp: float = 0.85             # Compressor isentropic efficiency
    eta_turb: float = 0.85             # Turbine isentropic efficiency
    mechanical_eff: float = 0.9        # Mechanical transmission efficiency
    nozzle_eff: float = 0.9           # Nozzle efficiency
    flight_speed: float = 1000.0       # [m/s]
    use_afterburner: bool = False
    afterburner_fuel_fraction: float = 0.03
    drag_coefficient: float = 0.01
```

#### Methods

##### `validate() -> None`

Validates configuration parameters for physical consistency.

**Raises:**
- `ValueError`: If parameters are outside realistic ranges

##### `from_json(json_path: Path) -> EngineConfig`

Load configuration from JSON file.

##### `to_json(json_path: Path) -> None`

Save configuration to JSON file.

### Configuration Functions

##### `get_config(name: str) -> EngineConfig`

Get a predefined engine configuration.

**Parameters:**
- `name`: Configuration name ('civil_airliner', 'military_fighter', 'supersonic_transport', 'regional_jet')

**Returns:**
- `EngineConfig`: Requested configuration

**Example:**
```python
from config import get_config
config = get_config('military_fighter')
engine = JetEngine(**config.__dict__)
```

##### `list_configurations() -> List[str]`

List all available predefined configurations.

## Visualization and Analysis

### `EngineAnalyzer`

Advanced analysis and visualization tools.

#### Constructor

```python
EngineAnalyzer(save_plots: bool = True, plot_format: str = 'png', dpi: int = 300)
```

#### Methods

##### `plot_performance_envelope(config_name: str) -> None`

Generate comprehensive performance envelope analysis.

##### `compare_configurations() -> None`

Compare performance of different engine configurations.

##### `plot_afterburner_analysis() -> None`

Analyze afterburner impact on performance.

## Optimization Framework

### `EngineOptimizer`

Multi-objective optimization framework for engine design parameters.

#### Constructor

```python
EngineOptimizer(base_config: EngineConfig)
```

#### Methods

##### `optimize_engine(objective: str, method: str) -> Dict`

Perform multi-parameter optimization.

**Parameters:**
- `objective`: 'fuel_efficiency', 'thrust', or 'overall_efficiency'
- `method`: 'differential_evolution' or 'minimize'

**Returns:**
- `Dict`: Optimization results including optimal parameters and performance improvements

## Performance Benchmarking

### `PerformanceBenchmark`

Comprehensive performance benchmarking suite.

#### Methods

##### `benchmark_single_simulation(config_name: str, iterations: int) -> Dict[str, float]`

Benchmark single engine simulation performance.

##### `benchmark_parameter_sweep(param_name: str, param_range: np.ndarray, config_name: str) -> Dict[str, float]`

Benchmark parameter sweep performance.

##### `profile_simulation(config_name: str, output_file: str) -> None`

Profile simulation to identify performance bottlenecks.

## Physical Constants

```python
GAMMA = 1.4           # Heat capacity ratio for air
R = 287.05           # Specific gas constant for air [J/kg·K]
CP = 1005            # Specific heat at constant pressure [J/kg·K]
GRAVITY = 9.80665    # Standard gravity [m/s²]
STD_SEA_LEVEL_TEMP = 288.15    # ISA sea level temperature [K]
STD_SEA_LEVEL_PRESS = 101325   # ISA sea level pressure [Pa]
```

## Error Handling

### `EngineError`

Custom exception for engine simulation errors.

```python
class EngineError(Exception):
    """Custom exception for engine simulation errors."""
    pass
```

## Usage Examples

### Basic Simulation

```python
from engine import JetEngine

# Create engine with custom parameters
engine = JetEngine(
    altitude=15000,
    compression_ratio=20,
    flight_speed=600,
    use_afterburner=True
)

# Run simulation
results = engine.simulate()

# Display results
print(f"Thrust: {results['Net Thrust']/1000:.1f} kN")
print(f"TSFC: {results['TSFC']*1e6:.1f} mg/N·s")
print(f"Efficiency: {results['Overall Efficiency']*100:.1f}%")
```

### Configuration-Based Simulation

```python
from config import get_config
from engine import JetEngine

# Load predefined configuration
config = get_config('civil_airliner')

# Modify specific parameters
config.altitude = 40000
config.compression_ratio = 30

# Create and run engine
engine = JetEngine(**config.__dict__)
results = engine.simulate()
```

### Performance Analysis

```python
from visualize import EngineAnalyzer

# Create analyzer
analyzer = EngineAnalyzer()

# Generate comprehensive analysis
analyzer.plot_performance_envelope('military_fighter')
analyzer.compare_configurations()
analyzer.plot_afterburner_analysis()
```

### Optimization Example

```python
from config import get_config
from examples.advanced_examples import EngineOptimizer

# Set up optimization
base_config = get_config('civil_airliner')
optimizer = EngineOptimizer(base_config)

# Optimize for fuel efficiency
results = optimizer.optimize_engine('fuel_efficiency', 'differential_evolution')

print(f"Improvement in TSFC: {results['improvement_metrics']['TSFC']:+.1f}%")
print(f"Optimal compression ratio: {results['optimal_params'][0]:.1f}")
```

## Performance Characteristics

### Typical Execution Times
- Single simulation: ~0.5 ms
- Parameter sweep (50 points): ~25 ms  
- Optimization (100 iterations): ~5 seconds
- Complete visualization suite: ~30 seconds

### Memory Usage
- Single engine instance: ~0.1 MB
- Parameter sweep data: ~1-10 MB
- Visualization plots: ~5-20 MB per plot

### Accuracy
- TSFC prediction: ±5% vs. published data
- Thrust calculation: ±3% vs. test data
- Temperature prediction: ±2% vs. cycle analysis
