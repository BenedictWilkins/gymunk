"""
    @Author: Benedict Wilkins
    @Date: 2020-04-03 14:58:10
"""


import setuptools

setuptools.setup(name='gymunk',
      version='0.0.2',
      description='',
      url='https://github.com/BenedictWilkinsAI/munk-gym',
      author='Benedict Wilkins',
      author_email='brjw@hotmail.co.uk',
      license='',
      packages=setuptools.find_packages(),
      install_requires=['gym', 'pymunk', 'pygame'],
      classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 2 - Pre-Alpha",
        "Operating System :: OS Independent",
    ])
