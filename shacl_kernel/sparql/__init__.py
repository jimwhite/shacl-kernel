"""
SPARQL functionality for the SHACL kernel.

This module provides SPARQL endpoint querying, magic commands, and result
formatting capabilities. It is based on and incorporates code from the
SPARQL kernel project (https://github.com/paulovn/sparql-kernel) by Paulo
Villegas, licensed under the 3-clause BSD License.

See the NOTICE file in the root directory for full attribution.
"""

__all__ = ['SparqlConnection']

from .connection import SparqlConnection
