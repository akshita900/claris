# CLARIS — System Architecture

## 1. System Objective

CLARIS is an evidence-centric framework for interpreting ICU monitor alarms.

The system does not aim to replace the ICU monitor or generate the initial alarm.

Instead, CLARIS receives an already-generated alarm and reconstructs the physiological evidence surrounding that event.

The core question is:

> When an ICU monitor raises an alarm, does the surrounding physiological evidence support the alarm, contradict it, or fail to provide enough evidence to determine its credibility?

---

## 2. Core Design Principle

CLARIS separates three different questions:

### Question 1 — Is the signal reliable?

This is the signal-quality question.

### Question 2 — What physiological event does the signal indicate?

This is the physiological interpretation question.

### Question 3 — What does the combined evidence imply about the alarm?

This is the evidence-reconciliation question.

Therefore:

```text
Signal Quality
      +
Physiological Evidence
      +
Temporal Relationship
      ↓
Evidence Reconciliation

                    ICU MONITOR
                         ↓
                    ALARM EVENT
                         ↓
              EVENT-CENTERED WINDOW
                  PRE / DURING / POST
                         ↓
              ┌──────────┼──────────┐
              ↓          ↓          ↓
             ECG        ABP        PPG
              ↓          ↓          ↓
        Signal Quality Assessment
              ↓          ↓          ↓
        Physiological Evidence Extraction
              ↓          ↓          ↓
              └──────────┼──────────┘
                         ↓
                TEMPORAL ALIGNMENT
                         ↓
              EVIDENCE RECONCILIATION
                         ↓
          ┌──────────────┼──────────────┐
          ↓              ↓              ↓
      SUPPORTS       CONTRADICTS    INSUFFICIENT
          └──────────────┼──────────────┘
                         ↓
                  EVIDENCE PROFILE
                         ↓
                  ALARM CREDIBILITY
                         ↓
                HUMAN-READABLE
                   EXPLANATION
alarm event: 
                         ALARM
                           ↓
───────────────|───────────|───────────|───────────────
               PRE        EVENT        POST

evidence profile: 
Alarm Event
    ↓
Signal Evidence
    ├── ECG
    │    ├── Reliability
    │    ├── Physiological evidence
    │    └── Relationship
    │
    ├── ABP
    │    ├── Reliability
    │    ├── Physiological evidence
    │    └── Relationship
    │
    └── PPG
         ├── Reliability
         ├── Physiological evidence
         └── Relationship
VT Alarm — Contradicted

The ECG signal was of high quality and showed a rapid
ventricular rhythm. However, the ABP signal was also of
high quality and did not show a corresponding pulsatile
response. The PPG signal was of insufficient quality for
additional confirmation.

The available multimodal evidence therefore contradicts
the alarm interpretation.
