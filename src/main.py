import os
import dotenv
from uploader import Uploader
import requests, json

def main():
    # Initialize env variables
    dotenv.load_dotenv()
    
    SEED_PHRASE = os.getenv("SEED_PHRASE")
    PASSWORD = os.getenv("PASSWORD")
    NETWORK_LINK_POSITION = os.getenv("NETWORK_LINK_POSITION") # 4 is Rinkeby, 1 is Mainnet
    TIER_START = os.getenv("TIER_START")
    TIER_STOP = os.getenv("TIER_STOP")
    TOKEN_START = os.getenv("TOKEN_START")
    TOKEN_STOP = os.getenv("TOKEN_STOP")

    tierStart = 0 if not TIER_START.isdigit() else int(TIER_START)
    tierStop = 0 if not TIER_STOP.isdigit() else int(TIER_STOP)
    tokenStart = 0 if not TOKEN_START.isdigit() else int(TOKEN_START)
    tokenStop = 0 if not TOKEN_STOP.isdigit() else int(TOKEN_STOP)

    baseURI = "https://zxerrorart.mypinata.cloud/ipfs/"

    tierURIs = [
      "QmdvLjh5ABv7soF4pVayFEfSh53aYVQNNzk8Nhv4JFmUun/",
      "QmVySf9khuDRujVydpMbDTMFDWyMc9NFQLzpuD1ZLygrNZ/",
      "Qmcd9HRe7hdH7v9Dy1EoP68Epmy3WVpK4fCBdTYL7Q4Raw/",
      "QmWas69B2ndXW1xVr6FQ7z7xcWSEP32GUDviEM5HC4bTiE/",
      "QmdLRVofw8STqmdkfZdLkGGsWDRg4oAL5WcUnG5Hfvn6TU/",
      "QmRj73gGSmUMPbmh45ZpLhMo9C4S7J89XtFziqKFuLyckz/"
    ]

    tokensPerTier = [
      24,
      24,
      512,
      1024,
      2048,
      4096
    ]

    metadata = []
    tierStart = tierStart - 1 if tierStart > 0 else 1
    tierStop = tierStop if 0 < tierStop <= len(tiersURIs) else len(tierURIs)
    for i in range(tierStart, tierStop):
      tierURI = tierURIs[i]
      tokenStart = tokenStart - 1 if tokenStart > 0 else 1
      tokenStop = tokenStop + 1 if tokenStop > 0 and tierStop > 0 and i == tierStop - 1 else tokensPerTier[i]
      for tokenID in range(tokenStart, tokenStop):
        url = baseURI + tierURI + str(tokenID) + ".json"
        print(url)
        response = requests.get(url)
        text = response.text
        data = json.loads(text)
        print(data["name"])
        metadata.append(data)

    # Initialize
    uploader = Uploader()
    uploader.connect_metamask(SEED_PHRASE, PASSWORD)

    # Connect to the specified network - ENTER THE APPROPRIATE NETWORK
    NETWORK_RPC = os.getenv("NETWORK_RPC")
    CHAIN_ID = os.getenv("CHAIN_ID")
    uploader.set_network(NETWORK_RPC, CHAIN_ID, NETWORK_LINK_POSITION) # Custom network to add to Metamask
    uploader.open_metamask()
    # uploader.set_network("", 0, 1) # Use a default network provided by Metamask

    # Connect to OpenSea
    uploader.connect_opensea(test=True)
    COLLECTION_URL = os.getenv("COLLECTION_URL")
    uploader.set_collection_url(COLLECTION_URL)

    uploader.upload(metadata)

    # Close
    uploader.close()

# Run main if this file is run directly
if __name__ == "__main__":
    main()