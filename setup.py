from setuptools import find_packages,setup

def get_packages(filename: str)->list[str]:
    '''This function will return a list of str,
      where each str is a python package name'''

    with open(filename,'r') as f:
        packages = f.readlines()
        packages = [pkg.replace("\n","") for pkg in packages if pkg != '-e .']
    
    return packages


setup(
    name='test',
    version='1.0.0',
    author='Avnish Mishra',
    author_email='avnishmishra.ai@gmail.com',
    url='https://github.com/AvnishMishra/test',
    license='MIT',
    description='test',
    packages=find_packages(),
    install_requires=get_packages('requirements.txt'))