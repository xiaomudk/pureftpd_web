import uliweb
from uliweb.utils.setup import setup
import apps

__doc__ = """doc"""

setup(name='pureftp_web',
    version=apps.__version__,
    description="Description of your project",
    package_dir = {'pureftp_web':'apps'},
    packages = ['pureftp_web'],
    include_package_data=True,
    zip_safe=False,
)
