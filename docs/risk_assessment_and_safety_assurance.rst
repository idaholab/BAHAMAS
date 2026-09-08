.. _risk-assessment-and-safety-assurance:

Risk Assessment and Safety Assurance of Digital Instrumentation and Control Systems
===================================================================================

:Authors: Congjian Wang, Tate H. Shorthill, Eward Chen, Jisuk Kim, and Svetlana Lawrence
:Organization: Idaho National Laboratory
:Report: INL/MIS-26-94209

1. Redundancy-guided system-theoretic hazard analysis (RESHA)
-------------------------------------------------------------

**Goal:** To identify hardware, software, interaction-related, and common-cause failures in highly redundant digital instrumentation and control (DI&C) systems. RESHA is intended to determine whether an individual digital failure, including a software common-cause failure (CCF), could become a single point of failure and cause loss of a required system function. Its results provide the qualitative basis for subsequent software-reliability quantification, system fault-tree evaluation, plant probabilistic risk assessment, and design optimization.

**Description:** RESHA combines **Systems-Theoretic Process Analysis (STPA)** with **fault-tree analysis (FTA)** and organizes the analysis according to the actual redundancy structure of the DI&C architecture. Unlike a conventional STPA application, RESHA explicitly examines redundancy at the system, division, unit, and module levels. This structure helps identify failures that may affect several nominally independent components.

RESHA considers both interactions between the DI&C system and the controlled plant process, referred to as **Type I interactions**, and interactions among digital components or systems, referred to as **Type II interactions**. Software failures in controllers are represented as **unsafe control actions (UCAs)**. Failures in sensors, communication modules, data-processing modules, and other intermediate processors are represented as **unsafe information flows (UIFs)**. A UIF may involve missing information, spurious information, incorrect timing or sequence, or an incorrect value.

The method is implemented through seven principal steps:

1. Develop a detailed representation of the system architecture, functions, interfaces, and redundancy.

2. Construct a hardware fault tree for a defined system top event.

3. Apply redundancy-guided STPA to identify relevant UCAs and UIFs.

4. Add the UCAs and UIFs to the hardware fault tree as software basic events.

5. Identify potential software CCFs from shared or duplicated UCA/UIF events.

6. Solve the integrated fault tree to identify minimal cut sets and single points of failure.

7. Identify failure triggers and recommend preventive, mitigative, redundancy, or diversity measures.

The primary outputs are an integrated hardware–software fault tree, candidate common-cause component groups, minimal cut sets, single points of failure, and recommendations for system modification.

**Advantages:** The method provides several important advantages for DI&C safety analysis:

-  It represents hardware, software, and digital interactions within a common and traceable model.

-  It preserves the actual multilevel redundancy of complex protection and safety-actuation architectures.

-  It identifies software CCF vulnerabilities that could be overlooked when redundant divisions are analyzed only at a high level.

-  The UIF concept extends hazard analysis to monitoring, communication, and information-processing components that do not directly control the physical process.

-  It can support design comparisons involving redundancy, software diversity, and hardware diversity.

-  It can be applied iteratively during design development, allowing hazards to be identified before the architecture is finalized.

**Conditions for Application:** RESHA is most suitable for safety-significant, software-intensive systems containing multiple redundant divisions, trains, processors, or communication pathways. Effective application requires:

-  a clearly defined system boundary, mission, hazard, and fault-tree top event;

-  sufficient architecture, requirements, logic, interface, communication, and functional information;

-  explicit identification of controllers, intermediate processors, sensors, actuators, and human interactions;

-  a level of decomposition detailed enough to expose meaningful dependencies without modeling insignificant internal variables;

-  physically distinguishable hardware platforms or communication boundaries for assigning UIFs;

-  consistent hazardous contexts for UCAs, UIFs, and the selected fault-tree top event; and

-  multidisciplinary review by DI&C, software, systems, PRA, human-factors, and CCF specialists.

