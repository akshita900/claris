Paper 1
Title: Sentinel Event Alert 50: Medical Device Alarm Safety in Hospitals
Link: https://www.jointcommission.org/en-us/knowledge-library/newsletters/sentinel-event-alert/issue-50
Organization: The Joint Commission (2013)

Clinical Importance
Intensive Care Units (ICUs) rely on bedside physiological monitors—including ECG, arterial blood pressure (ABP), pulse oximetry (SpO₂), ventilators, infusion pumps, and telemetry—to continuously monitor patient status. These devices are essential for guiding treatment decisions; however, the overwhelming number of alarm signals generated every day has created a significant patient safety challenge known as alarm fatigue.
The Joint Commission identified alarm fatigue as a national safety concern because clinicians are frequently exposed to hundreds of alarms per patient each day, the majority of which do not require clinical intervention.

What is Alarm Fatigue?
Alarm fatigue is a state of clinical desensitization caused by repeated exposure to excessive physiological alarms, particularly those that are false or non-actionable. As clinicians become overwhelmed by continuous alarm sounds, their ability to rapidly recognize and respond to genuinely critical events decreases.
Key takeaway for CLARIS: The problem is not the existence of alarms—it is the inability to distinguish meaningful alarms from unnecessary ones.
Why Do Excessive Alarms Occur?
The Joint Commission reports that the number of alarms can reach several hundred per patient per day, resulting in thousands of alarms across a single hospital unit. Approximately 85–99% of alarm signals do not require clinical intervention.



Primary causes
Default alarm limits are not individualized for patients.
Alarm thresholds are set too tightly.
ECG electrodes become dry or detached.
Pulse oximeter sensors are poorly positioned.
Multiple devices produce similar alarm sounds, making prioritization difficult.


Actionable vs Non-Actionable Alarms
Actionable Alarm
Non-Actionable Alarm
Indicates a physiological change requiring clinical intervention
Does not require intervention despite triggering an alarm
Reflects a genuine deterioration in patient condition
Often caused by artifact, poor sensor placement, or inappropriate alarm settings
Should prompt immediate assessment
Contributes to alarm fatigue and cognitive overload

Clinical interpretation: Non-actionable does not necessarily mean false; it means the alarm does not require immediate therapeutic action. This distinction is fundamental to CLARIS.
How Does Alarm Fatigue Affect Patient Safety?
The Joint Commission documented 98 reported alarm-related sentinel events between 2009 and 2012:
Outcome
Reported Events
Death
80
Permanent loss of function
13
Unexpected additional care / extended stay
5

These events were predominantly reported from telemetry, intensive care, emergency departments, and general medicine units. The report also notes that alarm-related events are underreported, meaning the true burden is likely greater.
Why this happens
Continuous exposure to non-actionable alarms leads to:
Desensitization to alarm sounds
Increased cognitive workload
Delayed recognition of genuine emergencies
Unsafe practices such as lowering alarm volume, disabling alarms, or widening alarm limits beyond safe ranges


Major Contributing Factors
The Joint Commission identified the following contributors to alarm-related events:
Alarm fatigue (most common contributing factor)
Improper or non-individualized alarm settings
Alarm signals turned off inappropriately
Inaudible alarms in certain care areas
Inadequate staff training
Poor integration between medical devices
Equipment malfunction and maintenance issues
These findings demonstrate that alarm safety is both a technical and workflow problem.
Joint Commission Recommendations
Rather than eliminating alarms, the report recommends improving alarm management through organizational and clinical processes:
Establish safe alarm management policies.
Create an inventory of alarm-equipped medical devices.
Develop standardized alarm-setting guidelines for high-risk areas.
Tailor alarm limits to individual patients whenever appropriate.
Maintain and regularly inspect monitoring equipment.
Train all clinical staff in alarm response.
Continuously review alarm trends using multidisciplinary teams.
 SEA_50_alarms_4_26_16.pdf
The emphasis is on better interpretation and management, not increasing the number of alarms.
Design Implications for CLARIS
This paper directly justifies the existence of CLARIS.
CLARIS supports clinicians—it does not replace them. This aligns with the Joint Commission's recommendation that alarm safety should enhance clinical workflow rather than automate decision-making.
 SEA_50_alarms_4_26_16.pdf
