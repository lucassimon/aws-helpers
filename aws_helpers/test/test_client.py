from botocore.exceptions import ClientError
import boto3.session
import unittest
from aws_helpers.client import load_access_keys, Client
from aws_helpers.test import REGION


class AccessKeysTest(unittest.TestCase):
    def test_load_access_keys(self):
        access_key, secret_key = load_access_keys(access_key_path='testfile.json')
        self.assertEqual('ABC',access_key)
        self.assertEqual('DEF',secret_key)

        self.assertRaises(OSError, lambda: load_access_keys('fail'))


class ClientTest(unittest.TestCase):
    client = Client(REGION)
    def test_fail_client(self):
        # Invalid region
        self.assertRaises(ValueError, lambda: return Client('EU (Ireland)'))
        # Invalid keys
        self.assertRaises(ValueError, lambda: return Client(REGION, lambda: load_access_keys('testfile.json')))

    def test_get_session(self):
        sess = client.get_session()
        # check that sess is correct
        print(dict(sess), type(sess))

    def test_get_resource(self):
        # Check that resource you get has correct boto3 type
        s3 = client.get_resource('s3')
        print(dict(s3), type(s3))
        





    