**Disadvantages and Limitations:** RESHA can require substantial effort for large, highly interconnected systems. Detailed control structures and integrated fault trees may become difficult to construct, review, and maintain. Results can also depend on analyst judgment when selecting system boundaries, decomposition levels, hazardous contexts, and potential CCF groups.

The method does not by itself calculate software-failure probabilities. Additional methods and evidence are required before system reliability or plant risk can be quantified. Criteria for deciding when shared software, inputs, tools, requirements, or operating environments create a credible software CCF remain partly judgment based.

Because the integrated model relies on conventional fault-tree logic, dynamic behaviors such as software reconfiguration, timing-dependent sequences, recovery actions, and changing operating states may be represented only approximately.

**References**

1. Bao, H., Shorthill, T., Chen, E., et al., *An Integrated Framework for Risk Assessment of High Safety-significant Safety-related Digital Instrumentation and Control Systems in Nuclear Power Plants: Methodology and Demonstration*, INL/RPT-22-68656, Idaho National Laboratory, 2022.

2. Bao, H., Shorthill, T., and Zhang, H., “Hazard Analysis for Identifying Common Cause Failures of Digital Safety Systems Using a Redundancy-Guided Systems-Theoretic Approach,” *Annals of Nuclear Energy*, Vol. 148, Article 107686, 2020.

3. Shorthill, T., Bao, H., Zhang, H., and Ban, H., “A Redundancy-Guided Approach for the Hazard Analysis of Digital Instrumentation and Control Systems in Advanced Nuclear Power Plants,” *Nuclear Technology*, Vol. 208, No. 5, pp. 892–911, 2022.

4. Leveson, N. G., and Thomas, J. P., *STPA Handbook*, 2018.

5. Clark, A. J., Williams, A. D., Muna, A., and Gibson, M., “Hazard and Consequence Analysis for Digital Systems—A New Approach to Risk Analysis in the Digital Era for Nuclear Power Plants,” *Transactions of the American Nuclear Society*, 2018.

2. Multiscale quantitative reliability analysis
-----------------------------------------------

Qualitative hazard analysis, such as RESHA, alone can identify how a digital I&C system may fail, but it cannot determine how likely those failures are or whether they affect system and plant safety. Digital I&C reliability depends on failure mechanisms at several interconnected scales, including residual software defects, unsafe control actions and unsafe information flows, hardware failures, dependencies among redundant components, and hardware or software common-cause failures. A quantitative approach is therefore required to translate RESHA findings into failure probabilities, distinguish risk-significant vulnerabilities from low-consequence concerns, and avoid relying solely on highly conservative bounding assumptions that may obscure the safety benefits of digital modernization. It also provides the evidence needed to compare redundancy and diversity alternatives, prioritize verification and testing, and support risk-informed design and licensing decisions.

The analysis converts the qualitative hardware, software, and interaction failures identified by RESHA into probabilistic estimates across the software-component, subsystem, and complete DI&C-system levels. **ORCAS** is applied under data-rich conditions, using software testing results, defect classification, test-coverage evidence, and software reliability growth models to estimate the probabilities of specific software failure modes. **BAHAMAS** is used under data-limited or early-design conditions, combining Bayesian belief networks and human reliability analysis to relate software-development errors, review effectiveness, and residual defects to software failure probabilities. These estimates are combined with hardware reliability data and CCF models, including a modified beta-factor method, and entered into the integrated RESHA fault tree to calculate system failure probabilities, identify important minimal cut sets, evaluate uncertainty, and provide quantitative inputs for plant consequence analysis and safety assurance.

2.1 BAHAMAS for software reliability analysis in data-limited conditions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** The Bayesian and Human-Reliability-Analysis-Aided Method for the Reliability Analysis of Software (BAHAMAS) estimates the probability of safety-significant software failure modes when sufficient testing, defect, or operational data are unavailable. It is intended primarily for early design stages, newly developed systems, or proprietary software for which detailed source code and failure histories cannot be accessed. BAHAMAS converts qualitative software failures identified by RESHA—particularly unsafe control actions and unsafe information flows—into quantitative basic-event probabilities for integrated fault trees. These probabilities can subsequently support system reliability calculations, software CCF analysis, probabilistic risk assessment, and comparison of alternative DI&C designs.

