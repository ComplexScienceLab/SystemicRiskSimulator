"系统性风险仿真模拟"

## 系统性风险仿真模拟


__version__ = '0.0.10.alpha'

## 导入第三方包（#NOTE 动态导入，严禁删除）
import platform
import os
import glob
from os import path
import warnings
import re
from pathlib import Path, PurePath
import importlib
import pkgutil
from dataclasses import dataclass
import itertools
from enum import Enum
import time
import numpy as np
import pandas as pd
from copy import deepcopy, copy
from dataclasses import dataclass
import logging
from typing import Union, Any, Optional
import igraph as ig
import matplotlib.pyplot as plt
import drawsvg as dw
import fitz
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import matplotlib.font_manager as fm
from matplotlib.font_manager import FontProperties
from functools import reduce
import random
import string

# env = {}
# env["folderpath_project"] = os.getcwd()
