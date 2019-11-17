from setuptools import setup, find_packages


MAJOR = 1
MINOR = 0
MICRO = 0
VERSION = '{}.{}.{}'.format(MAJOR, MINOR, MICRO)


def get_requirements():
    with open('./requirements.txt', 'r') as f:
        reqs = f.readlines()
    return reqs


def setup_package():
    excluded = []
    package_data = {'': ['*.config']}

    metadata = dict(
        name='chement',
        version=VERSION,
        description='A CLI tool for searching UID from ChEBI (chemicals), MeSH (diseases) and Entrez (gene/chemicals).',
        url='https://github.com/NaleRaphael/chement',
        packages=find_packages(exclude=excluded),
        package_data=package_data,
        include_package_data=True,
        install_requires=get_requirements(),
    )

    setup(**metadata)


if __name__ == '__main__':
    setup_package()        
