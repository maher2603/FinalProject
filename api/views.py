from http.client import HTTPResponse
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, VehicleForm, VehicleLogForm, PostForm, CommentForm, ReplyForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.http import JsonResponse
import json
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Vehicle, VehicleLog, Post, Comment, Reply
from django.contrib.auth.models import User
import requests, datetime
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout


def main_spa(request: HttpRequest) -> HTTPResponse:
    return render(request, 'base.html', {})

@csrf_exempt
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('main_spa')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save to the database yet
            form.save()  # Now save to the database
            login(request, user)
            return redirect('main_spa')
    else:
        form = CustomUserCreationForm()

    return render(request, 'api/spa/signup.html', {'form': form})

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                # Redirect to the 'next' page after successful login
                next_page = request.POST.get('next', '')  # Get the 'next' parameter from the form submission
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect('main_spa')  # Redirect to the main page if 'next' is not provided
            else:
                # Invalid username or password
                error_message = 'Invalid username or password. Please try again.'
        else:
            # Form is invalid, render login page with form and error message
            error_message = 'Invalid username or password. Please try again.'
        return render(request, 'api/spa/login.html', {'form': form, 'error_message': error_message})
    else:
        # GET request, render login page with empty form
        form = AuthenticationForm()
        # Pass the 'next' parameter to the login template
        return render(request, 'api/spa/login.html', {'form': form, 'next': request.GET.get('next', '')})

@csrf_exempt
def logout_view(request):
    auth_logout(request)
    return redirect('login')

@csrf_exempt
@login_required
def user_id_information(request, user_id):
    """
    Handles operations on the user.
    """
    getUser = User.objects.get(id=user_id)
    return JsonResponse(getUser.to_dict())

@csrf_exempt
@login_required
def user_api(request):
    """
    Handles operations on the user.
    """
    return JsonResponse(request.user.to_dict())

