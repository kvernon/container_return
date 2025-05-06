from setuptools import setup, find_packages

setup(
    name="jojanga_queries",
    version="1.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "reset-db=jojanga_queries.scripts.reset_db:initialize_challenge_db",
        ],
    },
)
