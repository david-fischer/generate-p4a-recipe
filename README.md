<h1 align="center">Recipe Generator for python-for-android</h1>

Python-CLI to easily create recipes for python-for-android. I use it for building a [kivy](https://kivy.org/#home)-app with [buildozer](https://buildozer.readthedocs.io/en/latest/).

This is useful if the installation with pip fails or you don't want to add all requirements manually to your *buildozer.spec* file, only to note on building that the dependencies itself have unmet dependencies.

* Searches PyPI or Github for source-url by api-request
* Prompts the user with a choice for possible versions
* Fetches the dependencies of a package recursively by use of pipdeptree on the **locally installed version** of the package

The generated recipe **should be seen as a template**, even though in **simple cases it can work out of the box**. See [Troubleshooting](#-troubleshooting)

## 🚧 Setup

### Installation

```
pip install git+https://github.com/david-fischer/generate-p4a-recipe.git
```

### Local recipes with buildozer

We need to add the path of our recipes in the apropriate place in the *buildozer.spec* of the project:

```
p4a.local_recipes = ./src/python-for-android/recipes/
```

## 🔧 Usage

Usage example:

```
python -m generate_p4a_recipe --package-name="some_package" --project-dir="/path/to/kivy-project/"
```

Help text:

```
python /path/to/script/generate_p4a_recipe.py -h

NAME
    generate_p4a_recipe.py - Recipe Generator for python-for-android

SYNOPSIS
    generate_p4a_recipe.py --package_name=PACKAGE_NAME <flags>

DESCRIPTION
    Obtains the necessary data to fill a recipe template for a package and saves it
    under <project_dir>/scr/python-for-android/recipes/<package_name>/__init__.py

    For full functionality <package_name> (in the desired version) and pipdeptree
    should be installed in the current python environment.

    For further info see https://github.com/david-fischer/generate-p4a-recipe#-troubleshooting .

ARGUMENTS
    PACKAGE_NAME
        Name of the package for which the recipe should be generated.

FLAGS
    --url=URL
        Source of the package. If not set, user is prompted with possible options.
    --version=VERSION
        If url is not set, user is prompted with possible options.
    --recipe_class=RECIPE_CLASS
        If not set, user is prompted with possible options.
    --project_dir=PROJECT_DIR
        Directory where the recipe should be saved. Defaults to ".".
```

## 🎯 Troubleshooting

* start script in correct python-environment

* make sure to have correct version of package installed (dependencies might change)

* have a look at https://python-for-android.readthedocs.io/en/latest/recipes/

* or https://github.com/kivy/python-for-android/tree/master/pythonforandroid/recipes

* when building with buildozer, you might need to clean the build for changes to take effect

* you might need additional dependencies like setuptools at build-time, which are not listed in the requirements

  -> check if necessary, add manually, try with call_hostpython_via_targetpython = False

## 📦 Dependencies

* [pystache](https://github.com/defunkt/pystache) - filling the template
* [fire](https://github.com/google/python-fire) - CLI
* [simple-term-menu](https://github.com/IngoHeimbach/simple-term-menu) - selection of options in terminal
* [attrs](https://www.attrs.org/en/stable/) - defining classes easily
* [requests](https://requests.readthedocs.io/en/master/) - making requests to the github- or pypi-api
* [pipdeptree](https://github.com/naiquevin/pipdeptree) - displays dependency tree of package
