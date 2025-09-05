"""Dry setup of liquid templating
"""

from liquid import CachingFileSystemLoader
from liquid import Environment


def get_liquid_env(
    template_dir: str, 
    autoescape: bool = False,
    ext: str = '.md'
) -> Environment:
    """Get a liquid templating env with a single function call
    """
    return Environment(
        autoescape=autoescape,
        loader=CachingFileSystemLoader(template_dir, ext=ext)
    )
