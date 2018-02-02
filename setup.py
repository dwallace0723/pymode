import setuptools
import pymode

if __name__ == "__main__":
    setuptools.setup(
        name="PyMode",
        version="1.0.1a1",
        description="Typed interactions with the Mode Analytics API",
        keywords=["mode analytics", "api"],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Software Development',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3'
        ],
        author="David Wallace",
        author_email="dwallace0723@gmail.com",
        maintainer="David Wallace",
        maintainer_email="dwallace0723@gmail.com",
        url="https://github.com/dwallace0723/pymode",
        license="MIT",
        packages=setuptools.find_packages(),
        install_requires=['requests'],
        python_requires='>=3'
    )
