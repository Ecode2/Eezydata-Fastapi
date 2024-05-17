"""Models of the ebills payment library
"""


from __future__ import absolute_import

from ebills.models.airtime import AirtimeModel, AirtimeResponse
from ebills.models.data import DataModel, DataResponse
from ebills.models.verify import VerifyModel, VerifyResponse
from ebills.models.cable import CableModel, CableResponse
from ebills.models.electricity import ElectricModel, ElectricResponse
from ebills.models.balance import BalanceResponse