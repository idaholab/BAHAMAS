======================
Software Failure Modes
======================

Unsafe Control Action
---------------------

Software has different modes of failure. The conditional probability of
software failure given the existence of certain defect types, has been
discussed and developed in previous work by Idaho National Laboratory (see :cite:`Bao2023RiskAssessment`). Data from
:cite:`Agnelo2019NoSQLDataset` and :cite:`Agnelo2020NoSQLDefects` were assessed in terms of their impact on the usability,
functionality, and performance from an end-user perspective, and were
assigned a unsafe control action (UCA) or unsafe information flow (UIF) category (equivalently, a mode of failure). The
assessment result provided conditional relationships, shown in
:numref:`table-u-1`. More specifically, :numref:`table-u-1`,
which provides a global perspective on the relationship between defect
types and UCA/UIF failure modes :cite:`Bao2023RiskAssessment`. As further classifications are
performed, these distributions can be continually improved. These
correlations are used by :eq:`uca1`, where is the
total number of defect types considered by BAHAMAS, and is the UCA/UIF
failure mode being evaluated. :numref:`table-u-1` provides the conditional probabilities used for:

.. _eq-uca1:

.. math::
  :label: uca1

  P(software\ failure\ of\ mode\ x) = \sum_{i=1}^{I} P(UC_x|Type_i)P(Type_i)


An inherent assumption in this work is that software failure results from active
defects. An implication of :eq:`uca1` is that the defect activation probability
equals one, and that the activation of defects is mutually exclusive (i.e.,
multiple defects are not activated simultaneously). In other words,
the probability of software failure is a summation of the contribution
of each defect type. Future work may investigate refinements to this activation probability.

.. _table-u-1:

.. table:: UCA/UIF Defect Type Correlation Table
  :align: center

  +---------------+---------------+---------------+---------------+------------+
  | Defect Class  | UCA/UIF       | UCA/UIF       | UCA/UIF       | UCA/UIF    |
  +===============+===============+===============+===============+============+
  |               | A             | B             | C             | D          |
  +---------------+---------------+---------------+---------------+------------+
  | Algorithm     | 0.217±0.051   | 0.525±0.068   | 0.124±0.044   | 0.134±0.019|
  +---------------+---------------+---------------+---------------+------------+
  | Assignment    | 0.288±0.152   | 0.667±0.130   | 0.045±0.072   | N/A        |
  +---------------+---------------+---------------+---------------+------------+
  | Checking      | 0.219±0.074   | 0.539±0.115   | 0.102±0.072   | 0.141±0.129|
  +---------------+---------------+---------------+---------------+------------+
  | Documentation | 0.250±0.250   | 0.250±0.250   | 0.250±0.250   | 0.250±0.250|
  +---------------+---------------+---------------+---------------+------------+
  | Function      | 0.250±0.154   | 0.518±0.064   | 0.157±0.092   | 0.074±0.216|
  +---------------+---------------+---------------+---------------+------------+
  | Interface     | 0.262±0.065   | 0.579±0.086   | 0.093±0.095   | 0.065±0.039|
  +---------------+---------------+---------------+---------------+------------+
  | Relationship  | 0.250±0.250   | 0.250±0.250   | 0.250±0.250   | 0.250±0.250|
  +---------------+---------------+---------------+---------------+------------+
  | Timing        | 0.095±0.334   | 0.190±0.289   | 0.524±0.423   | 0.190±0.289|
  +---------------+---------------+---------------+---------------+------------+

Note: This table was based on :cite:`Bao2023RiskAssessment`. These distributions may change as more
data are collected and data collection methods improve.