@csrf_exempt
@login_required
def update_user_profile(request):
    """
    updates the user profile when they input new content into the fields
    """
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            user = request.user
            user.username = data.get('username', user.username)
            user.dob = data.get('dob', user.dob)
            user.email = data.get('email', user.email)
            if 'profileImage' in data:
                user.profileImage = data.get('profileImage', user.profileImage)
            user.save()
            user_data = user.to_dict()
            return JsonResponse(user_data)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def add_vehicle(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            print("Received data:", request.body)
            try:
                data = json.loads(request.body.decode('utf-8'))
                registration_number = data.get('registration_number', '')
                make = data.get('make', '')
                colour = data.get('colour', '')
                year_of_manufacture = int(data.get('year_of_manufacture', None))
                fuel_type = data.get('fuel_type', '')
                engine_capacity = int(data.get('engine_capacity', None))
                tax_status = data.get('tax_status', '')
                tax_due_date_str = data.get('tax_due_date')
                mot_status = data.get('mot_status', '')
                mot_expiry_date_str = data.get('mot_expiry_date')

                print("Year:", year_of_manufacture)

                try:
                    mot_expiry_date = parse_date(mot_expiry_date_str)
                except ValueError as e:
                    return JsonResponse({'error': str(e)}, status=400)

                # Set tax_due_date to None if not provided
                tax_due_date = parse_date(tax_due_date_str) if tax_due_date_str else None

                print("User:", request.user)
                print("Engine:", engine_capacity)
                

                form = VehicleForm({
                    'user_id': request.user.id,
                    'registration_number': registration_number,
                    'make': make,
                    'colour': colour,
                    'year_of_manufacture': year_of_manufacture,
                    'fuel_type': fuel_type,
                    'engine_capacity': engine_capacity,
                    'tax_status': tax_status,
                    'tax_due_date': tax_due_date,
                    'mot_status': mot_status,
                    'mot_expiry_date': mot_expiry_date
                })

                print("Tax due date:", tax_due_date_str)
                print("MOT expiry date:", mot_expiry_date_str)
                
                if form.is_valid():
                    form.save()
                    return JsonResponse({'message': 'Vehicle added successfully'}, status=201)
                else:
                    print(form.errors)  # Print form errors to debug
                    return JsonResponse({'errors': form.errors}, status=400)

            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Invalid JSON data'}, status=400)

            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)  # Handle invalid date format
            
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'User is not authenticated'}, status=401)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def vehicle_search(request):
    if request.method == 'POST':
        url = "https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles"
        headers = {
            'x-api-key': '21LlpFg7j56n9VoFj0AfK065SG6Anw6IMOrpTx90',
            'Content-Type': 'application/json'
        }
        try:
            response = requests.post(url, headers=headers, data=request.body)
            return JsonResponse(response.json(), status=response.status_code)
        except requests.RequestException as e:
            return JsonResponse({'error': 'Failed to fetch vehicle data'}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
@login_required
def get_vehicles(request: HttpRequest) -> JsonResponse:
    """
    Retrieves all vehicles associated with the logged-in user.
    """
    if request.method == 'GET':
        try:
            # Retrieve all vehicles associated with the logged-in user
            vehicles = Vehicle.objects.filter(user_id=request.user)
            # Convert queryset to list of dictionaries
            #print(vehicles) #for debugging
            vehicle_data = []

            for vehicle in vehicles:
                # Create a dictionary with vehicle data
                vehicle_dict = {
                    'id': vehicle.id,
                    'registration_number': vehicle.registration_number,
                    'make': vehicle.make,
                    'colour': vehicle.colour,
                    'year_of_manufacture': vehicle.year_of_manufacture,
                    'fuel_type': vehicle.fuel_type,
                    'engine_capacity': vehicle.engine_capacity,
                    'tax_status': vehicle.tax_status,
                    'mot_status': vehicle.mot_status,
                    'mot_expiry_date': vehicle.mot_expiry_date,
                }

                # Include tax_due_date only if it's not None
                if vehicle.tax_due_date is not None:
                    vehicle_dict['tax_due_date'] = vehicle.tax_due_date
                
                vehicle_data.append(vehicle_dict)
            # Return the list of vehicle data as a JSON response
            #print(vehicle_data) #for debugging
            return JsonResponse(vehicle_data, safe=False)  # Set safe=False for serialization of lists
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
@login_required
def get_vehicle(request: HttpRequest, vehicle_id: int) -> JsonResponse:
    """
    Retrieves all vehicles associated with the logged-in user.
    """
    if request.method == 'GET':
        try:
            # Retrieve all vehicles associated with the logged-in user
            vehicles = Vehicle.objects.filter(user_id=request.user, id=vehicle_id)
            # Convert queryset to list of dictionaries
            #print(vehicles) #for debugging
            vehicle_data = [vehicle.to_dict() for vehicle in vehicles]
            # Return the list of vehicle data as a JSON response
            #print(vehicle_data) #for debugging
            return JsonResponse(vehicle_data, safe=False)  # Set safe=False for serialization of lists
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
@login_required
def remove_vehicle(request: HttpRequest, vehicle_id: int) -> JsonResponse:
    """
    Removes the specified vehicle associated with the logged-in user.
    """
    if request.method == 'DELETE':
        try:
            # Retrieve the vehicle associated with the logged-in user and the given vehicle_id
            vehicle = Vehicle.objects.get(user_id=request.user, id=vehicle_id)
            # Delete the vehicle
            vehicle.delete()
            return JsonResponse({'message': 'Vehicle removed successfully'}, status=200)
        except Vehicle.DoesNotExist:
            return JsonResponse({'error': 'Vehicle not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
@login_required
def add_vehicle_log(request, vehicle_id: int)  -> JsonResponse:
    if request.method == 'POST':
        print("Reached views.py")
        if request.user.is_authenticated:
            print("is authenticated")
            print(request.POST)
            try:
                data = request.POST
                files = request.FILES
                print("past data")
                print(data)
                title = data.get('title', '')
                date = parse_date(data.get('date'))
                cost = data.get('cost', 0)
                description = data.get('description', '')
                file_upload = files.get('file_upload', None)

                print(file_upload)

                form = VehicleLogForm({
                    'vehicle_id': vehicle_id,
                    'title': title,
                    'date': date,
                    'cost': cost,
                    'description': description,
                }, files)
                print("after form")

                if form.is_valid():
                    form.save()
                    return JsonResponse({'message': 'Vehicle log added successfully'}, status=201)
                else:
                    return JsonResponse({'errors': form.errors}, status=400)

            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Invalid JSON data'}, status=400)

            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400) 
            
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'User is not authenticated'}, status=401)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
@login_required
def get_vehicle_logs(request, vehicle_id):
    if request.method == 'GET':
        try:
            logs = VehicleLog.objects.filter(vehicle_id=vehicle_id).values('id', 'title', 'date', 'cost', 'description', 'file_upload')
            return JsonResponse(list(logs), safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
@login_required
def delete_vehicle_log(request, log_id):
    if request.method == 'DELETE':
        try:
            # Retrieve the log associated with the logged-in user and the given log_id
            log = VehicleLog.objects.get(id=log_id)
            # Delete the log
            log.delete()
            return JsonResponse({'message': 'Log deleted successfully'}, status=200)
        except VehicleLog.DoesNotExist:
            return JsonResponse({'error': 'Log not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
@login_required
def add_post(request)  -> JsonResponse:
    if request.method == 'POST':
        print("Reached views.py")
        if request.user.is_authenticated:
            print("is authenticated")
            print(request.POST)
            try:
                data = request.POST
                images = request.FILES
                print("past data")
                print(data)
                title = data.get('title', '')
                description = data.get('description', '')
                image_upload = images.get('image_upload', None)

                print(image_upload)

                form = PostForm({
                    'user_id': request.user.id,
                    'title': title,
                    'description': description,
                }, images)
                print("after form")

                if form.is_valid():
                    form.save()
                    return JsonResponse({'message': 'Post added successfully'}, status=201)
                else:
                    return JsonResponse({'errors': form.errors}, status=400)

            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Invalid JSON data'}, status=400)

            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400) 
            
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'User is not authenticated'}, status=401)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
@login_required
def get_posts(request):
    if request.method == 'GET':
        try:
            posts = Post.objects.all()
            serialized_posts = [post.to_dict() for post in posts]
            return JsonResponse(serialized_posts, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
@login_required
def get_post(request, post_id):
    if request.method == 'GET':
        try:
            post = Post.objects.get(id=post_id)
            serialized_posts = post.to_dict()
            return JsonResponse(serialized_posts, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
@login_required
def delete_post(request, post_id):
    if request.method == 'DELETE':
        try:
            # Retrieve the post associated with the given post_id
            post = Post.objects.get(id=post_id)
            # Delete the post
            post.delete()
            return JsonResponse({'message': 'Post deleted successfully'}, status=200)
        except VehicleLog.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User is not authenticated'}, status=401)

        data = json.loads(request.body)
        comment = data.get('comment', '')
        print("comment: " + comment)
        form = CommentForm({
            'user_id': request.user.id,
            'post_id': post_id,
            'comment': comment,
        })

        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Comment added successfully'}, status=201)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
@login_required
def get_comments(request, post_id):
    if request.method == 'GET':
        try:
            comments = Comment.objects.filter(post_id=post_id)
            serialized_posts = [comment.to_dict() for comment in comments]
            return JsonResponse(serialized_posts, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
@login_required
def delete_comment(request, comment_id):
    if request.method == 'DELETE':
        try:
            # Retrieve the comment associated with the given comment_id
            comment = Comment.objects.get(id=comment_id)
            # Delete the comment
            comment.delete()
            return JsonResponse({'message': 'Comment deleted successfully'}, status=200)
        except VehicleLog.DoesNotExist:
            return JsonResponse({'error': 'Comment not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
@login_required
def add_reply(request, comment_id):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User is not authenticated'}, status=401)

        data = json.loads(request.body)
        reply = data.get('reply', '')
        print("reply: " + reply)
        form = ReplyForm({
            'user_id': request.user.id,
            'comment_id': comment_id,
            'reply': reply,
        })

        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Reply added successfully'}, status=201)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
@login_required
def get_replies(request, comment_id):
    if request.method == 'GET':
        try:
            # print(Reply.objects.filter(comment_id=comment_id))
            replies = Reply.objects.filter(comment_id=comment_id)
            # print(replies)
            serialized_posts = [reply.to_dict() for reply in replies]
            return JsonResponse(serialized_posts, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
@login_required
def delete_reply(request, reply_id):
    if request.method == 'DELETE':
        try:
            # Retrieve the reply associated with the given reply_id
            reply = Reply.objects.get(id=reply_id)
            # Delete the reply
            reply.delete()
            return JsonResponse({'message': 'Reply deleted successfully'}, status=200)
        except VehicleLog.DoesNotExist:
            return JsonResponse({'error': 'Reply not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)