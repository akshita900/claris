# Problem Statement — Claris

## Background

Intensive Care Units (ICUs) rely on continuous physiological monitoring using electrocardiography (ECG), arterial blood pressure (ABP), and pulse oximetry (SpO₂). These monitors generate alarms whenever predefined thresholds or rhythm abnormalities are detected.

## The Clinical Problem

A substantial proportion of ICU alarms are non-actionable because they are triggered by signal artifacts, poor signal quality, patient movement, or transient physiological changes. The resulting excessive alarm burden contributes to alarm fatigue, making it more difficult for clinicians to rapidly identify genuinely critical events.

## Gap

Current bedside monitors primarily indicate that an alarm has occurred but provide limited explanation of the physiological context surrounding that event. Clinicians often interpret multiple waveforms simultaneously to determine whether an alarm reflects true deterioration or unreliable signal acquisition.

## Proposed Direction

Claris is an explainable multimodal alarm playback system that reconstructs the physiological context surrounding an ICU alarm using ECG, ABP, and SpO₂ waveforms. Rather than replacing bedside monitors, it aims to provide evidence-based contextual reasoning that helps distinguish physiologically supported alarms from artifact-driven or low-confidence events.

## Scope (Phase 0)

- Physiological signals: ECG, ABP, SpO₂
- Focus: ICU alarm interpretation
- Objective: Explain alarms, not diagnose disease
