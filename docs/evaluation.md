# CLARIS — Evaluation Plan

## 1. Evaluation Objective

The purpose of the CLARIS evaluation is to determine whether the proposed evidence-reconciliation framework can reliably interpret ICU alarm events using multimodal physiological waveform evidence.

The evaluation will not only measure whether CLARIS agrees with the reference alarm label.

It will also examine whether:

- signal quality assessment is reliable
- physiological evidence is correctly extracted
- multimodal evidence is correctly reconciled
- missing and unreliable signals are handled appropriately
- explanations accurately reflect the underlying evidence
- the framework provides useful information beyond a binary alarm classification

---

# 2. Initial Evaluation Dataset

The first evaluation will use the VTaC dataset with ventricular tachycardia alarms.

VTaC provides:

- real ICU VT alarm events
- multimodal physiological waveforms
- temporal context surrounding the alarm
- expert true/false annotations

VTaC will therefore provide the initial reference dataset for evaluating the CLARIS framework.

The use of VTaC as the first dataset does not restrict CLARIS to VT alarms permanently.

Future alarm families may be evaluated separately to test generalization.

---

# 3. Evaluation Levels

CLARIS will be evaluated at multiple levels.

```text
Level 1
Signal Quality
      ↓
Level 2
Physiological Evidence
      ↓
Level 3
Evidence Reconciliation
      ↓
Level 4
Alarm Credibility
      ↓
Level 5
Explanation