Credibility assessment is more valuable than generating another notification. The clinical problem is excessive alarms, not insufficient alarms.
Multimodal evidence (ECG + ABP + SpO₂) provides a stronger physiological basis for evaluating whether an alarm reflects a genuine patient event or sensor-related artifact.
Synchronized playback mirrors real clinical verification. Clinicians naturally review multiple waveforms to understand what happened before an alarm; CLARIS reconstructs that process digitally.
Patient-specific interpretation is consistent with individualized alarm management. Rather than predicting disease, CLARIS uses the patient's existing clinical context to interpret alarm credibility.
Research Gap Identified
Current bedside monitoring systems are highly effective at detecting physiological threshold violations, but they provide limited support in explaining whether an alarm is physiologically trustworthy. The Joint Commission recommends individualized alarm management and improved clinical processes, yet it does not propose an explainable multimodal credibility engine.
CLARIS addresses this gap by reconstructing the physiological context surrounding an ICU alarm and producing an evidence-based credibility assessment instead of another alarm.
Design Justification for CLARIS (derived from Sentinel Event Alert 50)
Joint Commission recommendation
How CLARIS aligns
Tailor alarm settings for individual patients
CLARIS incorporates the patient's existing clinical context when evaluating alarm credibility rather than treating every patient identically.


Identify situations where alarms are not clinically necessary
CLARIS does not suppress alarms; it distinguishes clinically supported alarms from potentially non-actionable or artifact-driven events through multimodal evidence.


Safe alarm management in high-risk areas
CLARIS is designed specifically for ICU physiological monitoring, supporting safer alarm interpretation in high-acuity environments.


Maintain accurate alarm-equipped devices
CLARIS evaluates waveform quality (ECG, ABP, SpO₂), making sensor integrity and signal reliability part of the credibility assessment rather than relying solely on numerical thresholds.


Individualized alarm limits
The paper emphasizes patient-specific monitoring; CLARIS extends this by providing contextual reasoning instead of a universal interpretation of alarms.




Reference
The Joint Commission. Sentinel Event Alert 50: Medical Device Alarm Safety in Hospitals. Issue 50, April 8, 2013.









Paper 2
A systematic review with evidence mapping of alarm management interventions in intensive care units
link : https://www.sciencedirect.com/science/article/abs/pii/S0964339726000601
Authors: Yaoyao Ding, Meng Zhang, Meng Zhou, Xiaojing Guo, Yuchen Zhang, Huimin Pang, Qingyan Guan & Yubiao Gai
Journal: Intensive and Critical Care Nursing (2026)
Study Type: Systematic Review with Evidence Mapping

Clinical Importance
This systematic review evaluates the current evidence on alarm management interventions in Intensive Care Units (ICUs). Rather than investigating a single intervention, the authors mapped published ICU studies to identify which strategies reduce alarm burden, improve nursing workflow, and enhance patient safety. The review also highlights methodological limitations and identifies research gaps that should guide future alarm management research.

Objective
To systematically map and characterize the available evidence on ICU alarm management interventions and provide guidance for future research and clinical practice.
Methodology
Parameter
Finding
Study period
2014–2024
Total studies reviewed
18
Randomized controlled trials
2
Quasi-experimental studies
16
Analysis method
Evidence Mapping
Quality assessment
ROBINS-I & Risk of Bias 2


Key Findings
ICUs generate approximately 100–350 alarms per bed per day.
85–99% of physiological alarms are nuisance or false-positive alarms.
Alarm fatigue contributes to delayed responses and increases the likelihood of adverse patient events.
Training clinicians and customizing alarm settings were identified as the most effective interventions for reducing alarm burden.
Although alarm management interventions showed positive outcomes, the overall evidence base was judged to have moderate-to-high risk of bias, indicating the need for stronger future research.
 

Existing Alarm Management Interventions
Intervention
Primary Purpose
Nurse training
Improve alarm response behaviour
Customized alarm settings
Reduce nuisance alarms
Technical support
Improve alarm management
Workflow interventions
Enhance clinical response
Equipment optimization
Improve monitoring reliability
Organizational protocols
Standardize alarm practices
Alarm management programs
Reduce overall alarm burden


