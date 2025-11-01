"""SHACL Kernel for Jupyter with integrated SPARQL support."""

from ipykernel.kernelbase import Kernel
from rdflib import Graph
from pyshacl import validate
from traitlets import List
import sys
import traceback
import logging

# Import SPARQL functionality (based on sparql-kernel by Paulo Villegas)
from .sparql.connection import SparqlConnection
from .sparql.magics import split_lines, process_magic, MAGICS, MAGIC_HELP
from .sparql.language import sparql_names, sparql_help
from .sparql.utils import data_msg


def is_magic(token, token_start, buf):
    """
    Detect if the passed token corresponds to a magic command: starts
    with a percent, and it's at the beginning of a line
    """
    return token[0] == '%' and (token_start == 0 or buf[token_start-1] == '\n')


def token_at_cursor(code, pos=0):
    """
    Find the token present at the passed position in the code buffer
     :return (tuple): a pair (token, start_position)
    """
    cl = len(code)
    end = start = pos
    # Go forwards while we get alphanumeric chars
    while end < cl and code[end].isalpha():
        end += 1
    # Go backwards while we get alphanumeric chars
    while start > 0 and code[start-1].isalpha():
        start -= 1
    # If previous character is a %, add it (potential magic)
    if start > 0 and code[start-1] == '%':
        start -= 1
    return code[start:end], start


