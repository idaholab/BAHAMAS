==============
Defect Removal
==============

Trigger Coverage
----------------

Verification and review activities are employed during software development to ensure the
software is reliable. The quality of these activities influences defect removal and overall
software quality. Orthogonal defect classification (ODC) indicates that reviews
performed during the software life cycle can help identify and remove defects.
Depending on the review, specific concepts, or triggers, are employed and
may bring out defects or allow them to surface.  High-quality review activities
should employ these triggers during each stage of the SDLC, thereby reducing
the probability of defects remaining within the software. On this basis, trigger coverage
has been selected as a metric for defect removal. The stage-level trigger coverage (TC),
given by :eq:`a-1`, is determined from the average of each task-level trigger
coverage (tc), which is the percent of relevant triggers that have been covered for a task
in a particular SDLC stage. Note that :math:`T` is the total number of relevant tasks for a given stage.

.. math::
  :label: a-1

  TC = \frac{1}{T} \sum_{i=1}^{T} (tc)_i

Review
------

In addition to trigger coverage, the average number of reviews for a given SDLC stage
is also referenced as a metric for defect removal. When tasks are reviewed or checked,
they are less likely to fail. Checkers are considered in human reliability analysis (e.g., THERP)
and represent recovery paths for a given activity. The average number of reviews for
a particular stage is defined by :eq:`a-2`, where :math:`r` is the average number of reviews
performed for each relevant task and :math:`T` is the total number of relevant tasks for a given
stage. As an example, for a given task, some triggers may be reviewed or checked multiple
times, whereas others are not. The average of these reviews represents :math:`r`.

.. math::
  :label: a-2

  R = \frac{1}{T} \sum_{i=1}^{T} (r)_i

ODC Triggers
------------

:numref:`table-r-1` shows the typical mapping of the triggers and review activities.
Our work adopts this mapping for convenience.

.. _table-r-1:

.. table:: ODC Triggers
  :align: center
  :widths: 30 80

  +----------------------------------------------------+---------------------------------------------+
  | **Review Activities**                              | **Triggers**                                |
  +----------------------------------------------------+---------------------------------------------+
  | For use during review activities associated with   | Design Conformance                          |
  |                                                    |                                             |
  | concept, design, and implementation stages of the  | Logic/Flow                                  |
  |                                                    |                                             |
  | software development life cycle.                   | Backward Compatibility                      |
  |                                                    |                                             |
  |                                                    | Lateral Compatibility                       |
  |                                                    |                                             |
  |                                                    | Concurrency                                 |
  |                                                    |                                             |
  |                                                    | Internal Document                           |
  |                                                    |                                             |
  |                                                    | Language Dependency                         |
  |                                                    |                                             |
  |                                                    | Side Effect                                 |
  |                                                    |                                             |
  |                                                    | Rare Situations                             |
  +----------------------------------------------------+---------------------------------------------+
  | For use during review activities associated with   | Simple Path                                 |
  |                                                    |                                             |
  | testing stages of the software development life    | Complex Path                                |
  |                                                    |                                             |
  | cycle.                                             | Test Coverage                               |
  |                                                    |                                             |
  |                                                    | Test Variation                              |
  |                                                    |                                             |
  |                                                    | Test Sequencing                             |
  |                                                    |                                             |
  |                                                    | Test Interaction                            |
  |                                                    |                                             |
  |                                                    | Workload/Stress                             |
  |                                                    |                                             |
  |                                                    | Recovery/Exception                          |
  |                                                    |                                             |
  |                                                    | Startup/Restart                             |
  |                                                    |                                             |
  |                                                    | Hardware Configuration                      |
  |                                                    |                                             |
  |                                                    | Software Configuration                      |
  |                                                    |                                             |
  |                                                    | Blocked Test (Previously Normal Mode)       |
  +----------------------------------------------------+---------------------------------------------+
