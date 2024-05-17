from ebills.rest import RestClient
from ebills.models import CableModel, CableResponse

class Cable:
    """Buy airtime using ebills api

    """
    def __init__(self):
        request = RestClient()
        self.request = request

    @classmethod
    def buy(cls, parameters: dict) -> CableResponse:
        """method to subscribe to cable tv

        Args:
            parameters (dict):
                phone: str. _Phone number for refrence length of 11 numbers_

                service_id: str. _cable type with options [dstv, gotv, startimes]_

                smartcard_number: str. _Tv decoder number length of 10 numbers_

                variation_id: str. _Type of cable tv plan_
                    [ dstv-padi , dstv-yanga , dstv-confam , dstv6 , dstv79 , dstv7 ,
                      dstv3 , dstv10 , dstv9 , confam-extra , yanga-extra , padi-extra , 
                      com-asia , dstv30 , com-frenchtouch , dstv33 , dstv40 , com-frenchtouch-extra ,
                      com-asia-extra , dstv43 , complus-frenchtouch , dstv45 , complus-french-extraview ,
                      dstv47 , dstv48 , dstv61 , dstv62 , hdpvr-access-service , frenchplus-addon , 
                      asia-addon , frenchtouch-addon , extraview-access , french11 , gotv-smallie , gotv-jinja ,
                      gotv-jolli , gotv-max , gotv-supa , nova , basic , smart , classic , super ]
                
        Raises:
            ValueError: error raised if parameters are not accurate

        Returns:
            CableResponse: 
        """

        if not parameters or type(parameters) is not dict:
            raise ValueError("parameters property required as a dictionary")

        response = cls().request.call_api(
            endpoint="tv",
            params=parameters,
            params_model=CableModel
        )

        return CableResponse( **response)


    @classmethod
    def available():
        pass