from setuptools import setup, find_packages

setup(
    name='EmployEase',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'rich',
        'numpy',
        'openai',
        'tiktoken',
        'setuptools',
        'wheel',
        'PyPDF2', 
        'python-docx',
        'textract'
    ],
    python_requires='>=3',
    entry_points={
        'console_scripts': [
            'employ_ease=src.scripts.Main:main',
        ],
    },
    
    author='Courtney Palmer',
    author_email='courtneylpalmer@nevada.unr.edu',
    description='A Python console application aiding job hunters using OpenAI.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='http://github.com/yourname/yourproject',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: GNU General Public License',
    ],
)
