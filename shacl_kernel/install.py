#!/usr/bin/env python3
"""Install the SHACL kernel spec."""

import json
import os
import sys
import argparse
from jupyter_client.kernelspec import KernelSpecManager
from pathlib import Path


def install_kernel_spec(user=True, prefix=None):
    """Install the SHACL kernel specification."""
    # Create the kernel.json specification
    kernel_json = {
        "argv": [
            sys.executable,
            "-m",
            "shacl_kernel",
            "-f",
            "{connection_file}"
        ],
        "display_name": "SHACL",
        "language": "shacl",
        "interrupt_mode": "signal",
        "metadata": {
            "debugger": False
        }
    }
    
    # Get the directory where this script is located
    here = Path(__file__).parent.absolute()
    
    # Create a temporary directory for kernel spec
    kernel_spec_dir = here / 'kernel_spec'
    kernel_spec_dir.mkdir(exist_ok=True)
    
    # Write kernel.json
    kernel_json_path = kernel_spec_dir / 'kernel.json'
    with open(kernel_json_path, 'w') as f:
        json.dump(kernel_json, f, indent=2)
    
    # Install the kernel spec
    ksm = KernelSpecManager()
    
    print(f"Installing SHACL kernel spec...")
    try:
        ksm.install_kernel_spec(
            str(kernel_spec_dir),
            kernel_name='shacl',
            user=user,
            prefix=prefix
        )
        print(f"SHACL kernel installed successfully!")
        print(f"Kernel installed for {'user' if user else 'system'}")
        
        # Show where it was installed
        kernel_dir = ksm.get_kernel_spec('shacl').resource_dir
        print(f"Kernel spec installed to: {kernel_dir}")
        
    except Exception as e:
        print(f"Error installing kernel spec: {e}", file=sys.stderr)
        return 1
    
    return 0


def main():
    """Main entry point for kernel installation."""
    parser = argparse.ArgumentParser(
        description='Install the SHACL Jupyter kernel spec'
    )
    parser.add_argument(
        '--user',
        action='store_true',
        help='Install for the current user instead of system-wide'
    )
    parser.add_argument(
        '--prefix',
        help='Installation prefix'
    )
    
    args = parser.parse_args()
    
    return install_kernel_spec(user=args.user, prefix=args.prefix)


if __name__ == '__main__':
    sys.exit(main())
