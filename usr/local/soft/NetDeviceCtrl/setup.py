from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='NetDeviceCtrl',
      version='1.0',
      description='Drivers and interfaces for using lab equipment over a network',
	    long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/CosmiQuantum/NetDeviceCtrl',
      author='Dylan Temples',
      author_email='dtemples@fnal.gov',
      license='MIT',
      packages=setuptools.find_packages(),
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      python_requires='>=3.6',
      # install_requires=[
      #   'socket',
      #   'urllib',
      #   'time',
      #   'tkinter',
      # ],
      zip_safe=False)
