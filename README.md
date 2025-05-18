# Title

description

## Prerequisites
- Python 3.12 or newer
- pip

## Installation
### Clone the Repository
```sh
git clone https://github.com/lukestagoll/cap-weighted-index-cli.git
cd cap-weighted-index-cli
```

### Create a Virtual Environment
```sh
python -m venv .venv
```

### Activate the Virtual Environment
#### Linux/macOS
```sh
source .venv/bin/activate
```

#### Windows (Powershell)
```sh
.\.venv\Scripts\Activate.ps1
```

### Install Dependencies
#### For Development Usage
Install in editable mode:
```sh
pip install -e .
```

#### For Standard Usage
Install:
```sh
pip install .
```

## Usage
The application can be run using `cap-weighted-index` or `cwi`.

Display help for the main command:
```sh
cwi --help
```

## Running Tests
Use Python’s built-in unittest discovery:
```sh
python -m unittest discover
```

## Generating documentation
Generate HTML docs for the CLI module with pydoc:
```sh
pydoc -w cap_weighted_index_cli.cli
```

## License
Distributed under the MIT License. See the LICENSE file for details.