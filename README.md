# excel_processor
This project is designed to process Excel files related to various financial data, specifically focusing on "Bolsa", "Novo Bolsa", "Parcela", and "DIH Pay". The application reads input files, processes the data, and generates output files with the processed information.

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