**Description:** BAHAMAS models the causal chain: Human errors during the software development lifecycle → residual software defects → software failure modes. A Bayesian belief network provides the overall computational structure. Human reliability analysis, such as Technique for Human Error Rate Prediction (THERP), supplies probabilities for errors introduced during six software lifecycle stages: concept development, requirement, design, implementation or coding, testing, and installation and maintenance.

The Bayesian network also represents the effectiveness of defect-removal activities. Review quality is evaluated from the coverage of applicable orthogonal-defect-classification (ODC) triggers and the average number of reviews performed for each lifecycle task. Review quality is classified from none to excellent, with more comprehensive and repeated reviews reducing the probability that defects remain in the delivered software. ODC-based relationships are then used to connect residual defect types to the four general UCA/UIF failure categories: failure to provide a required action or information, spurious provision, incorrect timing or sequence, and incorrect duration or value.

BAHAMAS estimates the **total software failure probability** associated with the selected failure mode. A typical BAHAMAS application consists of five steps:

1. Select a RESHA-identified software failure event, i.e., software failure mode, and define its component, action or information flow, and hazardous context.

2. Collect available software lifecycle plans, requirements, design descriptions, review records, and quality-assurance information.

3. Perform HRA for the relevant lifecycle tasks.

4. Assess the quality and extent of reviews and defect-removal activities.

5. Evaluate the Bayesian network to estimate the UCA/UIF probability and its uncertainty range.

**Advantages**

-  **Applicable with limited empirical data.** BAHAMAS does not require a large database of observed software failures or defects and can therefore be used before extensive testing or operation.

-  **Supports early risk-informed design.** It provides preliminary probabilities for comparing architectures, prioritizing verification activities, and evaluating redundancy and diversity alternatives.

-  **Integrates heterogeneous evidence.** The Bayesian network can combine lifecycle documentation, HRA results, review quality, defect classifications, expert judgment, and limited observations.

-  **Provides causal traceability.** The model connects development activities and human errors to residual defects and ultimately to specific safety-significant UCA/UIF events.

-  **Represents the benefit of quality assurance.** Sensitivity to review coverage and review frequency allows analysts to estimate how improved verification or inspection may reduce software risk.

-  **Compatible with FTA and PRA.** BAHAMAS outputs can be inserted as software basic-event probabilities in RESHA-derived fault trees and propagated to system- and plant-level risk models.

**Conditions for Application:** BAHAMAS is most appropriate when testing and operational data are insufficient for a data-driven method, but credible information about the software development process is available. Application requires a clearly defined UCA or UIF, a corresponding fault-tree location, and sufficient lifecycle information to identify development tasks and evaluate review quality.

The method should be applied by a multidisciplinary team familiar with software engineering, DI&C design, HRA, Bayesian modeling, ODC, hazard analysis, and PRA. Assumptions concerning human-error probabilities, task dependencies, defect distributions, review effectiveness, and the applicability of generic defect-to-failure relationships must be documented and subjected to sensitivity analysis. The present form is best suited to conventional, configuration-controlled software whose functionality is explicitly defined by source code. Adaptive AI or machine-learning systems require additional treatment because their behavior can change with training data, model updates, and operational conditions.

**Disadvantages and Limitations:** BAHAMAS produces an approximate, evidence-informed estimate rather than a direct empirical measurement of software reliability. Results can be highly sensitive to HRA inputs, expert judgments, review-quality scores, and assumed Bayesian conditional probabilities. THERP was developed principally for human actions in nuclear-plant operation rather than software development; its extension to concept development, coding, and testing therefore requires assumptions that have not been comprehensively validated.

