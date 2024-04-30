from .models import Collector
import csv

def collectors_filter(min_balance=None, max_balance=None, consumer_name=None, status=None):
    collectors = Collector.objects.all()

    if min_balance:
        collectors = collectors.filter(balance__gte=min_balance)
    if max_balance:
        collectors = collectors.filter(balance__lte=max_balance)
    if consumer_name:
        collectors = collectors.filter(consumer_name__icontains=consumer_name)
    if status:
        collectors = collectors.filter(status=status.upper())

    response_data = []
    for collector in collectors:
        data = {
            "client_reference_no": collector.client_reference_no,
            "balance": collector.balance,
            "status": collector.status,
            "consumer_name": collector.consumer_name,
            "consumer_address": collector.consumer_address,
            "ssn": collector.ssn
        }
        response_data.append(data)

    return response_data


def process_upload(file):
    file_text = file.read().decode('utf-8').splitlines()
    rows = []
    reader = csv.reader(file_text)
    column_names = next(reader)
    for row in reader:
        row_data = dict()
        for name, value in zip(column_names, row):
            row_data[name] = value
        rows.append(row_data)

    data = []
    for row in rows:
        collector = Collector(
            client_reference_no = row.get('client reference no'),
            balance = row.get('balance'),
            status = row.get('status'),
            consumer_name = row.get('consumer name'),
            consumer_address = row.get('consumer address'),
            ssn = row.get('ssn')
        )
        data.append(collector)
    Collector.objects.bulk_create(data)