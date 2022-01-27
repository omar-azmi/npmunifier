This package allows you to interface with node package managers (npm, yarn, pnpm, etc...) from within your python scripts
You can also configure `package.json` from within your `pyproject.toml`, making your codebase more compact
Moreover, you can use jinja templating on your `pyproject.toml` to share variables between the python portion of `pyproject.toml` and `packagejson` portion
See `package.toml` for an example of what a `package.json` would look like in a toml file

### Usage example
```python
from npmunifier import NodeProject
NodeProject() # => read pyproject.toml and interpret the initialization location and build `package.json` from the `packagejson` portion of the toml
NodeProject(
	pkgdir: Path = "./path/to/initialize/npm/",
	packagejson: json | Path | None = None
	#	json string => use this json string as the contents of package.json
	#	Path => load the provided file path as a json and use it as packagejson
	#	None => load Path(pkgdir, "package.json") file as packagejson
	packagejson_location: "mem" | "temp" | "file"
	#where to save the packagejson to?
	#	"mem" => save inside of memory (RAM)
	#	"temp" => save as a temp file that will destruct once the python process has terminated
	#	"file" => save as file that will remain in your hard disk even after this python process has terminated
)
TomlNodeProject(toml_path: Path = "./pyproject.toml")
nodeproject_from_toml(toml_path, packagejson_key = "packagejson")
init_nodeproject = nodeproject_from_toml("./pyproject.toml", "packagejson")
```

### FAQ
- will this support automatic creation and handling of multiple (in-memory) `package.json` files from within one `pyproject.toml`?
  ie: can I have:
```
# pyproject.toml

[python.stuff]
# ...

[package1.json]
# configure package1.json

[package2.json]
# configure package2.json
```
- - probably never. however, you can parse the toml and convert to json manually. though it won't be available in-memory

### Features to consider
- option to whether have `packagejson` created in-memory, or as temporary file that gets destroyed when the process ends, or as a permanent disk file that get overwritten each time
- option to whether wait for npm or not
- option to configure alternate node package managers (yarn, pnpm, etc...)
- think of a better name
- turn this into a poetry plugin?
- have its own section in `pyproject.toml` under `npmunifier` that will set things up when `NPMUnifier.init_project(path_to_pyproject)` is called
- ability to parse and append `package.json` to `pypackage.toml`
- think of a way to make the `pyproject.toml` a valid toml file with jinja's `{% ... %}` macro templating symbols, without just wrapping the templating block inside of a string.
- fyi: jinja's `{{ ... }}` variable templating symbols will need to be wrapped over double-qoutes, if you with for the variable to get interpreted as a string in the toml file. ie:
```
#script.py
var_first_name = "Person"
jinja_export(var_first_name)

#pyproject.toml
[project]
author.first_name = "{{ var_first_name }}" # -> author.first_name = "Person"
```