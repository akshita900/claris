# CLARIS — Novelty, Prior Art & Research Gap

## Purpose

The purpose of this document is to define the research gap that motivates CLARIS and to establish a defensible boundary around what the project does and does not claim as novel.

The literature review showed that most individual components considered for CLARIS already exist independently or in related combinations.

Therefore, CLARIS is not positioned as a new ECG algorithm, signal-quality algorithm, multimodal classifier, or generic explainable AI system.

The proposed research direction is an **evidence-centric alarm interpretation framework** that explicitly represents and reconciles the physiological evidence surrounding an individual ICU alarm.

---

# 1. What Already Exists

The literature reviewed during Phase 0 establishes prior work in the following areas.

## 1.1 ICU Alarm Fatigue

ICU alarm fatigue is a well-established clinical problem.

Large numbers of alarms may be:

- technically false
- clinically non-actionable
- caused by signal artifacts
- caused by inappropriate alarm settings
- repetitive or persistent

Existing research has investigated:

- alarm frequency
- false alarms
- alarm suppression
- alarm threshold optimization
- clinical consequences
- patient-specific alarm management
- computational approaches to reduce alarm burden

### CLARIS position

Alarm fatigue is the clinical motivation for CLARIS, not its technical novelty.

---

# 2. Signal Quality Assessment

## 2.1 ECG

Existing research has developed methods for:

- ECG artifact detection
- ECG signal-quality assessment
- QRS detection
- morphology analysis
- multilead consistency
- arrhythmia-specific signal-quality assessment

### CLARIS position

ECG quality assessment is established prior art.

CLARIS may use ECG signal quality as an input, but does not claim novelty for developing another ECG SQI.

---

## 2.2 ABP

Existing research has investigated:

- ABP waveform artifacts
- ABP signal-quality indices
- pulse morphology
- beat detection
- machine-learning-based artifact detection
- cross-signal ECG–ABP relationships

### CLARIS position

ABP quality assessment is established prior art.

CLARIS may use ABP quality as an input to its reasoning layer rather than treating ABP quality as the final output.

---

## 2.3 PPG / SpO₂

Existing research has investigated:

- motion artifact
- low perfusion
- sensor displacement
- pulse morphology
- PPG signal-quality assessment
- machine-learning-based PPG quality estimation
- ECG–PPG agreement

### CLARIS position

PPG signal-quality assessment is established prior art.

CLARIS does not claim novelty for PPG quality assessment itself.

---

# 3. Multimodal Alarm Validation

Existing ICU alarm research has already demonstrated that multiple physiological signals can be used together to validate alarms.

Examples include:

- ECG + ABP
- ECG + PPG
- ECG + ABP + PPG
- ECG + other physiological signals

These approaches have been used for:

- false-alarm suppression
- alarm classification
- signal-quality assessment
- physiological corroboration
- multimodal feature fusion

### CLARIS position

The use of multiple physiological signals for alarm validation is therefore not novel by itself.

The project must not be described simply as:

> "Combining ECG, ABP and PPG to detect false ICU alarms."

That would overlap substantially with existing work.

---

# 4. Cross-Signal Corroboration

Existing research has demonstrated that one physiological signal can be used to corroborate another.

For example:

```text
ECG indicates arrhythmia
        +
ABP shows corresponding pulsatile activity
        ↓
Evidence supporting the alarm
