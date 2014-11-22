__author__ = 'yoavschatzberg'
import datetime
import json
import mock
import siftpartner
import unittest
import sys
import requests.exceptions

def valid_create_new_account_response_json():
    return {
              "production":{
                "api_keys":[
                  {
                    "id":"54125bfee4b0beea0dfebfba",
                    "state":"ACTIVE",
                    "key":"492f506b096f0aa9"
                  }
                 ],
                 "beacon_keys":[
                   {
                     "id":"54125bfee4b0beea0dfebfbb",
                     "state":"ACTIVE",
                     "key":"5edb0c9c38"
                   }
                 ]
              },
              "sandbox":{
                "api_keys":[
                  {
                    "id":"54125bfee4b0beea0dfebfbd",
                    "state":"ACTIVE",
                    "key":"1c1155e8d391b161"
                  }
                ],
                "beacon_keys":[
                  {
                    "id":"54125bfee4b0beea0dfebfbe",
                    "state":"ACTIVE",
                    "key":"44063ef989"
                  }
                ]
              },
              "account_id":"54125bfee4b0beea0dfebfb9"
           }

def valid_get_accounts_list_response_json():
    return {
            "data": [
              {
                "account_id": "54125bfee4b0beea0dfebfb9",
                "production": {
                  "api_keys": [
                    {
                      "id": "54125bfee4b0beea0dfebfba",
                      "key": "492f506b096f0aa9",
                      "state": "ACTIVE"
                    }
                  ],
                  "beacon_keys": [
                    {
                      "id": "54125bfee4b0beea0dfebfbb",
                      "key": "5edb0c9c38",
                      "state": "ACTIVE"
                    }
                  ]
                },
                "sandbox": {
                  "api_keys": [
                    {
                      "id": "54125bfee4b0beea0dfebfbd",
                      "key": "1c1155e8d391b161",
                      "state": "ACTIVE"
                    }
                  ],
                  "beacon_keys": [
                    {
                      "id": "54125bfee4b0beea0dfebfbe",
                      "key": "44063ef989",
                      "state": "ACTIVE"
                    }
                  ]
                }
              },
              {
                "account_id": "541793ece4b0550b2274a8ed",
                "production": {
                  "api_keys": [
                    {
                      "id": "541793ece4b0550b2274a8ee",
                      "key": "c1ab335655fbcd3f",
                      "state": "ACTIVE"
                    }
                  ],
                  "beacon_keys": [
                    {
                      "id": "541793ece4b0550b2274a8ef",
                      "key": "461b33d204",
                      "state": "ACTIVE"
                    }
                  ]
                },
                "sandbox": {
                  "api_keys": [
                    {
                      "id": "541793ece4b0550b2274a8f1",
                      "key": "31d70b58b6030cde",
                      "state": "ACTIVE"
                    }
                  ],
                  "beacon_keys": [
                    {
                      "id": "541793ece4b0550b2274a8f2",
                      "key": "7eaa6fa0ea",
                      "state": "ACTIVE"
                    }
                  ]
                }
              }
            ],
            "has_more": False,
            "total_results": 2,
            "type": "partner_account"
          }

def valid_config_notification_url_response_json():
    return {
             "email_notification_threshold": 0.8999999761581421,
             "enable_sort_by_expected_loss": False,
             "http_notification_threshold": 0.15000000596046448,
             "http_notification_url": "http://api.partner.com/notify?id=%s",
             "is_production": False
           }

def valid_config_notification_url_properties():
    return {
            "http_notification_url": "http://api.partner.com/notify?id=%s",
            "http_notification_threshold": 0.60
           }

