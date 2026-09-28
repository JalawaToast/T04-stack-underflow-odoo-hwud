# AI Speech Therapy

An AI-assisted speech therapy application built with **Odoo 19** to help children practice pronunciation and allow therapists to monitor their speech-therapy sessions.

The application combines an Odoo-based management system with a **local, self-hosted pronunciation analysis service**. Speech recordings can be analyzed locally and the results are stored in Odoo for review.

> **Hackathon Project — T04 Stack Underflow**

---

## Features

### 👩‍⚕️ Therapist Management

Therapists can manage the complete speech-therapy workflow:

* Create and manage children
* Record child information and therapy goals
* Create pronunciation exercises
* Define target sounds
* Define difficulty levels
* Add instructions and example phrases
* Create and manage therapy sessions
* Upload speech recordings
* Run AI pronunciation analysis
* Review AI scores and feedback
* Add therapist notes

### 🧒 Child Experience

Children are intended to have a simplified experience focused on their therapy sessions.

A child account can:

* Access their sessions
* Upload speech recordings
* Practice assigned exercises
* Run pronunciation analysis
* View their pronunciation feedback

Children should only have access to their own session records.

### 🤖 Local AI Pronunciation Analysis

The project integrates with **OpenPronounce**, a local/open-source pronunciation assessment system.

The AI service analyzes:

* Speech transcription
* Pronunciation
* Phoneme errors
* Word errors
* Acoustic similarity
* Pronunciation score
* Feedback

The AI service runs locally rather than sending children's recordings to an external cloud AI API.

---

## Technology Stack

| Technology    | Purpose                      |
| ------------- | ---------------------------- |
| Odoo 19       | Application framework        |
| Python        | Backend and business logic   |
| XML           | Odoo views and menus         |
| CSV           | Access control               |
| OpenPronounce | Local pronunciation analysis |
| Wav2Vec2      | Speech/phoneme recognition   |
| FFmpeg        | Audio processing             |
| eSpeak-NG     | Phoneme processing           |
| Git/GitHub    | Version control              |

---

## Project Structure

```text
speech_therapy/
│
├── __init__.py
├── __manifest__.py
│
├── models/
│   ├── __init__.py
│   ├── child.py
│   ├── exercise.py
│   └── session.py
│
├── views/
│   ├── child_views.xml
│   ├── exercise_views.xml
│   ├── session_views.xml
│   └── menus.xml
│
└── security/
    ├── groups.xml
    ├── ir.model.access.csv
    └── rules.xml
```

Odoo modules are organized into Python models, XML views/data, security files, and a module manifest.

---

## Main Odoo Models

### Child

Model:

```text
speech.therapy.child
```

Stores information about the child participating in speech therapy.

Example information:

* Child name
* Date of birth
* Age
* Parent/guardian
* Parent phone
* Speech difficulty
* Therapy goals
* Notes
* Associated Odoo user

---

### Exercise

Model:

```text
speech.therapy.exercise
```

Stores speech-therapy exercises.

Each exercise can contain:

* Exercise name
* Target sound
* Difficulty
* Description
* Instructions
* Example phrase

Example:

```text
Exercise: Practice the R Sound
Target Sound: R
Difficulty: Easy
Example Phrase: The rabbit runs
```

---

### Session

Model:

```text
speech.therapy.session
```

Represents an individual therapy/practice session.

A session contains:

* Child
* Exercise
* Session date
* Duration
* Speech recording
* AI score
* AI transcription
* Phoneme error rate
* Word error rate
* AI feedback
* Therapist notes

---

## AI Architecture

The current architecture is:

```text
                    Odoo 19
                       │
                       │
                 Therapy Session
                       │
                       │
                 Speech Recording
                       │
                       ▼
          ┌─────────────────────────┐
          │   Local AI Server       │
          │   OpenPronounce         │
          │   localhost:8000        │
          └────────────┬────────────┘
                       │
                       ▼
              Pronunciation Analysis
                       │
              ┌────────┼────────┐
              │        │        │
              ▼        ▼        ▼
          Score   Transcription Errors
              │        │        │
              └────────┼────────┘
                       ▼
                    Odoo
                       │
                       ▼
              AI Analysis Results
```

The local pronunciation service exposes a `/pronunciation` endpoint that accepts an audio file, expected text, and language and returns pronunciation-analysis information.

---

## Example AI Workflow

A therapist creates an exercise:

```text
Exercise:
Practice the R Sound

Target Sound:
R

Example Phrase:
The rabbit runs
```

A session is then created for a child.

The child records the phrase.

The therapist or child selects:

```text
Analyze Speech
```

Odoo sends the recording and expected phrase to the local AI service.

