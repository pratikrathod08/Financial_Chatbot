from setuptools import setup, find_packages

setup(
    name="financial_chatbot",
    version="0.1",
    packages=find_packages(),
    # package_dir={"": "app"},
    install_requires=[ ],
    entry_points={
        "console_scripts": [
            "runapp = main:run"
        ]
    },
)
