from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='excel_processor',
    version='0.1.0',
    author='João Alonso',
    author_email='joao.alonso@a3sil.com.br',
    description='Gera um data base da C&A a partir de uma pasta de trabalho "Quadro Seguros Diário"',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/seu_usuario/excel_processor',  # URL do seu repositório
    packages=find_packages(), 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy>=2.2.3',
        'openpyxl>=3.1.5',
        'pandas>=2.2.3',
        'dearpygui>=1.9.0',        
    ],
    entry_points={
        'console_scripts': [            
            'run=src.backend.main:main',
            'run_app=src.frontend.app:main'
            
        ],
    },
)