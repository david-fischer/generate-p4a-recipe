from setuptools import setup

setup(
    name="generate-p4a-recipe",
    version="0.1",
    packages=["."],
    url="github.com/david-fischer/generate-p4a-recipe",
    license="MIT",
    author="david-fischer",
    author_email="david.fischer.git@posteo.de",
    description="Generates recipe for python-for-android.",
    install_requires=[
        "attrs",
        "fire",
        "pystache",
        "requests",
        "pipdeptree",
        "simple_term_menu",
    ],
    package_data={"": ["README.md", "recipe_template.stache", "LICENSE"]},
    include_package_data=True,
)
