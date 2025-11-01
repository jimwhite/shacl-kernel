#!/usr/bin/env python3
"""
Comprehensive test script for the SHACL kernel.
This demonstrates all the functionality of the kernel.
"""

from shacl_kernel.kernel import SHACLKernel
from unittest.mock import Mock


def test_kernel_creation():
    """Test that kernel can be created and has correct properties."""
    print("=" * 70)
    print("Test 1: Kernel Creation and Properties")
    print("=" * 70)
    
    kernel = SHACLKernel()
    
    # Verify kernel properties
    assert kernel.implementation == 'SHACL', "Implementation should be SHACL"
    assert kernel.language == 'shacl', "Language should be shacl"
    assert hasattr(kernel, 'data_graph'), "Should have data_graph"
    assert hasattr(kernel, 'shapes_graph'), "Should have shapes_graph"
    
    # Verify it inherits from Kernel
    from ipykernel.kernelbase import Kernel
    assert isinstance(kernel, Kernel), "Should inherit from Kernel"
    
    print(f"✓ Kernel implementation: {kernel.implementation} {kernel.implementation_version}")
    print(f"✓ Language: {kernel.language} {kernel.language_version}")
    print(f"✓ Banner: {kernel.banner}")
    print(f"✓ Inherits from ipykernel.kernelbase.Kernel")
    print()
    
    return kernel


def test_data_loading(kernel):
    """Test loading RDF data into the data graph."""
    print("=" * 70)
    print("Test 2: Loading RDF Data")
    print("=" * 70)
    
    # Mock the socket
    kernel.iopub_socket = Mock()
    
    # Load some test data
    data = """
@prefix ex: <http://example.org/> .
@prefix schema: <http://schema.org/> .

ex:Person1 a schema:Person ;
    schema:name "Alice" ;
    schema:age 30 ;
    schema:email "alice@example.org" .

ex:Person2 a schema:Person ;
    schema:name "Bob" ;
    schema:age 25 ;
    schema:email "bob@example.org" .
"""
    
    result = kernel.do_execute(data, silent=False)
    assert result['status'] == 'ok', "Data loading should succeed"
    
    print(f"✓ Loaded data successfully")
    print(f"✓ Data graph contains {len(kernel.data_graph)} triples")
    print()


def test_shapes_loading(kernel):
    """Test loading SHACL shapes."""
    print("=" * 70)
    print("Test 3: Loading SHACL Shapes")
    print("=" * 70)
    
    shapes = """
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
        sh:minCount 1 ;
        sh:datatype xsd:string ;
    ] .
"""
    
    result = kernel.do_execute(shapes, silent=False)
    assert result['status'] == 'ok', "Shapes loading should succeed"
    
    print(f"✓ Loaded shapes successfully")
    print(f"✓ Shapes graph contains {len(kernel.shapes_graph)} triples")
    print()


def test_validation(kernel):
    """Test SHACL validation."""
    print("=" * 70)
    print("Test 4: SHACL Validation")
    print("=" * 70)
    
    result = kernel.do_execute('%validate', silent=False)
    assert result['status'] == 'ok', "Validation should succeed"
    
    print(f"✓ Validation executed successfully")
    print()


def test_magic_commands(kernel):
    """Test various magic commands."""
    print("=" * 70)
    print("Test 5: Magic Commands")
    print("=" * 70)
    
    # Test %help
    result = kernel.do_execute('%help', silent=False)
    assert result['status'] == 'ok', "%help should succeed"
    print(f"✓ %help command works")
    
    # Test %show
    result = kernel.do_execute('%show', silent=False)
    assert result['status'] == 'ok', "%show should succeed"
    print(f"✓ %show command works")
    
    # Test %clear
    result = kernel.do_execute('%clear', silent=False)
    assert result['status'] == 'ok', "%clear should succeed"
    assert len(kernel.data_graph) == 0, "Data graph should be empty after clear"
    assert len(kernel.shapes_graph) == 0, "Shapes graph should be empty after clear"
    print(f"✓ %clear command works")
    print()


def test_tab_completion():
    """Test tab completion functionality."""
    print("=" * 70)
    print("Test 6: Tab Completion")
    print("=" * 70)
    
    kernel = SHACLKernel()
    
    # Test magic command completion
    result = kernel.do_complete('%da', 3)
    assert result['status'] == 'ok', "Completion should succeed"
    assert '%data' in result['matches'], "Should suggest %data"
    print(f"✓ Tab completion works for magic commands")
    print(f"✓ Matches for '%da': {result['matches']}")
    print()


def test_error_handling():
    """Test error handling."""
    print("=" * 70)
    print("Test 7: Error Handling")
    print("=" * 70)
    
    kernel = SHACLKernel()
    kernel.iopub_socket = Mock()
    
    # Try to parse invalid Turtle
    invalid_turtle = """
@prefix ex: <http://example.org/> .
ex:Invalid syntax here
"""
    
    result = kernel.do_execute(invalid_turtle, silent=False)
    assert result['status'] == 'error', "Invalid Turtle should return error"
    print(f"✓ Error handling works correctly")
    print()


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("SHACL Kernel Comprehensive Test Suite")
    print("=" * 70)
    print()
    
    try:
        kernel = test_kernel_creation()
        test_data_loading(kernel)
        test_shapes_loading(kernel)
        test_validation(kernel)
        test_magic_commands(kernel)
        test_tab_completion()
        test_error_handling()
        
        print("=" * 70)
        print("✓ All tests passed successfully!")
        print("=" * 70)
        print("\nThe SHACL kernel is working correctly and includes:")
        print("  • Proper inheritance from ipykernel.kernelbase.Kernel")
        print("  • RDF data loading in Turtle format")
        print("  • SHACL shapes loading")
        print("  • SHACL validation functionality")
        print("  • Magic commands (%data, %shapes, %validate, %show, %clear, %help)")
        print("  • Tab completion for magic commands")
        print("  • Error handling")
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
    import sys
    sys.exit(main())
