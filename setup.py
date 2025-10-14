from setuptools import setup, find_packages

setup(
    name="dl_assistant",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "watchdog>=3.0.0",
        "flask>=3.0.0",
        "PyYAML>=6.0.1",
        "Pillow>=10.1.0",
        "mutagen>=1.47.0",
        "PyPDF2>=3.0.1",
        "python-magic>=0.4.27",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "dl-assistant=dl_assistant.main:main",
        ],
    },
)