Design Implications for CLARIS
The findings of this review directly support the design philosophy of CLARIS.
Existing interventions primarily aim to:
Reduce the number of alarms.
Improve clinician response through education.
Optimize alarm thresholds and hospital workflows.
CLARIS addresses a complementary problem.
Rather than modifying alarm limits or suppressing alarms, CLARIS evaluates the credibility of an individual physiological alarm by reconstructing synchronized ECG, ABP, and SpO₂ waveforms within the patient's existing clinical context. This provides clinicians with an explainable assessment of whether an alarm is physiologically supported.
Research Gap
Current ICU alarm management research predominantly focuses on alarm reduction, threshold customization, and workflow optimization. Limited emphasis is placed on explainable multimodal credibility assessment, where synchronized physiological waveforms are used to determine the trustworthiness of an individual alarm. This gap forms the scientific foundation of CLARIS.
Reference
Ding Y, Zhang M, Zhou M, et al. A systematic review with evidence mapping of alarm management interventions in intensive care units. Intensive and Critical Care Nursing. 2026



Paper 3
Alarm fatigue among critical care unit and emergency room nurses: A multicentre cross-sectional study in Iran
Link: https://pmc.ncbi.nlm.nih.gov/articles/PMC13052555/
Study Type: Multicentre Cross-sectional Study
Clinical Importance
This multicentre study investigates the prevalence and severity of alarm fatigue among nurses working in Intensive Care Units (ICUs), Coronary Care Units (CCUs), and Emergency Rooms (ERs). Unlike technical alarm-management studies, it focuses on the psychological and behavioural impact of excessive physiological alarms on frontline healthcare professionals.
The study demonstrates that alarm fatigue is not only a technological issue but also a significant contributor to clinician workload and patient safety.
Study Overview
Parameter
Finding
Study design
Multicentre cross-sectional study
Hospitals included
6 teaching hospitals
Participants
260 nurses
Clinical areas
ICU, CCU & ER
Assessment tool
Nurses' Alarm Fatigue Questionnaire (NAFQ)

Key Findings
Prevalence of Alarm Fatigue
The mean alarm fatigue score was 26.38 ± 7.94, indicating an overall moderate level of alarm fatigue among participating nurses.
Severity
Percentage
No fatigue
9.6%
Mild
21.5%
Moderate
31.5%
Severe
26.9%
Very severe
10.5%

Major Sources of Alarms
The devices contributing most frequently to alarm exposure were:
Patient monitors (25.2%)
Syringe pumps (20.1%)
Ventilators (18.7%)
These findings suggest that physiological monitoring devices are the primary contributors to alarm burden in critical care settings.
Psychological & Behavioural Impact
The study reported that repeated alarm exposure resulted in:
Increased stress and irritability
Greater sensitivity to alarms during periods of emotional strain
Reduced attention caused by continuous alarm sounds
Occasional silencing or deactivation of alarms by some nurses
These behaviours illustrate how alarm fatigue can directly influence clinical workflow and patient safety.
Factors Associated with Alarm Fatigue
The study identified two significant associations:
Rotational shift work was associated with higher alarm fatigue.
Higher income was associated with lower alarm fatigue.
No significant relationship was found between alarm fatigue and age, gender, work experience, clinical unit, or overtime hours.
Design Implications for CLARIS
This study validates the human-centred purpose of CLARIS.
The primary users of CLARIS are ICU and emergency clinicians experiencing moderate-to-high alarm burden.
CLARIS should reduce cognitive decision burden, not replace clinical judgement.
Explainable waveform playback aligns with the way clinicians verify alarms before acting.
Evaluating alarm credibility may reduce unnecessary cognitive load without suppressing existing alarms.
Contribution to the Research Gap
This study demonstrates that alarm fatigue is prevalent among critical care nurses and is associated with behavioural changes that may compromise patient safety. However, it does not propose a system capable of explaining the physiological credibility of individual alarms.
CLARIS addresses this unmet need by combining synchronized ECG, ABP, and SpO₂ waveforms with patient clinical context to provide an explainable alarm credibility assessment.










 Paper 4
