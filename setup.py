from distutils.core import setup


setup(
    name = 'Uiautomator2Library',
    packages = ['Uiautomator2Library'],
    version = '0.1',
    author='robot',
    author_email = '',
    url = 'no',
    license='MIT',
    platforms='any',
    description = 'Robot Framework Android Test Library Based on Python uiautomator2',
    long_description = 
    """
    This is a test library for `Robot Framework <https://pypi.python.org/pypi/robotframework>`_ to bring keyword-driven testing to Android apps..

    It uses by using `Python uiautomator2 <https://pypi.org/project/uiautomator2>`_ internally.
    """,
    install_requires = [
                        'uiautomator2 >= 2.10'
                        ],
    classifiers  = [
                    'Development Status :: 3 - Alpha',
                    'License :: OSI Approved :: MIT License',
                    'Environment :: Console',
                    'Intended Audience :: Developers',
                    'Operating System :: POSIX :: Linux',
                    'Programming Language :: Python :: 3.7',
                    'Topic :: Software Development :: Testing'
                    ]
)