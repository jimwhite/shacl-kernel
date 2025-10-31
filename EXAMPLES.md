# SHACL Kernel Usage Examples

This document provides examples of using the SHACL kernel in Jupyter notebooks.

## Installation

First, install the kernel:

```bash
pip install -e .
install-shacl-kernel --user
```

## Basic Usage

### Example 1: Loading Data and Shapes

In a Jupyter notebook with the SHACL kernel:

**Cell 1: Load data**
```turtle
@prefix ex: <http://example.org/> .
@prefix schema: <http://schema.org/> .

ex:Person1 a schema:Person ;
    schema:name "John Doe" ;
    schema:age 30 .
```

Output:
```
Added 3 triples to data graph. Total: 3 triples.
```

**Cell 2: Load shapes**
```turtle
%shapes
@prefix ex: <http://example.org/> .
@prefix schema: <http://schema.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

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

Output:
```
Loaded shapes graph with 10 triples.
```

**Cell 3: Validate**
```
%validate
```

Output:
```
Validation PASSED

Validation Report
Conforms: True
```

## Example 2: Validation Failure

**Cell 1: Load invalid data**
```turtle
%data
@prefix ex: <http://example.org/> .
@prefix schema: <http://schema.org/> .

ex:Person1 a schema:Person ;
    schema:name "Jane Smith" .
    # Missing required age
```

**Cell 2: Load shapes (same as above)**
```turtle
%shapes
@prefix ex: <http://example.org/> .
@prefix schema: <http://schema.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:PersonShape a sh:NodeShape ;
    sh:targetClass schema:Person ;
    sh:property [
        sh:path schema:name ;
        sh:minCount 1 ;
    ] ;
    sh:property [
        sh:path schema:age ;
        sh:minCount 1 ;
        sh:datatype xsd:integer ;
    ] .
```

**Cell 3: Validate**
```
%validate
```

Output:
```
Validation FAILED

Validation Report
Conforms: False

Results (1):
Constraint Violation in MinCountConstraintComponent (http://www.w3.org/ns/shacl#MinCountConstraintComponent):
	Severity: sh:Violation
	Source Shape: [ ... ]
	Focus Node: ex:Person1
	Result Path: schema:age
	Message: Less than 1 values
```

## Example 3: Working with Multiple Data Graphs

**Cell 1: Add first person**
```turtle
@prefix ex: <http://example.org/> .
@prefix schema: <http://schema.org/> .

ex:Person1 a schema:Person ;
    schema:name "Alice" ;
    schema:age 30 .
```

**Cell 2: Add second person**
```turtle
@prefix ex: <http://example.org/> .
@prefix schema: <http://schema.org/> .

ex:Person2 a schema:Person ;
    schema:name "Bob" ;
    schema:age 25 .
```

**Cell 3: Show current graphs**
```
%show
```

Output shows both people in the data graph.

**Cell 4: Clear and start fresh**
```
%clear
```

## Magic Commands Reference

### `%data`
Loads a new data graph, replacing any existing data graph.

```turtle
%data
@prefix ex: <http://example.org/> .
ex:subject ex:predicate ex:object .
```

### `%shapes`
Loads a new shapes graph, replacing any existing shapes graph.

```turtle
%shapes
@prefix sh: <http://www.w3.org/ns/shacl#> .
# SHACL shapes here
```

### `%validate`
Validates the current data graph against the current shapes graph.

```
%validate
```

### `%show`
Displays the current data and shapes graphs.

```
%show
```

### `%clear`
Clears both the data and shapes graphs.

```
%clear
```

### `%help`
Shows help information about available magic commands.

```
%help
```

## Advanced Examples

### Example 4: Complex Shapes with Multiple Properties

```turtle
%shapes
@prefix ex: <http://example.org/> .
@prefix schema: <http://schema.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:PersonShape a sh:NodeShape ;
    sh:targetClass schema:Person ;
    sh:property [
        sh:path schema:name ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:datatype xsd:string ;
        sh:minLength 1 ;
    ] ;
    sh:property [
        sh:path schema:age ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:datatype xsd:integer ;
        sh:minInclusive 0 ;
        sh:maxInclusive 150 ;
    ] ;
    sh:property [
        sh:path schema:email ;
        sh:minCount 0 ;
        sh:maxCount 1 ;
        sh:datatype xsd:string ;
        sh:pattern "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$" ;
    ] ;
    sh:property [
        sh:path schema:knows ;
        sh:class schema:Person ;  # Must reference another Person
    ] .
```

### Example 5: Using RDFS Inference

The kernel uses RDFS inference during validation, which means it will understand:
- Class hierarchies (subClassOf)
- Property hierarchies (subPropertyOf)
- Domain and range constraints

```turtle
@prefix ex: <http://example.org/> .
@prefix schema: <http://schema.org/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

ex:Employee rdfs:subClassOf schema:Person .

ex:Employee1 a ex:Employee ;
    schema:name "John" ;
    schema:age 30 .
```

This will be validated against PersonShape even though Employee1 is not directly a schema:Person.

## Tips

1. **Incremental Development**: You can add data incrementally without `%data` magic. Each cell without a magic command adds to the existing data graph.

2. **Reloading Shapes**: Use `%shapes` to reload shapes when you need to modify your validation rules.

3. **Debugging**: Use `%show` to inspect the current state of your graphs.

4. **Starting Fresh**: Use `%clear` when you want to start a new validation scenario.

5. **RDFS Inference**: The validation uses RDFS inference, so consider using ontology features in your shapes.
