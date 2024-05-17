from ebills.rest import RestClient
from ebills.models import VerifyModel, VerifyResponse

class Verify:
    """Buy mobile data using ebills api

    """
    def __init__(self):
        request = RestClient()
        self.request = request

    @classmethod
    def verify(cls, parameters: dict) -> VerifyResponse:
        """method to verify cable and electric bill customer

        Args:
            parameters (dict):
                customer_id: str. _meter or smartcard number length of 10-11 numbers_

                service_id: str. _cable type with options_ 
                    [ dstv , gotv , startimes , abuja-electric , 
                    eko-electric , ibadan-electric , ikeja-electric , 
                    jos-electric , kaduna-electric , kano-electric , portharcout-electric ]

                variation_id: Optional[str]. _Type of electric bill _
                    [ prepaid ,  postpaid ]
                
        Raises:
            ValueError: error raised if parameters are not accurate

        Returns:
            VerifyResponse:
        """

        if not parameters or type(parameters) is not dict:
            raise ValueError("parameters property required as a dictionary")

        response = cls().request.call_api(
            endpoint="data",
            params=parameters,
            params_model=VerifyModel
        )

        return VerifyResponse( **response)