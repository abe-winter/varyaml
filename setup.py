import setuptools

setuptools.setup(
    name='varyaml',
    version='0.0.3',
    description='yaml parser with environment interpolation -- safe secrets in configs',
    url='https://github.com/abe-winter/varyaml',
    author='Abe Winter',
    author_email='awinter.public@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='yaml environment config configuration',
    py_modules=['varyaml'],
    install_requires=['pyyaml>=3'],
    extras_require={'test': ['pytest']},
)
