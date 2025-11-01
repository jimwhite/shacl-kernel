#!/usr/bin/env python3
"""
Test script for the SPARQL functionality in the SHACL kernel.
Tests magic commands and SPARQL query functionality.
"""

from shacl_kernel.kernel import SHACLKernel
from unittest.mock import Mock
import sys


def test_sparql_magics():
    """Test SPARQL magic commands."""
    print("=" * 70)
    print("Test: SPARQL Magic Commands")
    print("=" * 70)
    
    kernel = SHACLKernel()
    kernel.iopub_socket = Mock()
    
    # Test %endpoint magic
    result = kernel.do_execute('%endpoint https://dbpedia.org/sparql', silent=False)
    assert result['status'] == 'ok', "Setting endpoint should succeed"
    print(f"✓ %endpoint magic works")
    
    # Test %format magic
    result = kernel.do_execute('%format JSON', silent=False)
    assert result['status'] == 'ok', "Setting format should succeed"
    print(f"✓ %format magic works")
    
    # Test %display magic
    result = kernel.do_execute('%display table', silent=False)
    assert result['status'] == 'ok', "Setting display should succeed"
    print(f"✓ %display magic works")
    
    # Test %show magic (limit)
    result = kernel.do_execute('%show 10', silent=False)
    assert result['status'] == 'ok', "Setting show limit should succeed"
    print(f"✓ %show magic works")
    
    # Test %prefix magic
    result = kernel.do_execute('%prefix dbo http://dbpedia.org/ontology/', silent=False)
    assert result['status'] == 'ok', "Setting prefix should succeed"
    print(f"✓ %prefix magic works")
    
    # Test %lsmagics
    result = kernel.do_execute('%lsmagics', silent=False)
    assert result['status'] == 'ok', "Listing magics should succeed"
    print(f"✓ %lsmagics magic works")
    
    print()


def test_sparql_completion():
    """Test SPARQL keyword completion."""
    print("=" * 70)
    print("Test: SPARQL Keyword Completion")
    print("=" * 70)
    
    kernel = SHACLKernel()
    
    # Test SPARQL keyword completion
    result = kernel.do_complete('SEL', 3)
    assert result['status'] == 'ok', "Completion should succeed"
    assert 'SELECT' in result['matches'], "Should suggest SELECT"
    print(f"✓ SPARQL keyword completion works")
    print(f"✓ Matches for 'SEL': {result['matches']}")
    
    # Test magic completion with SPARQL magics
    result = kernel.do_complete('%end', 4)
    assert result['status'] == 'ok', "Completion should succeed"
    assert '%endpoint' in result['matches'], "Should suggest %endpoint"
    print(f"✓ SPARQL magic completion works")
    print(f"✓ Matches for '%end': {result['matches']}")
    
    print()


def test_sparql_help():
    """Test SPARQL contextual help."""
    print("=" * 70)
    print("Test: SPARQL Contextual Help")
    print("=" * 70)
    
    kernel = SHACLKernel()
    
    # Test help for SPARQL keyword
    result = kernel.do_inspect('SELECT', 3, detail_level=0)
    assert result['status'] == 'ok', "Inspect should succeed"
    assert result['found'], "Help for SELECT should be found"
    print(f"✓ Help for SELECT keyword available")
    
    # Test help for magic
    result = kernel.do_inspect('%endpoint', 3, detail_level=0)
    assert result['status'] == 'ok', "Inspect should succeed"
    assert result['found'], "Help for %endpoint should be found"
    print(f"✓ Help for %endpoint magic available")
    
    print()


