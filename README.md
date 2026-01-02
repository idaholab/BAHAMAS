# BAHAMAS
Bayesian and Human Reliability Analysis-Aided Method for the Reliability Analysis of Software (BAHAMAS)

![BAHAMAS architecture](docs/pics/bahamas_structure.png)

BAHAMAS evaluates software failures by tracking **defect introduction** and **defect removal** activities, their impact on the types of defects that may remain within software, and ultimately the **probability of software failure**.

The BAHAMAS Bayesian Belief Network (BBN) consists of the following nodes:

- **Red nodes**: Account for the introduction of defects by considering human errors at each stage of the Software Development Life Cycle (SDLC).
- **Blue nodes**: Account for the defect removal activities employed during the SDLC.
- **Purple nodes**: Account for the types of defects that remain in the software at any given stage of the SDLC.
- **Yellow node**: Accounts for the types of defects that remain in the software after all stages of the SDLC.
- **Green node**: Accounts for the software failure probability, based on the defects that remain in the software after the SDLC.

In total, BAHAMAS employs the following concepts. When accounting for defect introduction and removal, specific types of defects will remain in the software. Depending on the types of defects that remain, the software will exhibit certain failure modes.

## Web-App Tool
https://bahamas.streamlit.app

## Webpage
https://idaholab.github.io/BAHAMAS/

## Installation

Install required libraries:

```bash
  conda create -n bahamas_libs python=3.13
  conda activate bahamas_libs
  pip install toml streamlit==1.35 streamlit-aggrid==1.1.5 numpy>=1.24 pandas==2.3 scipy openpyxl pytest plotly kaleido matplotlib streamlit-option-menu jsonpointer streamlit_extras
```

This can be installed with pip (perferably in a venv):

```bash
pip install --verbose .
```

or


```bash
pip install --verbose --editable .
```
and then run with a command like:

```bash
bahamas -i examples/bnn.toml
```

The tests can be run with:

```bash
pytest
```

## Software Failure Probability Evaluation via Web App

```bash
cd app
streamlit run app.py
```

## Software Failure Probability Evaluation via CLI

### Run

```bash
conda activate bahamas_libs
cd /path/to/BAHAMAS/examples
python ../bahamas/main.py -i bbn.toml
```

### BAHAMAS Input

```toml
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
```

### Screen Output

```bash

  06-Aug-25 09:39:54 BAHAMAS              INFO     Welcome!
  06-Aug-25 09:39:54 BAHAMAS              INFO     Input file: ../data/Task_List.xlsx
  06-Aug-25 09:39:54 BAHAMAS              WARNING  Default output file ../data/out_Task_List.xlsx will be used
  06-Aug-25 09:39:54 BAHAMAS.ODC          INFO     Construct ODC Conditional Distribution for each SDLC stage
  06-Aug-25 09:39:54 BAHAMAS.UCA          INFO     Construct UCA ODC defect correlation distribution.
  06-Aug-25 09:39:54 BAHAMAS.BBN          INFO     Sampling HEP and DCP
  06-Aug-25 09:39:54 BAHAMAS.HEP          INFO     Calculate SDLC "Concept" stage HEP
  06-Aug-25 09:39:54 BAHAMAS.DCP          INFO     Calculate DCP for SDLC "Concept" stage
  06-Aug-25 09:39:54 BAHAMAS.HEP          INFO     Calculate SDLC "Requirement" stage HEP
  06-Aug-25 09:39:54 BAHAMAS.DCP          INFO     Calculate DCP for SDLC "Requirement" stage
  06-Aug-25 09:39:54 BAHAMAS.HEP          INFO     Calculate SDLC "Design" stage HEP
  06-Aug-25 09:39:54 BAHAMAS.DCP          INFO     Calculate DCP for SDLC "Design" stage
  06-Aug-25 09:39:54 BAHAMAS.HEP          INFO     Calculate SDLC "Implementation" stage HEP
  06-Aug-25 09:39:54 BAHAMAS.DCP          INFO     Calculate DCP for SDLC "Implementation" stage
  06-Aug-25 09:39:54 BAHAMAS.HEP          INFO     Calculate SDLC "Testing" stage HEP
  06-Aug-25 09:39:54 BAHAMAS.DCP          INFO     Calculate DCP for SDLC "Testing" stage
  06-Aug-25 09:39:54 BAHAMAS.HEP          INFO     Calculate SDLC "Install and Maintenance" stage HEP
  06-Aug-25 09:39:54 BAHAMAS.DCP          INFO     Calculate DCP for SDLC "Install and Maintenance" stage
  06-Aug-25 09:39:54 BAHAMAS.BBN          INFO     Sampling ODC
  06-Aug-25 09:39:54 BAHAMAS.BBN          INFO     Sampling UCA
  06-Aug-25 09:39:54 BAHAMAS.BBN          INFO     Compute marginal ODC
  06-Aug-25 09:39:54 BAHAMAS.BBN          INFO     BBN Propagation
  06-Aug-25 09:39:54 BAHAMAS.BBN          INFO     Compute UCA and total failure probabilities
  06-Aug-25 09:39:56 BAHAMAS              INFO     Software total failure: 2.9825182468709206e-05 with std 1.4002568043296736e-05
  06-Aug-25 09:39:56 BAHAMAS              INFO     UCA type: UCA-A, Mean: 7.127925281781246e-06, STD: 3.4908455837352817e-06
  06-Aug-25 09:39:56 BAHAMAS              INFO     UCA type: UCA-B, Mean: 1.3451519498232246e-05, STD: 6.3548059571775254e-06
  06-Aug-25 09:39:56 BAHAMAS              INFO     UCA type: UCA-C, Mean: 4.900300523766049e-06, STD: 2.4943170792606996e-06
  06-Aug-25 09:39:56 BAHAMAS              INFO     UCA type: UCA-D, Mean: 4.345437164929662e-06, STD: 2.336590212125128e-06
  06-Aug-25 09:39:56 BAHAMAS              INFO      ... Complete!
```

### Plots

SDLC Stage Failure Probabilities Based on Human Error Propagation
<img src="./docs/pics/hep_stage.png" alt="SDLC Stage Failure Probabilities Based on Human Error Propagation" width="800">
Software Orthogonal Defect Classification Failure Probabilities
<img src="./docs/pics/odc_sfp.png" alt="Software Orthogonal Defect Classification Failure Probabilities" width="800">
Software Unsafe Control Action Failure Probabilities
<img src="./docs/pics/uca_sfp.png" alt="Software Unsafe Control Action Failure Probabilities" width="800">
Total Software Failure Probability
<img src="./docs/pics/total_sfp.png" alt="Total Software Failure Probability" width="800">
