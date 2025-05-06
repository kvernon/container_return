from setuptools import setup, find_packages

setup(
    name='api',
    version='1.0',
    description='the API',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["flask"],
    python_requires="~=3.12",
    extras_require={"test": ["pytest", "coverage"]},
)
