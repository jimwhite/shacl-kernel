# SHACL Kernel

A Jupyter kernel for SHACL (Shapes Constraint Language) that enables interactive validation and exploration of RDF data using SHACL constraints.

## Features

- Interactive SHACL validation in Jupyter notebooks
- Support for loading data and shapes graphs
- Built on `ipykernel.kernelbase.Kernel` base class
- Magic commands for graph management and validation
- Turtle format support for RDF data

## Installation

### Prerequisites

- Python 3.8 or higher
- Jupyter or JupyterLab

### Install from source

```bash
# Clone the repository
git clone https://github.com/jimwhite/shacl-kernel.git
cd shacl-kernel

# Install the package
pip install -e .

# Install the kernel spec
python -m shacl_kernel.install --user
```

Or use the provided installation script:

```bash
pip install -e .
install-shacl-kernel --user
```

## Usage

After installation, you can create a new notebook with the SHACL kernel in Jupyter:

1. Open Jupyter Notebook or JupyterLab
2. Create a new notebook
3. Select "SHACL" as the kernel

### Magic Commands

The SHACL kernel supports the following magic commands:

- `%data` - Load data graph (Turtle format)
- `%shapes` - Load shapes graph (Turtle format)
- `%validate` - Validate data against shapes
- `%show` - Show current graphs
- `%clear` - Clear all graphs
- `%help` - Show help message

### Example

```turtle
# Load data graph
%data
@prefix ex: <http://example.org/> .
@prefix schema: <http://schema.org/> .

ex:Person1 a schema:Person ;
    schema:name "John Doe" ;
    schema:age 30 .
```

```turtle
# Load shapes graph
%shapes
@prefix ex: <http://example.org/> .
@prefix schema: <http://schema.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .

ex:PersonShape a sh:NodeShape ;
    sh:targetClass schema:Person ;
    sh:property [
        sh:path schema:name ;
        sh:minCount 1 ;
        sh:datatype xsd:string ;
    ] ;
    sh:property [
        sh:path schema:age ;
        sh:minCount 1 ;
        sh:datatype xsd:integer ;
    ] .
```

```
# Validate
%validate
```

## Architecture

The SHACL kernel is built on top of:

- **ipykernel**: Provides the `KernelBase` class for Jupyter kernel implementation
- **rdflib**: RDF graph parsing and manipulation
- **pyshacl**: SHACL validation engine

The kernel maintains two separate RDF graphs:
- **Data graph**: Stores the RDF data to be validated
- **Shapes graph**: Stores the SHACL shapes for validation

## Development

To set up a development environment:

```bash
# Clone the repository
git clone https://github.com/jimwhite/shacl-kernel.git
cd shacl-kernel

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Install the kernel spec
python -m shacl_kernel.install --user
```

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
