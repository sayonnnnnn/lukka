import streamlit as st 
import pandas as pd 
import requests 
import schedule
import time 

st.set_page_config (
    page_title="Lukka 30 Minutes",
    page_icon="random",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.subheader('The GraphQL query that is being executed')

# query = """
# query ($address: String!, $limit: Int!, $since: ISO8601DateTime) {
#   tron {
#     fees: contracts(
#       txOwner: {is: $address}
#       time: {since: $since}
#       options: {limit: $limit}
#     ) {
#       count
#       fee
#     }
#     in: transfers(receiver: {is: $address}) {
#       amount
#       currency {
#         name
#         address
#         symbol
#         tokenType
#         tokenId
#       }
#     }
#     out: transfers(sender: {is: $address}, receiver: {not: "system"}) {
#       amount
#       currency {
#         name
#         address
#         symbol
#         tokenType
#         tokenId
#       }
#     }
#     stake: contracts(txOwner: {is: $address}, contractType: {in: FreezeBalance}) {
#       amount
#       contractType
#     }
#     Unstake: contracts(txOwner: {is: $address}, contractType: {in: UnfreezeBalance}) {
#       amount
#       contractType
#     }
#     address(address: {in: [$address]}) {
#       claimableRewards
#     }
#   }
# }
# """

# variables = {
#   "address": "TCSqaoB1T52VStbXTdZgaJWc8nE6kAAkXo",
#   "limit": 11,
#   "since": "2022-04-17"
# }

# st.code(query, language='javascript')


def bitqueryAPICall(query: str, variables):  
    headers = {'X-API-KEY': 'BQY382aeV9EQUU7qZQAH8yVAcT6vXjYQ'}
    request = requests.post('https://graphql.bitquery.io/',
                            json={'query': query, 'variables': variables}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed and return code is {}.      {}'.format(request.status_code,query))

# result = bitqueryAPICall(query) 
# print(result)

# fees // count, fee
# in // amount, currency.name, currency.address, currency.symbol, currency.tokenType 
# out // amount, currency.name, currency.address, currency.symbol, currency.tokenType 
# stake // amount, contractType 
# Unstake // amount, contractType 
# address // claimableRewards 

def convert_df(df):
   return df.to_csv().encode('utf-8')

feesAmount, feesFee = [], []
stakeAmount, stakeContractType = [], []
inAmount, inCurrencyTokenType, inCurrencyAddress, inCurrencyName, inCurrencySymbol = [], [], [], [], []
outAmount, outCurrencyTokenType, outCurrencyAddress, outCurrencyName, outCurrencySymbol = [], [], [], [], []
UnstakeAmount, UnstakeContractType = [], []
addresses = []


def lukkaRun(query, variables):
	result = bitqueryAPICall(query, variables)
	st.write(result)

	# feesAmount, feesFee = [], []
	for i in result['data']['tron']['fees']:
		feesAmount.append(i['count'])
		feesFee.append(i['fee'])

	# inAmount, inCurrencyTokenType, inCurrencyAddress, inCurrencyName, inCurrencySymbol = [], [], [], [], []
	for j in result['data']['tron']['in']:
		inAmount.append(j['amount'])
		inCurrencyTokenType.append(j['currency']['tokenType'])
		inCurrencyAddress.append(j['currency']['address'])
		inCurrencyName.append(j['currency']['name'])
		inCurrencySymbol.append(j['currency']['symbol']) 

	# outAmount, outCurrencyTokenType, outCurrencyAddress, outCurrencyName, outCurrencySymbol = [], [], [], [], []
	for k in result['data']['tron']['out']:
		# for ss in k:
		outAmount.append(k['amount'])
		outCurrencyTokenType.append(k['currency']['tokenType'])
		outCurrencyAddress.append(k['currency']['address'])
		outCurrencyName.append(k['currency']['name'])
		outCurrencySymbol.append(k['currency']['symbol']) 

	# stakeAmount, stakeContractType = [], [] 
	for l in result['data']['tron']['stake']: 
		stakeAmount.append(l['amount'])
		stakeContractType.append(l['contractType'])

	# UnstakeAmount, UnstakeContractType = [], [] 
	for m in result['data']['tron']['Unstake']: 
		UnstakeAmount.append(m['amount'])
		UnstakeContractType.append(m['contractType'])

	# addresses = [] 
	for n in result['data']['tron']['address']:
		addresses.append(n['claimableRewards'])

	dfFees = pd.DataFrame(list(zip(feesAmount, feesFee)), columns=['Count', 'Fee'], dtype=float)
	dfIn = pd.DataFrame(list(zip(inAmount, inCurrencyName, inCurrencySymbol, inCurrencyAddress, inCurrencyTokenType)), columns=['Amount', 'Currency Name', 'Currency Symbol', 'Cuurency Address', 'Currency Token Type'])
	dfOut = pd.DataFrame(list(zip(outAmount, outCurrencyName, outCurrencySymbol, outCurrencyAddress, outCurrencyTokenType)), columns=['Amount', 'Currency Name', 'Currency Symbol', 'Cuurency Address', 'Currency Token Type'])
	dfStake = pd.DataFrame(list(zip(stakeAmount, stakeContractType)), columns=['Stake Amount', 'Stake Contract Type'])
	dfUnStake = pd.DataFrame(list(zip(UnstakeAmount, UnstakeContractType)), columns=['Unstake Amount', 'Unstake Contract Type'])
	dfAddress = pd.DataFrame(addresses, columns=['Claimable Rewards'])

	st.subheader('Fees')
	st.dataframe(dfFees)
	# csv1 = convert_df(dfFees)

	# st.download_button(
	#    "Press to Download",
	#    csv1,
	#    "fileFees.csv",
	#    "text/csv",
	#    key='download-csv'
	# )

	st.subheader('In')
	st.dataframe(dfIn)
	# csv2 = convert_df(dfIn)

	# st.download_button(
	#    "Press to Download",
	#    csv2,
	#    "fileIn.csv",
	#    "text/csv",
	#    key='download-csv'
	# )


	st.subheader('Out')
	st.dataframe(dfOut)
	# csv3 = convert_df(dfOut)

	# st.download_button(
	#    "Press to Download",
	#    csv3,
	#    "fileOut.csv",
	#    "text/csv",
	#    key='download-csv'
	# )


	st.subheader('Stake')
	st.dataframe(dfStake)
	# csv4 = convert_df(dfStake)

	# st.download_button(
	#    "Press to Download",
	#    csv4,
	#    "fileStake.csv",
	#    "text/csv",
	#    key='download-csv'
	# )


	st.subheader('Unstake')
	st.dataframe(dfUnStake)
	# csv7 = convert_df(dfUnStake)

	# st.download_button(
	#    "Press to Download",
	#    csv7,
	#    "fileUnstake.csv",
	#    "text/csv",
	#    key='download-csv'
	# )

	st.subheader('Address')
	st.dataframe(dfAddress)
	# csv8 = convert_df(dfAddress)

	# st.download_button(
	#    "Press to Download",
	#    csv8,
	#    "fileAddress.csv",
	#    "text/csv",
	#    key='download-csv'
	# )

	return dfFees, dfIn, dfOut, dfStake, dfAddress, dfUnStake

def lukkaAppend(query, variables, dfFees, dfIn, dfOut, dfStake, dfAddress, dfUnStake, keyy: int):
	res = bitqueryAPICall(query, variables)
	feesAmount1, feesFee1 = [], []
	for i in res['data']['tron']['fees']:
		feesAmount1.append(i['count'])
		feesFee1.append(i['fee'])

	inAmount1, inCurrencyTokenType1, inCurrencyAddress1, inCurrencyName1, inCurrencySymbol1 = [], [], [], [], []
	for j in res['data']['tron']['in']:
		inAmount1.append(j['amount'])
		inCurrencyTokenType1.append(j['currency']['tokenType'])
		inCurrencyAddress1.append(j['currency']['address'])
		inCurrencyName1.append(j['currency']['name'])
		inCurrencySymbol1.append(j['currency']['symbol']) 

	outAmount1, outCurrencyTokenType1, outCurrencyAddress1, outCurrencyName1, outCurrencySymbol1 = [], [], [], [], []
	for k in res['data']['tron']['out']:
		# for ss in k:
		outAmount1.append(k['amount'])
		outCurrencyTokenType1.append(k['currency']['tokenType'])
		outCurrencyAddress1.append(k['currency']['address'])
		outCurrencyName1.append(k['currency']['name'])
		outCurrencySymbol1.append(k['currency']['symbol']) 

	stakeAmount1, stakeContractType1 = [], [] 
	for l in res['data']['tron']['stake']: 
		stakeAmount1.append(l['amount'])
		stakeContractType1.append(l['contractType'])

	UnstakeAmount1, UnstakeContractType1 = [], [] 
	for m in res['data']['tron']['Unstake']: 
		UnstakeAmount1.append(m['amount'])
		UnstakeContractType1.append(m['contractType'])

	addresses1 = [] 
	for n in res['data']['tron']['address']:
		addresses1.append(n['claimableRewards'])

	dfFees1 = pd.DataFrame(list(zip(feesAmount1, feesFee1)), columns=['Count', 'Fee'], dtype=float)
	dfIn1 = pd.DataFrame(list(zip(inAmount1, inCurrencyName1, inCurrencySymbol1, inCurrencyAddress1, inCurrencyTokenType1)), columns=['Amount', 'Currency Name', 'Currency Symbol', 'Cuurency Address', 'Currency Token Type'])
	dfOut1 = pd.DataFrame(list(zip(outAmount1, outCurrencyName1, outCurrencySymbol1, outCurrencyAddress1, outCurrencyTokenType1)), columns=['Amount', 'Currency Name', 'Currency Symbol', 'Cuurency Address', 'Currency Token Type'])
	dfStake1 = pd.DataFrame(list(zip(stakeAmount1, stakeContractType1)), columns=['Stake Amount', 'Stake Contract Type'])
	dfUnStake1 = pd.DataFrame(list(zip(UnstakeAmount1, UnstakeContractType1)), columns=['Unstake Amount', 'Unstake Contract Type'])
	dfAddress1 = pd.DataFrame(addresses1, columns=['Claimable Rewards'])

	# dfFees.append(dfFees1)
	# dfAddress.append(dfAddress1)
	# dfIn.append(dfIn1)
	# dfOut.append(dfOut1)
	# dfStake.append(dfStake1)
	# dfUnStake.append(dfUnStake1)

	st.subheader('Fees')
	st.dataframe(dfFees1)
	csv1 = convert_df(dfFees1)

	st.download_button(
	   "Press to Download",
	   csv1,
	   "fileFees.csv",
	   "text/csv", 
	   key = keyy-1
	)

	st.subheader('In')
	st.dataframe(dfIn1)
	csv2 = convert_df(dfIn1)

	st.download_button(
	   "Press to Download",
	   csv2,
	   "fileIn.csv",
	   "text/csv",
	   key = keyy-2
	)


	st.subheader('Out')
	st.dataframe(dfOut1)
	csv3 = convert_df(dfOut1)

	st.download_button(
	   "Press to Download",
	   csv3,
	   "fileOut.csv",
	   "text/csv",
	   key = keyy-3
	)


	st.subheader('Stake')
	st.dataframe(dfStake1)
	csv4 = convert_df(dfStake1)

	st.download_button(
	   "Press to Download",
	   csv4,
	   "fileStake.csv",
	   "text/csv",
	   key = keyy-4
	)


	st.subheader('Unstake')
	st.dataframe(dfUnStake1)
	csv7 = convert_df(dfUnStake1)

	st.download_button(
	   "Press to Download",
	   csv7,
	   "fileUnstake.csv",
	   "text/csv",
	   key = keyy-5
	)

	st.subheader('Address')
	st.dataframe(dfAddress1)
	csv8 = convert_df(dfAddress1)

	st.download_button(
	   "Press to Download",
	   csv8,
	   "fileAddress.csv",
	   "text/csv",
	   key = keyy-6
	)



if __name__ == '__main__':
	query = """
	query ($address: String!, $limit: Int!, $since: ISO8601DateTime) {
	  tron {
	    fees: contracts(
	      txOwner: {is: $address}
	      time: {since: $since}
	      options: {limit: $limit}
	    ) {
	      count
	      fee
	    }
	    in: transfers(receiver: {is: $address}) {
	      amount
	      currency {
	        name
	        address
	        symbol
	        tokenType
	        tokenId
	      }
	    }
	    out: transfers(sender: {is: $address}, receiver: {not: "system"}) {
	      amount
	      currency {
	        name
	        address
	        symbol
	        tokenType
	        tokenId
	      }
	    }
	    stake: contracts(txOwner: {is: $address}, contractType: {in: FreezeBalance}) {
	      amount
	      contractType
	    }
	    Unstake: contracts(txOwner: {is: $address}, contractType: {in: UnfreezeBalance}) {
	      amount
	      contractType
	    }
	    address(address: {in: [$address]}) {
	      claimableRewards
	    }
	  }
	}
	"""

	variables = {
	  "address": "TCSqaoB1T52VStbXTdZgaJWc8nE6kAAkXo",
	  "limit": 11,
	  "since": "2022-04-17"
	}

	st.code(query, language='javascript')

	dfFees, dfIn, dfOut, dfStake, dfAddress, dfUnStake = lukkaRun(query, variables)

	i = 4320
	while True:
		# lukkaRun(query, variables)
		lukkaAppend(query, variables, dfFees, dfIn, dfOut, dfStake, dfAddress, dfUnStake, i)
		i -= 7 
		time.sleep(1800)

	# schedule.every(30).minutes.do(lukkaRun(query, variables))