class SHACLKernel(Kernel):
    """A Jupyter kernel for SHACL (Shapes Constraint Language) with SPARQL support."""
    
    implementation = 'SHACL'
    implementation_version = '2.0'
    language = 'shacl'
    language_version = '2.0'
    language_info = {
        'name': 'shacl',
        'mimetype': 'text/turtle',
        'file_extension': '.ttl',
        'codemirror_mode': 'turtle'
    }
    banner = "SHACL Kernel - Shapes Constraint Language with SPARQL support"

    # Add some items to notebook help menu
    help_links = List([
        {
            'text': "SHACL",
            'url': "https://www.w3.org/TR/shacl/",
        },
        {
            'text': "SPARQL",
            'url': "https://www.w3.org/TR/rdf-sparql-query/",
        },
        {
            'text': "SPARQL 1.1",
            'url': "https://www.w3.org/TR/sparql11-overview/",
        },
    ])

    def __init__(self, **kwargs):
        """Initialize the SHACL kernel with SPARQL support."""
        super().__init__(**kwargs)
        # Initialize graphs for SHACL data and shapes
        self.data_graph = Graph()
        self.shapes_graph = Graph()
        # Track execution count
        self._execution_count = 0
        # Initialize SPARQL connection
        self._sparql = SparqlConnection()
        # Setup logging
        self._klog = logging.getLogger(__name__)

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        """Execute SHACL/SPARQL code."""
        self._execution_count += 1
        
        if not silent:
            # Parse the code and determine what to do
            try:
                # Split lines and remove empty lines & comments
                code_noc = split_lines(code)
                if not code_noc:
                    return self._send_ok(None)

                # Detect if we've got magics
                magic_lines = []
                shacl_magic_lines = []
                sparql_magic_lines = []
                
                for line in code_noc:
                    if line[0] != '%':
                        break
                    # Separate SHACL and SPARQL magics
                    if line.lower().startswith(('%data', '%shapes', '%validate', '%clear', '%show', '%help')):
                        shacl_magic_lines.append(line)
                    else:
                        sparql_magic_lines.append(line)
                    magic_lines.append(line)

                # Process SHACL magics first (they work with content)
                if shacl_magic_lines:
                    # For SHACL magics, we need the content after the magic
                    remaining_code = '\n'.join(code_noc[len(magic_lines):])
                    for line in shacl_magic_lines:
                        result = self._handle_shacl_magic_command(line, remaining_code)
                        if result:
                            self.send_response(self.iopub_socket, 'stream', {
                                'name': 'stdout',
                                'text': result
                            })
                    # If we processed SHACL magics, don't process the rest
                    if shacl_magic_lines and not sparql_magic_lines:
                        return self._send_ok(None)

                # Process SPARQL magics
                if sparql_magic_lines:
                    out = [process_magic(line, self._sparql.cfg) for line in sparql_magic_lines]
                    self._send_multi(out, silent=silent)
                
                # Get remaining code after all magics
                code = '\n'.join(code_noc[len(magic_lines):])

                # If we have content left, process it
                if code:
                    # Check if it looks like a SPARQL query
                    if self._is_sparql_query(code):
                        # Execute as SPARQL query
                        result = self._sparql.query(code, num=self._execution_count)
                        return self._send_raw(result, silent=silent)
                    else:
                        # Process as SHACL/RDF content (only if no SHACL magics were processed)
                        if not shacl_magic_lines:
                            result = self._process_shacl_code(code)
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
                return self._send_error(e)
        
        return {
            'status': 'ok',
            'execution_count': self._execution_count,
            'payload': [],
            'user_expressions': {},
        }

    def _is_sparql_query(self, code):
        """Check if code looks like a SPARQL query."""
        code_upper = code.upper().strip()
        sparql_keywords = ['SELECT', 'CONSTRUCT', 'ASK', 'DESCRIBE', 
                          'INSERT', 'DELETE', 'LOAD', 'CLEAR', 'DROP', 'CREATE']
        return any(code_upper.startswith(kw) for kw in sparql_keywords)

    def _send_ok(self, data):
        """Send a successful response."""
        return {
            'status': 'ok',
            'execution_count': self._execution_count,
            'payload': [],
            'user_expressions': {},
        }

    def _send_multi(self, data, silent=False):
        """Send multiple messages to the frontend."""
        if data is not None and not silent:
            msg = data_msg(data, mtype='multi')
            self.send_response(self.iopub_socket, 'display_data', msg)

    def _send_raw(self, data, silent=False):
        """Send raw data to the frontend."""
        if data is not None and not silent:
            self.send_response(self.iopub_socket, 'display_data', data)
        return {
            'status': 'ok',
            'execution_count': self._execution_count,
            'payload': [],
            'user_expressions': {},
        }

    def _send_error(self, e):
        """Send an error response."""
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

    def _process_shacl_code(self, code):
        """Process SHACL/RDF code (non-SPARQL)."""
        lines = code.strip().split('\n')
        
        # Check for SHACL magic commands
        if lines[0].startswith('%'):
            return self._handle_shacl_magic_command(lines[0], '\n'.join(lines[1:]))
        
        # Default: treat as Turtle data and add to data graph
        before_count = len(self.data_graph)
        self.data_graph.parse(data=code, format='turtle')
        after_count = len(self.data_graph)
        added_count = after_count - before_count
        return f"Added {added_count} triples to data graph. Total: {after_count} triples."

    def _handle_shacl_magic_command(self, magic_line, content):
        """Handle SHACL-specific magic commands."""
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
            return self._get_help_text()
        
        else:
            return f"Unknown magic command: {magic}. Use %help for available commands."

    def _get_help_text(self):
        """Get comprehensive help text for both SHACL and SPARQL features."""
        return """SHACL Kernel - Available Commands

SHACL Magic Commands:
  %data      - Load data graph (Turtle format)
  %shapes    - Load shapes graph (Turtle format)
  %validate  - Validate data against shapes
  %show      - Show current graphs
  %clear     - Clear all graphs
  %help      - Show this help message

SPARQL Magic Commands (from sparql-kernel by Paulo Villegas):
  %endpoint <url>           - Set SPARQL endpoint (REQUIRED for SPARQL queries)
  %auth <method> <user> <pw> - Set HTTP authentication
  %qparam <name> [<value>]   - Add/delete custom query parameter
  %http_header <name> [<val>] - Add/delete HTTP header
  %prefix <name> [<uri>]     - Set/delete URI prefix
  %header <string> | OFF     - Add/delete SPARQL header line
  %graph <uri>               - Set default graph
  %format JSON|N3|XML|...    - Set result format
  %display raw|table|diagram - Set display format
  %lang <lang> | default     - Set preferred language(s)
  %show <n> | all            - Set maximum results shown
  %outfile <file> | off      - Save output to file
  %log <level>               - Set logging level
  %method get|post           - Set HTTP method
  %lsmagics                  - List all magic commands

Usage:
  - Use SHACL magics (%data, %shapes, %validate) for SHACL validation
  - Use SPARQL magics (%endpoint, etc.) and SPARQL queries for querying endpoints
  - Without magic commands, Turtle input is added to the data graph
"""

    def do_complete(self, code, cursor_pos):
        """Provide tab completion for both SHACL and SPARQL."""
        token, start = token_at_cursor(code, cursor_pos)
        tkn_low = token.lower()
        
        if is_magic(token, start, code):
            # Complete magic commands (both SHACL and SPARQL)
            shacl_magics = ['%data', '%shapes', '%validate', '%show', '%clear', '%help']
            all_magics = shacl_magics + list(MAGICS.keys())
            matches = [k for k in all_magics if k.startswith(tkn_low)]
        else:
            # Complete SPARQL keywords
            matches = [sparql_names[k] for k in sparql_names
                      if k.startswith(tkn_low)]
        
        if matches:
            return {
                'matches': matches,
                'cursor_start': start,
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

    def do_inspect(self, code, cursor_pos, detail_level=0):
        """Provide contextual help for SHACL and SPARQL."""
        # Find the token for which help is requested
        token, start = token_at_cursor(code, cursor_pos)
        
        # Find the help for this token
        if not is_magic(token, start, code):
            info = sparql_help.get(token.upper(), None)
        elif token == '%':
            info = self._get_help_text()
        else:
            # Check SPARQL magics
            info = MAGICS.get(token, None)
            if info:
                info = '{} {}\n\n{}'.format(token, *info)
            else:
                # Check SHACL magics
                shacl_help = {
                    '%data': 'Load data graph in Turtle format',
                    '%shapes': 'Load shapes graph in Turtle format',
                    '%validate': 'Validate data against shapes',
                    '%show': 'Show current graphs',
                    '%clear': 'Clear all graphs',
                    '%help': 'Show comprehensive help',
                }
                info = shacl_help.get(token, None)

        return {
            'status': 'ok',
            'data': {'text/plain': info or 'No help available'},
            'metadata': {},
            'found': info is not None
        }


if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=SHACLKernel)
