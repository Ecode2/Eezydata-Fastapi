# coding: utf-8


"""
    Ebills

    An API that developers can utilise to make payments for bills

    The version of the Ebills is 0.1.0
    Contact: ecode5814@gmail.com
"""


from __future__ import absolute_import
import os, dotenv
from dotenv import load_dotenv

load_dotenv(override=True)

__version__ = "0.1.0"
username=None
password=None

if os.getenv("EBILLS_USERNAME") and os.getenv("EBILLS_PASSWORD"):
    username = os.getenv("EBILLS_USERNAME")
    password = os.getenv("EBILLS_PASSWORD")
    print("Username and password set from environment variables")

from ebills.api.airtime import Airtime
from ebills.api.balance import Balance
from ebills.api.cable import Cable
from ebills.api.electricity import Electricity
from ebills.api.data import Data
from ebills.api.verify import Verify