The method further assumes that software defects can be traced to human errors, that human-error probabilities provide a meaningful surrogate for defect-introduction probabilities, and that generic relationships between defect classes and UCA/UIF modes are transferable to the software being assessed. Dependencies among lifecycle tasks may be difficult to represent, and treating them as independent can underestimate correlated errors.

**Tool:** `BAHAMAS source code <https://github.com/idaholab/BAHAMAS>`_ or `BAHAMAS documentation <https://idaholab.github.io/BAHAMAS/>`_

**References**

1. Bao, H., Shorthill, T., Chen, E., et al., *An Integrated Framework for Risk Assessment of High Safety-Significant Safety-Related Digital Instrumentation and Control Systems in Nuclear Power Plants: Methodology and Demonstration*, INL/RPT-22-68656, Idaho National Laboratory, 2022.

2. Shorthill, T., Bao, H., Zhang, H., and Ban, H., “A Novel Approach for Software Reliability Analysis of Digital Instrumentation and Control Systems in Nuclear Power Plants,” *Annals of Nuclear Energy*, Vol. 158, 2021.

3. Swain, A. D., and Guttmann, H. E., *Handbook of Human Reliability Analysis with Emphasis on Nuclear Power Plant Applications*, NUREG/CR-1278, U.S. Nuclear Regulatory Commission, 1983.

4. Chu, T.-L., Varuttamaseni, A., Yue, M., et al., *Developing a Bayesian Belief Network Model for Quantifying the Probability of Software Failure of a Protection System*, NUREG/CR-7233, U.S. Nuclear Regulatory Commission, 2018.

5. Kang, H. G., Lee, S. H., Lee, S. J., et al., “Development of a Bayesian Belief Network Model for Software Reliability Quantification of Digital Protection Systems in Nuclear Power Plants,” *Annals of Nuclear Energy*, Vol. 120, pp. 62–73, 2018.

6. Chillarege, R., Bhandari, I. S., Chaar, J. K., et al., “Orthogonal Defect Classification—A Concept for In-Process Measurements,” *IEEE Transactions on Software Engineering*, Vol. 18, No. 11, pp. 943–956, 1992.

2.2 ORCAS for software reliability analysis in data-rich conditions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** Orthogonal-Defect Classification for Assessing Software Reliability (ORCAS) is intended to quantify safety-significant software failure modes when sufficient software design, testing, defect, and operational evidence is available.

**Description:** ORCAS is an iterative, test-based, root-cause-oriented method that combines software testing, orthogonal defect classification (ODC), and software reliability growth models (SRGMs). Its main stages are:

1. **Collect system information.** Assemble software requirements specifications, software design descriptions, test plans and results, source code, anomaly reports, defect records, and relevant operational data.

2. **Define the scope.** Use RESHA and the integrated fault tree to identify the software components, functions, UCAs, and UIFs that require quantification.

3. **Evaluate testing adequacy.** Construct a requirements traceability matrix and trigger coverage assessment. Testing may include combinatorial testing, modified condition/decision coverage, boundary-value analysis, equivalence partitioning, sequence testing, stress testing, configuration testing, and recovery testing.

4. **Classify defects.** Categorize observed defects using ODC classes such as algorithm, assignment, checking, function, interface, relationship, and timing. Classification is based primarily on the nature of the defect and its corrective action.

5. **Quantify software failure modes.** Fit SRGMs to cumulative defect-discovery data for each applicable defect class. Data-derived conditional relationships are then used to translate defect-class failure probabilities into UCA/UIF probabilities.

6. **Evaluate confidence and uncertainty.** Examine the completeness of requirements and trigger coverage, stability of reliability predictions, parameter uncertainty, model uncertainty, and uncertainty in the defect-to-UCA/UIF relationships.

**Advantages**

-  **Empirical basis:** ORCAS uses observed testing and defect evidence rather than relying primarily on generic values or expert judgment.

-  **Failure-mode specificity:** It estimates probabilities for particular UCA/UIF categories instead of assigning a single reliability value to the complete software system.

