# Contributing to Jet Engine Simulator

Thank you for your interest in contributing to the Jet Engine Performance Simulator! This document provides guidelines for contributing to this project.

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Required packages listed in `requirements.txt`

### Development Setup
1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/jet_engine_sim.git
   cd jet_engine_sim
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run tests to ensure everything works:
   ```bash
   python TestJetEngine.py
   ```

## 🛠️ Development Workflow

### Code Style
- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Add docstrings for all public functions and classes
- Run `black .` for code formatting
- Run `flake8 .` for linting

### Testing
- Add tests for all new functionality
- Ensure all existing tests pass
- Aim for >90% code coverage
- Test edge cases and error conditions

### Commit Messages
Use conventional commit format:
```
feat: add new engine configuration type
fix: correct TSFC calculation for high altitudes
docs: update README with installation instructions
test: add edge case tests for compressor efficiency
```

## 📋 Types of Contributions

### 🐛 Bug Reports
- Use the issue template
- Include minimal reproduction example
- Specify Python version and OS
- Include error messages/stack traces

### 💡 Feature Requests
- Check existing issues first
- Describe the use case clearly
- Consider implementation complexity
- Discuss API design implications

### 🔧 Code Contributions
- Start with an issue discussion
- Keep changes focused and atomic
- Include tests and documentation
- Update CHANGELOG.md

## 🧪 Testing Guidelines

### Running Tests
```bash
# Run all tests
python TestJetEngine.py

# Run with verbose output
python TestJetEngine.py -v

# Run performance benchmarks
python benchmark.py
```

### Test Categories
- **Unit Tests**: Test individual functions/methods
- **Integration Tests**: Test component interactions
- **Edge Case Tests**: Test boundary conditions
- **Performance Tests**: Validate computational efficiency

## 📚 Documentation

### Code Documentation
- Use Google-style docstrings
- Document all parameters and return values
- Include usage examples for complex functions
- Explain physical/mathematical concepts

### README Updates
- Keep installation instructions current
- Update feature lists
- Add new configuration examples
- Include performance benchmarks

## 🚦 Pull Request Process

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Write clean, well-documented code
   - Add comprehensive tests
   - Update documentation

3. **Test thoroughly**:
   ```bash
   python TestJetEngine.py
   python -m flake8 .
   python -m mypy engine.py config.py
   ```

4. **Submit pull request**:
   - Use descriptive title and description
   - Reference related issues
   - Include screenshots for GUI changes
   - Ensure CI passes

### PR Review Criteria
- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] No breaking changes (or properly documented)
- [ ] Performance impact is acceptable

## 🏗️ Architecture Guidelines

### Core Principles
- **Modularity**: Keep components loosely coupled
- **Extensibility**: Design for easy feature additions
- **Performance**: Maintain computational efficiency
- **Reliability**: Handle edge cases gracefully

### Adding New Engine Types
1. Add configuration to `config.py`
2. Update validation logic
3. Add corresponding tests
4. Update documentation
5. Include performance benchmarks

### Adding New Analysis Features
1. Extend `visualize.py` or create new module
2. Follow existing plotting conventions
3. Add interactive capabilities where appropriate
4. Include example usage

## 🔬 Scientific Accuracy

### Thermodynamic Models
- Validate against established references
- Include citations for equations/methods
- Test against known benchmarks
- Document assumptions and limitations

### Physical Constraints
- Ensure results are physically realistic
- Add bounds checking for parameters
- Validate units and conversions
- Test extreme operating conditions

## 📈 Performance Considerations

### Computational Efficiency
- Profile new features with `benchmark.py`
- Avoid unnecessary computations
- Consider vectorization for parameter sweeps
- Document performance characteristics

### Memory Usage
- Monitor memory consumption growth
- Clean up temporary variables
- Use appropriate data structures
- Test with large parameter ranges

## 🤝 Community Guidelines

### Code of Conduct
- Be respectful and inclusive
- Focus on constructive feedback
- Help newcomers learn
- Celebrate diverse perspectives

### Communication
- Use clear, professional language
- Provide context for technical discussions
- Ask questions when uncertain
- Share knowledge generously

## 📞 Getting Help

- **Issues**: Use GitHub issues for bugs/features
- **Discussions**: Use GitHub discussions for questions
- **Email**: [your.email@domain.com] for private matters

## 🎉 Recognition

Contributors will be acknowledged in:
- README.md contributors section
- Release notes for significant contributions
- Special recognition for major features

Thank you for helping make this project better! 🚀