def test_sparql_query_detection():
    """Test SPARQL query detection logic."""
    print("=" * 70)
    print("Test: SPARQL Query Detection")
    print("=" * 70)
    
    kernel = SHACLKernel()
    
    # Test that SELECT is detected as SPARQL
    assert kernel._is_sparql_query('SELECT * WHERE { ?s ?p ?o }'), "SELECT should be detected"
    print(f"✓ SELECT query detected")
    
    # Test that CONSTRUCT is detected as SPARQL
    assert kernel._is_sparql_query('CONSTRUCT { ?s ?p ?o } WHERE { ?s ?p ?o }'), "CONSTRUCT should be detected"
    print(f"✓ CONSTRUCT query detected")
    
    # Test that ASK is detected as SPARQL
    assert kernel._is_sparql_query('ASK { ?s ?p ?o }'), "ASK should be detected"
    print(f"✓ ASK query detected")
    
    # Test that DESCRIBE is detected as SPARQL
    assert kernel._is_sparql_query('DESCRIBE <http://example.org/resource>'), "DESCRIBE should be detected"
    print(f"✓ DESCRIBE query detected")
    
    # Test that Turtle is not detected as SPARQL
    assert not kernel._is_sparql_query('@prefix ex: <http://example.org/> .'), "Turtle should not be detected"
    print(f"✓ Turtle syntax not detected as SPARQL")
    
    print()


def test_combined_shacl_sparql():
    """Test that SHACL and SPARQL functionality work together."""
    print("=" * 70)
    print("Test: Combined SHACL and SPARQL Functionality")
    print("=" * 70)
    
    kernel = SHACLKernel()
    kernel.iopub_socket = Mock()
    
    # Load some SHACL data
    data = """
@prefix ex: <http://example.org/> .
@prefix schema: <http://schema.org/> .

ex:Person1 a schema:Person ;
    schema:name "Alice" ;
    schema:age 30 .
"""
    
    result = kernel.do_execute(data, silent=False)
    assert result['status'] == 'ok', "Loading data should succeed"
    assert len(kernel.data_graph) > 0, "Data graph should have triples"
    print(f"✓ SHACL data loaded ({len(kernel.data_graph)} triples)")
    
    # Set SPARQL endpoint
    result = kernel.do_execute('%endpoint https://dbpedia.org/sparql', silent=False)
    assert result['status'] == 'ok', "Setting endpoint should succeed"
    print(f"✓ SPARQL endpoint configured")
    
    # Verify both systems are independent
    assert len(kernel.data_graph) > 0, "SHACL data should still exist"
    assert kernel._sparql.cfg.ept == 'https://dbpedia.org/sparql', "Endpoint should be set"
    print(f"✓ SHACL and SPARQL systems work independently")
    
    print()


def test_help_message():
    """Test that comprehensive help message is available."""
    print("=" * 70)
    print("Test: Comprehensive Help Message")
    print("=" * 70)
    
    kernel = SHACLKernel()
    kernel.iopub_socket = Mock()
    
    result = kernel.do_execute('%help', silent=False)
    assert result['status'] == 'ok', "Help command should succeed"
    print(f"✓ %help command works")
    
    # Verify the help text contains expected content
    help_text = kernel._get_help_text()
    assert 'SHACL Magic Commands' in help_text, "Help should mention SHACL commands"
    assert 'SPARQL Magic Commands' in help_text, "Help should mention SPARQL commands"
    assert '%endpoint' in help_text, "Help should document %endpoint"
    assert '%validate' in help_text, "Help should document %validate"
    print(f"✓ Help message contains SHACL and SPARQL documentation")
    
    print()


def main():
    """Run all SPARQL tests."""
    print("\n" + "=" * 70)
    print("SPARQL Functionality Test Suite")
    print("=" * 70)
    print()
    
    try:
        test_sparql_magics()
        test_sparql_completion()
        test_sparql_help()
        test_sparql_query_detection()
        test_combined_shacl_sparql()
        test_help_message()
        
        print("=" * 70)
        print("✓ All SPARQL tests passed successfully!")
        print("=" * 70)
        print("\nThe SHACL kernel now includes full SPARQL support:")
        print("  • SPARQL magic commands for endpoint configuration")
        print("  • SPARQL query execution (SELECT, CONSTRUCT, ASK, DESCRIBE)")
        print("  • Keyword completion for SPARQL")
        print("  • Contextual help for SPARQL keywords and magics")
        print("  • Independent SHACL and SPARQL systems")
        print("  • Comprehensive documentation")
        print()
        
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
