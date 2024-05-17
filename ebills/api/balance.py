from ebills.rest import RestClient
from ebills.models import BalanceResponse

class Balance:
    """Check ebills account balance

    """
    def __init__(self):
        request = RestClient()
        self.request = request

    @classmethod
    def check(cls) -> BalanceResponse:
        """method to check account balance

        Returns:
            BalanceResponse: 
        """

        response = cls().request.call_api(
            endpoint="balance"
        )

        return BalanceResponse( **response)
