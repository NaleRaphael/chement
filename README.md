# ChemEnt
A CLI tool for searching UID from ChEBI (chemicals), MeSH (diseases) and Entrez (gene/chemicals).

## Requirements
- requests >= 2.7.0

## Installation
- Install from git by `pip`

    ```bash
    $ pip install git+https://github.com/NaleRaphael/chement.git
    ```

- Clone and install from source

    ```bash
    $ git clone https://github.com/NaleRaphael/chement.git
    $ cd chement
    $ pip install .
    ```

- To uninstall this package:

    ```bash
    $ pip uninstall chement
    ```

## Usage
```bash
$ python -m chement [chebi/mesh/entrez] [term_to_be_searched]

# e.g.
# $ python -m chement chebi asparagine
# $ python -m chement mesh cardiomegaly
# $ python -m chement entrez rab10
```

## Notice
If you need to use the service of MeSH and Entrez **frequently**, you may need to acquire **API keys** from them.

After you got API keys, you can save them as files named `mesh.api.key` and `entrez.api.key`, then put them under the folder `chement`.
