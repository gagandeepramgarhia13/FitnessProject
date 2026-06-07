# import csv

# from tracker.models import FoodDatabase


# CSV_FILE = "food_databse.csv"


# with open(
#     CSV_FILE,
#     encoding="utf-8"
# ) as file:

#     reader = csv.DictReader(file)

#     count = 0

#     for row in reader:

#         try:

#             FoodDatabase.objects.get_or_create(

#                 name=row["name"],

#                 defaults={

#                     "calories":
#                     float(row["calories"]),

#                     "protein":
#                     float(row["protein"]),

#                     "carbs":
#                     float(row["carbs"]),

#                     "fat":
#                     float(row["fat"]),

#                     "fibre":
#                     float(row["fibre"])
#                 }
#             )

#             count += 1

#             if count % 100 == 0:

#                 print(
#                     f"Imported {count} foods"
#                 )

#         except Exception as e:

#             print(e)

# print("Import completed")

import os
import sys
import csv
import django

# Make sure project root is on sys.path so Django can import the project package
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

# Ensure Django settings are configured when running this script directly
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fitnesstracker.settings")
django.setup()

from tracker.models import FoodDatabase

# Resolve CSV relative to project root
CSV_FILE = os.path.join(BASE_DIR, "food_databse.csv")


with open(CSV_FILE, encoding="utf-8") as file:
    reader = csv.DictReader(file)

    count = 0

    for row in reader:
        try:
            FoodDatabase.objects.get_or_create(
                name=row["name"],
                defaults={
                    "calories": float(row.get("calories", 0) or 0),
                    "protein": float(row.get("protein", 0) or 0),
                    "carbs": float(row.get("carbs", 0) or 0),
                    "fat": float(row.get("fat", 0) or 0),
                    "fibre": float(row.get("fibre", 0) or 0),
                },
            )

            count += 1

            if count % 100 == 0:
                print(f"Imported {count} foods")

        except Exception as e:
            print(e)

print("Import completed")