The AI returns analysis such as:

```text
Score: 60.07

Transcription:
THE RABBIT RUNS

Word Error Rate:
0%

Phoneme Error Rate:
72.73%

Feedback:
You need to better pronounce these words: the
```

The results are then stored in the Odoo session.

---

## User Roles

The application is designed around two primary roles.

### Therapist

Therapists can access:

```text
Speech Therapy
├── Children
├── Exercises
└── Sessions
```

They can manage children, exercises, and therapy sessions.

### Child

Children should have access to:

```text
Speech Therapy
└── Sessions
```

A child should only be able to access sessions associated with their own account.

Odoo supports this through groups, access-control lists, and record rules. Access rights control model-level permissions, while record rules can restrict access to particular records.

---

## Installation

### Requirements

* Windows
* Odoo 19
* Python 3.10+
* Git
* FFmpeg
* eSpeak-NG
* OpenPronounce
* Python dependencies required by OpenPronounce

---

## Odoo Installation

Place the module inside an Odoo addons directory.

Example:

```text
C:\Program Files\Odoo 19.0.20260714\server\workshop\Workshop\
```

The module should be:

```text
speech_therapy/
```

Make sure the addons directory is included in the Odoo configuration.

Then start Odoo:

```powershell
cd "C:\Program Files\Odoo 19.0.20260714\server"
python odoo-bin -c odoo.conf
```

Open:

```text
http://localhost:8069
```

Install or upgrade the **AI Speech Therapy** module.

---

## OpenPronounce Setup

Clone OpenPronounce:

```powershell
git clone https://github.com/Halleck45/OpenPronounce.git
```

Install the required dependencies according to the OpenPronounce project.

Start the local pronunciation server:

```powershell
uvicorn server:app --host 127.0.0.1 --port 8000
```

The AI server should then be available at:

```text
http://127.0.0.1:8000
```

Health check:

```text
http://127.0.0.1:8000/health
```

---

## Security

The application uses Odoo's built-in security mechanisms.

### Access Rights

Model-level access is controlled through:

```text
security/ir.model.access.csv
```

Permissions include:

* Read
* Write
* Create
* Delete

### Groups

User roles are defined using Odoo groups:

```text
Therapist
Child
```

### Record Rules

Record rules are used to restrict children to their own therapy sessions.

Conceptually:

```text
Current User
     │
     ▼
Child Account
     │
     ▼
Associated Child
     │
     ▼
Only that child's sessions
```

Odoo evaluates access rights before record rules, with access rights controlling model-level operations and record rules restricting which records are accessible.

---

## Privacy

The project is designed with privacy in mind.

Speech recordings are processed through a **local AI server** rather than being sent to a third-party cloud AI service.

This architecture is particularly useful for a child-focused application because audio recordings can remain within the local development environment.

The application is intended as an educational/practice tool and **not as a replacement for a qualified speech-language therapist or a clinical diagnostic system**.

---

## Current Status

### Completed

* [x] Odoo 19 module created
* [x] Child model
* [x] Exercise model
* [x] Therapy session model
* [x] Child management interface
* [x] Exercise management interface
* [x] Session management interface
* [x] Speech recording upload
* [x] Analyze Speech button
* [x] Local OpenPronounce server
* [x] Odoo → AI integration
* [x] AI results stored in sessions
* [x] Therapist/child security architecture

### Planned

* [ ] Child-friendly dashboard
* [ ] Visual pronunciation feedback
* [ ] Progress tracking
* [ ] Session history
* [ ] Therapist dashboard
* [ ] Exercise recommendations
* [ ] Improved child-specific pronunciation scoring
* [ ] Gamification and rewards
* [ ] Improved UI/UX for demonstration

---

## Development

After modifying Python/XML/security files:

1. Restart Odoo.
2. Upgrade the module.
3. Test the affected functionality.
4. Check the Odoo server logs for errors.

For security changes, restart Odoo and update the module so the modified security data is loaded. Odoo's documentation specifically recommends updating the module after changing module data/security files.

---

## Git Workflow

Clone the repository:

```powershell
git clone https://github.com/JalawaToast/T04-stack-underflow-odoo-hwud.git
```

Enter the project:

```powershell
cd T04-stack-underflow-odoo-hwud
```

Check changes:

```powershell
git status
```

Add changes:

```powershell
git add .
```

Commit:

```powershell
git commit -m "Update AI speech therapy application"
```

Push:

```powershell
git push
```

---

## Team

**T04 Stack Underflow**

Hackathon project focused on combining Odoo with local AI-powered speech-practice technology.

---

## License

This project is a hackathon project.

The licensing of third-party components, including OpenPronounce and its dependencies, remains subject to their respective licenses.
