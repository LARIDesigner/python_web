from django.http import Http404
from django.shortcuts import render
from .middlewares import Middlewares
from .serializers import UserSerializer,CustomTokenObtainParirSerializer, UserListSerializer, UserUpdateSerializer
from .permissions import ValidToken, ValidAdmin
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import UserModel
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
class CreateUserView(generics.CreateAPIView):
    
    model=UserModel

    serializer_class = UserSerializer

class CustomTokenObtainParirView (TokenObtainPairView): 
    serializer_class= CustomTokenObtainParirSerializer

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token=request.data.get("refresh_token")
        if refresh_token:
            try:
                token = refresh_token
                token.blacklist()
                return Response({"detail":"logout realizado com sucesso"},status=200)
            except Exception as e:
                return Response({"detail":"Erro ao faler lougout!"},status=400)
        return Response({"detail":"O token de autenticação (refresh_token) é necessario para fazer o logout!"},status=400)
class CreteUserView(generics.CreateAPIView):
        model=UserModel
        serializer_class= UserSerializer

class UserViewPrivate(APIView):
    permission_classes = [ValidToken]
    queryset = UserModel.objects.all()

    def get_queryset(self,pk):
        try:
            return self.queryset.get(pk=pk)
        except UserModel.DoesNotExist:
            raise Http404
    
    def put(self,request):
        user_id = Middlewares.decode(request.headers)
        tipo = self.get_queryset(user_id)
        data = UserSerializer(tipo).data

        # if(user_id == id):
        menssagem = 'Changed not passwrod'
        user = self.get_queryset(user_id)
        userAnt = serializer = UserSerializer(user)
        data = request.data

        try:

            if(data["password"] and user.check_password(data['password_back'])):
                user.set_password(make_password(data['password']))
                data['password']=make_password(data['password'])
                menssagem= "Changed password"
        except:
            menssagem= 'Changed not passwrod'
            print(user.password)
        
        
        
        serializer = UserUpdateSerializer(user,data=data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "detail": "Atulizado com sucesso!!", "menssagem":menssagem
            },status=200)
        
        return Response(serializer.error, status=404)
    # else:
    #     return Response({"detail":"Não autorizado!"})





class AdimView(APIView):
    permission_classes= [ValidToken, ValidAdmin]
    queryset = UserModel.objects.all()

    def get_object(self, pk, tipo):
        try:
            return self.queryset.get(pk=pk,tipo=tipo)
        except UserModel.DoesNotExist:
            raise Http404
    
    def get(self, request, id=None):

        if id is not None:
            user = self.get_object(id, tipo="client")
            serializer = UserListSerializer(user)
        else:
            users = self.queryset.filter(tipo="client")
            serializer = UserListSerializer(users, many=True)

        return Response(serializer.data)
    
    def patch(self, request, id):
        user=self.get_object(id,tipo="client")
        serializer = UserSerializer(user, data=request.data,partial=True)
        print(user)
        if serializer.is_valid():
            serializer.save()
            serializer = UserListSerializer(serializer.data)

            return Response(serializer.data,status=200)
        return Response(serializer.errors, status=400)
         