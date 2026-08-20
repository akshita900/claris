Literature Synthesis
Phase 1 · Clinical Foundation of CLARIS
Overview
A literature review of four foundational studies was conducted to understand alarm fatigue from clinical, organizational, human, and computational perspectives. Collectively, the evidence demonstrates that alarm fatigue is not simply caused by excessive alarms, but by the inability of current monitoring systems to distinguish physiologically meaningful alarms from technically false or clinically non-actionable events.
The reviewed literature consistently supports three conclusions:
Alarm fatigue is a documented patient safety problem.
Existing interventions primarily reduce alarm burden rather than explain alarm credibility.
Explainable multimodal assessment remains an important research opportunity for ICU decision support.

Theme 1: Alarm fatigue is a documented patient safety problem
The Joint Commission first established alarm fatigue as a national patient safety concern after documenting alarm-related sentinel events in intensive care environments. Continuous physiological monitoring generates hundreds of alarms per patient each day, yet the overwhelming majority do not require immediate clinical intervention. This excessive exposure contributes to clinician desensitization, delayed responses, and increased risk of adverse patient outcomes.
Supporting evidence
Hundreds of physiological alarms may occur per ICU patient each day.
Approximately 85–99% of alarms are false or non-actionable.
Alarm fatigue is associated with delayed recognition of genuinely critical events.
Safe alarm management requires individualized monitoring rather than universal thresholds.
Implication for CLARIS: The problem is not insufficient monitoring; it is insufficient interpretation of alarm credibility.
Theme 2: Alarm fatigue is a human and cognitive burden
The multicentre Iranian study shifts the discussion from technology to clinicians. Across 260 ICU, CCU, and ER nurses, alarm fatigue was observed at predominantly moderate-to-severe levels, demonstrating that continuous alarm exposure directly affects cognitive workload and clinical behaviour.
Human factors identified
Increased stress and irritability during alarm exposure.
Reduced attention caused by repetitive non-actionable alarms.
Occasional silencing or deactivation of alarms.
Rotational shift work increased alarm fatigue.
These findings establish ICU nurses as the primary end users of CLARIS and reinforce the need for systems that reduce decision burden rather than generate additional notifications.
Theme 3: Existing alarm management focuses on reducing alarm burden
The evidence-mapping systematic review analyzed 18 intervention studies published between 2014 and 2024. The review found that the most effective strategies were clinician training and customized alarm settings, while workflow optimization and organizational protocols further improved alarm management.
Current intervention strategies

Strategy
Primary objective
Nurse training
Improve alarm response
Customized alarm limits
Reduce nuisance alarms
Technical support
Improve device management
Workflow protocols
Standardize clinical practice
Equipment optimization
Improve monitoring reliability


Although these interventions successfully reduce overall alarm burden, they do not evaluate whether an individual alarm is physiologically trustworthy.
Implication for CLARIS: CLARIS complements existing alarm management instead of replacing it.
Theme 4: Computational research prioritizes technical correctness
The computational systematic review examined 69 engineering studies investigating IT-based solutions for ICU alarm fatigue. Most computational systems were designed to detect technically false alarms, assess signal quality, predict patient deterioration, or redesign alarm presentation.
Dominant computational directions
Computational approach
Purpose
Signal quality assessment
Remove technically false alarms
Machine learning classifiers
Improve false alarm detection
Patient deterioration models
Predict critical events
Novel alarm presentation
Reduce acoustic burden


The review also demonstrated that ECG, ABP, and SpO₂ are the three most extensively studied physiological signals in ICU alarm research, validating the multimodal foundation of CLARIS.
Pasted markdown.md
Engineering insight
Current systems determine whether an alarm is technically correct far more often than whether it is clinically meaningful.
Integrated Findings
Across all four papers, a consistent pattern emerges.

Evidence
Collective conclusion
Clinical literature
Alarm fatigue is a patient safety issue
Human factors
Nurses experience measurable cognitive burden
Organizational research
Training and customization reduce alarm burden
Computational research
Engineering focuses mainly on false alarm reduction


No reviewed paper proposes an explainable system that reconstructs synchronized ECG, ABP, and SpO₂ evidence to evaluate the credibility of an individual ICU alarm within the patient's clinical context.
Pasted markdown.md
Scientific Foundation of CLARIS
The literature collectively supports the design philosophy of CLARIS:
Support clinicians, not replace them.
Evaluate alarm credibility rather than disease prediction.
Use synchronized ECG, ABP, and SpO₂ as multimodal evidence.
Incorporate patient clinical context instead of universal interpretation.
Provide explainable playback that mirrors real ICU verification workflow.
Rather than functioning as another alarm-generation system, CLARIS is positioned as an Explainable Clinical Decision Support System that assists clinicians in determining whether an ICU physiological alarm is genuinely supported by multimodal physiological evidence.
Research Gap
Despite significant advances in alarm management, existing literature predominantly addresses alarm reduction, threshold customization, signal quality, and workflow optimization. Comparatively limited emphasis is placed on explainable multimodal credibility assessment, where synchronized physiological waveforms and patient clinical context are used to determine whether an individual alarm is clinically trustworthy.
CLARIS is proposed to address this gap by reconstructing the physiological context surrounding an ICU alarm and generating an evidence-based credibility assessment while preserving clinician authority and existing bedside monitoring systems.
Conclusion — ICU Alarm Fatigue
The four reviewed studies collectively establish ICU alarm fatigue as a well-documented clinical, human, and engineering challenge. Evidence consistently demonstrates that intensive care environments generate a high volume of physiological alarms, the majority of which are false or non-actionable, resulting in increased cognitive workload, clinician desensitization, and potential threats to patient safety. Existing alarm management strategies—including clinician training, customized alarm settings, workflow optimization, and computational false-alarm reduction—have significantly improved alarm burden but remain primarily focused on reducing alarm frequency rather than explaining alarm credibility.
From this literature, a clear design direction emerges: the next generation of ICU decision-support systems should not replace bedside monitors or suppress alarms, but provide clinicians with explainable, evidence-based interpretation of physiological alarm events. This conclusion forms the scientific foundation for CLARIS, whose objective is to evaluate the credibility of ICU alarms through synchronized ECG, arterial blood pressure (ABP), and SpO₂ waveforms within the patient's existing clinical context.

