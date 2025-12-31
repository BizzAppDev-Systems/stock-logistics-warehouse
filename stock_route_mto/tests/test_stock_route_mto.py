# Copyright (C) 2026: BizzAppDev Systems Pvt. Ltd.(https://www.bizzappdev.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo.tests import TransactionCase

from odoo.addons.stock_route_mto import post_init_hook


class TestStockRouteMTO(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.route_model = cls.env["stock.route"]
        cls.mto_route = cls.route_model.create(
            {
                "name": "Test MTO Route",
                "is_mto": True,
            }
        )
        cls.route = cls.route_model.create(
            {
                "name": "Test Route",
            }
        )

    def test_search_create_is_mto_routes(self):
        """Test : Check Created two routes, one with is_mto True, one False"""
        mto_routes = self.route_model.search([("is_mto", "=", True)])
        self.assertTrue(len(mto_routes) == 1, " There should be one MTO route")
        self.assertEqual(
            mto_routes.id,
            self.mto_route.id,
            " The MTO route should be the one created with is_mto True",
        )

    def test_post_init_hook_sets_is_mto(self):
        """Test : the post init hook sets is_mto on MTO routes"""
        warehouse = self.env.ref("stock.warehouse0")
        self.mto_route = warehouse.mto_pull_id.route_id
        self.mto_route.write({"is_mto": False})
        post_init_hook(self.env)
        self.assertTrue(
            self.mto_route.is_mto,
            "The MTO route should have is_mto set to True after post_init_hook",
        )
