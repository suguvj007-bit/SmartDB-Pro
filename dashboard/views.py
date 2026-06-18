from django.shortcuts import render,redirect
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from smartdb_engine.database import SmartDB

def home(request):


 db = SmartDB()

 total_records = db.count_records()

 logs = []

 try:
    log_file = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../../data/logs.txt"
        )
    )

    with open(log_file, "r") as file:
        logs = file.readlines()[-5:]
        logs.reverse()

 except:
    pass

 try:
    count_file = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../../data/search_count.txt"
        )
    )

    with open(count_file, "r") as file:
        total_searches = file.read()

 except:
    total_searches = 0

 context = {
    "total_records": total_records,
    "total_searches": total_searches,
    "logs": logs
}

 return render(request, "home.html", context)


def records(request):

    db = SmartDB()

    records = db.get_all()

    print(records)

    context = {
        "records": records
    }

    return render(request, "records.html", context)

def add_record(request):
    if request.method=="POST":

        record_id=request.POST["record_id"]
        name=request.POST["name"]
        course=request.POST["course"]

        db=SmartDB()

        record={
            "name":name,
            "course":course
        }

        db.insert(record_id,record)
        return redirect("records")
    return render(request, "add_record.html")

def delete_record(request, record_id):

    db = SmartDB()

    db.delete(record_id)

    return redirect("records")

def search_record(request):
    results={}

    if request.method=="POST":
        name=request.POST["name"]
        db=SmartDB()

        results=db.indexed_search(name)

        count_file=os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "../../data/search_count.txt"
            )
        )
        try:
            with open(count_file,"r")as file:
                count=int(file.read())
        except:
            count=0
        count+=1
        with open(count_file,"w")as file:
            file.write(str(count))
    return render(
        request,
        "search.html",
        {"results":results}
    )

def analytics(request):

    db = SmartDB()

    records = db.get_all()

    total_records = len(records)

    course_count = {}

    for record in records.values():

        course = record["course"].title()
        if course in course_count:
            course_count[course] += 1
        else:
            course_count[course] = 1

    context = {
        "total_records": total_records,
        "course_count": course_count,
        "courses":list(course_count.keys()),
        "counts":list(course_count.values())
    }

    return render(
        request,
        "analytics.html",
        context
    )

def edit_record(request, record_id):
    db=SmartDB()

    if request.method=="POST":

        name= request.POST["name"]
        course= request.POST["course"]

        updated_record={
            "name": name,
            "course": course
        }

        db.update(record_id, updated_record)

        return redirect("records")
    record= db.get(record_id)

    context={
        "record_id": record_id,
        "record": record
    }

    return render(
        request,
        "edit_record.html",
        context
    )

def activity_logs(request):
    logs=[]

    try:
        with open("../data/logs.txt","r") as file:
            logs=file.readlines()
        logs.reverse()

    except:
        logs=["Not Logs Available"]

    return render(
        request,
        "activity_logs.html",
        {"logs":logs}
    )