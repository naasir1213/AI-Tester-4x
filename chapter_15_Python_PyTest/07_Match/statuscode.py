status=501

match status:
      case 200 | 201:
          print("Request Successful")
      case 300:
          print("Redirection")
      case 400:
          print("Bad Request")
      case 401:
          print("Unauthorized")
      case 403:
          print("Forbidden")
      case 404:
          print("Not Found")
      case 500:
          print("Internal Server Error")
      case  _:
          print("Unknown Status")