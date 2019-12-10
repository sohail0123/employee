from django.shortcuts import render
import json,requests

def login(request):
    try:
        value  = request.session["user"]
        return render(request,"welcome.html",{'session':value})
    except KeyError:
        return render(request,"login.html")

def loginCheck(request):
    id = request.POST.get("eidno")
    password =  request.POST.get("epassword")
    login_details={"eidno":id,"epassword":password}
    json_data=json.dumps(login_details)
    try:
        res = requests.post("http://127.0.0.1:8000/elogin_check/", data=json_data)
        if res.status_code == 200:
            js=res.json()
            request.session["user"] = id
            return render(request,"welcome.html",{"data":js})
        else:
            return render(request,"login.html",{"login_error":"please enter correct details"})
    except requests.exceptions.ConnectionError:
        return render(request,"login.html",{"error":"Sever is not Available"})

def homePage(request):
    return render(request,"welcome.html")

def enterMarks(request):
    try:
        value = request.session["user"]
    except KeyError:
        return login(request)
    else:
        return render(request,"addmarks.html",{"session":value})

def reqMixin(request):
    sid = request.POST.get("sid")
    sname = request.POST.get("sname")
    tel = request.POST.get("tel")
    eng = request.POST.get("eng")
    maths_a = request.POST.get("maths_a")
    maths_b = request.POST.get("maths_b")
    science = request.POST.get("science")
    social = request.POST.get("social")
    marks = {"student_id":sid,"student_name":sname,"telugu":tel,"english":eng,"maths_a":maths_a,"maths_b":maths_b,
             "science":science,"social":social}
    json_data = json.dumps(marks)
    return json_data

def saveMarks(request):
    json_data = reqMixin(request)
    try:
        res = requests.post("http://127.0.0.1:8000/s_marks/",data=json_data)
        print("save marks",res.status_code)
        if  res.status_code == 200:
            return render(request,"addmarks.html",{"ok":"success saved"})
        else:
            return render(request,"addmarks.html",{"error":"enter correct details"})
    except requests.exceptions.ConnectionError:
        return render(request,"addmarks.html",{"serror":"server is not available"})


def update(request):
    return render(request,"update.html")

def updateId(request):
    uid = request.GET.get("uid")
    try:
        res = requests.put("http://127.0.0.1:8000/update/"+uid+"/")
        if  res.status_code == 200:
            js=res.json()
            return render(request,"update.html",{"ok":js})
        else:
            return render(request,"update.html",{"error":"enter correct student id"})
    except requests.exceptions.ConnectionError:
        return render(request,"update.html",{"serror":"server is not available"})


def saveUpdate(request):
    json_data = reqMixin(request)
    try:
        res = requests.post("http://127.0.0.1:8000/s_update/",data=json_data)
        if  res.status_code == 200:
            return render(request,"update.html",{"update":" marks updated "})
        else:
            return render(request,"update.html",{"error":"enter correct details"})
    except requests.exceptions.ConnectionError:
        return render(request,"update.html",{"serror":"server is not available"})


def logOut(request):
    del request.session["user"]
    return render(request,"login.html")