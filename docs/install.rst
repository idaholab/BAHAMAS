============
Installation
============

How to Install
--------------

Installation
++++++++++++

Using conda:

.. code:: bash

  conda create -n bahamas_libs python=3.13
  conda activate bahamas_libs
  pip install toml streamlit streamlit-aggrid==1.1.5 numpy>=1.24 pandas==2.3 scipy openpyxl xlsxwriter pytest plotly kaleido matplotlib streamlit-option-menu jsonpointer streamlit_extras

Using `uv <https://docs.astral.sh/uv/>`_:

.. code:: bash

  uv sync --python 3.13
  source .venv/bin/activate

Clone
+++++

.. code:: bash

  git clone git@github.inl.gov:congjian-wang/BAHAMAS.git


Test
++++

.. code:: bash

  cd BAHAMAS/tests
  pytest


How to Run BAHAMAS
------------------

.. code:: bash

  cd /path/to/BAHAMAS/examples
  # run BAHAMAS to evaluate software failure probability based Bayesian Belief Network
  python ../bahamas/main.py -i bbn.toml
  # run BAHAMAS to generate common cause component groups based on coupling factors
  python ../bahamas/main.py -i ccf.toml


How to Run BAHAMAS Web App
--------------------------

.. code:: bash

  cd app
  streamlit run app.py

How to Build the User Manual
----------------------------

* Install Sphinx libraries.

  .. code:: bash

    pip install sphinx sphinx-rtd-theme nbsphinx sphinx-copybutton sphinxcontrib-bibtex sphinx-autoapi
    conda install pandoc
    cd docs
    make html
    cd _build/html
    python3 -m http.server

* Build the HTML and open your browser (http://localhost:8000).

  .. code:: bash

    cd docs
    make html
    cd _build/html
    python3 -m http.server

* Build Latex.

  .. code:: bash

    cd docs
    make latex
    cd _build/latex
    make
    open bahamas.pdf
