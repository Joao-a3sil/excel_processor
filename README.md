# Excel Processor

This project is designed to process Excel files related to various financial data, specifically focusing on "Bolsa", "Novo Bolsa", "Parcela", and "DIH Pay". The application reads input files, processes the data, and generates output files with the processed information.

## Project Structure

```
excel_processor
├── processor
│   ├── __init__.py
│   ├── main.py
│   ├── process
│   │   ├── __init__.py
│   │   ├── process_bolsa.py
│   │   ├── process_cea.py
│   │   ├── process_dih_pay.py
│   │   ├── process_novo_bolsa.py
│   │   └── process_parcela.py
│   └── util
│       ├── __init__.py
│       └── util.py
├── input
│   └── (place your input files here)
├── output
│   └── (generated files will be saved here)
├── setup.py
├── run_process.bat
└── README.md
```

## Installation

To install the required dependencies, run:

```
pip install -r requirements.txt
```

## Usage

To run the application, execute the following command:

```
python processor/main.py
```

Alternatively, you can use the provided batch file:

```
run_process.bat
```

## Features

- **Data Processing**: The application processes various financial data from Excel files, creating identification codes, filtering data, and saving the results to new files.
- **Execution Time Measurement**: The application measures the execution time of each processing function for performance tracking.
- **Output Management**: Processed data is saved in the `output` directory for easy access.

## Future Improvements

- **Organize by Feature**: Consider restructuring the project to organize files by feature rather than by type.
- **Use Classes**: Refactor processing functions into classes to encapsulate data and behavior.
- **Configuration Management**: Implement a configuration file for managing settings and parameters.
- **Add Tests**: Create a tests directory with unit tests for each processing function.
- **Enhanced Documentation**: Provide more detailed usage examples and project structure explanations.
- **Logging**: Implement logging for better tracking of application behavior and errors.
- **Type Hinting**: Use type hints in function signatures for improved clarity and static type checking.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.