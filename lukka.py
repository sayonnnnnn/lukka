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


def lukkaRun(query, variables):
	result = bitqueryAPICall(query, variables)
	st.write(result)

	feesAmount, feesFee = [], []
	for i in result['data']['tron']['fees']:
		feesAmount.append(i['count'])
		feesFee.append(i['fee'])

	inAmount, inCurrencyTokenType, inCurrencyAddress, inCurrencyName, inCurrencySymbol = [], [], [], [], []
	for j in result['data']['tron']['in']:
		inAmount.append(j['amount'])
		inCurrencyTokenType.append(j['currency']['tokenType'])
		inCurrencyAddress.append(j['currency']['address'])
		inCurrencyName.append(j['currency']['name'])
		inCurrencySymbol.append(j['currency']['symbol']) 

	outAmount, outCurrencyTokenType, outCurrencyAddress, outCurrencyName, outCurrencySymbol = [], [], [], [], []
	for k in result['data']['tron']['out']:
		# for ss in k:
		outAmount.append(k['amount'])
		outCurrencyTokenType.append(k['currency']['tokenType'])
		outCurrencyAddress.append(k['currency']['address'])
		outCurrencyName.append(k['currency']['name'])
		outCurrencySymbol.append(k['currency']['symbol']) 

	stakeAmount, stakeContractType = [], [] 
	for l in result['data']['tron']['stake']: 
		stakeAmount.append(l['amount'])
		stakeContractType.append(l['contractType'])

	UnstakeAmount, UnstakeContractType = [], [] 
	for m in result['data']['tron']['Unstake']: 
		UnstakeAmount.append(m['amount'])
		UnstakeContractType.append(m['contractType'])

	addresses = [] 
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
	csv1 = convert_df(dfFees)

	st.download_button(
	   "Press to Download",
	   csv1,
	   "fileFees.csv",
	   "text/csv",
	   key='download-csv'
	)

	st.subheader('In')
	st.dataframe(dfIn)
	csv2 = convert_df(dfIn)

	st.download_button(
	   "Press to Download",
	   csv2,
	   "fileIn.csv",
	   "text/csv",
	   key='download-csv'
	)


	st.subheader('Out')
	st.dataframe(dfOut)
	csv3 = convert_df(dfOut)

	st.download_button(
	   "Press to Download",
	   csv3,
	   "fileOut.csv",
	   "text/csv",
	   key='download-csv'
	)


	st.subheader('Stake')
	st.dataframe(dfStake)
	csv4 = convert_df(dfStake)

	st.download_button(
	   "Press to Download",
	   csv4,
	   "fileStake.csv",
	   "text/csv",
	   key='download-csv'
	)


	st.subheader('Unstake')
	st.dataframe(dfUnStake)
	csv7 = convert_df(dfUnStake)

	st.download_button(
	   "Press to Download",
	   csv7,
	   "fileUnstake.csv",
	   "text/csv",
	   key='download-csv'
	)

	st.subheader('Address')
	st.dataframe(dfAddress)
	csv8 = convert_df(dfAddress)

	st.download_button(
	   "Press to Download",
	   csv8,
	   "fileAddress.csv",
	   "text/csv",
	   key='download-csv'
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

	while True:
		lukkaRun(query, variables)
		time.sleep(1800)

	# schedule.every(30).minutes.do(lukkaRun(query, variables))

