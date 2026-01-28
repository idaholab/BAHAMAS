# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

import numpy as np
import logging
from scipy.stats import truncnorm

from bahamas.sdlc_stage_hep_calculation import sdlc_stage_hep_calculation
from bahamas.sdlc_stage_hep_calculation_approx import sdlc_stage_hep_calculation_approx
from bahamas.human_error_mode_distribution import get_hemd_from_spreadsheet
from bahamas.stage_odc_distribution import get_stage_odc_dist
from bahamas.defect_conditional_probability import stage_dcp_calculation
from bahamas.uca_defect_correlation import get_uca_defect_correlation_dist
from bahamas.utils import SDLC_stages, ODC_types, UCA_types
from bahamas.plot_utils import plot_histogram

logger = logging.getLogger('BAHAMAS.BBN')

class BBN(object):
  """
    Bayesian belief network for reliability analysis of software
  """

  def __init__(self, defect_file, task_file, num_samples=1000, approx=False, data=None, seed=42):
    self.num_samples = num_samples
    self._approx = approx
    self._data = data
    np.random.seed(seed)
    self._uca = UCA_types
    self._odc = ODC_types
    self._sdlc = SDLC_stages
    self._defect = defect_file
    self._task = task_file
    self.prob_stage = {} # HEP for each stage
    self.prob_odc = {} # ODC marginal probability
    self.prob_dcp = {} # DEP for each stage
    self.prob_total = None # Software total probability
    self.prob_uca = {} # UCA probability
    self._hemd_dist = {}
    if not self._approx:
      _, self._hemd_dist =  get_hemd_from_spreadsheet(self._defect)
    self.prob_stage_odc = get_stage_odc_dist(self._defect)
    self.prob_uca_correlation = get_uca_defect_correlation_dist(self._defect)
    self._G = 0.25
    self.review_trigger_factor = np.exp(-8)*self._G # The same as the value used in Software_Quality_Survey.py

  def initialize_stage(self):
    G = self._G
    for stage, vals in self._data.items():
      rev = vals['review']
      trigger = vals['trigger']
      if 'samples' not in vals.keys():
        mean = vals['mean']
        std = vals['std']
        a = (0 - mean) / std
        b = (1 - mean) / std
        dist = truncnorm(a, b, loc=mean, scale=std)
        total = dist.rvs(size=self.num_samples)
        self.prob_stage[stage] = total
        self.prob_dcp[stage] = G*np.exp(-4.*rev*trigger)
      else:
        self.prob_stage[stage] = vals['samples']
        self.prob_dcp[stage] = G*np.exp(-4.*rev*trigger)/self.review_trigger_factor

  def calculate(self):
    """Calculate software failure probability based on BBN
    """
    logger.info('Sampling HEP and DCP')
    for stage in self._sdlc:
      if self._approx:
        if self._task is not None:
          # calculate human error propagation for each SDLC stage [sampled values]
          self.prob_stage[stage], _ = sdlc_stage_hep_calculation_approx(self._task, stage, self.num_samples, distribution="norm")
          # calculate DCP for each SDLC stage [single value without sampling]
          self.prob_dcp[stage] = stage_dcp_calculation(self._task, stage)
      else:
        if self._task is None:
          raise IOError("Task List input file is requested, but missing!")
        # calculate human error propagation for each SDLC stage [sampled values]
        self.prob_stage[stage], _ = sdlc_stage_hep_calculation(self._task, stage, self._hemd_dist, self.num_samples)
        # calculate DCP for each SDLC stage [single value without sampling]
        self.prob_dcp[stage] = stage_dcp_calculation(self._task, stage)

    if len(self.prob_stage) == 0 and self._data is not None:
      self.initialize_stage()

    # Sample stage ODC conditional probability
    logger.info('Sampling ODC')
    prob_stage_odc = {}
    for stage in self._sdlc:
      prob_stage_odc[stage] = {}
      for odc in self._odc:
        prob_stage_odc[stage][odc] = self.prob_stage_odc[stage][odc].rvs(self.num_samples)

    # Sample UCA correlation
    logger.info('Sampling UCA')
    prob_uca_correlation = {}
    for uca in self._uca:
      prob_uca_correlation[uca] = {}
      for odc in self._odc:
        prob_uca_correlation[uca][odc] = self.prob_uca_correlation[uca][odc].rvs(self.num_samples)

    # Calculate Marginal Probability
    logger.info('Compute marginal ODC')
    prob_stage_odc_marg = {}
    for stage in self._sdlc:
      prob_stage_odc_marg[stage] = {}
      for odc in self._odc:
        prob_stage_odc_marg[stage][odc] = prob_stage_odc[stage][odc] * self.prob_stage[stage] * self.prob_dcp[stage]

    # Propagate uncertainties via BBN
    logger.info('BBN Propagation')
    level = 2
    concept, requirement, design, implementation, testing, InMain = SDLC_stages
    for odc in self._odc:
      prob = 0
      for k in range(level):
        for l in range(level):
          for m in range(level):
            for n in range(level):
              for p in range(level):
                for q in range(level):
                  ak = prob_stage_odc_marg[concept][odc] if k == 0 else 1. - prob_stage_odc_marg[concept][odc]
                  bl = prob_stage_odc_marg[requirement][odc] if l == 0 else 1. - prob_stage_odc_marg[requirement][odc]
                  cm = prob_stage_odc_marg[design][odc] if m == 0 else 1. - prob_stage_odc_marg[design][odc]
                  dn = prob_stage_odc_marg[implementation][odc] if n == 0 else 1. - prob_stage_odc_marg[implementation][odc]
                  ep = prob_stage_odc_marg[testing][odc] if p == 0 else 1. - prob_stage_odc_marg[testing][odc]
                  fq = prob_stage_odc_marg[InMain][odc] if q == 0 else 1. - prob_stage_odc_marg[InMain][odc]
                  factor = 0. if np.all([k,l,m,n,p,q]) else 1.
                  prob += factor * ak * bl * cm * dn * ep * fq
      self.prob_odc[odc] = prob

    logger.info('Compute UCA and total failure probabilities')
    # Evaluate UCA probability and Total probability
    self.prob_total = 0.
    for uca in self._uca:
      prob = 0.
      for odc in self._odc:
        prob += self.prob_odc[odc] * prob_uca_correlation[uca][odc]
      self.prob_uca[uca] = prob
      self.prob_total += prob

  def get_total_failure_probability(self):
    """Get total failure probability

    Returns:
        tuple: mean, sigma, and samples
    """
    mean = np.mean(self.prob_total)
    sigma = np.std(self.prob_total)
    return mean, sigma, self.prob_total

  def get_uca(self, uca_type):
    """Get UCA probability

    Args:
        uca_type (str): Type of UCA

    Returns:
        tuple: mean, sigma, and samples
    """
    prob_uca = self.prob_uca[uca_type]
    mean = np.mean(prob_uca)
    sigma = np.std(prob_uca)
    return mean, sigma, prob_uca


  def plot(self, type='all', save=False, show=True):
    """Plot calculated data

    Args:
        type (str, optional): Type of plots to plot (defaults to 'all')
        save (bool, optional): Save plots into .png file if True (defaults to False)

    Returns:
      list or figure object: plotly figure object
    """
    fig = None
    if type.lower() == 'all':
      fig1 = plot_histogram(self.prob_stage, title='Software Development Life Cycle Stage Failure Probabilities Based on Human Error Propagation', save=save, show=show)
      fig2 = plot_histogram(self.prob_odc, title='Software ODC Failure Probabilities', save=save, show=show)
      fig3 = plot_histogram(self.prob_uca, title='Software UCA Failure Probabilities', save=save, show=show)
      fig4 = plot_histogram({'Total Failure Probability':self.prob_total}, title='Total Software Failure Probability', save=save, show=show)
      fig = [fig1, fig2, fig3, fig4]
    elif type.lower() == 'stage':
      fig = plot_histogram(self.prob_stage, title='Software Development Life Cycle Stage Failure Probabilities Based on Human Error Propagation', save=save, show=show)
    elif type.lower() == 'odc':
      fig = plot_histogram(self.prob_odc, title='Software ODC Failure Probabilities', save=save, show=show)
    elif type.lower() == 'uca':
      fig = plot_histogram(self.prob_uca, title='Software UCA Failure Probabilities', save=save, show=show)
    elif type.lower() == 'total':
      fig = plot_histogram({'Total Failure Probability':self.prob_total}, title='Total Software Failure Probability', save=save, show=show)

    return fig

