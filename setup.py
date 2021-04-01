from setuptools import setup, find_packages

setup(name='bldr',
      version='0.4',
      description='bldr framework',
      url='http://github.com/bldr/bldr_cmd',
      author='Michael Schmidt',
      author_email='michael@dedesignworks.com',
      license='MIT',

      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          'click',
          'sh',
          'diff-match-patch',
          'jinja2',
          'toml',
          'GitPython',
      ],
      entry_points = {
        'console_scripts': ['bldr=bldr.cli:cli'],
      },
)