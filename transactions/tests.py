from django.test import TestCase
from users.tests import login_user, create_user
from http import HTTPStatus
import json
from transactions.payment_processor import process_payments, USD_TO_MXN


class TestTransactionsViews(TestCase):
    def test_payments_endpoint_success(self):
        create_user(self.client)
        login_resp = login_user(self.client)
        self.assertEqual(login_resp.status_code, HTTPStatus.OK)

        amount1 = 1160

        payments_resp = self.client.post(
            "/api/payments",
            headers={
                "Authorization": f"Bearer {login_resp.json()['access']}"
            },
            data=json.dumps([
                {
                    "amount": amount1,
                    "currency": "MXN"
                }
            ]),
            format='json',
            content_type='application/json'
        )

        self.assertEqual(payments_resp.status_code, HTTPStatus.OK)
        data = payments_resp.json()
        assert data['total'] == 1000.0
        assert data['taxes'] == 160.0
        assert data['commission'] == 0
        assert data['total'] + data['taxes'] + data['commission'] == amount1

    def test_payments_endpoint_failed_due_to_bad_creds(self):
        create_user(self.client)
        login_resp = login_user(self.client)
        self.assertEqual(login_resp.status_code, HTTPStatus.OK)

        amount1 = 1160

        payments_resp = self.client.post(
            "/api/payments",
            headers={
                "Authorization": f"{login_resp.json()['access']}"
            },
            data=json.dumps([
                {
                    "amount": amount1,
                    "currency": "MXN"
                }
            ]),
            format='json',
            content_type='application/json'
        )

        self.assertEqual(payments_resp.status_code, HTTPStatus.FORBIDDEN)

    def test_payment_processor_with_single_mxn_and_above_500(self):
        amount1 = 1160

        payments = [
            {
                "amount": 1160,
                "currency": "MXN"
            }
        ]

        data = process_payments(payments)
        assert data['total'] == 1000.0
        assert data['taxes'] == 160.0
        assert data['commission'] == 0
        assert round(data['total'] + data['taxes'] + data['commission'], 2) == amount1

    def test_payment_processor_with_single_mxn_and_below_500(self):
        amount1 = 499

        payments = [
            {
                "amount": 499,
                "currency": "MXN"
            }
        ]

        data = process_payments(payments)
        assert data['total'] == 499.0
        assert data['taxes'] == 0
        assert data['commission'] == 0
        assert round(data['total'] + data['taxes'] + data['commission'], 2) == amount1

    def test_payment_processor_with_multi_mxn_and_combined_threshold(self):
        amount1 = 1160
        amount2 = 400

        payments = [
            {
                "amount": amount1,
                "currency": "MXN"
            }, {
                "amount": amount2,
                "currency": "MXN"
            }
        ]

        data = process_payments(payments)
        assert data['total'] == 1400.0
        assert data['taxes'] == 160.0
        assert data['commission'] == 0
        assert round(data['total'] + data['taxes'] + data['commission'], 2) == amount1 + amount2

    def test_payment_processor_with_multi_mxn_and_usd_and_combined_threshold(self):
        amount1 = 60
        amount2 = 20
        amount3 = 1160

        payments = [
            {
                "amount": amount1,
                "currency": "USD"
            },
            {
                "amount": amount2,
                "currency": "USD"
            },
            {
                "amount": amount3,
                "currency": "MXN"
            }
        ]

        data = process_payments(payments)
        total_amount_in_mxn = (amount1 * USD_TO_MXN) + (amount2 * USD_TO_MXN) + amount3
        assert round(data['total'] + data['taxes'] + data['commission'], 2) == total_amount_in_mxn
