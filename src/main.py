import os
import dotenv
from uploader import Uploader
import requests, json

def main():
    # Initialize env variables
    dotenv.load_dotenv()
    SEED_PHRASE = os.getenv("SEED_PHRASE")
    PASSWORD = os.getenv("PASSWORD")

    Initialize
    uploader = Uploader()
    uploader.connect_metamask(SEED_PHRASE, PASSWORD)

    # Connect to the specified network - ENTER THE APPROPRIATE NETWORK
    NETWORK_RPC = os.getenv("NETWORK_RPC")
    CHAIN_ID = os.getenv("CHAIN_ID")
    uploader.set_network(NETWORK_RPC, CHAIN_ID) # Custom network to add to Metamask
    uploader.open_metamask()
    uploader.set_network("", 0, 1) # Use a default network provided by Metamask

    # Connect to OpenSea
    uploader.connect_opensea(test=True)
    COLLECTION_URL = os.getenv("COLLECTION_URL")
    uploader.set_collection_url(COLLECTION_URL)

    baseURI = "https://zxerrorart.mypinata.cloud/ipfs/"

    tierURIs = [
      "QmdvLjh5ABv7soF4pVayFEfSh53aYVQNNzk8Nhv4JFmUun/",
      # "QmVySf9khuDRujVydpMbDTMFDWyMc9NFQLzpuD1ZLygrNZ/",
      # "Qmcd9HRe7hdH7v9Dy1EoP68Epmy3WVpK4fCBdTYL7Q4Raw/",
      # "QmWas69B2ndXW1xVr6FQ7z7xcWSEP32GUDviEM5HC4bTiE/",
      # "QmdLRVofw8STqmdkfZdLkGGsWDRg4oAL5WcUnG5Hfvn6TU/",
      # "QmRj73gGSmUMPbmh45ZpLhMo9C4S7J89XtFziqKFuLyckz/"
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
    for i, tierURI in enumerate(tierURIs):
      for tokenID in range(1, tokensPerTier[i]):
        url = baseURI + tierURI + str(tokenID) + ".json"
        print(url)
        response = requests.get(url)
        text = response.text
        data = json.loads(text)
        print(data["name"])
        metadata.append(data)

    try:
      uploader.upload(metadata)
      uploader.sign_transaction()
    except Exception as e:
      print(f"Failed to upload NFT {i} '{data['name']}' for reason '{e}'.")

    # Close
    uploader.close()

# Run main if this file is run directly
if __name__ == "__main__":
    main()