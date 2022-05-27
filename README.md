# Lukka Tron Support 


### Check Lukka Bitquery Tron GraphQL query support
Check the web application hosted in 
### https://share.streamlit.io/sayonnnnnn/lukka/main/lukka.py 

### GraphQL query 
```
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
```
