from odoo import models, fields


class SpeechTherapyChild(models.Model):
    _name = 'speech.therapy.child'
    _description = 'Speech Therapy Child'
    _order = 'name'

    name = fields.Char(
        string='Child Name',
        required=True
    )

    date_of_birth = fields.Date(
        string='Date of Birth'
    )

    age = fields.Integer(
        string='Age'
    )

    parent_name = fields.Char(
        string='Parent / Guardian'
    )

    parent_phone = fields.Char(
        string='Parent Phone'
    )

    speech_difficulty = fields.Text(
        string='Speech Difficulty'
    )

    therapy_goals = fields.Text(
        string='Therapy Goals'
    )

    notes = fields.Text(
        string='Notes'
    )

    active = fields.Boolean(
        string='Active',
        default=True
    )