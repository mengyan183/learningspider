# -*- coding: UTF-8 -*-
"""
Copyright 2019 [xingguo] All rights Reserved.
"""
import unittest

from first_thrift_test.client import start_client
from first_thrift_test.server import start_server

"""
   @author xingguo
   @date 1/18/2019 1:15 PM 
   @since 1.0.0 
"""


class TestThrift(unittest.TestCase):
    def test_start_server(self):
        start_server()

    def test_start_client(self):
        start_client()
