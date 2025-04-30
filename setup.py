from setuptools import setup, find_packages

setup(
    name="projectfm",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "azure-cognitiveservices-speech==1.32.0",
        "pyautogui==0.9.54",
        "pytesseract==0.3.10",
        "keyboard==0.13.5",
        "Pillow==10.0.0",
        "opencv-python==4.8.0.76",
        "numpy==1.24.3",
        "python-dotenv==1.0.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A voice-controlled assistant for Football Manager",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/projectfm",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
) 