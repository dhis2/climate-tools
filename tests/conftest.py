import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--notebook-kernel",
        action="store",
        default=None,
        help="Jupyter kernel name to use for notebook tests"
    )

@pytest.fixture(scope="session")
def notebook_kernel(request):
    """
    Fixture to provide the kernel name to tests.
    Can be overridden with --notebook-kernel CLI option.
    """
    kernel = request.config.getoption("--notebook-kernel")
    return kernel
