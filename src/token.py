class Token:

    def __init__(self, api_key: str, api_secret: str, access_key: str, access_secret: str):
        self.__api_key = api_key
        self.__api_secret = api_secret
        self.__access_key = access_key
        self.__access_secret = access_secret

    @property
    def api_key(self):
        return self.__api_key

    @property
    def api_secret(self):
        return self.__api_secret

    @property
    def access_key(self):
        return self.__access_key

    @property
    def access_secret(self):
        return self.__access_secret
