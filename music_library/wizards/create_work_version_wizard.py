# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class CreateWorkVersionWizard(models.TransientModel):
    _name = "create.work.version.wizard"
    _description = "Create a work version with needed instruments"

    work_ids = fields.Many2many(comodel_name="music.work")
    performer_ids = fields.One2many(comodel_name="create.work.version.wizard.performer", inverse_name="wizard_id")

    is_original = fields.Boolean(default=True)

    def action_create_versions(self):
        self.ensure_one()
        if not self.performer_ids:
            raise UserError(_("You must add at least an instrument or a category!"))

        self.performer_ids.check_required_field()

        for work in self.work_ids:
            new_version = self.env['music.work.version'].create({'work_id': work.id, 'is_original': self.is_original})
            for performer in self.performer_ids:
                self.env['music.work.version.instrument'].create({
                    'work_version_id': new_version.id,
                    'instrument_id': performer.instrument_id.id,
                    'instrument_category_id': performer.instrument_category_id.id,
                    'quantity': performer.quantity,
                })


class CreateWorkVersionWizardPerformer(models.TransientModel):
    _name = "create.work.version.wizard.performer"
    _description = "An instrument or category used in the version"

    wizard_id = fields.Many2one(comodel_name="create.work.version.wizard")
    instrument_id = fields.Many2one(comodel_name="instrument")
    instrument_category_id = fields.Many2one(comodel_name="instrument.category")
    quantity = fields.Integer(default=1)

    def check_required_field(self):
        for rec in self:
            if (not rec.instrument_id and not rec.instrument_category_id) or (rec.instrument_id and rec.instrument_category_id):
                raise UserError(_("You must choose either an instrument or a category"))

