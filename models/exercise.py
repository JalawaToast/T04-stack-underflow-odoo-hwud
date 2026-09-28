from odoo import models, fields


class SpeechTherapyExercise(models.Model):
    _name = 'speech.therapy.exercise'
    _description = 'Speech Therapy Exercise'
    _order = 'name'

    name = fields.Char(
        string='Exercise Name',
        required=True
    )

    target_sound = fields.Char(
        string='Target Sound',
        help='Example: R, S, TH'
    )

    difficulty = fields.Selection(
        [
            ('easy', 'Easy'),
            ('medium', 'Medium'),
            ('hard', 'Hard'),
        ],
        string='Difficulty',
        default='easy'
    )

    description = fields.Text(
        string='Description'
    )

    instructions = fields.Text(
        string='Instructions'
    )

    example_phrase = fields.Char(
        string='Example Phrase'
    )

    active = fields.Boolean(
        string='Active',
        default=True
    )