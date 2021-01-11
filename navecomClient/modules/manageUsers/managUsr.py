from django.contrib.auth import authenticate, login, logout

class ManagUsr():

    def loggin(self,request, usr, passw):
        user = authenticate(request, username=usr, password=passw)
        if user is not None:
            try:
                login(request, user)
                return user
            except Exception as error:
                print("error al iniciar sesion : " , error)
                return False
        else:
            return False
    
    def logOut(self, request):
        logout(request)
        return True

