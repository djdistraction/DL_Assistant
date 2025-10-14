# Contributing to DL_Assistant

Thank you for your interest in contributing to DL_Assistant! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/DL_Assistant.git
   cd DL_Assistant
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

## Development Workflow

1. Create a new branch for your feature/fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and test them thoroughly

3. Run the test suite:
   ```bash
   python -m unittest discover tests
   ```

4. Commit your changes with clear, descriptive messages:
   ```bash
   git commit -m "Add feature: description of changes"
   ```

5. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

6. Open a Pull Request on GitHub

## Code Style

- Follow PEP 8 style guidelines for Python code
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and concise

## Testing

- Write tests for all new features
- Ensure all tests pass before submitting a PR
- Aim for good test coverage of new code

## Documentation

- Update the README.md if you add new features
- Add examples to EXAMPLES.md for new functionality
- Update docstrings for modified functions

## What to Contribute

### Bug Reports

- Check if the bug has already been reported
- Include steps to reproduce
- Include expected vs actual behavior
- Include system information (OS, Python version)

### Feature Requests

- Check if the feature has already been requested
- Explain the use case and benefits
- Be open to discussion and feedback

### Code Contributions

Areas where contributions are welcome:

- Additional metadata extractors for more file types
- Support for more file formats
- UI/UX improvements for the dashboard
- Performance optimizations
- Additional tests
- Documentation improvements
- Bug fixes

## Code Review Process

1. All contributions require code review
2. Maintainers will review your PR and may request changes
3. Address feedback and update your PR
4. Once approved, your PR will be merged

## Questions?

Feel free to open an issue for any questions about contributing!

Thank you for contributing to DL_Assistant! 🎉
