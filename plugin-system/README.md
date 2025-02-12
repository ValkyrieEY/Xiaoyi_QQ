# README.md Content

# Plugin System

This project implements a plugin system that allows for dynamic loading and management of plugins. The system is designed to load Python files from a specified directory, enabling extensibility and modularity.

## Features

- Automatically loads plugins from a designated directory.
- Filters out plugins with the prefix `fix_`, preventing them from being activated.
- Provides a sample question-and-answer plugin as an example of how to create plugins.

## Directory Structure

- `src/plugins`: Contains all plugin files.
  - `example_qa.py`: A sample question-and-answer plugin.
  - `fix_broken.py`: A plugin that is not loaded due to its prefix.
- `src/core`: Contains core functionality for loading and managing plugins.
- `src/config`: Configuration files for the plugin system.
- `src/main.py`: The entry point for the application.
- `tests`: Contains unit tests for the plugin system.

## Installation

1. Clone the repository.
2. Navigate to the project directory.
3. Install the required dependencies using:

   ```
   pip install -r requirements.txt
   ```

## Usage

To run the plugin system, execute the following command:

```
python src/main.py
```

This will initialize the plugin manager and load all applicable plugins from the specified directory.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.