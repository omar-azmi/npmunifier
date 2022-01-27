import json
import subprocess
from collections.abc import Iterable
from functools import partial
from pathlib import Path


def run_npm(pkgdir: Path = "./", cmd: str = None, args: list[str] = None, npm_bin = "npm", wait = True):
	"""Run npm (npm_bin) command (cmd) with arguments (args) from directory (pkgdir)

	:param pkgdir: directory where npm should get invoked, defaults to "./"
	:type pkgdir: Path, optional
	:param cmd: an npm command, such as `init` or `install` etc..., defaults to None
	:type cmd: str, optional
	:param args: list of arguments to pass to the command, defaults to None
	:type args: list[str], optional
	:param npm_bin: name of the npm binary that's accessible via shell, defaults to "npm"
	:type npm_bin: str, optional
	:param wait: wait for npm command to finish. defaults to True
	:type wait: bool, optional
	"""
	pkgdir = Path(pkgdir)
	args = args if isinstance(args, Iterable) else [] if args is None else [args]
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
	"""Create a basic interface to a Node Package Manager CLI

	:param packagejson_path: path to `package.json`
	:type packagejson_path: Path | json string
	:param bin: npm's binary alias. example: npm.exe, or yarn.exe, or pnpm, etc...
	:type bin: str
	:param commands: construct a set of class methods that invoke npm commands, defaults to None
	:type commands: list[str], optional
	"""
	def __init__(self, packagejson_path: Path | json, bin: str, commands: list[str] = None):
		self._commands = commands or [
			#default set of npm commands. these will get transformed into class methods
			#commands with a dash `-` will get converted into methods with an underscore `_`
			"build",
			"init",
			"install",
			"uninstall",
			"update",
			"link",
			"unlink",
			"run-script",
			"start",
			"stop",
			"test",
		]
		self._packagejson_path = Path(packagejson_path)
		self._packagejson_contents = None
		self._npm_bin = bin

	@property
	def packagejson_path(self) -> str:
		"""Get ``package.json`` file path."""
		if Path(self._packagejson_path).parts[-1] != "package.json":
			assert(self._packagejson_path.is_dir())
			return Path(self._packagejson_path, "package.json")
		else:
			return self._packagejson_path
	
	@property
	def packagejson(self) -> json:
		"""Read ``package.json`` contents."""
		if self._packagejson_contents is None:
			with open(self.packagejson_path, "r") as f:
				self._packagejson_contents = json.load(f)
		return self._packagejson_contents

	def _run_npm(self, command, *args, **kwargs):
		"""Run an npm command at `package.json`'s directory
		by default, the call is blocking until npm is finished and output is directed to stdout.
		if `wait=False` is passed to the method, you get a handle to the process (return value of `subprocess.Popen`).
		:param command: npm command to run.
		:param args: list of arguments.
		:param wait: wait for NPM command to finish. defaults to True
		"""
		return run_npm(
			self.packagejson_path.parent,
			command,
			npm_bin=self._npm_bin,
			args=args,
			**kwargs
		)

	def __getattr__(self, name):
		"""Run partial function for an npm command."""
		name = name.replace('_', '-')
		if name in self._commands:
			return partial(self._run_npm, name)
		raise AttributeError("Unregistered NPM command.")


####a bunch of derived classes####

class NPMPackage(NodePackageManager):
	def __init__(self, packagejson_path: Path, bin: str = "npm", commands: list[str] = None):
		super().__init__(packagejson_path, bin = bin, commands = commands)


class PNPMPackage(NodePackageManager):
	def __init__(self, packagejson_path: Path, bin: str = "pnpm", commands: list[str] = None):
		commands = commands or ["build", "init", "add", "remove", "install", "uninstall", "prune", "update", "link", "unlink", "run-script", "start", "stop", "test"]
		super().__init__(packagejson_path, bin = bin, commands = commands)


class YARNPackage(NodePackageManager):
	def __init__(self, packagejson_path: Path, bin: str = "yarn", commands: list[str] = None):
		commands = commands or ["build", "init", "add", "remove", "upgrade", "link", "unlink", "run-script", "start", "stop", "test"]
		super().__init__(packagejson_path, bin = bin, commands = commands)
	
	def install(self, *args, **kwargs):
		self._run_npm("", args=args, **kwargs)
