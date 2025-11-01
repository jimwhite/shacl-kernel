# SHACL Kernel

A Jupyter kernel for SHACL (Shapes Constraint Language) that enables interactive validation and exploration of RDF data using SHACL constraints, with integrated SPARQL query support.

## Features

- Interactive SHACL validation in Jupyter notebooks
- Support for loading data and shapes graphs
- Built on `ipykernel.kernelbase.Kernel` base class
- Magic commands for graph management and validation
- **Integrated SPARQL endpoint querying** (from [sparql-kernel](https://github.com/paulovn/sparql-kernel))
- **Comprehensive SPARQL magic commands** for endpoint configuration and query control
- Turtle format support for RDF data
- Multiple result display formats (table, raw, diagram)

## Attribution

This kernel integrates SPARQL functionality from the [SPARQL kernel project](https://github.com/paulovn/sparql-kernel) by Paulo Villegas, licensed under the 3-clause BSD License. See the NOTICE file for complete attribution details.

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

#### SHACL Commands

- `%data` - Load data graph (Turtle format)
- `%shapes` - Load shapes graph (Turtle format)
- `%validate` - Validate data against shapes
- `%show` - Show current graphs
- `%clear` - Clear all graphs
- `%help` - Show comprehensive help message

#### SPARQL Commands

The kernel includes full SPARQL support via magic commands from the sparql-kernel project:

- `%endpoint <url>` - Set SPARQL endpoint (**REQUIRED** for SPARQL queries)
- `%auth <method> <user> <password>` - Set HTTP authentication (basic/digest)
- `%qparam <name> [<value>]` - Add or delete a custom query parameter
- `%http_header <name> [<value>]` - Add or delete an HTTP header
- `%prefix <name> [<uri>]` - Set or delete a URI prefix for all queries
- `%header <string> | OFF` - Add or delete a SPARQL header line
- `%graph <uri>` - Set default graph for queries
- `%format JSON | N3 | XML | default | any | none` - Set result format
- `%display raw | table [withtypes] | diagram [svg|png]` - Set display format
- `%lang <lang> [...] | default | all` - Set preferred language(s) for labels
- `%show <n> | all` - Set maximum number of results shown
- `%outfile <filename> | off` - Save raw output to a file
- `%log <level>` - Set logging level (critical|error|warning|info|debug)
- `%method get | post` - Set HTTP method
- `%lsmagics` - List all available magic commands

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

### SPARQL Query Example

```sparql
# Set endpoint for DBpedia
%endpoint https://dbpedia.org/sparql

# Query for famous scientists
SELECT ?person ?name ?birthDate WHERE {
  ?person a dbo:Scientist ;
          rdfs:label ?name ;
          dbo:birthDate ?birthDate .
  FILTER (lang(?name) = 'en')
}
LIMIT 10
```

## Architecture

The SHACL kernel is built on top of:

- **ipykernel**: Provides the `KernelBase` class for Jupyter kernel implementation
- **rdflib**: RDF graph parsing and manipulation
- **pyshacl**: SHACL validation engine
- **SPARQLWrapper**: SPARQL endpoint communication (from sparql-kernel)

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
