from setuptools import setup

setup(
    name='splatprint',
    version='0.1.0',    
    description='A macro generator for NXBT to print Splatoon 3 posts via Bluetooth.',
    # url='',
    author='Wryvrrrn',
    license='MIT',
    packages=['splatprint'],
    install_requires=['numpy',
                      'Pillow'
    ],
)