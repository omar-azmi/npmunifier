from __future__ import annotations
import json
from pathlib import Path
import jinja2
import tomlkit
import os
import subprocess
import sys


def run_npm(pkgdir, cmd, args=None, npm_bin="npm", wait=True):
	"""Run NPM."""
	command = [npm_bin, cmd] + list(args)
	if wait:
		return subprocess.call(command, cwd=pkgdir)
	else:
		return subprocess.Popen(
			command,
			stdout=subprocess.PIPE,
			stderr=subprocess.STDOUT,
			cwd=pkgdir,
		)

class NodePackageManager:
	def __init__(self, package_json_path: Path | str , bin: str, commands = None):
		self._commands = commands or [
			#default set of npm commands. these will get transformed into class methods
			#commands with a dash `-` will get converted into methods with an underscore `_`
			"build",
			"init",
			"install",
			"link",
			"run-script",
			"start",
			"stop",
			"test",
		]
		self._package_json_path = Path(package_json_path)
		self._package_json_contents = None
		self._npm_bin = bin

	@property
	def package_json_path(self) -> str:
		"""Get ``package.json`` file path."""
		if Path(self._package_json_path).parts[-1] != "package.json":
			assert(self._package_json_path.is_dir())
			return Path(self._package_json_path, "package.json")
		else:
			return self._package_json_path
	
	@property
	def package_json(self) -> json:
		"""Read ``package.json`` contents."""
		if self._package_json_contents is None:
			with open(self.package_json_path, "r") as f:
				self._package_json_contents = json.load(f)
		return self._package_json_contents

	def _run_npm(self, command, *args, **kwargs):
		"""Run an NPM command.
		By default the call is blocking until NPM is finished and output is directed to stdout.
		If ``wait=False`` is passed to the method, you get a handle to the process (return value of ``subprocess.Popen``).
		:param command: NPM command to run.
		:param args: List of arguments.
		:param wait: Wait for NPM command to finish. By default
		"""
		return run_npm(
			dirname(self.package_json_path),
			command,
			npm_bin=self._npm_bin,
			args=args,
			**kwargs
		)

	def __getattr__(self, name):
		"""Run partial function for an NPM command."""
		name = name.replace('_', '-')
		if name in self._commands:
			return partial(self._run_npm, name)
		raise AttributeError('Invalid NPM command.')


class NodeProject:
	"""Handle parsing ``pyproject.toml`` and outputting a ``package.json`` at the specified path, whether as a temporary file, or in-memory file, or as a filesystem file that is not destroyed after the process ends"""
	"""NodeProject arguments are either specified in ``pyproject.toml`` under ``[npmunifier]``, else the default class values are used"""
	pass