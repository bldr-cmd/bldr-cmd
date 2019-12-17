from setuptools import setup

setup(name='bldr',
      version='0.1',
      description='bldr framework',
      url='http://github.com/bldr/bldr_cmd',
      author='Michael Schmidt',
      author_email='michael@dedesignworks.com',
      license='MIT',
      packages=['bldr'],
      entry_points = {
        'console_scripts': ['bldr=bldr_cmd.command_line:main'],
      },
      zip_safe=False)