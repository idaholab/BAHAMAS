===================
Defect Introduction
===================

Human Error Modes Distributions
-------------------------------

This work assumes that the Technique for Human Error Rate Prediction (THERP) can be extended to address human errors
in the SDLC by assuming that the SDLC errors can be classified as either diagnostic, commission, or
omission errors. THERP is a systematic method used for evaluating human errors probabilities in
various tasks, along with their potential impact on system performance. THERP has guidance for scoring
certain activities closely related to diagnostic, commission, or omission errors.
Ultimately, it is these human error probabilities (HEPs) and the combinations thereof that is employed by
BAHAMAS. The various combinations of diagnosis, omission, and commission errors can be evaluated through
Monte Carlo sampling using distributions from :numref:`table-1`. The results are the distributions used for assessing each SDLC task.

The distributions are given below in :numref:`table-1`. Each SDLC task is assessed for the dominant
combination of human error modes.

.. _table-1:

.. table:: Error Mode Distributions
  :align: center

  +------+---------------------------------------------+----------------+----------------+
  | Key  | Description                                 | mu             | sigma          |
  +======+=============================================+================+================+
  | D1   | Diagnosis Error (Diagnosis-1)               | -9.21034       | 2.0676         |
  +------+---------------------------------------------+----------------+----------------+
  | D2   | Simple Diagnosis Error (Diagnosis-2)        | -11.5129       | 2.0676         |
  +------+---------------------------------------------+----------------+----------------+
  | O    | Omission Error                              | -5.80914       | 0.978382       |
  +------+---------------------------------------------+----------------+----------------+
  | C    | Commission Error                            | -5.80914       | 0.978382       |
  +------+---------------------------------------------+----------------+----------------+
  | OC   | Omission and Commission Errors              | -5.116         | 0.978382       |
  +------+---------------------------------------------+----------------+----------------+
  | D1C  | Diagnosis-1 and Commission                  | -5.63215       | 0.94217        |
  +------+---------------------------------------------+----------------+----------------+
  | D1O  | Diagnosis-1 and Omission                    | -5.63215       | 0.94217        |
  +------+---------------------------------------------+----------------+----------------+
  | D1OC | Diagnosis-1, Omission and Commission        | -5.00712       | 0.942896       |
  +------+---------------------------------------------+----------------+----------------+
  | D2C  | Diagnosis-2 and Commission                  | -5.77788       | 0.960271       |
  +------+---------------------------------------------+----------------+----------------+
  | D2O  | Diagnosis-2 and Omission                    | -5.77788       | 0.960271       |
  +------+---------------------------------------------+----------------+----------------+
  | D2OC | Diagnosis-2, Omission and Commission        | -5.09867       | 0.966776       |
  +------+---------------------------------------------+----------------+----------------+


Diagnosis- or Understanding-Type Errors (D1)
--------------------------------------------

Performer
  Group consisting of stakeholders, engineers, and managers.

Background
  The process of defining a project is similar to assessing or diagnosing a new situation. There may be similarities with
  past experiences, but ultimately the scenario represents a new problem that must be solved. THERP was designed for
  assessing activities within the context of a nuclear power plant; therefore, its application must fit similar conditions.
  THERP prescribes HEPs for group activities associated with diagnoses of abnormal events.
  Diagnosing an abnormal event is assumed to be akin to solving a new problem. Experience, training, and expertise play a role in the
  diagnosis. But ultimately, the effort is not strictly routine. Hence, because each project is unique, we shall assume this
  is equivalent to diagnosing an abnormal event.

Error source
  Faulty diagnosis.

HEP
  Lognormal distribution. Median :math:`1.0 \times 10^{-4}`, EF 30.

**Note: D1 will be used for all general diagnosis- or understanding-type errors.**

Diagnosis- or Understanding-Type Errors (D2)
--------------------------------------------

Performer
  Group consisting of stakeholders, engineers, and managers.

Background
  Same as previous, but extended to represent less stress, more time, or, equivalently, to represent a simpler
  diagnostic event. This has the effect of shifting the median of the distribution from :math:`1 \times 10^{-4}` to :math:`1 \times 10^{-5}`.

Error source
  Faulty diagnosis.

Human Error Probability
  Lognormal distribution. Median :math:`1 \times 10^{-5}`, EF 30.

**Note: D2 is applied for less complex tasks (i.e., pre-defined, well-understood tasks)**

Errors of Omission (O) and Errors of Commission (C)
---------------------------------------------------

Performer
  Group consisting of stakeholders, engineers, and managers.

Background
  THERP does not provide guidance on the creation of technical documents, code, etc. This process may involve omission
  or commission errors.

Error source
  One or more things may be overlooked or left out when completing a task. At other times, wrong or incorrect
  details or actions may arise.

Guidance
  THERP indicates that, when an appropriate HEP is unavailable, the nominal value of :math:`3 \times 10^{-3}` is to be assigned for errors of omission
  or errors of commission. The case study assumes that for those events not clearly
  omission- or commission-dominant, a union of the two will be used. This value can be approximated using the rare event
  approximation or by assuming that A and B are independent. Ultimately, the result is given as :math:`P(A or B) = P(A) + P(B) = 6 \times 10^{-3}`.

HEPs
  Omission only (O): lognormal distribution; median :math:`3 \times 10^{-3}`, EF 5.
  Commission only (C): lognormal distribution; median :math:`3 \times 10^{-3}`, EF 5.
  Omission or commission possible (O-C): lognormal distribution; median :math:`6 \times 10^{-3}`, EF 5.

