import os
import dotenv
from uploader import Uploader
import requests, json

def main():
    # Initialize env variables
    dotenv.load_dotenv()
    SEED_PHRASE = os.getenv("SEED_PHRASE")
    PASSWORD = os.getenv("PASSWORD")
    NETWORK_LINK_POSITION = os.getenv("NETWORK_LINK_POSITION")
    if os.getenv("TIER_START").isdigit():
        TIER_START = int(os.getenv("TIER_START"))
    else:
        TIER_START = 0
    if os.getenv("TIER_STOP").isdigit():
        TIER_STOP = int(os.getenv("TIER_STOP"))
    else:
        TIER_STOP = 0
    if os.getenv("TOKEN_START").isdigit():
        TOKEN_START = int(os.getenv("TOKEN_START"))
    else:
        TOKEN_START = 0
    if os.getenv("TOKEN_STOP").isdigit():
        TOKEN_STOP = int(os.getenv("TOKEN_STOP"))
    else:
        TOKEN_STOP = 0
    # For NETWORK_LINK_POSITION, 4 is Rinkeby, 1 is Mainnet - so value should be changed to 1 in .env on mainnet

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
    tierStart = TIER_START - 1 if TIER_START > 0 else 1
    tierStop = TIER_STOP if TIER_STOP > 0 else len(tierURIs)
    for i in range(tierStart, tierStop):
      tierURI = tierURIs[i]
      tokenStart = TOKEN_START - 1 if TOKEN_START > 0 else 1
      tokenStop = TOKEN_STOP + 1 if TOKEN_STOP > 0 and TIER_STOP > 0 and i == TIER_STOP - 1 else tokensPerTier[i]
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