-  **Strong traceability:** Requirements, tests, detected defects, corrective actions, UCA/UIF events, and fault-tree basic events can be linked within one assessment.

-  **Testing-gap identification:** The requirements traceability matrix and trigger coverage assessment identify functions, operating conditions, and interfaces that need additional testing.

-  **Combined qualitative and quantitative evidence:** ORCAS provides both numerical estimates and evidence concerning the completeness and credibility of the assessment.

-  **Iterative improvement:** Results can be updated as additional tests, defect records, and operational experience become available.

-  **Compatibility with PRA:** The resulting UCA/UIF probabilities can be incorporated into fault trees and propagated to system- and plant-level risk models.

**Conditions:** ORCAS is most appropriate for mature, configuration-controlled software under **data-rich conditions**.

**Disadvantages and Limitations:** ORCAS is data- and resource-intensive. White-box testing, requirements tracing, defect classification, and reliability-growth modeling can require extensive access to proprietary software and substantial effort from software, testing, reliability, and PRA specialists. High-quality safety software may produce very few observed defects; paradoxically, this can leave too little data to support a statistically stable SRGM.

**References**

1. Bao, H., Shorthill, T., Chen, E., et al., *An Integrated Framework for Risk Assessment of High Safety-Significant Safety-Related Digital Instrumentation and Control Systems in Nuclear Power Plants: Methodology and Demonstration*, INL/RPT-22-68656, Idaho National Laboratory, 2022.

2. Chillarege, R., Bhandari, I. S., Chaar, J. K., et al., “Orthogonal Defect Classification—A Concept for In-Process Measurements,” *IEEE Transactions on Software Engineering*, Vol. 18, No. 11, pp. 943–956, 1992.

3. International Business Machines, *Orthogonal Defect Classification, Version 5.2, for Software Design and Code*, IBM, 2013.

4. Jayakumar, A., Kuhn, D. R., Simons, B., et al., *A Pseudo-Exhaustive Software Testing Framework for Embedded Digital Devices in Nuclear Power*, National Institute of Standards and Technology, 2021.

5. Kuhn, D. R., Kacker, R. N., and Lei, Y., *Practical Combinatorial Testing*, NIST Special Publication 800-142, National Institute of Standards and Technology, 2010.

6. Goel, A. L., and Okumoto, K., “Time-Dependent Error-Detection Rate Model for Software Reliability and Other Performance Measures,” *IEEE Transactions on Reliability*, Vol. 28, No. 3, pp. 206–211, 1979.

7. Kim, M. C., Jang, S. C., and Ha, J., “Possibilities and Limitations of Applying Software Reliability Growth Models to Safety-Critical Software,” *Nuclear Engineering and Technology*, Vol. 39, No. 2, pp. 129–132, 2007.

8. Shorthill, T., Chen, E., Kim, J., et al., *An Integrated Framework for Risk Assessment of Safety-Related Digital Instrumentation and Control Systems in Nuclear Power Plants: Methodology Refinement and Exploration*, INL/RPT-24-80888, Idaho National Laboratory, 2024.

2.3 Software common cause failure modeling and estimation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** To determine whether a shared software defect, triggering condition, or dependency could cause two or more redundant digital components, divisions, or systems to fail together. This analysis is necessary because conventional reliability models often assume that redundant components fail independently. That assumption can substantially overestimate the reliability of a digital I&C system when the components use common requirements, software, algorithms, platforms, inputs, support systems, or development processes. CCF modeling partitions the estimated software failure probability into independent and dependent contributions and provides quantitative CCF basic events for fault-tree and plant risk analyses.

**Description:** The hybrid modified beta-factor approach uses a group-specific defense parameter to divide each common-cause component group (CCCG) total failure probability into independent and common-cause portions. The parameter is evaluated using factors such as information or input similarity, understanding of the software, analysis and feedback, human-machine interfaces, safety culture and training, configuration control, and testing. The resulting CCF events are inserted into the fault tree and propagated to system reliability and plant consequence models.

