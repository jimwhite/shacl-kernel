# SHACL Kernel Examples

This document provides examples of using the SHACL kernel with both SHACL validation and SPARQL query functionality.

## SHACL Validation Examples

### Example 1: Basic SHACL Validation

Load data:
```turtle
%data
@prefix ex: <http://example.org/> .
@prefix schema: <http://schema.org/> .

ex:Person1 a schema:Person ;
    schema:name "Alice Smith" ;
    schema:age 30 ;
    schema:email "alice@example.org" .

ex:Person2 a schema:Person ;
    schema:name "Bob Jones" ;
    schema:age 25 .
```

Load shapes:
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
        sh:minInclusive 0 ;
        sh:maxInclusive 150 ;
    ] ;
    sh:property [
        sh:path schema:email ;
        sh:minCount 1 ;
        sh:datatype xsd:string ;
    ] .
```

Validate:
```
%validate
```

Expected output: Validation will FAIL because ex:Person2 is missing the email property.

### Example 2: Show Current Graphs

```
%show
```

This displays the contents of both the data and shapes graphs.

### Example 3: Clear Graphs

```
%clear
```

This removes all triples from both graphs.

## SPARQL Query Examples

### Example 1: Query DBpedia for Scientists

Set up the endpoint:
```
%endpoint https://dbpedia.org/sparql
%format JSON
%display table
%show 10
```

Query for scientists:
```sparql
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?person ?name ?birthDate WHERE {
  ?person a dbo:Scientist ;
          rdfs:label ?name ;
          dbo:birthDate ?birthDate .
  FILTER (lang(?name) = 'en')
}
ORDER BY ?birthDate
LIMIT 10
```

### Example 2: Set Prefixes for Easier Queries

```
%prefix dbo http://dbpedia.org/ontology/
%prefix dbr http://dbpedia.org/resource/
%prefix rdfs http://www.w3.org/2000/01/rdf-schema#
```

Now you can use shorter queries:
```sparql
SELECT ?label WHERE {
  dbr:Albert_Einstein rdfs:label ?label .
  FILTER (lang(?label) = 'en')
}
```

### Example 3: ASK Query

Check if a fact exists:
```sparql
ASK {
  <http://dbpedia.org/resource/Albert_Einstein> a <http://dbpedia.org/ontology/Scientist>
}
```

### Example 4: CONSTRUCT Query

Create a new RDF graph:
```sparql
%format N3
%display diagram svg

CONSTRUCT {
  ?person <http://example.org/hasName> ?name .
} WHERE {
  ?person a dbo:Scientist ;
          rdfs:label ?name .
  FILTER (lang(?name) = 'en')
}
LIMIT 5
```

### Example 5: Use Authentication

For endpoints that require authentication:
```
%auth basic username password
```

Or using environment variables:
```
%auth basic env:SPARQL_USER env:SPARQL_PASS
```

### Example 6: Custom Query Parameters

Add API keys or other parameters:
```
%qparam apikey YOUR_API_KEY
%qparam timeout 30000
```

### Example 7: Display Options

Change how results are displayed:
```
%display table withtypes    # Show data types in table
%display raw                # Show raw response
%display diagram png        # Show RDF graph as PNG diagram
```

### Example 8: Language Preferences

Set preferred languages for labels:
```
%lang en es fr              # Prefer English, Spanish, French
%lang default               # Use default languages
%lang all                   # Show all languages
```

## Combined SHACL and SPARQL Workflow

1. Load local data for validation:
```turtle
%data
@prefix ex: <http://example.org/> .
ex:Resource1 a ex:Thing ;
    ex:property "value" .
```

2. Validate against local shapes:
```turtle
%shapes
@prefix ex: <http://example.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
ex:ThingShape a sh:NodeShape ;
    sh:targetClass ex:Thing .
```

```
%validate
```

3. Query external SPARQL endpoint for additional context:
```
%endpoint https://dbpedia.org/sparql
```

```sparql
SELECT ?related WHERE {
  ?related rdfs:label "Thing"@en .
}
LIMIT 5
```

## Magic Commands Reference

### SHACL Commands
- `%data` - Load data graph
- `%shapes` - Load shapes graph
- `%validate` - Validate data against shapes
- `%show` - Display current graphs
- `%clear` - Clear all graphs
- `%help` - Show help

### SPARQL Commands
- `%endpoint <url>` - Set SPARQL endpoint (required)
- `%format <fmt>` - Set result format (JSON, XML, N3)
- `%display <mode>` - Set display mode (table, raw, diagram)
- `%prefix <name> <uri>` - Set namespace prefix
- `%show <n>` - Limit results shown
- `%auth <method> <user> <pass>` - Set authentication
- `%qparam <name> <value>` - Add query parameter
- `%http_header <name> <value>` - Add HTTP header
- `%graph <uri>` - Set default graph
- `%header <text>` - Add header to queries
- `%lang <langs>` - Set language preferences
- `%outfile <file>` - Save output to file
- `%log <level>` - Set logging level
- `%method <get|post>` - Set HTTP method
- `%lsmagics` - List all magics

## Tips

1. Use `%lsmagics` to see all available magic commands
2. Use `%help` to see comprehensive documentation
3. SHACL magics work with local graphs
4. SPARQL magics work with remote endpoints
5. Both systems can be used independently in the same notebook
6. Tab completion works for both SPARQL keywords and magic commands
7. Shift-Tab shows contextual help for keywords and magics
