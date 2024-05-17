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


class SplitCreate(object):
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
        'name': 'str',
        'type': 'str',
        'subaccounts': 'list[SplitSubaccounts]',
        'currency': 'str',
        'bearer_type': 'str',
        'bearer_subaccount': 'str'
    }

    attribute_map = {
        'name': 'name',
        'type': 'type',
        'subaccounts': 'subaccounts',
        'currency': 'currency',
        'bearer_type': 'bearer_type',
        'bearer_subaccount': 'bearer_subaccount'
    }

    def __init__(self, name=None, type=None, subaccounts=None, currency=None, bearer_type=None, bearer_subaccount=None, local_vars_configuration=None):  # noqa: E501
        """SplitCreate - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._type = None
        self._subaccounts = None
        self._currency = None
        self._bearer_type = None
        self._bearer_subaccount = None
        self.discriminator = None

        self.name = name
        self.type = type
        self.subaccounts = subaccounts
        self.currency = currency
        if bearer_type is not None:
            self.bearer_type = bearer_type
        if bearer_subaccount is not None:
            self.bearer_subaccount = bearer_subaccount

    @property
    def name(self):
        """Gets the name of this SplitCreate.  # noqa: E501

        Name of the transaction split  # noqa: E501

        :return: The name of this SplitCreate.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this SplitCreate.

        Name of the transaction split  # noqa: E501

        :param name: The name of this SplitCreate.  # noqa: E501
        :type name: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def type(self):
        """Gets the type of this SplitCreate.  # noqa: E501

        The type of transaction split you want to create.  # noqa: E501

        :return: The type of this SplitCreate.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this SplitCreate.

        The type of transaction split you want to create.  # noqa: E501

        :param type: The type of this SplitCreate.  # noqa: E501
        :type type: str
        """
        if self.local_vars_configuration.client_side_validation and type is None:  # noqa: E501
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

    @property
    def subaccounts(self):
        """Gets the subaccounts of this SplitCreate.  # noqa: E501

        A list of object containing subaccount code and number of shares  # noqa: E501

        :return: The subaccounts of this SplitCreate.  # noqa: E501
        :rtype: list[SplitSubaccounts]
        """
        return self._subaccounts

    @subaccounts.setter
    def subaccounts(self, subaccounts):
        """Sets the subaccounts of this SplitCreate.

        A list of object containing subaccount code and number of shares  # noqa: E501

        :param subaccounts: The subaccounts of this SplitCreate.  # noqa: E501
        :type subaccounts: list[SplitSubaccounts]
        """
        if self.local_vars_configuration.client_side_validation and subaccounts is None:  # noqa: E501
            raise ValueError("Invalid value for `subaccounts`, must not be `None`")  # noqa: E501

        self._subaccounts = subaccounts

    @property
    def currency(self):
        """Gets the currency of this SplitCreate.  # noqa: E501

        The transaction currency  # noqa: E501

        :return: The currency of this SplitCreate.  # noqa: E501
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """Sets the currency of this SplitCreate.

        The transaction currency  # noqa: E501

        :param currency: The currency of this SplitCreate.  # noqa: E501
        :type currency: str
        """
        if self.local_vars_configuration.client_side_validation and currency is None:  # noqa: E501
            raise ValueError("Invalid value for `currency`, must not be `None`")  # noqa: E501

        self._currency = currency

    @property
    def bearer_type(self):
        """Gets the bearer_type of this SplitCreate.  # noqa: E501

        This allows you specify how the transaction charge should be processed  # noqa: E501

        :return: The bearer_type of this SplitCreate.  # noqa: E501
        :rtype: str
        """
        return self._bearer_type

    @bearer_type.setter
    def bearer_type(self, bearer_type):
        """Sets the bearer_type of this SplitCreate.

        This allows you specify how the transaction charge should be processed  # noqa: E501

        :param bearer_type: The bearer_type of this SplitCreate.  # noqa: E501
        :type bearer_type: str
        """

        self._bearer_type = bearer_type

    @property
    def bearer_subaccount(self):
        """Gets the bearer_subaccount of this SplitCreate.  # noqa: E501

        This is the subaccount code of the customer or partner that would bear the transaction charge if you specified subaccount as the bearer type  # noqa: E501

        :return: The bearer_subaccount of this SplitCreate.  # noqa: E501
        :rtype: str
        """
        return self._bearer_subaccount

    @bearer_subaccount.setter
    def bearer_subaccount(self, bearer_subaccount):
        """Sets the bearer_subaccount of this SplitCreate.

        This is the subaccount code of the customer or partner that would bear the transaction charge if you specified subaccount as the bearer type  # noqa: E501

        :param bearer_subaccount: The bearer_subaccount of this SplitCreate.  # noqa: E501
        :type bearer_subaccount: str
        """

        self._bearer_subaccount = bearer_subaccount

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
        if not isinstance(other, SplitCreate):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SplitCreate):
            return True

        return self.to_dict() != other.to_dict()
