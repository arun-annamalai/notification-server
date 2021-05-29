import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="notification_server",
    version="0.0.1",
    author="Arun Annamalai",
    author_email="arunannamala2@gmail.com",
    description="A package to run scripts and notify you of happenings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arun-annamalai/notification_server",
    project_urls={
        "Bug Tracker": "https://github.com/arun-annamalai/notification_server/issues",
    },
    install_requires=[
        'schedule',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
)