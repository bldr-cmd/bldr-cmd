from setuptools import setup, find_packages

setup(name='bldr',
      version='0.15',
      description='bldr',
      url='http://github.com/bldr-cmd/bldr-cmd',
      author='Michael Schmidt',
      author_email='michael@dedesignworks.com',
      license='Apache 2.0',

      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          'click',
          'sh',
          'diff-match-patch',
          'jinja2',
          'toml',
          'GitPython',
          'git-url-parse',
      ],
      entry_points = {
        'console_scripts': ['bldr=bldr.cli:cli'],
      },
)