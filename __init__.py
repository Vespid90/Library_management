# -*- coding: utf-8 -*-

from . import controllers
from . import models
from . import wizard

def duration_loan(env):
    env['ir.config_parameter'].set_param('library_loan.return_duration_due', '90')

