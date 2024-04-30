from django.test import TestCase, Client
from django.urls import reverse
from .models import Collector
from io import StringIO

class AccountsTestCase(TestCase):
    def setUp(self):
        Collector.objects.create(
            client_reference_no = 'ffeb5d88-e5af-45f0-9637-16ea469c58c0',
            balance = 59638.99,
            status = 'INACTIVE',
            consumer_name = 'Jessica Williams',
            consumer_address = '0233 Edwards Glens Allisonhaven, HI 91491',
            ssn = '018-79-4253',
        )

        Collector.objects.create(
            client_reference_no = '553efdb3-2baf-4c2a-88e2-7417d6bb0409',
            balance = 53670.34,
            status = 'PAID_IN_FULL',
            consumer_name = 'Heather Lambert',
            consumer_address = '616 Miller Heights Suite 268 North Josephview, UT 90983',
            ssn = '130-57-9448',
        )

        Collector.objects.create(
            client_reference_no = '03759711-89b9-40b8-9f2d-a3821c0779f2',
            balance = 11082.68,
            status = 'IN_COLLECTION',
            consumer_name = 'Gregory Marks',
            consumer_address = 'PSC 0156, Box 4223 APO AA 18544',
            ssn = '185-47-4236',
        )

        Collector.objects.create(
            client_reference_no = '3389eac9-ce2c-4bfc-9a59-6035d00bfe22',
            balance = 1365.34,
            status = 'IN_COLLECTION',
            consumer_name = 'Thomas Lynch',
            consumer_address = '340 Craig Plain Apt. 475 Brittanymouth, HI 20687',
            ssn = '435-27-5002',
        )

    def test_accounts_get_all(self):
        url = reverse('accounts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        expect_value = [
            {'client_reference_no': 'ffeb5d88-e5af-45f0-9637-16ea469c58c0', 'balance': '59638.99', 'status': 'INACTIVE', 'consumer_name': 'Jessica Williams', 'consumer_address': '0233 Edwards Glens Allisonhaven, HI 91491', 'ssn': '018-79-4253'},
            {'client_reference_no': '553efdb3-2baf-4c2a-88e2-7417d6bb0409', 'balance': '53670.34', 'status': 'PAID_IN_FULL', 'consumer_name': 'Heather Lambert', 'consumer_address': '616 Miller Heights Suite 268 North Josephview, UT 90983', 'ssn': '130-57-9448'},
            {'client_reference_no': '03759711-89b9-40b8-9f2d-a3821c0779f2', 'balance': '11082.68', 'status': 'IN_COLLECTION', 'consumer_name': 'Gregory Marks', 'consumer_address': 'PSC 0156, Box 4223 APO AA 18544', 'ssn': '185-47-4236'},
            {'client_reference_no': '3389eac9-ce2c-4bfc-9a59-6035d00bfe22', 'balance': '1365.34', 'status': 'IN_COLLECTION', 'consumer_name': 'Thomas Lynch', 'consumer_address': '340 Craig Plain Apt. 475 Brittanymouth, HI 20687', 'ssn': '435-27-5002'}
        ]
        self.assertEqual(response.json()['data'], expect_value)

    def test_accounts_get_filter_min_inclusive(self):        
        url = reverse('accounts') + '?min_balance=59638.99'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        expect_value = [
            {'client_reference_no': 'ffeb5d88-e5af-45f0-9637-16ea469c58c0', 'balance': '59638.99', 'status': 'INACTIVE', 'consumer_name': 'Jessica Williams', 'consumer_address': '0233 Edwards Glens Allisonhaven, HI 91491', 'ssn': '018-79-4253'}
        ]
        self.assertEqual(response.json()['data'], expect_value)

    def test_accounts_get_filter_min_invalid(self):        
        url = reverse('accounts') + '?min_balance=abc'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

    def test_accounts_get_filter_max_inclusive(self):        
        url = reverse('accounts') + '?max_balance=1365.34'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        expect_value = [
            {'client_reference_no': '3389eac9-ce2c-4bfc-9a59-6035d00bfe22', 'balance': '1365.34', 'status': 'IN_COLLECTION', 'consumer_name': 'Thomas Lynch', 'consumer_address': '340 Craig Plain Apt. 475 Brittanymouth, HI 20687', 'ssn': '435-27-5002'}
        ]
        self.assertEqual(response.json()['data'], expect_value)
    
    def test_accounts_get_filter_max_invalid(self):        
        url = reverse('accounts') + '?max_balance=abc'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
    
    def test_accounts_get_filter_consumer_name(self):        
        url = reverse('accounts') + '?consumer_name=Thomas Lynch'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        expect_value = [
            {'client_reference_no': '3389eac9-ce2c-4bfc-9a59-6035d00bfe22', 'balance': '1365.34', 'status': 'IN_COLLECTION', 'consumer_name': 'Thomas Lynch', 'consumer_address': '340 Craig Plain Apt. 475 Brittanymouth, HI 20687', 'ssn': '435-27-5002'}
        ]
        self.assertEqual(response.json()['data'], expect_value)
      
    def test_accounts_get_filter_consumer_name_invalid(self):        
        url = reverse('accounts') + '?consumer_name=231232'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data'], [])
      
    def test_accounts_get_filter_status_paid_in_full(self):        
        url = reverse('accounts') + '?status=collected'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        expect_value = [
            {'client_reference_no': '553efdb3-2baf-4c2a-88e2-7417d6bb0409', 'balance': '53670.34', 'status': 'PAID_IN_FULL', 'consumer_name': 'Heather Lambert', 'consumer_address': '616 Miller Heights Suite 268 North Josephview, UT 90983', 'ssn': '130-57-9448'}
        ]
        self.assertEqual(response.json()['data'], expect_value)

    def test_accounts_get_filter_status_in_collection(self):     
        url = reverse('accounts') + '?status=in_collection'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        expect_value = [
            {'client_reference_no': '03759711-89b9-40b8-9f2d-a3821c0779f2', 'balance': '11082.68', 'status': 'IN_COLLECTION', 'consumer_name': 'Gregory Marks', 'consumer_address': 'PSC 0156, Box 4223 APO AA 18544', 'ssn': '185-47-4236'},
            {'client_reference_no': '3389eac9-ce2c-4bfc-9a59-6035d00bfe22', 'balance': '1365.34', 'status': 'IN_COLLECTION', 'consumer_name': 'Thomas Lynch', 'consumer_address': '340 Craig Plain Apt. 475 Brittanymouth, HI 20687', 'ssn': '435-27-5002'}
        ]
        self.assertEqual(response.json()['data'], expect_value)
    
    def test_accounts_get_filter_status_invalid(self):     
        url = reverse('accounts') + '?status=123'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

    def test_accounts_get_filter_mix(self):     
        url = reverse('accounts') + '?min_balance=2000&max_balance=58000.01&status=collected'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        expect_value = [
            {'client_reference_no': '553efdb3-2baf-4c2a-88e2-7417d6bb0409', 'balance': '53670.34', 'status': 'PAID_IN_FULL', 'consumer_name': 'Heather Lambert', 'consumer_address': '616 Miller Heights Suite 268 North Josephview, UT 90983', 'ssn': '130-57-9448'}
        ]
        self.assertEqual(response.json()['data'], expect_value)

    def test_accounts_get_filter_mix_not_contains(self):     
        url = reverse('accounts') + '?min_balance=2000&max_balance=58000.01&status=inactive'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data'], [])

