import os
import json
import requests
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
# import google.generativeai as genai
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from datetime import date, datetime
from .models import FoodDatabase
from .models import *
from dotenv import load_dotenv
from django.contrib import messages
load_dotenv()
 

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("register"))
    user = request.user

    person = Person.objects.get(user=user)

    calorie_goal = person.goalcalorie

    foods = Food.objects.filter(user=user, date=date.today())
    total_calorie_gain = 0
    for food in foods:
        total_calorie_gain += food.calories

    name = user.first_name

    current_date = date.today()
    person_birthday = person.bday
    age = current_date.year - person_birthday.year

    return render(
        request,
        "tracker/index.html",
        {
            "name": name,
            "calorie_goal": calorie_goal,
            "calories_remaining": calorie_goal - total_calorie_gain,
            "total_calorie_gain": total_calorie_gain,
        },
    )


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "tracker/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        return render(request, "tracker/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        name = request.POST["user-name"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request,
                "tracker/register.html",
                {"message": "Passwords must match."},
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = name
            user.save()
        except IntegrityError:
            return render(
                request,
                "tracker/register.html",
                {"message": "Username already taken."},
            )

        sex = request.POST["user-sex"]
        bday = request.POST["user-bday"]
        height = request.POST["user-height"]
        weight = request.POST["user-weight"]
        goalweight = request.POST["user-goalweight"]
        activity = request.POST["user-activity"]

        lvl_activity = {"1": 1.2, "2": 1.375, "3": 1.55, "4": 1.725}

        current_date = date.today()
        person_birthday = bday.split("-")
        age = current_date.year - int(person_birthday[0])

        if sex == "male":
            bmr = 66 + (6.23 * int(weight)) + (12.7 * int(int(height) * 0.394)) - (6.8 * age)
        else:
            bmr = 655 + (4.35 * int(weight)) + (4.7 * int(int(height) * 0.394)) - (4.7 * age)

        maintainance_calories = int(bmr * lvl_activity[activity])

        goal_weight = goalweight
        currentweight = weight
        if goal_weight > currentweight:
            calorie_goal = maintainance_calories + 200
        elif goal_weight < currentweight:
            calorie_goal = maintainance_calories - 200
        else:
            calorie_goal = maintainance_calories

        person = Person(
            user=user,
            sex=sex,
            bday=bday,
            height=height,
            weight=int(weight),
            goalweight=int(goalweight),
            activity=activity,
            maintainance=maintainance_calories,
            goalcalorie=calorie_goal,
            )
        person.save()

        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        return render(request, "tracker/register.html")


@login_required
def profile(request):
    user = request.user
    person = Person.objects.get(user=user)

    return render(request, "tracker/profile.html", {"person": person})


def edit_profile(request):
    user = request.user
    person = Person.objects.get(user=user)
    if request.method == "POST":
        height = request.POST["height"]
        weight = request.POST["weight"]
        goalweight = request.POST["goalweight"]
        activity = request.POST["activity"]
        goalcalorie = request.POST["goalcalorie"]

        sex = person.sex
        bday = person.bday

        current_date = date.today()
        person_birthday = str(bday).split("-")
        age = current_date.year - int(person_birthday[0])

        lvl_activity = {"1": 1.2, "2": 1.375, "3": 1.55, "4": 1.725, "5": 1.9}

        if sex == "male":
            bmr = 66 + (6.23 * int(weight)) + (12.7 * int(int(height) * 0.394)) - (6.8 * age)
        else:
            bmr = 655 + (4.35 * int(weight)) + (4.7 * int(int(height) * 0.394)) - (4.7 * age)

        maintainance_calories = int(bmr * lvl_activity[activity])

        person.height = height
        person.weight = weight
        person.goalweight = goalweight
        person.activity = activity
        person.goalcalorie = goalcalorie
        person.maintainance = maintainance_calories
        person.save()

    return HttpResponseRedirect(reverse("index"))



@login_required
def addFood(request, meal):

    # GET SELECTED DATE

    selected_date = request.GET.get("date")

    # IF USER SELECTED DATE

    if selected_date:

        selected_date = datetime.strptime(
            selected_date,
            "%Y-%m-%d"
        ).date()

    # OTHERWISE USE TODAY

    else:

        selected_date = timezone.now().date()

    # ADD FOOD

    if request.method == "POST":

        food_name = request.POST.get(
            "food-name"
        ).strip()

        amount_g = int(
            request.POST.get(
                "food-amount"
            )
        )

        # FIND FOOD IN DATABASE

        food_data = FoodDatabase.objects.filter(

            name__icontains=food_name

        ).first()

        # IF FOOD NOT FOUND

        if not food_data:

            return render(

                request,

                "tracker/add-food.html",

                {

                    "meal": meal,

                    "selected_date":
                    selected_date,

                    "error":
                    "Food not found in database."
                }
            )

        # CREATE FOOD ENTRY

        food_obj = Food(

            user=request.user,

            name=food_data.name,

            calories=round(
                (food_data.calories * amount_g) / 100,
                1
            ),

            protein=round(
                (food_data.protein * amount_g) / 100,
                1
            ),

            carbs=round(
                (food_data.carbs * amount_g) / 100,
                1
            ),

            fat=round(
                (food_data.fat * amount_g) / 100,
                1
            ),

            fibre=round(
                (food_data.fibre * amount_g) / 100,
                1
            ),

            grams=amount_g,

            meal=meal,

            date=selected_date
        )

        food_obj.save()

        # RETURN TO SAME DATE

        return redirect(
    f"/food/diary?date={selected_date.strftime('%Y-%m-%d')}"
)

    # OPEN PAGE

    return render(

        request,

        "tracker/add-food.html",

        {

            "meal": meal,

            "selected_date":
            selected_date
        }
    )

def get_food_info(request, food_item):

    if request.method == "GET":

        try:

            food_item = food_item.strip().lower()

            # Exact match
            food = FoodDatabase.objects.filter(
                name__iexact=food_item
            ).first()

            # Startswith match
            if not food:

                food = FoodDatabase.objects.filter(
                    name__istartswith=food_item
                ).order_by("name").first()

            # Contains match
            if not food:

                food = FoodDatabase.objects.filter(
                    name__icontains=food_item
                ).order_by("name").first()

            # Not found
            if not food:

                return JsonResponse({

                    "food_api": {

                        "name": food_item,

                        "serving_size_g": 100,

                        "calories": 0,

                        "protein": 0,

                        "carbs": 0,

                        "fat": 0,

                        "fibre": 0
                    }
                })

            return JsonResponse({

                "food_api": {

                    "name": food.name,

                    "serving_size_g": 100,

                    "calories": food.calories,

                    "protein": food.protein,

                    "carbs": food.carbs,

                    "fat": food.fat,

                    "fibre": food.fibre
                }
            })

        except Exception as e:

            return JsonResponse(
                {"error": str(e)},
                status=500
            )



def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'tracker/change_password.html', {'form': form})


