from flask import Response

from app.custom_errors import AppError

class APIResponse:
    def __init__(self, response:list | Response = [], type:str = None, pagination_data:dict = None, error:AppError = None) -> None:
        if isinstance(response,Response):
            return response.get_json()

        self.response = response
        self.type = type
        self.pagination_data = pagination_data
        self.error = error

        self._size = len(self.response) if not isinstance(self.response, Response) else 1

    def get_response(self):
        return {
            "response":["Base Response"],
            "metadata":{
                "type":"schema",
                "size":self._size,
                "api_version":"v0",
                "type_response":"list",
                "pagination":{
                    "page":self.pagination_data.get("page",0),
                    "pages":self.pagination_data.get("pages",0),
                    "limit":self.pagination_data.get("limit",0),
                    "total":self.pagination_data.get("total",0)
                }
            }
        }
    
    def get_error_response(self):
        return {
            "data": [],
            "metadata": {
                "context": self.error.extra.get("context", ""),
                "error": self.error.error,
                "message": self.error.message,
                "details": self.error.details,
                **{k: v for k, v in self.error.extra.items() if k != "context"}
            }
        }

class APIResponseV1(APIResponse):
    def get_response(self):
        return {
            "response":self.response,
            "metadata":{
                "type":self.type,
                "size":self._size,
                "api_version":"v1",
                "type_response":"list",
                "pagination":{
                    "page":self.pagination_data.get("page",0),
                    "pages":self.pagination_data.get("pages",0),
                    "limit":self.pagination_data.get("limit",0),
                    "total":self.pagination_data.get("total",0)
                }
            }
        }
    
version_list:dict[str,APIResponse] = {
    "v1": APIResponseV1,
}

def get_version(version:str = None) -> APIResponse:
    if not version:
        return APIResponseV1
    
    return version_list.get(version,APIResponseV1)