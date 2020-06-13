"""
  /^^   /^^
  /^^   /^^
/^/^ /^ /^^  /^^ /^ /^^  /^^   /^^
  /^^   /^^ /^^  /^  /^^  /^^ /^^
  /^^   /^/^^    /^   /^^   /^^^
  /^^   /^^ /^^  /^^ /^^     /^^
   /^^  /^^  /^^ /^^        /^^
                 /^^      /^^

Travian: Kingdom utilities for your need.
"""

__name__ = 'tkpy'
__version__ = '0.0.1.a1'
__author__ = 'didadadida93'
__author_email__ = 'didadadida93@gmail.com'
__description__ = 'Travian: Kingdom utilities for your need.'
__license__ = 'MIT'


from .map import Map
from .hero import Hero
from .farmlist import Farmlist
from .notepads import Notepad
from .villages import Villages
from .utilities import _login as login
