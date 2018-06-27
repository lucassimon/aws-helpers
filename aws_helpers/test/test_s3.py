from aws_helpers.s3 import S3Client, S3Bucket
from botocore.exceptions import ClientError
import unittest
from aws_helpers.test import TEST_BUCKET_NAME, CD_BUCKET_NAME, REGION


class TestS3(unittest.TestCase):
    s3client = S3Client(REGION)

    def test_get_bucket(self):
        self.assertEqual(TEST_BUCKET_NAME, self.s3client.get_bucket(TEST_BUCKET_NAME).name)
        self.assertRaises(ValueError, self.s3client.get_bucket)

    def test_get_all_buckets(self):
        self.assertTrue(lambda: TEST_BUCKET_NAME in self.s3client.get_all_buckets())
    
    def test_create_bucket(self):
        try:
            bucket = self.s3client.get_bucket(CD_BUCKET_NAME)
            bucket.delete()
        except:
            pass
        self.s3client.create_bucket(CD_BUCKET_NAME)
        self.assertRaises(ClientError, lambda: self.s3client.create_bucket(CD_BUCKET_NAME))

    def test_delete_bucket(self):
        try:
            # Try to create bucket if it doesn't exist
            self.s3client.create_bucket(CD_BUCKET_NAME)
        except:
            pass
        self.s3client.get_bucket(CD_BUCKET_NAME).delete()


class TestBucket(unittest.TestCase):
    bucket = S3Bucket(TEST_BUCKET_NAME, REGION)

    def test_upload_file(self):
        self.bucket.upload_file('testfile.json', 'permtestfile.json')
        self.bucket.upload_file('testfile.json', 'testfile.json')
        self.assertEqual('testfile.json', list(self.bucket.get_files('testfile.json'))[0].key)
    
    def test_put_file(self):
        self.bucket.delete_files('testfile2.json')
        self.bucket.put_file('testfile.json', 'testfile2.json', mock=True)
        self.assertEqual(None, None if not list(self.bucket.get_files('testfile2.json')) else 'some')
        self.bucket.put_file('testfile.json', 'testfile2.json')
        self.assertEqual('testfile2.json', list(self.bucket.get_files('testfile2.json'))[0].key)
    
    def test_delete_files(self):
        self.bucket.delete_files('testfile', mock=True)
        self.assertEqual('some', None if not list(self.bucket.get_files('testfile.json')) else 'some')
        self.assertEqual('some', None if not list(self.bucket.get_files('testfile2.json')) else 'some')
        self.bucket.delete_files('testfile')
        self.assertEqual(None, None if not list(self.bucket.get_files('testfile.json')) else 'some')
        self.assertEqual(None, None if not list(self.bucket.get_files('testfile2.json')) else 'some')

    def test_get_file(self):
        self.assertEqual('permtestfile.json', list(self.bucket.get_files('permtestfile.json'))[0].key)
        self.assertEqual(None, None if not list(self.bucket.get_files('testfile.json')) else 'some')
    
    def test_upload_direcory(self):
        self.bucket.upload_directory('./', 'test/')
        self.assertEqual('some', None if not list(self.bucket.get_files('test/')) else 'some')

    
if __name__=="__main__":
    unittest.main()
