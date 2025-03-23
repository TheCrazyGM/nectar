from __future__ import absolute_import, division, print_function, unicode_literals

import logging

from beem.account import Account
from beem.steem import Steem

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    # stm = Steem(node="https://testnet.timcliff.com/")
    # stm = Steem(node="https://testnet.steemitdev.com")
    stm = Steem(node="https://api.steemit.com")
    stm.wallet.unlock(pwd="pwd123")

    account = Account("beembot", steem_instance=stm)
    print(account.get_voting_power())

    account.transfer("holger80", 0.001, "SBD", "test")
