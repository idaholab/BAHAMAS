# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

import os
import numpy as np
import pytest

from bahamas.sdlc_stage_hep_calculation import sdlc_stage_hep_calculation
from bahamas.human_error_mode_distribution import get_hemd_from_spreadsheet
from bahamas.stage_odc_distribution import get_stage_odc_dist
from bahamas.defect_conditional_probability import stage_dcp_calculation
from bahamas.uca_defect_correlation import get_uca_defect_correlation_dist
from bahamas.software_total_failure_probability_bbn import BBN
from bahamas.utils import SDLC_stages, ODC_types, UCA_types


workdir = os.path.dirname(__file__)
defect_data = os.path.join(workdir, '..', 'data', 'Defect_Data.xlsx')
task_data = os.path.join(workdir, '..', 'data', 'Task_List.xlsx')

def test_HEP_EMD():
    _, d = get_hemd_from_spreadsheet(defect_data)

    value = d["D2C"].pdf(0.6)
    expected = 2.0301163385771801e-07

    assert value == pytest.approx(expected, rel=1e-6, abs=1e-12)

def test_stage_odc_dist():
    d = get_stage_odc_dist(defect_data)

    # Tolerances
    rel_tol = 1e-6
    abs_tol = 1e-12

    # CDF checks
    assert d["Concept"]["Documentation"].cdf(0.99) == pytest.approx(
        7.327789556831712e-06, rel=rel_tol, abs=abs_tol
    )
    assert d["Requirement"]["Algorithm"].cdf(0.1) == pytest.approx(
        0.0012975084733137195, rel=rel_tol, abs=abs_tol
    )

    # Mean checks
    assert d["Concept"]["Documentation"].mean() == pytest.approx(
        (1000 + 0.5) / (1.0 + 1000), rel=rel_tol, abs=abs_tol
    )
    assert d["Requirement"]["Assignment"].mean() == pytest.approx(
        (26 + 0.5) / (1.0 + 375), rel=rel_tol, abs=abs_tol
    )
    assert d["Design"]["Checking"].mean() == pytest.approx(
        (26 + 0.5) / (1.0 + 375), rel=rel_tol, abs=abs_tol
    )
    assert d["Implementation"]["Function"].mean() == pytest.approx(
        (372 + 0.5) / (1.0 + 2292), rel=rel_tol, abs=abs_tol
    )
    assert d["Testing"]["Interface"].mean() == pytest.approx(
        (361 + 0.5) / (1.0 + 2464), rel=rel_tol, abs=abs_tol
    )
    assert d["Install and Maintenance"]["Relationship"].mean() == pytest.approx(
        (91 + 0.5) / (1.0 + 2464), rel=rel_tol, abs=abs_tol
    )
    assert d["Design"]["Timing"].mean() == pytest.approx(
        (13 + 0.5) / (1.0 + 375), rel=rel_tol, abs=abs_tol
    )

def test_dcp():
    dcp_gold = [
        3.497242685425109e-05,
        0.0002529112181892472,
        3.9544415406499936e-05,
        5.478224783437511e-05,
        3.7439121863896394e-05,
        5.478224783437511e-05,
    ]

    # Tolerances for floating-point / probabilistic calculations
    rel_tol = 1e-6
    abs_tol = 1e-12

    for i, stage in enumerate(SDLC_stages):
        dcp = stage_dcp_calculation(task_data, stage)
        assert dcp == pytest.approx(dcp_gold[i], rel=rel_tol, abs=abs_tol)