**Advantages:** The hybrid method can represent one component as a member of several CCCGs, allowing system-wide, division-level, rack-level, and inter-system dependencies to be evaluated. It is also usable during data-limited or early-design conditions because qualitative evidence and structured expert judgment can supplement sparse operational data. It supports comparison of redundancy and diversity alternatives, identification of risk-significant dependencies, and evaluation of whether proposed defense-in-depth measures provide meaningful risk reduction.

**Conditions for Application:**

-  A defined software failure mode, such as a UCA or UIF.

-  A total software failure probability.

-  Sufficient architecture, requirements, software-design, input, communication, maintenance, and configuration information to identify CCCGs.

-  Explicit treatment of intra-system and inter-system dependencies.

-  Documented assumptions regarding component similarity, group membership, diversity credit, and model boundaries.

**Disadvantages and Limitations:** Software CCF operating data are extremely limited, so model parameters frequently depend on qualitative scoring and expert judgment. Results can therefore be sensitive to analyst interpretation, CCCG definition, assumed diversity, and the selected defense scores. The method has not yet undergone comprehensive validation using extensive nuclear software CCF data, and multiple independent experts are recommended for scoring and review.

**References**

1. Shorthill, T., Chen, E., Kim, J., et al., *An Integrated Framework for Risk Assessment of Safety-Related Digital Instrumentation and Control Systems in Nuclear Power Plants: Methodology Refinement and Exploration*, INL/RPT-24-80888, Idaho National Laboratory, 2024.

2. Bao, H., Shorthill, T., Chen, E., et al., *An Integrated Framework for Risk Assessment of High Safety-Significant Safety-Related Digital Instrumentation and Control Systems in Nuclear Power Plants: Methodology and Demonstration*, INL/RPT-22-68656, Idaho National Laboratory, 2022.

3. Mosleh, A., Rasmuson, D., and Marshall, F., *Guidelines on Modeling Common-Cause Failures in Probabilistic Risk Assessment*, NUREG/CR-5485, U.S. Nuclear Regulatory Commission, 1998.

4. Kančev, D., and Čepin, M., “A New Method for Explicitly Modelling Single-Failure Events within Different Common-Cause-Failure Groups,” *Reliability Engineering & System Safety*, Vol. 103, pp. 84–93, 2012.

5. Humphreys, R. A., “Assigning a Numerical Value to the Beta Factor Common Cause Evaluation,” *Reliability ’87*, 1987.

6. Muhlheim, M., and Wood, R., *Technical Basis for Evaluating Software-Related Common-Cause Failures*, Oak Ridge National Laboratory, 2016.

7. International Electrotechnical Commission, *IEC 61508-6: Functional Safety of Electrical/Electronic/Programmable Electronic Safety-Related Systems—Guidelines on the Application of IEC 61508-2 and IEC 61508-3*, 2nd ed., 2010.

3. Generative AI-Assisted Software Reliability Analysis
--------------------------------------------------------

**Goal:** To assist engineers in extracting, organizing, and reasoning over the large volume of information needed to evaluate safety-critical digital instrumentation and control software. Potential applications include identifying software hazards, reconstructing system control structures, generating candidate unsafe control actions and unsafe information flows, reviewing requirements and tests, classifying defects, identifying common dependencies, and retrieving evidence for diversity and defense-in-depth assessments. GAI is best treated as an **engineering support tool**, not as a stand-alone reliability-quantification method.

**Description:** Generative AI models, particularly large language models and multimodal foundation models, generate text or structured information by learning relationships within large training datasets. Multimodal models can process both text and images, allowing them to examine software requirements, design descriptions, test records, defect reports, regulatory guidance, tables, system diagrams, and control-flow figures. For nuclear DI&C applications, a general-purpose model should be adapted using **retrieval-augmented generation (RAG), prompt engineering, prompt chaining, or fine-tuning**. RAG supplements the model with authoritative external documents without modifying the model itself.

A typical GAI-assisted reliability workflow consists of:

