# EDI-AI Automation Mapper

An AI-powered automation tool for processing EDI files and generating ERP mapping outputs.

## Overview

This project automates the processing of EDI files (X12, EDIFACT) and generates mapping outputs for ERP systems (SAP IDoc, Oracle flat files). It uses machine learning to suggest mappings between EDI fields and ERP fields, reducing the manual effort required for EDI onboarding.

## Features

- File monitoring and automatic processing
- Support for multiple file types:
  - EDI files (X12, EDIFACT)
  - PDF specifications
  - CSV files
- AI-powered mapping suggestions using sentence transformers
- Configurable ERP field definitions
- Detailed logging and error handling

## Project Structure

```
EDI-AI-automation-mapper/
├── input/              # Input directory for EDI files, PDFs, etc.
├── output/             # Output directory for generated mappings
├── models/             # Machine learning models and mapping engine
├── scripts/            # Utility scripts and file processors
├── logs/               # Application logs
├── main.py            # Main application entry point
└── requirements.txt    # Python dependencies
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/EDI-AI-automation-mapper.git
cd EDI-AI-automation-mapper
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your input files in the `input/` directory:
   - EDI files (.edi)
   - PDF specifications
   - CSV files

2. Run the application:
```bash
python main.py
```

3. The application will:
   - Monitor the input directory for new files
   - Process files as they arrive
   - Generate mapping suggestions
   - Save results to the output directory

## Configuration

The application can be configured by modifying the following:

- ERP field definitions in `models/mapping_engine.py`
- File processing settings in `scripts/file_processor.py`
- Logging configuration in `main.py`

## Development

### Adding New File Types

To add support for new file types:

1. Add the file extension to `FileProcessor.supported_extensions`
2. Implement a new processing method in `FileProcessor`
3. Update the mapping logic in `MappingEngine` if needed

### Testing

Run the test suite:
```bash
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
