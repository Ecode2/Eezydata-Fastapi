from ebills.rest import RestClient
from ebills.models import AirtimeModel, AirtimeResponse

class Airtime:
    """Buy airtime using ebills api

    """
    def __init__(self):
        request = RestClient()
        self.request = request

    @classmethod
    def buy(cls, parameters: dict) -> AirtimeResponse:
        """method to buy airtime

        Args:
            parameters (dict):
                phone: str. _Phone number of the receipient length of 11 numbers_
                network_id: str. _Network type [mtn, glo, airtel, etisalat]_
                amount: int. _Amount of airtime to be bought_

        Raises:
            ValueError: error raised if parameters are not accurate

        Returns:
            AirtimeResponse: 
        """

        if not parameters or type(parameters) is not dict:
            raise ValueError("parameters property required as a dictionary")

        response = cls().request.call_api(
            endpoint="airtime",
            params=parameters,
            params_model=AirtimeModel
        )

        return AirtimeResponse( **response)

    @classmethod
    def available():
        pass