1. Defining the system, software function, reliability question, and required output.

2. Establishing a controlled knowledge base containing approved requirements, design, test, defect, hazard, and regulatory documents.

3. Providing a domain-specific dictionary for DI&C components, interfaces, software functions, and connection types.

4. Using the model to extract control structures, inputs, outputs, dependencies, requirements, tests, and reported defects.

5. Generating candidate UCAs, UIFs, loss scenarios, software CCFs, test cases, or evidence mappings.

6. Checking every intermediate result against the source documents and correcting the prompt, retrieved context, or system representation as necessary.

7. Transferring only reviewed and accepted results to fault trees, CCF models, or assurance-case tools.

**Advantages:**

-  **Reduced engineering effort:** GAI can rapidly search, summarize, and compare large collections of requirements, design documents, test reports, and regulatory guidance.

-  **Multimodal analysis:** It can combine information from narrative text, tables, figures, and block diagrams.

-  **Expanded hazard coverage:** The model can suggest additional UCAs, UIFs, loss scenarios, failure causes, and test conditions for expert consideration.

-  **Improved knowledge management:** RAG can connect generated conclusions to project-specific documents and support requirements-to-test, defect-to-failure, and claim-to-evidence traceability.

-  **Support for D3 and CCF reviews:** GAI can extract regulatory decision criteria and search system documentation for evidence of common or diverse software, hardware, inputs, functions, and development practices.

**Conditions:** GAI should be applied only when the analysis has a clearly defined scope and uses authoritative, configuration-controlled source information. The model version, system instructions, prompts, retrieval settings, knowledge-base contents, and generated outputs should be recorded to support reproducibility.

The knowledge base should contain sufficient DI&C-specific information because a general-purpose model may not possess accurate knowledge of the target architecture. Complex diagrams should be decomposed into smaller sections, and tables or figures may need to be supplied separately. A custom terminology dictionary and structured output template should be used to reduce ambiguity. All safety-significant outputs require independent review by qualified DI&C, software, reliability, PRA, and human-factors specialists.

**Disadvantages and Limitations:** GAI outputs are stochastic and sensitive to the wording, order, and contextual information in the prompt. Different executions may therefore produce different hazard lists or system interpretations. Models may hallucinate unsupported information, omit relevant details, combine content from unrelated document sections, or express uncertain conclusions with unjustified confidence.

**References**

1. Shorthill, T., Chen, E., Kim, J., et al., *An Integrated Framework for Risk Assessment of Safety-Related Digital Instrumentation and Control Systems in Nuclear Power Plants: Methodology Refinement and Exploration*, INL/RPT-24-80888, Idaho National Laboratory, 2024.

2. Athe, P., Bao, H., Wang, C., Chen, E., Shorthill, T. H., and Dinh, N., “Using Generative Pretrained Transformer to Perform System Theoretic Process Analysis for Digital Instrumentation and Control Systems,” *2024 ANS Winter Conference and Expo*, pp. 328–331, 2024, doi: 10.13182/T131-45945.

3. Athe, P., and Dinh, N., “Testing Generative Pre-Trained Transformer for Knowledge Abstraction and Reasoning for Nuclear Reactor Design and Safety Applications,” *Probabilistic Safety Assessment and Management 2023 Topical Conference*, 2023.

4. Qi, Y., Zhao, X., Khastgir, S., and Huang, X., “Safety Analysis in the Era of Large Language Models: A Case Study of STPA Using ChatGPT,” arXiv:2304.01246, 2023.

5. Leveson, N. G., and Thomas, J. P., *STPA Handbook*, MIT-STAMP-001, Massachusetts Institute of Technology, 2018.

6. Gao, Y., Xiong, Y., Gao, X., et al., “Retrieval-Augmented Generation for Large Language Models: A Survey,” arXiv:2312.10997, 2023.

4. Safety Assurance for DI&C
----------------------------

