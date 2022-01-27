from collections.abc import Iterable
from pathlib import Path

import jinja2
import tomlkit

from .npmtools import NodePackageManager, run_npm


class NodeProject:
	"""Handle parsing ``pyproject.toml`` and outputting a ``package.json`` at the specified path, whether as a temporary file, or in-memory file, or as a filesystem file that is not destroyed after the process ends"""
	"""NodeProject arguments are either specified in ``pyproject.toml`` under ``[npmunifier]``, else the default class values are used"""
	def __init__(self, node_project_dir: Path = "./", package_manager: NodePackageManager = None):
		pass
	def parse_packagejson_from_toml(self):
		pass
	def run_npm(self, *args):
		run_npm(*args)