Computational approaches to alleviate alarm fatigue in intensive care medicine: A systematic literature review
Link: https://www.frontiersin.org/journals/digital-health/articles/10.3389/fdgth.2022.843747/full#h1
Study Type: PRISMA Systematic Literature Review
Domain: Intensive Care Medicine · Computational Alarm Management
Publications Reviewed: 69 peer-reviewed studies
Research Questions
What IT-based approaches have been developed to improve alarm management in intensive care medicine?
How do these computational systems contribute to reducing alarm fatigue?
 Pasted markdown.md
Clinical Importance
Modern Intensive Care Units rely on continuous physiological monitoring using ECG, arterial blood pressure (ABP), pulse oximetry (SpO₂), respiratory monitoring, and other bedside sensors. These systems improve patient safety by generating alarms whenever physiological parameters exceed predefined thresholds. However, the review highlights that 72–99% of ICU alarms are either technically false or clinically irrelevant, creating an overwhelming alarm burden that contributes to clinician desensitization, delayed responses, and patient harm.
Pasted markdown.md
Unlike previous literature focusing on organizational policies, this review investigates computational and engineering solutions, making it directly relevant to the development of CLARIS.
Study Objectives
The authors conducted a PRISMA-based systematic review to identify, categorize, and evaluate computational approaches designed to alleviate alarm fatigue in intensive care medicine. Rather than measuring alarm fatigue itself, the review examines how information technology, machine learning, signal processing, and novel alarm presentation systems have attempted to improve alarm management.
Pasted markdown.md
Methodology
Parameter
Finding
Review framework
PRISMA
Records identified
184
Records after screening
69
Literature databases
PubMed, IEEE Xplore, ACM, Web of Science, arXiv
Study focus
Computational alarm management in ICUs
Time restriction
None

The review excluded non-English, non-peer-reviewed, and non-ICU publications while retaining only implemented IT-based alarm management solutions.
Pasted markdown.md
Understanding ICU Alarm Fatigue
The paper introduces an important distinction that becomes central to CLARIS.
Types of Physiological Alarms
Alarm Type
Definition
Technically false
Alarm caused by artefacts, poor signal quality, or sensor malfunction
Technically true but clinically irrelevant
Physiological change exists but does not require intervention
Technically true and clinically actionable
Requires immediate clinical assessment or treatment

The authors argue that existing ICU systems perform reasonably well at detecting threshold violations but struggle to determine clinical relevance, resulting in large numbers of unnecessary alarms.
Pasted markdown.md
CLARIS Insight: This distinction becomes the conceptual basis of Alarm Credibility.
Existing Computational Approaches
The review identifies three major engineering strategies used to combat alarm fatigue.
1. Reduction of Technically False Alarms
The largest body of research focuses on eliminating alarms caused by signal artefacts and poor waveform quality.
Typical methods include:
ECG signal quality assessment
ABP waveform validation
Motion artefact detection
Signal Quality Indices (SQIs)
Machine learning classifiers
Limitation
These systems determine whether the signal is technically correct—not whether the alarm is clinically meaningful.
Pasted markdown.md
2. Per-Patient Risk Assessment
A smaller group of studies predicts patient deterioration before critical events occur.
Examples include prediction of:
Acute hypotension
Sustained hypotension
Cardiac arrest
Mortality
ICU deterioration
Limitation
These systems prioritize patients rather than evaluate the credibility of the alarm itself. CLARIS intentionally avoids becoming a disease prediction platform.
Pasted markdown.md
3. Novel Alarm Presentation
Several publications redesigned how alarms reach clinicians instead of changing the alarms themselves.
Examples include:
Vibrotactile wearable devices
Head-mounted displays
Smartphone notification systems
Adaptive alarm loudness
Personalized alarm routing
Limitation
These approaches reduce acoustic burden but do not explain why an alarm occurred.
Pasted markdown.md
Physiological Signals Most Studied
One of the strongest validations for CLARIS appears here.
Among 69 publications, the dominant physiological modalities were:
Physiological Signal
Number of Studies
ECG / Heart Rate / Arrhythmia
51
Arterial Blood Pressure (ABP)
15
Oxygen Saturation (SpO₂)
12
Respiratory Monitoring
7
Intracranial Pressure
4
Central Venous Pressure
3

