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
