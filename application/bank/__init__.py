from flask import blueprints
from . import views

bank = blueprints.Blueprint("bank", __name__, url_prefix="/api/bank")

bank.add_url_rule('/post_schema',
                  view_func=views.BankAccountEntryPostSchemaView.as_view('bank_account_entry_post_schema'))
bank.add_url_rule('/',
                  view_func=views.BankAccountEntryIndexView.as_view('bank_account_entry_index'))
bank.add_url_rule('/<int:character_id>',
                  view_func=views.BankAccountEntryCharacterIndexView.as_view('bank_account_entry_character_index'))
bank.add_url_rule('/entry/<int:ind>',
                  view_func=views.BankAccountEntryDetailView.as_view('bank_account_entry_detail'))
bank.add_url_rule('/<int:character_id>/balance',
                  view_func=views.BankAccountBalanceView.as_view('bank_account_balance'))
