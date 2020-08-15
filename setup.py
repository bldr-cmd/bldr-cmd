from setuptools import setup, find_packages

setup(name='bldr',
      version='0.1',
      description='bldr framework',
      url='http://github.com/bldr/bldr_cmd',
      author='Michael Schmidt',
      author_email='michael@dedesignworks.com',
      license='MIT',

      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          'Click',
      ],
      entry_points = {
        'console_scripts': ['bldr=bldr.command_line:main'],
      },
)