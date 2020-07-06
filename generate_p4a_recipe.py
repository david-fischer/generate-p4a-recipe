import os
import re
import subprocess
import sys

import attr
import fire
import pystache
import requests
from simple_term_menu import TerminalMenu

STACHE_TEMPLATE_PATH = f"{sys.path[0]}/recipe_template.stache"
RECIPES = [
    "PythonRecipe",
    "CythonRecipe",
    "TargetPythonRecipe",
    "CompiledComponentsPythonRecipe",
    "CppCompiledComponentsPythonRecipe",
    "BootstrapNDKRecipe",
    "NDKRecipe",
    "Recipe",
]


@attr.s
class RecipeData:
    """Recipe Generator for python-for-android

Obtains the necessary data to fill a recipe template for a package and saves it
under <project_dir>/scr/python-for-android/recipes/<package_name>/__init__.py

For full functionality <package_name> (in the desired version) and pipdeptree
should be installed in the current python environment.

Args:
    package_name: Name of the package for which the recipe should be generated.
    url: Source of the package. If not set, user is prompted with possible options.
    version: If url is not set, user is prompted with possible options.
    recipe_class:
        If not set, user is prompted with possible options.
    project_dir: Directory where the recipe should be saved.
        Defaults to ".".
"""

    package_name_upper = attr.ib(default="", init=False)
    depends_with_version = attr.ib(default="", init=False)
    depends_without_version = attr.ib(default="", init=False)
    package_name = attr.ib()
    url = attr.ib(default="")
    version = attr.ib(default="** SET VERSION STRING **")
    recipe_class = attr.ib(default="")
    project_dir = attr.ib(default=".")

    def __attrs_post_init__(self):
        self.package_name_upper = self.package_name.capitalize()
        self.set_dependencies()
        if not self.recipe_class:
            self.recipe_class = RECIPES[
                TerminalMenu(title="Choose Recipe-Class:", menu_entries=RECIPES).show()
            ]
        if not self.url:
            self.set_url_and_version()
        self.save_recipe()
        print(
            "\nNote: If the compilation fails, you might need additional dependencies for the installation (e.g. "
            "setuptools). If this is the case, add them manually to the recipe. You might also need to set "
            "call_hostpython_via_targetpython=True"
        )

    def set_dependencies(self):
        pipdeptree_out = subprocess.run(
            f"pipdeptree -f -p {self.package_name}".split(" "),
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        ).stdout.decode("utf-8")
        dependencies = re.findall("^[\W]+([^\s]+)",pipdeptree_out,flags=re.MULTILINE)
        self.depends_with_version = list(set(dependencies))[1:]
        self.depends_without_version = [re.search(r"(^[\w\-\_]+)", dep)[0] for dep in self.depends_with_version]
        print(self.depends_with_version)
        print(self.depends_without_version)

    def get_pypi_url_and_version(self):
        json_response = requests.get(f"https://pypi.org/pypi/{self.package_name}/json").json()
        current_version = json_response["info"]["version"]
        summary = json_response["info"]["summary"]
        versions = list(json_response["releases"].keys())
        terminal_menu = TerminalMenu(
            [current_version + " (current stable)"] + versions[::-1],
            title=f"{self.package_name}:\n{summary}\n\nSelect version:",
        )
        choice_index = terminal_menu.show()
        version = current_version if choice_index == 0 else versions[-choice_index]
        url = json_response["releases"][version][-1]["url"]
        return url, version

    def get_github_url_and_version(self):
        json_response = requests.get(
            f"https://api.github.com/search/repositories?q={self.package_name}"
        ).json()
        menu_entries = [f'{json_response["items"][i]["full_name"]}|{i}' for i in range(10)]
        preview_function = lambda i: json_response["items"][int(i)]["description"]
        terminal_menu = TerminalMenu(
            title="Github:", menu_entries=menu_entries, preview_command=preview_function
        )
        repo_api_url = json_response["items"][terminal_menu.show()]["url"] + "/tags"
        json_response = requests.get(repo_api_url).json()
        versions = ["master"] + [item["name"] for item in json_response]
        terminal_menu = TerminalMenu(title="Version:", menu_entries=versions)
        version = versions[terminal_menu.show()]
        url = json_response[0]["tarball_url"].rsplit("/", 1)[0] + "/{version}"
        return url, version

    def set_url_and_version(self):
        if TerminalMenu(
            title="Select source for package:", menu_entries=["PyPI", "github"]
        ).show():
            self.url, self.version = self.get_github_url_and_version()
        else:
            self.url, self.version = self.get_pypi_url_and_version()

    def recipe_str(self):
        with open(STACHE_TEMPLATE_PATH, "r") as template_file:
            recipe_string = template_file.read()
            recipe_string = pystache.render(recipe_string, vars(self))
            return recipe_string

    def save_recipe(self):
        dirs = [
            self.project_dir,
            "src",
            "python-for-android",
            "recipes",
            self.package_name,
            "__init__.py",
        ]
        dir_tree = ["/".join(dirs[: i + 1]) for i in range(1, len(dirs))]
        for directory in dir_tree[:-1]:
            if not os.path.exists(directory):
                os.makedirs(directory)
        out_path = dir_tree[-1]
        if not os.path.exists(out_path):
            with open(out_path, "w") as out_file:
                out_file.write(self.recipe_str())
        else:
            print(f"Recipe at {out_path} already exists. Delete manually and restart.")
        exit()


if __name__ == "__main__":
    fire.Fire(RecipeData)
