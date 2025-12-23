=========================================
BAHAMAS Input Configuration (TOML Syntax)
=========================================

**Purpose:**
This configuration file defines the parameters, input file paths, and analysis options for the BAHAMAS input system.
The TOML syntax follows the JSON schema validation described in the *BAHAMAS/bahamas/validation.py*.

---------------------------
Software Failure Evaluation
---------------------------

The configuration file contains one top-level table:

.. code-block:: toml

  [BBN]

This table includes three nested subtables:

- ``[BBN.params]`` — Defines sampling and reproducibility parameters.
- ``[BBN.files]`` — Specifies paths to required data files.
- ``[BBN.analysis]`` — Selects the type of analysis to perform.

BBN.params
++++++++++

**Description:**
Defines the analysis sampling configuration.

**Syntax Example:**

.. code-block:: toml

  [BBN.params]
  samples = 40000
  seed = 2

**Parameters:**

- **samples** *(integer, required)*
  The number of samples used in the analysis.
  Must be an integer greater than or equal to 1.
  Example: ``samples = 40000``.

- **seed** *(integer, optional)*
  The random number seed to ensure reproducibility.
  Must be a positive integer.
  Example: ``seed = 2``.


BBN.files
+++++++++

**Description:**
Specifies input file paths required for the analysis.

**Syntax Example:**

.. code-block:: toml

  [BBN.files]
  task = "../data/Task_List.xlsx"
  defect = "../data/Defect_Data.xlsx"
  approx = "../data/sdlc_macro.xlsx"

**File Entries:**

- **task** *(string, conditionally required)*
  Path to the task list file.
  Required **only** when ``[BBN.analysis].type = "precise"``.

- **defect** *(string, required)*
  Path to the defect data file.

- **approx** *(string, conditionally required)*
  Path to the SDLC macro data file.
  Required **only** when ``[BBN.analysis].type = "approx"``.

**Notes:**
All paths should be valid relative or absolute file paths, and may use URI-style notation.


BBN.analysis
++++++++++++

**Description:**
Defines the type of analysis to be performed.

**Syntax Example:**

.. code-block:: toml

  [BBN.analysis]
  type = 'precise'

**Parameters:**

- **type** *(string, required)*
  Defines the analysis mode.
  Acceptable values:

  - ``'precise'`` → Task-level assessment.
  - ``'approx'`` → Stage-level assessment.

**Conditional Logic:**

- If ``type = 'precise'`` → ``[BBN.files].task`` **must** be provided.
- If ``type = 'approx'`` → ``[BBN.files].approx`` **must** be provided.


Example Full Configuration
++++++++++++++++++++++++++

**Complete Example:**

.. code-block:: toml

  [BBN]

  [BBN.params]
  samples = 40000
  seed = 2

  [BBN.files]
  task = "../data/Task_List.xlsx"
  defect = "../data/Defect_Data.xlsx"
  approx = "../data/sdlc_macro.xlsx"

  [BBN.analysis]
  type = 'precise'


Validation Summary
++++++++++++++++++

- ``samples`` and ``defect`` are always required.
- ``seed`` is optional.
- ``task`` or ``approx`` is required, depending on the analysis ``type``.
- No additional keys beyond those listed are allowed in the ``BBN`` table.


------------------------------------------------------
Common Cause Failure Input Configuration (TOML Syntax)
------------------------------------------------------

**Purpose:**
This defines the file inputs and (optionally) which common cause component groups (CCCGs) to generate and how to name the outputs.


Overall Structure
+++++++++++++++++

The configuration has one top-level table:

.. code-block:: toml

  [CCF]

This table may contain two subtables:

- ``[CCF.files]`` — **Required.** Declares the input structure file.
- ``[CCF.generate]`` — Optional. Selects which CCCGs to generate, and sets output naming/options.


CCF.files
+++++++++

**Description:**
CCF file configurations.

**Syntax Example:**

.. code-block:: toml

  [CCF.files]
  structure = "../data/Scenario_6.csv"

**Entries:**

- **structure** *(string, required)*
  Path to the structure file.
  Example: ``structure = "../data/Scenario_6.csv"``.

.. warning::
  ``structure`` must be provided in order for the configuration to be valid.


CCF.generate
++++++++++++

**Description:**
Optional settings to generate CCCGs and control output naming and type.

**Syntax Example:**

.. code-block:: toml

  [CCF.generate]
  output_file_base = "s6_cccg"
  output_type = "csv"
  final = true
  single = true
  double = true
  triple = true

**Parameters:**

- **output_file_base** *(string, optional)*
  Base name used for generated output files.
  Example: ``"s6_cccg"``.

- **output_type** *(string, optional; enum)*
  Type/format of the output file.
  Allowed values: ``"csv"``.
  Example: ``output_type = "csv"``.

- **final** *(boolean, optional)*
  Generate the final CCCGs output if ``true``.

- **single** *(boolean, optional)*
  Generate single CCCGs output if ``true``.

- **double** *(boolean, optional)*
  Generate double CCCGs output if ``true``.

- **triple** *(boolean, optional)*
  Generate triple CCCGs output if ``true``.

.. note::
  All ``[CCF.generate]`` keys are optional; include only the ones relevant to your run.


Example Full Configuration
++++++++++++++++++++++++++

**Complete Example:**

.. code-block:: toml

  [CCF]

  [CCF.files]
  structure = "../data/Scenario_6.csv"

  [CCF.generate]
  output_file_base = "s6_cccg"
  output_type = "csv"
  final = true
  single = true
  double = true
  triple = true


Validation Summary
++++++++++++++++++

- **Required**
  - ``CCF.files.structure`` *(string)*.
- **Optional**
  - All keys under ``[CCF.generate]`` (strings/booleans as defined above)
- **Types & Constraints**
  - ``output_type`` must be one of: ``"csv"``.

