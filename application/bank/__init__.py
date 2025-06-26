from flask import blueprints
from . import views

bank = blueprints.Blueprint("bank", __name__, url_prefix="/api/bank")

bank.add_url_rule('/post_schema',
                  view_func=views.BankAccountEntryPostSchemaView.as_view('bank_account_entry_post_schema'))
bank.add_url_rule('/<int:character_id>',
                  view_func=views.BankAccountEntryIndexView.as_view('bank_account_entry_index'))
bank.add_url_rule('/account_entry/<int:ind>',
                  view_func=views.BankAccountEntryDetailView.as_view('bank_account_entry_detail'))
bank.add_url_rule('/balance/<int:ind>',
                  view_func=views.BankAccountBalanceView.as_view('bank_account_balance'))
