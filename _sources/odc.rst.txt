==================
Defect Types (ODC)
==================

During software development, defects or bugs arise, and their
concentrations change throughout development as they are influenced by
the conducted review activities :cite:`Chillarege1992ODC` :cite:`Agnelo2019NoSQLDataset`
:cite:`Agnelo2020NoSQLDefects`. The ODC methodology has produced
a scheme that categorizes software defects into eight orthogonal classes
(i.e., types). The present work relies on this classification scheme to help
predict software failure probabilities. Historical ODC data
provides a collection of defects, along with the activities (and
triggers) used to find them. We mapped these activities to SDLC stages so as to provide
a convenient view of defect types for a given stage. ODC design
review activities are mapped to the concept and requirements stages, ODC
code inspection activities are mapped to the design and implementation
stages, and ODC testing activities are mapped to the testing and the
installation & maintenance stages. Bayesian inference :cite:`Dezfuli2009BayesianInference` was applied to
develop distributions for each defect type at each stage of the SDLC .
This was done by taking a binomial model, and Jeffreys noninformative prior,
then obtaining a posterior beta distribution to represent the general
expected defect types for each stage. The posterior distribution is
given as a beta with parameters :math:`\alpha + x` and :math:`\beta + y - x`,
where `x` is the number of
observed events, `y` is the number of trials, and :math:`\alpha = 0.5` and :math:`\beta = 0.5` for
Jeffreys noninformative prior :cite:`Dezfuli2009BayesianInference` :cite:`Atwood2003ParameterEstimation`. Distributions can be produced
readily from the data given in :numref:`table-o-1`.

.. _table-o-1:

.. table:: ODC Defect-Type Data for Each Review Activity
    :align: center

    +-----------------------------------------+------+------------+-----+------+------+------+------+------+
    | Typical categories of review            | Al.  | As.        | Ch. | Doc. | Fun. | Int. | Rel. | Tim. |
    +=========================================+======+============+=====+======+======+======+======+======+
    | Activities                              |      |            |     |      |      |      |      |      |
    +-----------------------------------------+------+------------+-----+------+------+------+------+------+
    | Design review                           | 56   | 26         | 26  | 107  | 90   | 57   | 0    | 13   |
    +-----------------------------------------+------+------------+-----+------+------+------+------+------+
    | Code inspection                         | 1215 | 153        | 240 | 58   | 372  | 221  | 8    | 25   |
    +-----------------------------------------+------+------------+-----+------+------+------+------+------+
    | Testing                                 | 1277 | 181        | 269 | 12   | 245  | 361  | 91   | 28   |
    +-----------------------------------------+------+------------+-----+------+------+------+------+------+

Note: Algorithm (Al.), Assignment (As.), Checking (Ch.), Documentation (Doc.), Function (Fun.), Interface (Int.),
Relationship (Rel.), and Timing (Tim.).

Defects classification serves as a basis for an equation that can
predict defect distributions for each software development stage.
Depending on the defect removal efforts, there is an expectation that
the probability of defects remaining is expected to be influenced. As expressed by
Humphreys :cite:`Humphreys1987BetaFactor`, design improvements can be considered a function (likely
nonlinear) of effort and time. A model was developed for this work so as to
express the conditional probability of specific defect types remaining,
given the state defect introduction and removal activities. :eq:`eq-odc1` is the defect conditional probability (DCP)
equation, where `G` is the general expected probability for a defect type
for a given SDLC stage (based on the posterior distributions obtained from
:numref:`table-o-1`), `TC` is the stage-level trigger coverage, and `R` is the average number of
reviews performed for each task in the SDLC stage.

.. math::
    :label: eq-odc1

    DCP = \begin{cases} StageReview(all\ states)\ and\ StageDefect\ (yes), & DCP = Ge^{-4TCR}\\ StageReview(all\ states)\ and\ StageDefect(no), & DCP = 0 \end{cases}
