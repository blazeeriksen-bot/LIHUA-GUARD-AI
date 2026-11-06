# 🌸 LIHUA GUARD AI #

Version: 0.2

AI Security Assistant System.

# Current Development #

- Core Architecture
- AI Vision System
- Face Recognition
- Threat Detection
- Voice Response

# Status #

Development Phase

# Version History #

# v0.2 Core Security Foundation #
Status: Stable ✅

Features:
- Core System
- Threat Score
- Decision Engine
- Security Logger
- Alert System

Test Result:
System running successfully.
## v0.3 - Context-Aware Threat Analysis

LIHUA now adds a first context layer before a dangerous-object detection can contribute to threat scoring.

Context evidence includes:
- dangerous object + nearby tracked person
- normalized spatial relation to the person bounding box
- tracked object movement
- whether the object is approaching the person
- persistence across multiple frames

A stationary isolated knife/bat does not contribute a threat score in this context layer. This is an initial prototype; thresholds are frame/pixel based and should be calibrated with real camera data before production use.
