from setuptools import setup

import replace_me
try:
    import pypandoc
    long_description = pypandoc.convert_text(replace_me.__doc__, format='md', to='rst')
except ImportError:
    long_description = replace_me.__doc__

setup(
    name='replace_me',
    version='0.1.4',
    py_modules=['replace_me'],
    install_requires=[
    ],
    author='BoppreH',
    author_email='boppreh@gmail.com',
    url='https://github.com/boppreh/replace_me',
    license='MIT',
    description='Modify your own source code with this piece of Python black magic',
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)