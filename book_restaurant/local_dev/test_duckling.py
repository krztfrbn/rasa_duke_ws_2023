# importing the necesary packages 
import wit 
import logging
import duckling 

# initialize wit.ai instance using api-token 
access_token = "XWJMI5ASPWR2G55FXMBC5WMZ24XZHFKG"
#access_token = "RNTEUNMG3KKOOOJG46VIULTTZPWN7RZY"
client = wit.Wit(access_token) 

client.logger.setLevel(logging.WARNING)

# capturing numeric entity using raw text(example0) using wit.ai client instance 
example0 = "set an alarm tomorrow at 7am"
response = client.message(example0) 
print(response)