@login_required
def deleteFood(request, id):

    food = Food.objects.get(
        id=id,
        user=request.user
    )

    food.delete()

    return redirect("food")

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required
def editFood(request, id):

    food = get_object_or_404(

        Food,

        id=id,

        user=request.user
    )

    if request.method == "POST":

        amount_g = int(
            request.POST.get(
                "food-amount"
            )
        )

        # FIND CLOSEST MATCH

        food_data = FoodDatabase.objects.filter(

            name__icontains=food.name

        ).first()

        # IF NO FOOD FOUND

        if not food_data:

            return render(

                request,

                "tracker/edit-food.html",

                {

                    "food": food,

                    "error":
                    "Food not found in database."
                }
            )

        # UPDATE VALUES

        food.grams = amount_g

        food.calories = round(
            (food_data.calories * amount_g) / 100,
            1
        )

        food.protein = round(
            (food_data.protein * amount_g) / 100,
            1
        )

        food.carbs = round(
            (food_data.carbs * amount_g) / 100,
            1
        )

        food.fat = round(
            (food_data.fat * amount_g) / 100,
            1
        )

        food.fibre = round(
            (food_data.fibre * amount_g) / 100,
            1
        )

        food.save()

        return redirect(
    f"/food/diary?date={food.date}"
)

    return render(

        request,

        "tracker/edit-food.html",

        {

            "food": food
        }
    )

@login_required
def foodDiary(request):

    # GET SELECTED DATE

    selected_date = request.GET.get("date")

    # IF USER CHOOSES DATE

    if selected_date:

        selected_date = datetime.strptime(
            selected_date,
            "%Y-%m-%d"
        ).date()

    # OTHERWISE USE TODAY

    else:

        selected_date = timezone.now().date()

    # BREAKFAST ITEMS

    breakfast_food_items = Food.objects.filter(

        user=request.user,

        meal="breakfast",

        date=selected_date

    )

    # LUNCH ITEMS

    lunch_food_items = Food.objects.filter(

        user=request.user,

        meal="lunch",

        date=selected_date

    )

    # DINNER ITEMS

    dinner_food_items = Food.objects.filter(

        user=request.user,

        meal="dinner",

        date=selected_date

    )

    # ALL FOODS OF SELECTED DATE

    all_foods = Food.objects.filter(

        user=request.user,

        date=selected_date

    )

    # TOTAL CALCULATIONS

    total_calories = sum(
        food.calories for food in all_foods
    )

    total_protein = sum(
        food.protein for food in all_foods
    )

    total_carbs = sum(
        food.carbs for food in all_foods
    )

    total_fat = sum(
        food.fat for food in all_foods
    )

    total_fibre = sum(
        food.fibre for food in all_foods
    )

    # CONTEXT

    context = {

        "selected_date": selected_date,

        "breakfast_food_items":
        breakfast_food_items,

        "lunch_food_items":
        lunch_food_items,

        "dinner_food_items":
        dinner_food_items,

        "total_calories":
        round(total_calories, 1),

        "total_protein":
        round(total_protein, 1),

        "total_carbs":
        round(total_carbs, 1),

        "total_fat":
        round(total_fat, 1),

        "total_fibre":
        round(total_fibre, 1)
    }

    # RENDER PAGE

    return render(

        request,

        "tracker/food.html",

        context
    )

