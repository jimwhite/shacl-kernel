# SPARQL Integration Summary

## Overview

This document summarizes the integration of SPARQL kernel functionality into the SHACL kernel. The integration is based on the [sparql-kernel project](https://github.com/paulovn/sparql-kernel) by Paulo Villegas, which is licensed under the 3-clause BSD License.

## What Was Added

### 1. SPARQL Module (`shacl_kernel/sparql/`)

The following files were adapted from the sparql-kernel project:

- **constants.py** - Configuration constants and default values
- **utils.py** - Utility functions for message formatting and error handling
- **language.py** - SPARQL keyword definitions and contextual help text
- **magics.py** - Magic command processing for SPARQL configuration
- **connection.py** - SPARQL endpoint connection and query execution
- **drawgraph.py** - RDF graph visualization support (requires Graphviz)

All files include proper attribution in their headers.

### 2. Enhanced Kernel (`shacl_kernel/kernel.py`)

The kernel was enhanced to support both SHACL and SPARQL operations:

- Separate processing for SHACL and SPARQL magic commands
- Automatic detection of SPARQL queries vs RDF/Turtle content
- Tab completion for SPARQL keywords and all magic commands
- Contextual help for SPARQL keywords and magics
- Independent operation of SHACL validation and SPARQL querying

### 3. Dependencies

Added to `setup.py`:
- `SPARQLWrapper>=2.0.0` - For SPARQL endpoint communication

### 4. Documentation

- **NOTICE** - Attribution file for sparql-kernel sources
- **README.md** - Updated with SPARQL features and attribution
- **EXAMPLES_FULL.md** - Comprehensive usage examples for both SHACL and SPARQL
- **test_sparql.py** - Full test coverage for SPARQL functionality

## Features

### SHACL Features (Original, Preserved)

- Load RDF data graphs in Turtle format
- Load SHACL shapes graphs
- Validate data against shapes
- View and clear graphs
- Magic commands: `%data`, `%shapes`, `%validate`, `%show`, `%clear`, `%help`

### SPARQL Features (New)

#### Magic Commands for Configuration

- `%endpoint <url>` - Set SPARQL endpoint (required for queries)
- `%auth <method> <user> <password>` - HTTP authentication (basic/digest)
- `%qparam <name> [<value>]` - Custom query parameters
- `%http_header <name> [<value>]` - Custom HTTP headers
- `%prefix <name> [<uri>]` - Namespace prefixes for queries
- `%header <string> | OFF` - SPARQL header lines
- `%graph <uri>` - Default graph
- `%format JSON | N3 | XML | ...` - Result format
- `%display raw | table | diagram` - Display mode
- `%lang <langs>` - Language preferences for labels
- `%show <n> | all` - Result limit
- `%outfile <file> | off` - Save output to file
- `%log <level>` - Logging level
- `%method get | post` - HTTP method
- `%lsmagics` - List all available magics

#### SPARQL Query Support

- **SELECT** - Query for variable bindings
- **CONSTRUCT** - Build new RDF graphs
- **ASK** - Boolean queries
- **DESCRIBE** - Resource descriptions
- **INSERT/DELETE** - Update operations (if endpoint supports)

#### Display Options

- **Table** - Formatted table display with optional type information
- **Raw** - Unformatted response
- **Diagram** - Visual RDF graph (SVG/PNG, requires Graphviz)

#### Auto-completion and Help

- Tab completion for SPARQL keywords
- Tab completion for all magic commands
- Contextual help (Shift-Tab) for keywords and magics
- Comprehensive help via `%help` command

## Testing

### Test Coverage

1. **test_kernel.py** (7 tests)
   - Kernel creation and properties
   - RDF data loading
   - SHACL shapes loading
   - SHACL validation
   - Magic commands
   - Tab completion
   - Error handling

2. **test_sparql.py** (6 tests)
   - SPARQL magic commands
   - SPARQL keyword completion
   - SPARQL contextual help
   - SPARQL query detection
   - Combined SHACL and SPARQL functionality
   - Comprehensive help message

### Test Results

All tests pass (13/13):
- ✅ All original SHACL tests pass
- ✅ All new SPARQL tests pass
- ✅ No security vulnerabilities detected (CodeQL)
- ✅ Code review issues resolved

## Architecture

### Separation of Concerns

The integration maintains clear separation between SHACL and SPARQL functionality:

1. **SHACL Operations**
   - Work with local RDF graphs (`self.data_graph`, `self.shapes_graph`)
   - Magic commands: `%data`, `%shapes`, `%validate`, `%show`, `%clear`
   - Uses `rdflib.Graph` and `pyshacl`

2. **SPARQL Operations**
   - Work with remote SPARQL endpoints
   - Magic commands: `%endpoint`, `%format`, `%display`, etc.
   - Uses `SPARQLWrapper` and `self._sparql.cfg`

3. **Shared Functionality**
   - `%help` - Shows documentation for both systems
   - Tab completion - Works for both SHACL and SPARQL magics
   - Contextual help - Available for both SPARQL keywords and magics

### Query Detection

The kernel automatically determines whether input is:
1. A SPARQL query (starts with SELECT, CONSTRUCT, ASK, DESCRIBE, etc.)
2. RDF/Turtle data (everything else)

This allows seamless switching between SHACL validation and SPARQL querying in the same notebook.

## Usage Examples

See `EXAMPLES_FULL.md` for comprehensive examples including:
- SHACL validation workflows
- SPARQL endpoint queries
- Combined SHACL and SPARQL usage
- All magic command examples

## Attribution

This integration is based on code from the sparql-kernel project:
- **Project**: https://github.com/paulovn/sparql-kernel
- **Author**: Paulo Villegas
- **License**: 3-clause BSD License
- **Files**: All files in `shacl_kernel/sparql/`

See the `NOTICE` file for complete attribution and license text.

## Compatibility

- **Python**: 3.8+
- **ipykernel**: 6.0.0+
- **rdflib**: 6.0.0+
- **pyshacl**: 0.20.0+
- **SPARQLWrapper**: 2.0.0+
- **Graphviz**: Optional, for diagram visualization

## Future Enhancements

Possible future improvements:
1. Add more visualization options for SHACL validation results
2. Support for SHACL advanced features integration with SPARQL
3. Query result caching
4. Batch query execution
5. SPARQL endpoint autoconfiguration from common sources

## Conclusion

The integration successfully combines SHACL validation and SPARQL querying capabilities in a single Jupyter kernel, maintaining the original SHACL functionality while adding comprehensive SPARQL support through well-designed magic commands and proper attribution to the original sparql-kernel project.