def test_uca_defect_correlation():
    ## Data for norm distribution
    # data = np.array([
    # [0.217, 0.0255, 0.525, 0.034, 0.124, 0.022, 0.134, 0.0095],
    # [0.288, 0.076, 0.667, 0.065, 0.045, 0.036, 0, 0],
    # [0.219, 0.037, 0.539, 0.0575, 0.102, 0.036, 0.141, 0.0645],
    # [0.25, 0.125, 0.25, 0.125, 0.25, 0.125, 0.25, 0.125],
    # [0.25, 0.077, 0.518, 0.032, 0.157, 0.046, 0.074, 0.108],
    # [0.262, 0.0325, 0.579, 0.043, 0.093, 0.0475, 0.065, 0.0195],
    # [0.25, 0.125, 0.25, 0.125, 0.25, 0.125, 0.25, 0.125],
    # [0.095, 0.167, 0.19, 0.1445, 0.524, 0.2115, 0.19, 0.1445]
    # ])
    ## Data for truncated normal distribution
    data = np.array([
        2.17000000e-01, 2.55000000e-02, 2.88023094e-01, 7.59562269e-02,
        2.19000000e-01, 3.69999989e-02, 2.56905982e-01, 1.17689469e-01,
        2.50157985e-01, 7.67429390e-02, 2.62000000e-01, 3.25000000e-02,
        2.56905982e-01, 1.17689469e-01, 1.74228858e-01, 1.18680274e-01,
        5.25000000e-01, 3.40000000e-02, 6.66999948e-01, 6.49998672e-02,
        5.38999999e-01, 5.74999999e-02, 2.56905982e-01, 1.17689469e-01,
        5.18000000e-01, 3.20000000e-02, 5.79000000e-01, 4.30000000e-02,
        2.56905982e-01, 1.17689469e-01, 2.16813548e-01, 1.22746487e-01,
        1.24000001e-01, 2.19999969e-02, 5.23521165e-02, 3.01844519e-02,
        1.02260018e-01, 3.56287876e-02, 2.56905982e-01, 1.17689469e-01,
        1.57054236e-01, 4.59073196e-02, 9.58592444e-02, 4.45215116e-02,
        2.56905982e-01, 1.17689469e-01, 5.21162941e-01, 1.98439447e-01,
        1.34000000e-01, 9.50000000e-03, 5.00000000e-15, 2.88675135e-15,
        1.43393694e-01, 6.17819499e-02, 2.56905982e-01, 1.17689469e-01,
        1.19224107e-01, 7.91971989e-02, 6.50300873e-02, 1.94497665e-02,
        2.56905982e-01, 1.17689469e-01, 2.16813548e-01, 1.22746487e-01,
    ])

    dist_dict = get_uca_defect_correlation_dist(defect_data)

    # Tolerances: numerical integration + truncation effects
    rel_tol = 1e-6
    abs_tol = 1e-10

    n_odc = len(ODC_types)

    for i, uca in enumerate(UCA_types):
        for j, odc in enumerate(ODC_types):
            mean_expected = data[i * n_odc * 2 + j * 2]
            std_expected  = data[i * n_odc * 2 + j * 2 + 1]

            mean_val = dist_dict[uca][odc].mean()
            std_val  = dist_dict[uca][odc].std()

            assert mean_val == pytest.approx(
                mean_expected, rel=rel_tol, abs=abs_tol
            )
            assert std_val == pytest.approx(
                std_expected, rel=rel_tol, abs=abs_tol
            )


def test_BNN():
    uca_mean = [
        7.154187342983309e-06,
        1.3478917428646428e-05,
        4.902251562039053e-06,
        4.34464021192543e-06,
    ]
    uca_sigma = [
        3.155548430508983e-06,
        5.5923036374815045e-06,
        2.4813382880915815e-06,
        1.920421171162386e-06,
    ]

    software_BBN = BBN(defect_data, task_data, num_samples=1000)
    software_BBN.calculate()
    total_failure_mean, total_failure_sigma, _ = (
        software_BBN.get_total_failure_probability()
    )

    # Tolerances suitable for MC / floating-point noise
    rel_tol = 1e-6
    abs_tol = 1e-10

    assert total_failure_mean == pytest.approx(
        2.9879996545594217e-05, rel=rel_tol, abs=abs_tol
    )
    assert total_failure_sigma == pytest.approx(
        1.240158963980545e-05, rel=rel_tol, abs=abs_tol
    )

    for i, uca in enumerate(UCA_types):
        mean, sigma, _ = software_BBN.get_uca(uca)
        assert mean == pytest.approx(uca_mean[i], rel=rel_tol, abs=abs_tol)
        assert sigma == pytest.approx(uca_sigma[i], rel=rel_tol, abs=abs_tol)
