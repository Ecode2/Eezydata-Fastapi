# coding: utf-8

"""
    Paystack

    The OpenAPI specification of the Paystack API that merchants and developers can harness to build financial solutions in Africa.  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: techsupport@paystack.com
"""


import inspect
import pprint
import re  # noqa: F401
import six

from paystack.configuration import Configuration


class DedicatedVirtualAccountCreate(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'customer': 'str',
        'preferred_bank': 'str',
        'subaccount': 'str',
        'split_code': 'str'
    }

    attribute_map = {
        'customer': 'customer',
        'preferred_bank': 'preferred_bank',
        'subaccount': 'subaccount',
        'split_code': 'split_code'
    }

    def __init__(self, customer=None, preferred_bank=None, subaccount=None, split_code=None, local_vars_configuration=None):  # noqa: E501
        """DedicatedVirtualAccountCreate - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._customer = None
        self._preferred_bank = None
        self._subaccount = None
        self._split_code = None
        self.discriminator = None

        self.customer = customer
        if preferred_bank is not None:
            self.preferred_bank = preferred_bank
        if subaccount is not None:
            self.subaccount = subaccount
        if split_code is not None:
            self.split_code = split_code

    @property
    def customer(self):
        """Gets the customer of this DedicatedVirtualAccountCreate.  # noqa: E501

        Customer ID or code  # noqa: E501

        :return: The customer of this DedicatedVirtualAccountCreate.  # noqa: E501
        :rtype: str
        """
        return self._customer

    @customer.setter
    def customer(self, customer):
        """Sets the customer of this DedicatedVirtualAccountCreate.

        Customer ID or code  # noqa: E501

        :param customer: The customer of this DedicatedVirtualAccountCreate.  # noqa: E501
        :type customer: str
        """
        if self.local_vars_configuration.client_side_validation and customer is None:  # noqa: E501
            raise ValueError("Invalid value for `customer`, must not be `None`")  # noqa: E501

        self._customer = customer

    @property
    def preferred_bank(self):
        """Gets the preferred_bank of this DedicatedVirtualAccountCreate.  # noqa: E501

        The bank slug for preferred bank. To get a list of available banks, use the List Providers endpoint  # noqa: E501

        :return: The preferred_bank of this DedicatedVirtualAccountCreate.  # noqa: E501
        :rtype: str
        """
        return self._preferred_bank

    @preferred_bank.setter
    def preferred_bank(self, preferred_bank):
        """Sets the preferred_bank of this DedicatedVirtualAccountCreate.

        The bank slug for preferred bank. To get a list of available banks, use the List Providers endpoint  # noqa: E501

        :param preferred_bank: The preferred_bank of this DedicatedVirtualAccountCreate.  # noqa: E501
        :type preferred_bank: str
        """

        self._preferred_bank = preferred_bank

    @property
    def subaccount(self):
        """Gets the subaccount of this DedicatedVirtualAccountCreate.  # noqa: E501

        Subaccount code of the account you want to split the transaction with  # noqa: E501

        :return: The subaccount of this DedicatedVirtualAccountCreate.  # noqa: E501
        :rtype: str
        """
        return self._subaccount

    @subaccount.setter
    def subaccount(self, subaccount):
        """Sets the subaccount of this DedicatedVirtualAccountCreate.

        Subaccount code of the account you want to split the transaction with  # noqa: E501

        :param subaccount: The subaccount of this DedicatedVirtualAccountCreate.  # noqa: E501
        :type subaccount: str
        """

        self._subaccount = subaccount

    @property
    def split_code(self):
        """Gets the split_code of this DedicatedVirtualAccountCreate.  # noqa: E501

        Split code consisting of the lists of accounts you want to split the transaction with  # noqa: E501

        :return: The split_code of this DedicatedVirtualAccountCreate.  # noqa: E501
        :rtype: str
        """
        return self._split_code

    @split_code.setter
    def split_code(self, split_code):
        """Sets the split_code of this DedicatedVirtualAccountCreate.

        Split code consisting of the lists of accounts you want to split the transaction with  # noqa: E501

        :param split_code: The split_code of this DedicatedVirtualAccountCreate.  # noqa: E501
        :type split_code: str
        """

        self._split_code = split_code

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = inspect.getargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, DedicatedVirtualAccountCreate):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DedicatedVirtualAccountCreate):
            return True

        return self.to_dict() != other.to_dict()
