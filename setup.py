import setuptools

# Long description
with open('README.md', 'r') as fh:
    long_description = fh.read()


# Requirements
def get_requirements():
    with open('requirements.txt', 'r') as f:
        requirements = f.read().splitlines()
        return requirements


setuptools.setup(
    name="tweet-capture",
    version="0.2.4",
    author="Alperen Çetin",
    author_email="xacnio@pm.me",
    description="Take a tweet screenshot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Xacnio/tweetcapture",
    packages=setuptools.find_packages(),
    install_requires=get_requirements(),
    data_files=[("", ["requirements.txt"])],
    entry_points={
        "console_scripts": ["tweetcapture=tweetcapture.cli:main"]},
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license='MIT',
    keywords="tweet screenshot",
    python_requires=">=3.6"
)
