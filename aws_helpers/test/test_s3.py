from aws_helpers.s3 import S3Client, S3Bucket
from botocore.exceptions import ClientError
import unittest

TEST_BUCKET_NAME = 'test.bucket.ps-george'
CD_BUCKET_NAME = 'test.bucket.ps-george123'
REGION = 'eu-west-1'

class S3TestCase(unittest.TestCase):
    """
    """
    def setUp(self):
        pass

    def tearDown(self):
        pass

class TestS3(S3TestCase):
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

class TestBucket(S3TestCase):
    bucket = S3Bucket(TEST_BUCKET_NAME, REGION)

    def test_upload_file(self):
        self.bucket.upload_file('testfile.txt', 'permtestfile.txt')
        self.bucket.upload_file('testfile.txt', 'testfile.txt')
        self.assertEqual('testfile.txt', list(self.bucket.get_files('testfile.txt'))[0].key)
    
    def test_put_file(self):
        self.bucket.delete_files('testfile2.txt')
        self.bucket.put_file('testfile.txt', 'testfile2.txt', mock=True)
        self.assertEqual(None, None if not list(self.bucket.get_files('testfile2.txt')) else 'some')
        self.bucket.put_file('testfile.txt', 'testfile2.txt')
        self.assertEqual('testfile2.txt', list(self.bucket.get_files('testfile2.txt'))[0].key)
    
    def test_delete_files(self):
        self.bucket.delete_files('testfile', mock=True)
        self.assertEqual('some', None if not list(self.bucket.get_files('testfile.txt')) else 'some')
        self.assertEqual('some', None if not list(self.bucket.get_files('testfile2.txt')) else 'some')
        self.bucket.delete_files('testfile')
        self.assertEqual(None, None if not list(self.bucket.get_files('testfile.txt')) else 'some')
        self.assertEqual(None, None if not list(self.bucket.get_files('testfile2.txt')) else 'some')

    def test_get_file(self):
        self.assertEqual('permtestfile.txt', list(self.bucket.get_files('permtestfile.txt'))[0].key)
        self.assertEqual(None, None if not list(self.bucket.get_files('testfile.txt')) else 'some')
    
    def test_upload_direcory(self):
        self.bucket.upload_directory('./', 'test/')
        self.assertEqual('some', None if not list(self.bucket.get_files('test/')) else 'some')

    
if __name__=="__main__":
    unittest.main()
