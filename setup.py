import setuptools

setuptools.setup(
    name='website-sitemap-parser',
    version='0.0.5',
    author="Bart Machielsen",
    author_email="bartmachielsen@gmail.com",
    description="Website Sitemap Parser",
    install_requires=[
        'requests'
    ],
    # long_description='',
    # long_description_content_type="text/markdown",
    url="https://github.com/bartmachielsen/website-sitemap-parser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)
