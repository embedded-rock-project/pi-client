import requests, threading

"""
RockDection class is meant to send data
"""
class RockDetection:
    """
    Init takes in a post_route (string)
    If empty or no string given then post route will be set as an empty string
    """
    def __init__(self, post_route: str = "") -> None:
        if isinstance(post_route, str):  
            self.post_route = post_route
        else:
            self.post_route = ""
        
    """
    Creates a thread for the post request (meant for slow respones)
    """
    def send_post(self, post_route: str = None, data: dict = None) -> None:
        if not isinstance(post_route, str):
            if self.post_route != "":
                r = threading.Thread(target=self.__send_post_json, args=(self.post_route, data)).start()
            else:
                pass
        else:
            threading.Thread(target=self.__send_post_json, args=(post_route, data)).start()

    """
    This function is explictly not suppose to be used outside the class
    Sends data through a given post route
    """
    def __send_post_json(self, post_route: str = None, data: dict = None) -> None:
        if isinstance(post_route, str):
            if isinstance(data, dict):
                r = requests.post(post_route, json=data)
                # r.json() returns the returned json data from the server
                if r.status_code == 200:
                    print("Request was complete successfully.")
                else:
                    print("{} {}.\n {}".format(
                        "Warning: the status code return was",
                        r.status_code,
                        "This may be because of an underlining issue with the server."))
            else:
                print("ERROR: Data must be a dict or not be empty.")
        else:
            print("ERROR: Post url must be a string or not be empty.")


client = RockDetection("http://localhost:5000/data") # sets the default post route to the string given
client.send_post(data={'data': 'something'}) #sends data to post route