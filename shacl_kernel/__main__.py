"""Entry point for the SHACL kernel."""

from .kernel import SHACLKernel

if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=SHACLKernel)
