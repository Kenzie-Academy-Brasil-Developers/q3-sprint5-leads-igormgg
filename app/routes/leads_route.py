from flask import Blueprint

from app.controllers.leads_controller import create_leads, delete_leads, get_leads, patch_leads

bp_leads = Blueprint("bp_leads", __name__, url_prefix="/leads")

bp_leads.post("")(create_leads)
bp_leads.get("")(get_leads)
bp_leads.patch("<string:email>")(patch_leads)
bp_leads.delete("<string:email>")(delete_leads)