class TestSiftPythonClient(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.test_local_key = 'a_fake_test_local_api_key'
        self.test_global_key = 'a_fake_test_global_api_key'

        self.test_local_partner_id = 'a_fake_test_local_partner_id'
        self.test_global_partner_id = 'a_fake_test_global_partner_id'

        self.test_unicode_local_key = u'a_fake_test_local_api_key'
        self.test_unicode_global_key = u'a_fake_test_global_api_key'

        self.test_unicode_local_partner_id = u'a_fake_test_local_partner_id'
        self.test_unicode_global_partner_id = u'a_fake_test_global_partner_id'

        self.sift_client = siftpartner.Client(self.test_local_key, self.test_local_partner_id)


    def test_global_api_key_and_partner_id(self):
        self.assertRaises(RuntimeError, siftpartner.Client)
        siftpartner.api_key = self.test_global_key
        siftpartner.partner_id = self.test_global_partner_id
        local_key = self.test_local_key
        local_partner_id = self.test_local_partner_id

        client1 = siftpartner.Client()
        client2 = siftpartner.Client(local_key, local_partner_id)

        self.assertEqual(client1.api_key, self.test_global_key, "Client was not instantiated with global api key")
        self.assertEqual(client1.partner_id,
                         self.test_global_partner_id,
                         "Client was not instantiated with global partner id"
        )

        self.assertEqual(client2.api_key, self.test_local_key, "Client was not instantiated with local api key")
        self.assertEqual(client2.partner_id,
                         self.test_local_partner_id,
                         "Client was not instantiated with local partner id"
        )

    def test_unicode_global_api_key_and_partner_id(self):
        siftpartner.api_key = self.test_unicode_global_key
        siftpartner.partner_id = self.test_unicode_global_partner_id
        local_key = self.test_unicode_local_key
        local_partner_id = self.test_unicode_local_partner_id

        client1 = siftpartner.Client()
        client2 = siftpartner.Client(local_key, local_partner_id)

        self.assertEqual(client1.api_key, self.test_global_key, "Client was not instantiated with global api key")
        self.assertEqual(client1.partner_id,
                         self.test_global_partner_id,
                         "Client was not instantiated with global partner id"
        )

        self.assertEqual(client2.api_key, self.test_local_key, "Client was not instantiated with local api key")
        self.assertEqual(client2.partner_id,
                         self.test_local_partner_id,
                         "Client was not instantiated with local partner id"
        )

    def test_create_new_account_with_empty_site_url_fails(self):
        mock_response = mock.Mock()
        mock_response.content = json.dumps(valid_create_new_account_response_json())
        mock_response.json.return_value = json.loads(mock_response.content)
        mock_response.status_code = 200
        with mock.patch('requests.post') as mock_post:
            mock_post.return_value = mock_response
            self.assertRaises(RuntimeError, self.sift_client.new_account, "",
                                        "owner@somefakeurl.com",
                                        "dropcam.dan@somefakeurl.com",
                                        "s0mepA55word"
                )

    def test_create_new_account_with_null_site_url_fails(self):
        mock_response = mock.Mock()
        mock_response.content = json.dumps(valid_create_new_account_response_json())
        mock_response.json.return_value = json.loads(mock_response.content)
        mock_response.status_code = 200
        with mock.patch('requests.post') as mock_post:
            mock_post.return_value = mock_response
            self.assertRaises(RuntimeError, self.sift_client.new_account, None,
                                        "owner@somefakeurl.com",
                                        "dropcam.dan@somefakeurl.com",
                                        "s0mepA55word"
                )

    def test_create_new_account_with_invalid_site_url_fails(self):
        mock_response = mock.Mock()
        mock_response.content = json.dumps(valid_create_new_account_response_json())
        mock_response.json.return_value = json.loads(mock_response.content)
        mock_response.status_code = 200
        with mock.patch('requests.post') as mock_post:
            mock_post.return_value = mock_response
            self.assertRaises(RuntimeError, self.sift_client.new_account, {},
                                        "owner@somefakeurl.com",
                                        "dropcam.dan@somefakeurl.com",
                                        "s0mepA55word"
                )

    def test_create_new_account_with_empty_site_email_fails(self):
        mock_response = mock.Mock()
        mock_response.content = json.dumps(valid_create_new_account_response_json())
        mock_response.json.return_value = json.loads(mock_response.content)
        mock_response.status_code = 200
        with mock.patch('requests.post') as mock_post:
            mock_post.return_value = mock_response
            self.assertRaises(RuntimeError, self.sift_client.new_account, "somefakeurl.com",
                                        "",
                                        "dropcam.dan@somefakeurl.com",
                                        "s0mepA55word"
            )

    def test_create_new_account_with_null_site_email_fails(self):
        mock_response = mock.Mock()
        mock_response.content = json.dumps(valid_create_new_account_response_json())
        mock_response.json.return_value = json.loads(mock_response.content)
        mock_response.status_code = 200
        with mock.patch('requests.post') as mock_post:
            mock_post.return_value = mock_response
            self.assertRaises(RuntimeError, self.sift_client.new_account, "somefakeurl.com",
                                        None,
                                        "dropcam.dan@somefakeurl.com",
                                        "s0mepA55word"
            )

    def test_create_new_account_with_invalid_site_email_fails(self):
        mock_response = mock.Mock()
        mock_response.content = json.dumps(valid_create_new_account_response_json())
        mock_response.json.return_value = json.loads(mock_response.content)
        mock_response.status_code = 200
        with mock.patch('requests.post') as mock_post:
            mock_post.return_value = mock_response
            self.assertRaises(RuntimeError, self.sift_client.new_account, "somefakeurl.com",
                                        {},
                                        "dropcam.dan@somefakeurl.com",
                                        "s0mepA55word"
            )

    def test_create_new_account_with_empty_analyst_email_fails(self):
        mock_response = mock.Mock()
        mock_response.content = json.dumps(valid_create_new_account_response_json())
        mock_response.json.return_value = json.loads(mock_response.content)
        mock_response.status_code = 200
        with mock.patch('requests.post') as mock_post:
            mock_post.return_value = mock_response
            self.assertRaises(RuntimeError, self.sift_client.new_account, "somefakeurl.com",
                                        "owner@somefakeurl.com",
                                        "",
                                        "s0mepA55word"
            )

    def test_create_new_account_with_null_analyst_email_fails(self):
        mock_response = mock.Mock()
        mock_response.content = json.dumps(valid_create_new_account_response_json())
        mock_response.json.return_value = json.loads(mock_response.content)
        mock_response.status_code = 200
        with mock.patch('requests.post') as mock_post:
            mock_post.return_value = mock_response
            self.assertRaises(RuntimeError, self.sift_client.new_account, "somefakeurl.com",
                                        "owner@somefakeurl.com",
                                        None,
                                        "s0mepA55word"
            )

    def test_create_new_account_with_invalid_analyst_email_fails(self):
        mock_response = mock.Mock()
        mock_response.content = json.dumps(valid_create_new_account_response_json())
        mock_response.json.return_value = json.loads(mock_response.content)
        mock_response.status_code = 200
        with mock.patch('requests.post') as mock_post:
            mock_post.return_value = mock_response
            self.assertRaises(RuntimeError, self.sift_client.new_account, "somefakeurl.com",
                                        "owner@somefakeurl.com",
                                        {},
                                        "s0mepA55word"
            )

    def test_create_new_account_with_empty_password_fails(self):
        mock_response = mock.Mock()
        mock_response.content = json.dumps(valid_create_new_account_response_json())
        mock_response.json.return_value = json.loads(mock_response.content)
        mock_response.status_code = 200
        with mock.patch('requests.post') as mock_post:
            mock_post.return_value = mock_response
            self.assertRaises(RuntimeError, self.sift_client.new_account, "somefakeurl.com",
                                        "owner@somefakeurl.com",
                                        "dropcam.dan@somefakeurl.com",
                                        ""
            )

    def test_create_new_account_with_null_password_fails(self):
        mock_response = mock.Mock()
        mock_response.content = json.dumps(valid_create_new_account_response_json())
        mock_response.json.return_value = json.loads(mock_response.content)
        mock_response.status_code = 200
        with mock.patch('requests.post') as mock_post:
            mock_post.return_value = mock_response
            self.assertRaises(RuntimeError, self.sift_client.new_account, "somefakeurl.com",
                                        "owner@somefakeurl.com",
                                        "dropcam.dan@somefakeurl.com",
                                        None
            )

    def test_create_new_account_with_invalid_password_fails(self):
        mock_response = mock.Mock()
        mock_response.content = json.dumps(valid_create_new_account_response_json())
        mock_response.json.return_value = json.loads(mock_response.content)
        mock_response.status_code = 200
        with mock.patch('requests.post') as mock_post:
            mock_post.return_value = mock_response
            self.assertRaises(RuntimeError, self.sift_client.new_account, "somefakeurl.com",
                                        "owner@somefakeurl.com",
                                        "dropcam.dan@somefakeurl.com",
                                        {}
            )

    def test_create_new_account_ok(self):
        mock_response = mock.Mock()
        mock_response.content = json.dumps(valid_create_new_account_response_json())
        mock_response.json.return_value = json.loads(mock_response.content)
        mock_response.status_code = 200
        with mock.patch('requests.post') as mock_post:
            mock_post.return_value = mock_response
            response = self.sift_client.new_account("somefakeurl.com",
                                                    "owner@somefakeurl.com",
                                                    "dropcam.dan@somefakeurl.com",
                                                    "s0mepA55word"
            )
            mock_post.assert_called_with('https://partner.siftscience.com/v3/partners/'
                                         '%s/accounts' % self.sift_client.partner_id,
                                         data=mock.ANY,
                                         headers=mock.ANY,
                                         timeout=mock.ANY,
                                         params={}
            )
            self.assertTrue(response.is_ok())
            self.assertTrue('production' in response.body.keys())
            self.assertTrue('sandbox' in response.body.keys())
            self.assertTrue('account_id' in response.body.keys())

    def test_get_accounts_list_ok(self):
        mock_response = mock.Mock()
        mock_response.content = json.dumps(valid_get_accounts_list_response_json())
        mock_response.json.return_value = json.loads(mock_response.content)
        mock_response.status_code = 200
        with mock.patch('requests.get') as mock_post:
            mock_post.return_value = mock_response
            response = self.sift_client.get_accounts()
            mock_post.assert_called_with('https://partner.siftscience.com/v3/partners/'
                                         '%s/accounts' % self.sift_client.partner_id,
                                         headers=mock.ANY,
                                         timeout=mock.ANY,
            )
            self.assertTrue(response.is_ok())
            self.assertTrue('has_more' in response.body.keys())
            self.assertFalse(response.body['has_more'])
            self.assertTrue('total_results' in response.body.keys())
            self.assertEqual(response.body['total_results'], 2)
            self.assertTrue('data' in response.body.keys())
            self.assertEqual(len(response.body['data']), 2)


    def test_config_notifications_url_with_null_config_fails(self):
        mock_response = mock.Mock()
        mock_response.content = json.dumps(valid_config_notification_url_response_json())
        mock_response.json.return_value = json.loads(mock_response.content)
        mock_response.status_code = 200
        with mock.patch('requests.put') as mock_post:
            mock_post.return_value = mock_response
            self.assertRaises(RuntimeError, self.sift_client.update_notification_config, None)

    def test_config_notifications_url_with_invalid_config_fails(self):
        mock_response = mock.Mock()
        mock_response.content = json.dumps(valid_config_notification_url_response_json())
        mock_response.json.return_value = json.loads(mock_response.content)
        mock_response.status_code = 200
        with mock.patch('requests.put') as mock_post:
            mock_post.return_value = mock_response
            self.assertRaises(RuntimeError, self.sift_client.update_notification_config, "some_string")

    def test_config_notification_url_ok(self):
        mock_response = mock.Mock()
        mock_response.content = json.dumps(valid_config_notification_url_response_json())
        mock_response.json.return_value = json.loads(mock_response.content)
        mock_response.status_code = 200
        with mock.patch('requests.put') as mock_post:
            mock_post.return_value = mock_response
            response = self.sift_client.update_notification_config(valid_config_notification_url_properties())
            mock_post.assert_called_with('https://partner.siftscience.com/v3/accounts/'
                                         '%s/config' % self.sift_client.partner_id,
                                         data=mock.ANY,
                                         headers=mock.ANY,
                                         timeout=mock.ANY,
            )
            self.assertTrue(response.is_ok())




def main():
    unittest.main()

if __name__ == '__main__':
    main()