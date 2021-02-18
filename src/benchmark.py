import os
import time

import boto3

from serverless_utils.http import json_lambda


LENGTH_PRIMARY = 1000
LENGTH_SECONDARY = 1000


def benchmark_with_primary_only():
    t = boto3.resource('dynamodb').Table(os.environ['PRIMARY_KEY_ONLY'])
    results = []
    start = time.time()
    for i in range(LENGTH_PRIMARY):
        results.append(t.get_item(Key={'composite_code_to_system': f'loinc:{i}_rxnorm'})['Item']['value'])
    print('primary only took', time.time() - start, 'for', LENGTH_PRIMARY, 'values')


def benchmark_with_secondary_key():
    t = boto3.resource('dynamodb').Table(os.environ['WITH_SECONDARY_KEY'])
    results = []
    start = time.time()
    for i in range(LENGTH_SECONDARY):
        results.append(t.get_item(Key={'composite_code': f'loinc:{i}', 'to_system': 'rxnorm'})['Item']['value'])
    print('with secondary took', time.time() - start, 'for', LENGTH_SECONDARY, 'values')


def upload():
    t = boto3.resource('dynamodb').Table(os.environ['PRIMARY_KEY_ONLY'])
    for i in range(LENGTH_PRIMARY):
        t.put_item(Item={'composite_code_to_system': f'loinc:{i}_rxnorm', 'value': 'foba'})
    t = boto3.resource('dynamodb').Table(os.environ['WITH_SECONDARY_KEY'])
    for i in range(LENGTH_SECONDARY):
        t.put_item(Item={'composite_code': f'loinc:{i}', 'to_system': 'rxnorm', 'value': 'foba'})


@json_lambda
def api(event, context):
    if event['httpMethod'] == 'GET':
        benchmark_with_primary_only()
        benchmark_with_secondary_key()
    else:
        upload()
    return ''
