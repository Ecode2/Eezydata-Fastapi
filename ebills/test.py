from ebills.models import AirtimeResponse, AirtimeModel
from ebills.models import DataResponse, DataModel
from ebills.models import VerifyResponse, VerifyModel
from ebills.models import CableResponse, CableModel
from ebills.models import ElectricResponse, ElectricModel

from pprint import pprint

username="Ecode2"
password="Elias_code11"


airtime1 = {"code":"success","message":"Airtime successfully delivered","data":{"network":"MTN","phone":"09123550994","amount":"NGN2000","order_id":"3100"}}
airtime2 = {"code":"failure","message":"Your wallet balance (NGN1067.65) is insufficient to make this airtime purchase of NGN2000","order_id":"3289"}
#response1 = AirtimeResponse.get_info(airtime1)


data_model = {"phone": "09123550994", "network_id": "mt", "variation_id": "M1024"}
data_response1 = {"code":"failure","message":"Invalid data variation_id. Please, crosscheck and enter the correct variation_id.","order_id":"3456"}
data_response2 = {"code":"success","message":"Data successfully delivered","data":{"network":"MTN","data_plan":"MTN Data 1GB – 30 Days","phone":"09123550994","amount":"NGN259","order_id":"2443"}}
#response1= DataModel( **data_model)
#response2= DataResponse.get_info(data_response2)

verify_mode = {"customer_id":62418234034, "service_id":"ikeja-electric", "variation_id":"prepaid"}
verify_response1 = {"code":"success","message":"Customer details successfully retrieved","data":{"customer_id":"62418234034","customer_name":"FIRSTNAME LASTNAME","customer_address":"10 Example Street, Town, State","customer_arrears":"0.00","decoder_status":None,"decoder_due_date":None,"decoder_balance":None}}
verify_response2 = {"code":"failure","message":"Invalid Meter Number"}
#response1 = VerifyModel( **verify_mode)
#response2 = VerifyResponse.get_info(verify_response2)

cable_mode = {"phone": "09060636536", "service_id":"gotv", "smartcard_number":"7032400086", "variation_id":"gotv-max"}
cable_response1 = {"code":"success","message":"Cable TV subscription successfully delivered","data":{"cable_tv":"GOtv","subscription_plan":"GOtv Max","smartcard_number":"7032400086","phone":"09123550994","amount":"NGN3280","amount_charged":"NGN3247.2","service_fee":"NGN0.00","order_id":"2876"}}
cable_response2 = {"code":"failure","message":"Invalid Smartcard Number","order_id":"3652"}
#response1 = CableModel( **cable_mode)
#response2 = CableResponse.get_info(cable_response1)

electric_mode = {"phone": "09060636536", "service_id":"ikeja-electric", "meter_number":"62418234034", "variation_id":"prepaid", "amount": 3000}
electric_response1 = {"code":"success","message":"Electricity bill successfully paid","data":{"electricity":"Ikeja (IKEDC)","meter_number":"62418234034","token":"Token: 5345 8765 3456 3456 1232","units":"47.79kwH","phone":"09123550994","amount":"NGN3000","amount_charged":"NGN2970","order_id":"4324"}}
electric_response2 = {"code":"failure","message":"Invalid Meter Number","order_id":"3907"}
#response1 = ElectricModel( **electric_mode)
#response2 = ElectricResponse.get_info(electric_response1)


#pprint( response1 )