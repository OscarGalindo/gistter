#!/usr/bin/env python

import os
import readline
from pprint import pprint

from flask import *
from gistter import *
from gistter.models import *

os.environ['PYTHONINSPECT'] = 'True'