**Goal:** To establish and maintain justified confidence that digital I&C software is acceptably safe and reliable for its defined functions, operating conditions, mission time, and lifecycle configuration. A **safety assurance case (SAC)** makes this justification explicit by connecting safety claims to structured arguments and supporting evidence. It complements numerical software-reliability estimates by explaining why the requirements, development processes, hazard analyses, testing results, reliability models, and risk controls collectively support the conclusion that the software can be used safely.

**Description:** A software SAC can be represented using **Goal Structuring Notation (GSN)**, which organizes the assurance argument through goals, strategies, evidence or solutions, contexts, assumptions, and justifications. For nuclear DI&C software, the top-level goal is that the software is safe under specified operating conditions. This goal is first decomposed into two complementary claims: **all applicable safety requirements are satisfied**, and **the risks associated with identified hazards are sufficiently mitigated**. Each claim is then divided into functional assurance and process assurance.

**Advantages**

-  **Improved traceability:** Links safety claims to requirements, hazards, lifecycle activities, reliability estimates, and supporting evidence.

-  **Integration of diverse evidence:** Combines deterministic requirements, qualitative hazard analysis, quantitative reliability analysis, process evidence, and expert review.

-  **Balanced product and process assurance:** Evaluates both whether the software performs correctly and whether it was developed, verified, operated, and maintained through trustworthy processes.

-  **Greater transparency and reviewability:** Makes the reasoning, assumptions, limitations, and evidence gaps visible to designers, independent reviewers, and regulators.

-  **Lifecycle applicability:** Supports initial design, licensing, installation, operation, maintenance, modification, and retirement.

-  **Modularity and reuse:** Standardized decomposition strategies and hierarchical labels allow argument patterns to be reused across components and projects.

-  **Identification of evidence gaps:** Undeveloped or weakly supported claims reveal where additional testing, analysis, documentation, or risk reduction is required.

**Conditions:** Effective application requires a clearly defined system boundary, safety function, operating context, lifecycle configuration, and top-level assurance claim. Requirements and hazards must be sufficiently complete, uniquely identified, and traceable to verification evidence and risk controls. All assumptions concerning software failure probabilities, common-cause failures, model uncertainty, test representativeness, independence, and diversity should be stated explicitly.

**Disadvantages and Limitations:** Developing and maintaining a detailed SAC can require substantial effort. Large assurance cases may become difficult to navigate and can contain omissions, circular reasoning, inconsistent decomposition, or unsupported assumptions unless standardized patterns and independent reviews are used. Safety assurance is primarily an organizational and reasoning framework, not a stand-alone software-reliability quantification method. It does not independently calculate failure probabilities or prove that software is fault-free.

**References**

1. Kelly, T. P., and Weaver, R. A., “The Goal Structuring Notation: A Safety Argument Notation,” *Proceedings of the Dependable Systems and Networks Workshop on Assurance Cases*, 2004.

2. SCSC Assurance Case Working Group, *Goal Structuring Notation Community Standard, Version 3*, SCSC-141C, 2021.

3. International Atomic Energy Agency, *Dependability Assessment of Software for Safety Instrumentation and Control Systems at Nuclear Power Plants*, IAEA NP-T-3.27, 2018.

4. U.S. Nuclear Regulatory Commission, *Verification, Validation, Reviews, and Audits for Digital Computer Software Used in Safety Systems of Nuclear Power Plants*, Regulatory Guide 1.168, 2013.

5. U.S. Nuclear Regulatory Commission, *Developing Software Life-Cycle Processes for Digital Computer Software Used in Safety Systems of Nuclear Power Plants*, Regulatory Guide 1.173, 2013.

6. IEEE, *IEEE Standard for System and Software Verification and Validation*, IEEE Std 1012-2012, 2012.

7. Shorthill, T., Chen, E., Kim, J., et al., *An Integrated Framework for Risk Assessment of Safety-Related Digital Instrumentation and Control Systems in Nuclear Power Plants: Methodology Refinement and Exploration*, INL/RPT-24-80888, Idaho National Laboratory, 2024.
