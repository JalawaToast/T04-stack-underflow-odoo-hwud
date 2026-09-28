from odoo import models, fields
from odoo.exceptions import UserError
import requests
import base64


class SpeechTherapySession(models.Model):
    _name = 'speech.therapy.session'
    _description = 'Speech Therapy Session'
    _order = 'date desc'

    child_id = fields.Many2one(
        'speech.therapy.child',
        string='Child',
        required=True,
        ondelete='cascade'
    )

    exercise_id = fields.Many2one(
        'speech.therapy.exercise',
        string='Exercise',
        required=True,
        ondelete='cascade'
    )

    date = fields.Datetime(
        string='Session Date',
        default=fields.Datetime.now,
        required=True
    )

    duration = fields.Float(
        string='Duration (seconds)'
    )

    recording = fields.Binary(
        string='Speech Recording',
        attachment=True
    )

    recording_filename = fields.Char(
        string='Recording Filename'
    )

    ai_score = fields.Float(
        string='AI Score'
    )

    ai_feedback = fields.Text(
        string='AI Feedback'
    )

    ai_transcription = fields.Text(
        string='AI Transcription'
    )

    ai_phoneme_error_rate = fields.Float(
        string='Phoneme Error Rate'
    )

    ai_word_error_rate = fields.Float(
        string='Word Error Rate'
    )

    therapist_notes = fields.Text(
        string='Therapist Notes'
    )

    def action_analyze_speech(self):
        for record in self:

            # Make sure a recording exists
            if not record.recording:
                raise UserError(
                    "Please upload a speech recording before analyzing."
                )

            # The exercise's example phrase becomes the expected speech.
            expected_text = record.exercise_id.example_phrase

            if not expected_text:
                raise UserError(
                    "Please add an Example Phrase to the selected exercise "
                    "before analyzing the recording."
                )

            try:
                # Decode Odoo's Base64 binary field
                audio_data = base64.b64decode(record.recording)

                # Send recording to the local OpenPronounce server
                response = requests.post(
                    'http://127.0.0.1:8000/pronunciation',
                    files={
                        'file': (
                            record.recording_filename or 'recording.wav',
                            audio_data
                        )
                    },
                    data={
                        'expected_text': expected_text,
                        'lang': 'en'
                    },
                    timeout=120
                )

                response.raise_for_status()

                result = response.json()

            except requests.exceptions.ConnectionError:
                raise UserError(
                    "Could not connect to the local AI server.\n\n"
                    "Please make sure OpenPronounce is running on "
                    "http://127.0.0.1:8000"
                )

            except requests.exceptions.Timeout:
                raise UserError(
                    "The AI analysis took too long.\n\n"
                    "Please try again with a shorter recording."
                )

            except requests.exceptions.RequestException as error:
                raise UserError(
                    "The AI server returned an error:\n\n%s" % error
                )

            # Store AI results in Odoo
            record.ai_score = result.get('score', 0)

            record.ai_transcription = result.get(
                'transcription',
                result.get('transcribe', '')
            )

            differences = result.get('differences', {})

            record.ai_phoneme_error_rate = (
                differences.get('phoneme_error_rate', 0) * 100
            )

            record.ai_word_error_rate = (
                differences.get('word_error_rate', 0) * 100
            )

            # Use OpenPronounce feedback if available
            feedback = result.get('feedback', '')

            if not feedback:
                errors = differences.get('errors', [])

                if errors:
                    words = [
                        error.get('word', '')
                        for error in errors
                        if error.get('word')
                    ]

                    feedback = (
                        "Practice these sounds/words: "
                        + ", ".join(words)
                    )
                else:
                    feedback = "Good job! Keep practicing."

            record.ai_feedback = feedback