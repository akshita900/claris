# CLARIS — Dataset

## 1. Dataset Selection

The initial CLARIS prototype will use the **Ventricular Tachycardia Alarm Collection (VTaC)** dataset.

VTaC was selected because it provides real ICU ventricular tachycardia alarm events together with multimodal physiological waveform data and expert alarm labels.

This makes it suitable for testing the CLARIS evidence-reconciliation concept without requiring the project to create a new alarm dataset.

---

## 2. Dataset Overview

VTaC contains:

- 5,037 ventricular tachycardia alarm events
- 1,441 true VT alarms
- 3,596 false VT alarms
- 28.61% true alarms
- at least two ECG leads
- PPG and/or ABP
- 250 Hz sampling rate
- 5 minutes of waveform data before the alarm
- 1 minute of waveform data after the alarm

The data were collected across:

- three major US hospitals
- three monitor manufacturers

The dataset contains expert annotations identifying whether the VT alarm was considered true or false.

---

## 3. Why VTaC Was Selected

VTaC is particularly appropriate for CLARIS for four reasons.

### 3.1 Real ICU Alarm Events

The dataset contains actual monitor-generated VT alarm events rather than artificially generated alarm timestamps.

### 3.2 Multimodal Waveforms

The availability of ECG together with ABP and/or PPG allows CLARIS to examine complementary physiological evidence.

### 3.3 Temporal Context

Each alarm is accompanied by waveform data before and after the alarm.

This supports event-centered analysis rather than analysis of a single isolated sample.

### 3.4 Expert Labels

The expert true/false annotations provide an external reference for evaluating the CLARIS interpretation.
## 16. Dataset Strategy

VTaC will be used as the **first benchmark dataset** for CLARIS, with ventricular tachycardia as the initial alarm family.

This does not define the overall scope of CLARIS.

CLARIS is intended as a general evidence-reconciliation framework for ICU alarms. VT is being used as the first implementation case because VTaC provides real ICU alarm events, multimodal waveforms, temporal context, and expert annotations.

Following the initial VT implementation, additional ICU alarm or physiological event families will be investigated where suitable datasets and multimodal signals are available.

The purpose of this expansion is to determine whether the CLARIS evidence-reconciliation framework generalizes beyond a single alarm type.
---

## 4. Initial CLARIS Signal Set

The first implementation will focus on:

| Signal | Role in CLARIS |
|---|---|
| ECG | Primary electrical evidence |
| ABP | Central hemodynamic evidence |
| PPG | Peripheral pulse evidence |

Not every alarm contains every signal.

CLARIS must therefore be designed to operate with incomplete multimodal information.

---

## 5. Alarm Event Definition

For the initial prototype, an alarm will be treated as an **event/episode** rather than as a single timestamp.

The available waveform surrounding the alarm will be divided conceptually into:

```text
PRE-ALARM
     ↓
ALARM EVENT
     ↓
POST-ALARM
