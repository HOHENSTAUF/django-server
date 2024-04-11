from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def register(request):
    return Response({})

@api_view(['POST'])
def login(request):
    return Response({})

@api_view(['POST'])
def refresh(request):
    return Response({})

@api_view(['POST'])
def logout(request):
    return Response({})

@api_view('GET')
def me(request):
    return Response({})

'''
@api_view(['PUT'])
def me(request):
    return Response({})
'''