from ebills.rest import RestClient
from ebills.models import ElectricModel, ElectricResponse

class Electricity:
    """Pay for electric bills

    """
    def __init__(self):
        request = RestClient()
        self.request = request

    @classmethod
    def buy(cls, parameters: dict) -> ElectricResponse:
        """method to pay electric bill

        Args:
            parameters (dict):
                phone: str. _Phone number for refrence length of 11 numbers_

                service_id: str. _bill type with options 
                    [ abuja-electric , eko-electric , ibadan-electric , 
                    ikeja-electric , jos-electric , kaduna-electric , 
                    kano-electric , portharcout-electric ]_

                meter_number: str. _Prepaid or postpaid meter number length of 11 numbers_

                variation_id: str. _Type of electric bill plan_
                    [ prepaid ,  postpaid ]
                
                amount: int. _Price of kW to purchase_
        Raises:
            ValueError: error raised if parameters are not accurate

        Returns:
            ElectricResponse: 
        """

        if not parameters or type(parameters) is not dict:
            raise ValueError("parameters property required as a dictionary")

        response = cls().request.call_api(
            endpoint="electricity",
            params=parameters,
            params_model=ElectricModel
        )

        return ElectricResponse( **response)


    @classmethod
    def available():
        pass