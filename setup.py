import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="giggity", 
    version="1.0.0",
    author="Adam Musciano",
    author_email="amusciano@gmail.com",
    description="CLI Git Sleuth Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/needmorecowbell/giggity",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[            
        'requests==2.20.0',
        'nested_lookup==0.2.12'
    ],
    entry_points = {
                    'console_scripts': ['giggity = giggity.giggity:main'],
                        },
    python_requires='>=3.6',
    ),