Interpretation
The literature consistently identifies ECG, ABP, and SpO₂ as the primary physiological signals involved in ICU alarm research, validating CLARIS's multimodal architecture.
Pasted markdown.md
Datasets Used in Alarm Fatigue Research
The review reveals an important trend in computational research.
Most frequently used datasets
Dataset
Purpose
MIMIC-II
ICU physiological monitoring
PhysioNet
Public waveform repository
PhysioNet/CinC 2015
False arrhythmia alarm detection
Custom hospital datasets
Institution-specific studies

The authors also note that newer databases such as MIMIC-III, HiRID, and eICU were surprisingly underutilized, highlighting opportunities for future research.
Pasted markdown.md
Design implication: CLARIS should be built upon validated public ICU waveform datasets before pursuing prospective clinical data.
Computational Models Identified
The review compared the algorithms used across studies.
Model Category
Observation
Decision Trees
Frequently used
Random Forests
Highly common
Gradient Boosting
Popular
Support Vector Machines
Widely used
Logistic Regression
Explainable baseline
Neural Networks / LSTM
Less common

The authors conclude that explainable models dominate alarm fatigue research, largely because clinicians require transparent reasoning rather than black-box predictions.
Pasted markdown.md
CLARIS Principle: Explainability is a design requirement, not a feature.
Signal Quality Indicators (SQIs)
A major subsection of the review discusses Signal Quality Indicators.
SQIs evaluate whether a physiological waveform is reliable before interpreting it.
Common SQI applications
Waveform
Purpose
ECG
Beat detection & noise assessment
ABP
Pulse morphology validation
PPG / SpO₂
Motion artefact identification

Rather than relying solely on threshold values, SQIs assess waveform integrity, reducing technically false alarms.
Pasted markdown.md
Relevance to CLARIS
CLARIS can incorporate waveform quality assessment as one component of its credibility engine before contextual interpretation.
Human–Computer Interaction Findings
Interestingly, only 8 of the 69 studies included user studies involving healthcare professionals, and most involved 9–15 participants.
This indicates that many alarm-management technologies remain proof-of-concept rather than clinically integrated systems.
Pasted markdown.md
Implication
CLARIS should prioritize clinician usability alongside algorithmic performance.
Critical Research Gaps Identified
This is the single most important section of the paper.
The authors explicitly state that future research should focus less on what is technically easy and more on clinical needs.
Gaps identified by the review
Lack of systems classifying alarms as clinically actionable vs non-actionable
Few methods evaluating clinical relevance rather than technical correctness
Limited availability of labelled actionable-alarm datasets
Absence of intelligent systems for learning patient-specific alarm thresholds
Need for larger validated ICU alarm databases
 Pasted markdown.md
These statements form the strongest academic justification for CLARIS.
Design Implications for CLARIS
This review directly influences the system architecture.
Evidence from Literature
CLARIS Decision
72–99% alarms are false or irrelevant
Focus on credibility assessment
ECG, ABP & SpO₂ dominate ICU research
Use these as primary modalities
Explainable models preferred
Transparent reasoning over black-box AI
SQIs improve technical validity
Evaluate waveform quality before interpretation
Clinical relevance is underexplored
Distinguish actionable vs non-actionable alarms
User studies are limited
Design for real clinician workflow

Research Gap
Existing computational alarm-management systems predominantly evaluate technical correctness, predict patient deterioration, or redesign alarm delivery. Very few systems assess whether an individual physiological alarm is clinically credible using synchronized multimodal evidence. Furthermore, the review identifies a significant lack of datasets containing clinically labelled actionable and non-actionable alarms, making this an important direction for future research.
Pasted markdown.md
CLARIS addresses this gap by reconstructing synchronized ECG, ABP, and SpO₂ waveforms within the patient's existing clinical context to generate an explainable alarm credibility assessment rather than another alarm.
Key Contributions to CLARIS
Validated physiological foundation
The literature independently identifies ECG, ABP, and SpO₂ as the three dominant modalities in ICU alarm research.
Established engineering gap
Current computational systems mainly reduce technically false alarms; clinical credibility remains comparatively underexplored.
Justified explainability
Transparent models and interpretable reasoning are consistently favored over black-box approaches in critical care.
Supported CLARIS architecture
Multimodal waveform reconstruction, signal quality evaluation, contextual interpretation, and clinician-centered workflow are all supported by findings from this review.






