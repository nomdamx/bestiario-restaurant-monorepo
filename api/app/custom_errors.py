class AppError(Exception):
    default_error = "Application Error"
    default_message = "An error ocurred"
    default_status_code = 500

    def __init__(self,* ,error:str = None, message:str = None, status_code:int = None, details:str = None, extra:dict = None):
        self.error = error or self.default_error
        self.message = message or self.default_message
        self.details = details or ""
        self.status_code = status_code or self.default_status_code
        self.extra = extra or {}

class ValidationError(AppError):
    default_error = "Validation Error"
    default_message = "Invalid data provided"
    default_status_code = 422

class DatabaseError(AppError):
    default_error = "Database Error"
    default_message = "A database operation has failed"
    default_status_code = 500
        
class ArgsError(AppError):
    default_error = "Attribute Error"
    default_message = "Invalid attribute in query"
    default_status_code = 500

class VersionError(AppError):
    default_error = "API Version Error"
    default_message = "Invalid Versioning in API"
    default_status_code = 500
        
class InvalidIDError(AppError):
    default_error = "ID Error"
    default_message = "Invalid ID provided"
    default_status_code = 500

class InvalidFile(AppError):
    default_error = "File Error"
    default_message = "Invalid File Provided"
    default_status_code = 500