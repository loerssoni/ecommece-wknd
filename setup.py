from setuptools import setup
setup(
    name='ecommerce',
    version='0.1.0',    
    author='loerssoni',
    license='BSD 2-clause',
    packages=['shared'],
    install_requires=['boto3',
                      'pandas',
                      'scikit-learn'
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  

    ],
)
