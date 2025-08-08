# Class-Companion

Class-Companion is an open-source project designed to simplify classroom management tasks such as student attendance, image-based identification, and reminders. Built with Python, it provides tools for automating and tracking essential classroom activities.

## Features

- **Automated Attendance:** Scripts for marking student attendance efficiently, including support for both manual and image-based methods.
- **Student Details Management:** Utilities for handling student information.
- **Image Recognition:** Tools for taking and training student images, leveraging Haar cascade classifiers for facial recognition.
- **Reminders:** JSON-based reminder system to help instructors keep track of important tasks.
- **Voice Support:** Basic voice assistance capabilities through `ccvoice.py`.

## Directory Overview

- `Attendance/`, `maths/`: Folders related to attendance recording and potentially math utilities.
- `StudentDetails/`: Handles student-specific data.
- `TrainingImage/`, `TrainingImageLabel/`: For storing raw and labeled training images.
- `UI_Image/`: User interface images.
- `attendance.py`, `automaticAttedance.py`, `show_attendance.py`: Scripts managing manual and automated attendance processes.
- `takeImage.py`, `trainImage.py`: Scripts for capturing and training student facial images.
- `haarcascade_frontalface_alt.xml`, `haarcascade_frontalface_default.xml`: Haar cascade XML files used for face detection.
- `reminders.json`: Stores reminder data.
- `ccvoice.py`: Provides voice command capabilities.
- `summarizer.py`: Possible text summarization utility.

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/Sagewiiz/Class-Companion.git
cd Class-Companion
