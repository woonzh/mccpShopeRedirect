# Shopee seller authorisation

## Steps
1) Go to https://mccptester.herokuapp.com/shopee and click submit
2) You will be redirected to the shopee seler login page
3) After login you will be redirected back to mccptester website with the relevant credentials (if successful)

## Code
Refer to mccpAPI.py and shopee.py

### mccpAPI.py
class ShopeeURL: This is the API call that returns the encoded shopee URL to be redirected to. Go to shopee.py to see the generation of the URL
class ShopeeRedirect: This is the handler for the api callback from shopee. It will return the shopID if successful and an error msg if unsuccessful

### Shopee.py
Shows the generation of the url for the first redirect (from mccptester to shopee for seller login).

The credentials such as key etc. is extracted from the shopee partners page, after login
