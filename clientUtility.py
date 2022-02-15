from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin
import time
import base64
import requests


class Utility:
    def __init__(self) -> None:
        # Base ID for generating itemIds on the go
        self.baseId = "RandomEluvioItemId"
        # Base Url of the API end point
        self.baseUrl = "https://challenges.qluv.io/items/"
        # List of URLS to be sent
        self.listOfUrls = []
        #self.listOfUrls = np.zeros((numberoFItems,), dtype=np.uint64)

    def generateUrlWithIds(self, numberOfIds):
        """
        numberOfIds : It is the number of ids to which you want to send the request to. One URL per ID.
        """
        for i in range(numberOfIds):
            self.listOfUrls.append(urljoin(self.baseUrl, (self.baseId+str(i))))

    def baseEncode(self, itemId):
        """
        itemId : Encode itemid in to base64 format
        return : returns the encoded value of the string
        """
        try:
            sample_string_bytes = itemId.encode("ascii")
            base64_bytes = base64.b64encode(sample_string_bytes)
            base64_string = base64_bytes.decode("ascii")
            return base64_string
        except Exception as err:
            print("Error while encoding the itemId {0} and error is {1}".format(itemId, err))

    def generateRequest(self, url):
        """
        url : URL for a given item ID
        This method parses the itemID and adds authorization header to the request and returns the response object
        """
        try:
            itemId = url.rsplit('/', 1)[-1]
            header = self.baseEncode(itemId)
            dictHeader = {"Authorization": header}
            return requests.get(urljoin(self.baseUrl, itemId), headers=dictHeader)
        except Exception as err:
            # Not raising an exception because it will not send next requests if exception is raised
            print("Error while sending request on URL {0} and error is {1}".format(url, err))

    def sendRequest(self, numberIds):
        """
        numberIds: Total number of request IDS you want to query the API
        """
        try:
            # Generates the URL for the every item
            self.generateUrlWithIds(numberIds)
            # It sends 5 concurrent requests to API and 'pool.map' each thread to each item of the list
            # so that there are no unnessary queries to API end point 
            with ThreadPoolExecutor(max_workers=5) as pool:
                startTime = time.time()
                response_list = list(pool.map(self.generateRequest,self.listOfUrls))
                endTime = time.time()

            print("Total time taken for third option %s"%str(endTime-startTime))

            for item in response_list:
                if item.status_code != 200:
                    print("Status Code of request is {0} and URL is {1}".format(item.status_code, item.url))
                # Printing the response output
                print(item.text)

        except Exception as err:
            # Not raising an exception because it will not send next requests if exception is raised
            print("Error occured while performing get request {0}".format(err))


if __name__ == "__main__":
    numberOfId = 100
    obj = Utility()
    obj.sendRequest(numberOfId)

    
