# -*- coding: utf-8 -*-
import unittest

from parameterized import parameterized

from nectar import Steem
from nectar.asset import Asset
from nectar.exceptions import AssetDoesNotExistsException
from nectar.instance import set_shared_steem_instance

from .nodes import get_hive_nodes


class Testcases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bts = Steem(node=get_hive_nodes(), nobroadcast=True, num_retries=10)
        cls.steemit = Steem(node="https://api.steemit.com", nobroadcast=True, num_retries=10)
        set_shared_steem_instance(cls.bts)

    @parameterized.expand(
        [
            ("normal"),
            ("steemit"),
        ]
    )
    def test_assert(self, node_param):
        if node_param == "normal":
            stm = self.bts
        else:
            stm = self.steemit
        with self.assertRaises(AssetDoesNotExistsException):
            Asset("FOObarNonExisting", full=False, steem_instance=stm)

    @parameterized.expand(
        [
            ("normal", "HBD", "HBD", 3, "@@000000013"),
            ("normal", "HIVE", "HIVE", 3, "@@000000021"),
            ("normal", "VESTS", "VESTS", 6, "@@000000037"),
            ("normal", "@@000000013", "HBD", 3, "@@000000013"),
            ("normal", "@@000000021", "HIVE", 3, "@@000000021"),
            ("normal", "@@000000037", "VESTS", 6, "@@000000037"),
        ]
    )
    def test_properties(self, node_param, data, symbol_str, precision, asset_str):
        if node_param == "normal":
            stm = self.bts
        else:
            stm = self.testnet
        asset = Asset(data, full=False, steem_instance=stm)
        self.assertEqual(asset.symbol, symbol_str)
        self.assertEqual(asset.precision, precision)
        self.assertEqual(asset.asset, asset_str)

    def test_assert_equal(self):
        stm = self.bts
        asset1 = Asset("HBD", full=False, steem_instance=stm)
        asset2 = Asset("HBD", full=False, steem_instance=stm)
        self.assertTrue(asset1 == asset2)
        self.assertTrue(asset1 == "HBD")
        self.assertTrue(asset2 == "HBD")
        asset3 = Asset("HIVE", full=False, steem_instance=stm)
        self.assertTrue(asset1 != asset3)
        self.assertTrue(asset3 != "HBD")
        self.assertTrue(asset1 != "HIVE")

        a = {"asset": "@@000000021", "precision": 3, "id": "HIVE", "symbol": "HIVE"}
        b = {"asset": "@@000000021", "precision": 3, "id": "@@000000021", "symbol": "HIVE"}
        self.assertTrue(Asset(a, steem_instance=stm) == Asset(b, steem_instance=stm))

    """
    # Mocker comes from pytest-mock, providing an easy way to have patched objects
    # for the life of the test.
    def test_calls(mocker):
        asset = Asset("USD", lazy=True, steem_instance=Steem(offline=True))
        method = mocker.patch.object(Asset, 'get_call_orders')
        asset.calls
        method.assert_called_with(10)
    """
