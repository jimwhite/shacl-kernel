"""SHACL Kernel for Jupyter."""

from ipykernel.kernelbase import Kernel
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS, SH, XSD
from pyshacl import validate
import sys
import traceback
from io import StringIO


class SHACLKernel(Kernel):
    """A Jupyter kernel for SHACL (Shapes Constraint Language)."""
    
    implementation = 'SHACL'
    implementation_version = '1.0'
    language = 'shacl'
    language_version = '1.0'
    language_info = {
        'name': 'shacl',
        'mimetype': 'text/turtle',
        'file_extension': '.ttl',
        'codemirror_mode': 'turtle'
    }
    banner = "SHACL Kernel - Shapes Constraint Language"

    def __init__(self, **kwargs):
        """Initialize the SHACL kernel."""
        super().__init__(**kwargs)
        # Initialize graphs for data and shapes
        self.data_graph = Graph()
        self.shapes_graph = Graph()
        # Track execution count
        self._execution_count = 0

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        """Execute SHACL code."""
        self._execution_count += 1
        
        if not silent:
            # Parse the code and determine what to do
            try:
                result = self._process_code(code)
                
                if result:
                    self.send_response(self.iopub_socket, 'stream', {
                        'name': 'stdout',
                        'text': result
                    })
                
                return {
                    'status': 'ok',
                    'execution_count': self._execution_count,
                    'payload': [],
                    'user_expressions': {},
                }
            except Exception as e:
                # Capture the full traceback
                exc_type, exc_value, exc_traceback = sys.exc_info()
                tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                error_msg = ''.join(tb_lines)
                
                self.send_response(self.iopub_socket, 'stream', {
                    'name': 'stderr',
                    'text': error_msg
                })
                
                return {
                    'status': 'error',
                    'execution_count': self._execution_count,
                    'ename': type(e).__name__,
                    'evalue': str(e),
                    'traceback': tb_lines
                }
        
        return {
            'status': 'ok',
            'execution_count': self._execution_count,
            'payload': [],
            'user_expressions': {},
        }

    def _process_code(self, code):
        """Process SHACL code and return results."""
        lines = code.strip().split('\n')
        
        # Check for special commands
        if lines[0].startswith('%'):
            return self._handle_magic_command(lines[0], '\n'.join(lines[1:]))
        
        # Default: treat as Turtle data and add to data graph
        self.data_graph.parse(data=code, format='turtle')
        return f"Added {len(code.split())} triples to data graph. Total: {len(self.data_graph)} triples."

    def _handle_magic_command(self, magic_line, content):
        """Handle magic commands."""
        magic = magic_line.strip().lower()
        
        if magic == '%shapes':
            # Load shapes graph
            self.shapes_graph = Graph()
            self.shapes_graph.parse(data=content, format='turtle')
            return f"Loaded shapes graph with {len(self.shapes_graph)} triples."
        
        elif magic == '%data':
            # Load data graph
            self.data_graph = Graph()
            self.data_graph.parse(data=content, format='turtle')
            return f"Loaded data graph with {len(self.data_graph)} triples."
        
        elif magic == '%validate':
            # Validate data against shapes
            if len(self.shapes_graph) == 0:
                return "Error: No shapes graph loaded. Use %shapes to load shapes first."
            if len(self.data_graph) == 0:
                return "Error: No data graph loaded. Use %data to load data first."
            
            conforms, results_graph, results_text = validate(
                self.data_graph,
                shacl_graph=self.shapes_graph,
                inference='rdfs',
                abort_on_first=False,
            )
            
            output = []
            output.append(f"Validation {'PASSED' if conforms else 'FAILED'}")
            output.append(f"\n{results_text}")
            
            return '\n'.join(output)
        
        elif magic == '%clear':
            # Clear graphs
            self.data_graph = Graph()
            self.shapes_graph = Graph()
            return "Cleared all graphs."
        
        elif magic == '%show':
            # Show current graphs
            output = []
            output.append(f"Data graph: {len(self.data_graph)} triples")
            if len(self.data_graph) > 0:
                output.append("\nData:")
                output.append(self.data_graph.serialize(format='turtle'))
            
            output.append(f"\nShapes graph: {len(self.shapes_graph)} triples")
            if len(self.shapes_graph) > 0:
                output.append("\nShapes:")
                output.append(self.shapes_graph.serialize(format='turtle'))
            
            return '\n'.join(output)
        
        elif magic == '%help':
            return """Available magic commands:
%data      - Load data graph (Turtle format)
%shapes    - Load shapes graph (Turtle format)
%validate  - Validate data against shapes
%show      - Show current graphs
%clear     - Clear all graphs
%help      - Show this help message

Without magic commands, input is treated as Turtle data added to the data graph.
"""
        
        else:
            return f"Unknown magic command: {magic}. Use %help for available commands."

    def do_complete(self, code, cursor_pos):
        """Provide tab completion."""
        # Basic magic command completion
        if code.startswith('%'):
            commands = ['%data', '%shapes', '%validate', '%show', '%clear', '%help']
            matches = [cmd for cmd in commands if cmd.startswith(code[:cursor_pos])]
            return {
                'matches': matches,
                'cursor_start': 0,
                'cursor_end': cursor_pos,
                'metadata': {},
                'status': 'ok'
            }
        
        return {
            'matches': [],
            'cursor_start': cursor_pos,
            'cursor_end': cursor_pos,
            'metadata': {},
            'status': 'ok'
        }


if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=SHACLKernel)
