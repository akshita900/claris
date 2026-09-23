CLARIS
Clinical Alarm Reconstruction & Interpretability System
Research Question
Can multimodal physiological waveforms and patient clinical context improve the credibility assessment of ICU physiological alarms through explainable contextual reconstruction?
Goal
Validate the clinical problem, understand ICU physiology, and establish the scientific foundation for CLARIS as an explainable clinical decision support system for ICU alarm credibility assessment.
Vision
Develop an explainable ICU alarm credibility engine that assists clinicians in distinguishing physiologically supported alarms from artifact-driven or non-actionable events without replacing existing bedside monitoring.
Core Concepts
Alarm Credibility
Alarm credibility is the degree to which an ICU physiological alarm is supported by synchronized evidence across ECG, arterial blood pressure (ABP), and SpO₂ waveforms within the patient's clinical context. It represents the trustworthiness of an alarm, not the severity of the patient's condition.
Patient Clinical Context
Patient clinical context refers to the patient's existing diagnosis, physiological baseline, ICU specialty, and monitoring profile. CLARIS uses this information to interpret alarm credibility—it does not infer or predict disease.
Project Foundation
Q: What is CLARIS?
A: CLARIS (Clinical Alarm Reconstruction & Interpretability System) is an explainable clinical decision support system that evaluates the credibility of physiological ICU alarms. By reconstructing synchronized ECG, arterial blood pressure (ABP), and SpO₂ waveforms surrounding an alarm event, CLARIS provides clinicians with evidence-based contextual reasoning and synchronized playback for clinical review.
Q: What problem does CLARIS solve?
A: CLARIS addresses one of the major contributors to ICU alarm fatigue: the high volume of non-actionable and potentially artifact-driven physiological alarms. Rather than suppressing alarms, it assists clinicians in determining whether an alarm is physiologically credible through multimodal waveform evidence and contextual reconstruction.
CLARIS is designed to support clinician judgment and does not replace bedside monitors, existing alarm systems, or clinical decision-making.
Q: Why is alarm fatigue dangerous?
A: Alarm fatigue occurs when clinicians are exposed to an excessive number of physiological alarms, many of which are false or non-actionable. Continuous exposure increases cognitive workload, contributes to desensitization, and may delay recognition of genuinely critical events. It is therefore recognized as a significant patient safety challenge in intensive care environments.
Q: Why is CLARIS different from disease prediction?
A: CLARIS does not diagnose diseases or predict patient conditions. It assumes the patient's clinical context is already known and focuses exclusively on evaluating the credibility of ICU monitor alarms. Its objective is to explain why an alarm occurred, whether it is supported by multimodal physiological evidence, and provide synchronized playback of the event for clinical interpretation.
Q: Why is playback clinically valuable?
A: ICU clinicians rarely rely on a single numerical value when verifying alarms. Instead, they examine multiple physiological waveforms simultaneously to understand the sequence of events preceding an alarm. CLARIS reconstructs a synchronized 30-second physiological window, enabling playback of ECG, ABP, and SpO₂ waveforms so clinicians can investigate the evidence supporting or contradicting the alarm.
Scope of CLARIS (Version 1)
Inputs
ECG waveform
Arterial Blood Pressure (ABP) waveform
SpO₂ and plethysmographic waveform
Patient clinical context (existing diagnosis and baseline)
Output
Alarm credibility assessment
Evidence-based contextual explanation
Synchronized waveform playback
Clinician decision support
CLARIS does not:
Predict diseases
Replace ICU monitors
Suppress or override clinical alarms
Make autonomous clinical decisions
Phase 0 Outcome
By the end of Phase 0, CLARIS should have a scientifically validated foundation demonstrating:
Why ICU alarm fatigue remains a critical clinical problem.
How ECG, ABP, and SpO₂ contribute to alarm interpretation.
Why multimodal contextual reconstruction is clinically valuable.
How patient clinical context influences alarm credibility.
The research gap that CLARIS is designed to address.

