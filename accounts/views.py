from .forms import CustomUserCreationForm
from rest_framework.views import APIView
from .emails import send_registration_email
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class AddUserView(APIView):

	def post(self, request):
		form = CustomUserCreationForm(request.data)
		if form.is_valid():
			user = form.save()
			send_registration_email(user.email)
			return Response({'message': f'{user.role.capitalize()} added successfully'}, status=status.HTTP_201_CREATED)
		return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)