from typing import Any
import requests
from ebills import username, password
from ebills.models.verify import VerifyModel



class RestClient:
    """Make request to the api directly with this class

    """
    def __init__(self):
        self.base_url = "https://ebills.ng/wp-json/api/v1/"


        self.query = {
            "username": username,
            "password": password
        }

    # method to access api endpoint
    @classmethod
    def call_api(cls, endpoint:str="balance", params:dict=None, params_model:Any=None) -> dict:
        """GET method to api

        Args:
            endpoint (str, optional): Specify the api endpoint to access. _Defaults to balance_

            params (dict, optional): Query parameters required by the specified endpoint. _Defaults to None_

            params_model (Any, optional): Pydantic model of the query parameter. _Defaults to None_

        Raises:
            ValueError: returns error if endpoint is defined and params is not

        Returns:
            _type_: _description_
        """

        if endpoint != "balance" and not params:
            raise ValueError("parameters incomplete or empty")

        if params_model:

            params = params_model( **params).dict()
            pop_key = None
            for k, v in params.items():
                if v is None and params_model is VerifyModel:
                    pop_key = k
                    continue

                if v is None:
                    raise ValueError("parameters incomplete or empty")

            if pop_key:
                params.pop(pop_key)

            cls().query.update(params)

        query = "" 
        for k, v in cls().query.items():
            query += f"&{k}={v}"
        

        url = f"{cls().base_url}{endpoint}?{query[1:]}"
        response = requests.request(method="GET", url=url)

        return response.json()

