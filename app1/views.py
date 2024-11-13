from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Forms,TurfBooking ,Events_Ticket# Adjust this to your actual model
import json
from django.shortcuts import get_object_or_404
import random
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets,permissions
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import *
from .models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from django_ratelimit.decorators import ratelimit
@csrf_exempt
@require_POST
def contact_form(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        message = data.get('message')

        if not email or not message:
            return JsonResponse({'error': 'All fields are required!'}, status=400)

        contact = Forms(email=email, message=message)
        contact.save()
        return JsonResponse({'success': 'Message sent!'})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def book_slot(request):
    print("book_slot function called")
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method!'}, status=405)

    try:
        data = json.loads(request.body)
        print('Request body:', request.body)  # Check the request body
        game = data.get('game')
        date = data.get('date')
        print('game:', game, 'date:', date)

        if not game or not date:
            return JsonResponse({'error': 'All fields are required!'}, status=400)

        booked_times = TurfBooking.objects.filter(game=game, date=date)
        print('Booked times:', booked_times)  # Log booked times
        
        turf_availability = {
            "standard": [],
            "premium": [],
            "deluxe": []
        }

        for booking in booked_times:
            turf_availability[booking.turf_type].append(booking.time)
        print(turf_availability)

        return JsonResponse(turf_availability)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        print('Error:', str(e))  # Log the error
        return JsonResponse({'error': str(e)}, status=500)









@csrf_exempt  # Use with caution; consider CSRF protection in production
def ticket(request, booking_id=None):
    if request.method == 'POST':
        # Handle booking creation
        try:
            data = json.loads(request.body)
            turf_details = []
            total_price = 0
            game = data.get('game')
            turf_names = data.get('turf')  # Expecting a list
            times = data.get('time')        # Expecting a list
            prices = data.get('price')      # Expecting a list
            g_date = data.get('date')

            # Generate a random ticket ID between 100000000 and 10000000000
            ticket_id = random.randint(100000000, 10000000000)

            # Build the turf details and save bookings
            for turf, time, price in zip(turf_names, times, prices):
                booking = TurfBooking(game=game, date=g_date, time=time, turf_type=turf, ticket_no=ticket_id)
                booking.save()
                turf_details.append({
                    'game': game,
                    'turf': turf,
                    'g_date': g_date,
                    'time': time,
                    'price': int(price)
                })
                total_price += int(price)

            # Prepare the response for booking creation
            response_data = {
                'date': datetime.today().date().isoformat(),
                'total_price': total_price,
                'turf_details': turf_details,
                'booking_id': ticket_id
            }
            return JsonResponse({'status': 'success', 'data': response_data})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    elif request.method == 'GET' and booking_id:
        # Handle fetching booking details
        try:
            booking = TurfBooking.objects.get(ticket_no=booking_id)
            booking_details = {
                'game': booking.game,
                'date': booking.date,
                'time': booking.time,
                'turf': booking.turf_type,
                'price': booking.price,  # Adjust based on your model's attributes
            }
            return JsonResponse({'status': 'success', 'data': booking_details})

        except TurfBooking.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Booking not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


def event_ticket(request):
    events = Events_Ticket.objects.all()  # Fetch all events
    events_list = [
        {
            'id': event.id,
            'name': event.name,
            'date': event.date,
            'time': event.time,
            'venue': event.venue,
            'image': event.image.url if event.image else None  # Get the URL of the image
        }
        for event in events
    ]
    return JsonResponse(events_list, safe=False)

class EventTicketViewSet(viewsets.ModelViewSet):
    queryset=Event_Bookings.objects.all()
    serializer_class=EventTicketSerializer
class TurfBookingViewSet(viewsets.ModelViewSet):
    queryset=TurfBooking.objects.all()
    serializer_class=TurfBookingSerializer

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Optionally, generate a token
        token = CustomTokenObtainPairSerializer.get_token(user)

        return Response({
            'user': serializer.data,
            'token': str(token),
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    # @ratelimit(key='ip', rate='3/m', method='POST', block=True)  # Limit to 3 attempts per minute
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": user.id,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TurfDetailsUser(APIView):

    def get(self, request, user_id):
    
        bookings = TurfBooking.objects.filter(user=user_id)
        serializer = TurfBookingSerializer(bookings, many=True)
        return Response(serializer.data)

class EventDetailsUser(APIView):
    def get(self,request,user_id):
        bookings=Event_Bookings.objects.filter(user=user_id)
        serializer=EventTicketSerializer(bookings,many=True)
        return Response(serializer.data)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = LoginSerializer
# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer



# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer
#     permission_classes = [permissions.AllowAny]

#     def post(self, request, *args, **kwargs):
#         email = request.data.get('email')
#         password = request.data.get('password')
#         print(f"Attempting to authenticate user with email: {email}")
#         # Authenticate the user
#         user = authenticate(request, username=email, password=password)
        
#         if user is not None:
#             # If authentication is successful, generate the tokens
#             return super().post(request, *args, **kwargs)
#         else:
#             # If authentication fails, return an error
#             return Response({'error': 'Invalid credentials'}, status=401)

# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [AllowAny]

# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = UserSerializer
#     # You can customize the token response here if needed
#     pass