class ConsumersTestCase(TestCase):
    def setUp(self):
        Collector.objects.create(
            client_reference_no = 'ffeb5d88-e5af-45f0-9637-16ea469c58c0',
            balance = 59638.99,
            status = 'INACTIVE',
            consumer_name = 'Jessica Williams',
            consumer_address = '0233 Edwards Glens Allisonhaven, HI 91491',
            ssn = '018-79-4253',
        )

        Collector.objects.create(
            client_reference_no = '553efdb3-2baf-4c2a-88e2-7417d6bb0409',
            balance = 53670.34,
            status = 'PAID_IN_FULL',
            consumer_name = 'Heather Lambert',
            consumer_address = '616 Miller Heights Suite 268 North Josephview, UT 90983',
            ssn = '130-57-9448',
        )

        Collector.objects.create(
            client_reference_no = '03759711-89b9-40b8-9f2d-a3821c0779f2',
            balance = 11082.68,
            status = 'IN_COLLECTION',
            consumer_name = 'Gregory Marks',
            consumer_address = 'PSC 0156, Box 4223 APO AA 18544',
            ssn = '185-47-4236',
        )

        Collector.objects.create(
            client_reference_no = '3389eac9-ce2c-4bfc-9a59-6035d00bfe22',
            balance = 1365.34,
            status = 'IN_COLLECTION',
            consumer_name = 'Thomas Lynch',
            consumer_address = '340 Craig Plain Apt. 475 Brittanymouth, HI 20687',
            ssn = '435-27-5002',
        )
    
    def test_consumers(self):
        url = reverse('consumers')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        expect_value = ['Jessica Williams', 'Heather Lambert', 'Gregory Marks','Thomas Lynch']
        self.assertEqual(sorted(response.json()['data']), sorted(expect_value))

class CollectorModelTestCase(TestCase):
    def setUp(self):
        Collector.objects.create(
            client_reference_no = 'ffeb5d88-e5af-45f0-9637-16ea469c58c0',
            balance = 59638.99,
            status = 'INACTIVE',
            consumer_name = 'Jessica Williams',
            consumer_address = '0233 Edwards Glens Allisonhaven, HI 91491',
            ssn = '018-79-4253',
        )

    def test_collector_str_method(self):
        collector = Collector.objects.get(client_reference_no='ffeb5d88-e5af-45f0-9637-16ea469c58c0')
        self.assertEqual(
            str(collector),
            "client_reference_no: ffeb5d88-e5af-45f0-9637-16ea469c58c0, balance: 59638.99, status: INACTIVE, consumer_name: Jessica Williams, consumer_address: 0233 Edwards Glens Allisonhaven, HI 91491, ssn: 018-79-4253"
        )

class UploadTestCase(TestCase):
    def test_upload_post(self):
        client = Client()
        csv_content = "client reference no,balance,status,consumer name,consumer address,ssn\n553efdb3-2baf-4c2a-88e2-7417d6bb0409,53670.34,PAID_IN_FULL,Heather Lambert,123 Main St,123-45-6789\n"
        csv_file = StringIO(csv_content)
        response = client.post(reverse('upload'), {'file': csv_file})
        self.assertEqual(response.status_code, 200)
