from ebills.rest import RestClient
from ebills.models import DataModel, DataResponse

class Data:
    """Buy mobile data using ebills api

    """
    def __init__(self):
        request = RestClient()
        self.request = request

    @classmethod
    def buy(cls, parameters: dict) -> DataResponse:
        """method to buy mobile data

        Args:
            parameters (dict):
                phone: str. _Phone number for refrence length of 11 numbers_

                network_id: str. _Network type [mtn, glo, airtel, etisalat]_
                
                variation_id: str. _Type of mobile data plan_
                    [ 500 , M1024 , M2024 , 3000 , 5000 , 10000 , 
                    mtn-20hrs-1500 , mtn-30gb-8000 , mtn-40gb-10000 , 
                    mtn-75gb-15000 , glo100x , glo200x , G500 , G2000 , 
                    G1000 , G2500 , G3000 , G4000 , G5000 , G8000 , glo10000 , 
                    airt-1100 , airt-1300 , airt-1650 , airt-2200 , airt-3300 , 
                    airt-5500 , airt-11000 , airt-330x , airt-550 , airt-500x , 
                    airt-1650-2 , 9MOB1000 , 9MOB34500 , 9MOB8000 , 9MOB5000 ]
                
        Raises:
            ValueError: error raised if parameters are not accurate

        Returns:
            DataResponse: 
        """

        if not parameters or type(parameters) is not dict:
            raise ValueError("parameters property required as a dictionary")

        response = cls().request.call_api(
            endpoint="data",
            params=parameters,
            params_model=DataModel
        )

        return DataResponse( **response)
    
    @classmethod
    def available():
        pass