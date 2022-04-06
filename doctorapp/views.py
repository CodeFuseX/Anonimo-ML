from msilib.schema import ListView
from django.shortcuts import redirect, render
from doctorapp.models import Session, ReportDoc
from home.models import Resources,editProfile, FollowersCount,FriendRequest,Bank,Doctor
# Create your views here.
from django.contrib.auth.models import User,auth
from blogapp.models import Post,Report
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def doctorHome(request):
    return render(request,'docHome.html')

def doctoranonym(request):
    doc = len(Doctor.objects.filter(doctor_username=request.user))
    doc_present = False
    if doc>0:
        doc_present=True
    allProfiles = editProfile.objects.filter(count_mentalH__gte=3, approval=1, doc_assigned =0)
    print(allProfiles)
    allPosts = Post.objects.filter(mentalH ='suicide')
    print(allPosts)
    #allPosts = len(Post.objects.filter(author=))
    #print(allPosts)
    return render(request,'docAnonym.html',{'allProfiles':allProfiles,'allPosts':allPosts,'doc_present':doc_present})


def user_report(request,id):
    users_details = editProfile.objects.get(id=id)
    
    name = users_details.profile_user
    post_count = len(Post.objects.filter(author=name))
    allPosts = Post.objects.filter(author=name)
    bio = users_details.bio
    hobbies = users_details.hobbies
    image = users_details.image

    template_path = 'pdf2.html'
    context = {'name': name,'bio':bio, 'image':image,'hobbies':hobbies,'post_count':post_count,'allPosts':allPosts}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    #If we want to download:
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    #If we want to only display it
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response,)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



def render_pdf_view(request):
    template_path = 'pdf1.html'
    context = {'myvar': 'this is your template context'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    #If we want to download:
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    #If we want to only display it
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response,)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def docsession(request):
    doc = len(Doctor.objects.filter(doctor_username=request.user))
    doc_present = False
    if doc>0:
        doc_present=True

    allPatients = Session.objects.all().filter(doctor_username=request.user)
    all_patient_details = []
    session_details = []
    report_details = []
    allR = []
    for patient in allPatients:
        allPatients_details = User.objects.get(username = patient.patient_username)
        allP = editProfile.objects.get(profile_user = allPatients_details.id)
        
        allR = ReportDoc.objects.filter(patient_username = patient.patient_username)
        all_patient_details.append(allP)
        session_details.append(patient)
        report_details.append(allR)

        
    print(all_patient_details)
    print("?",session_details)
    print("report", allR)

    

    return render(request,'docsessions.html',{'doc_present':doc_present,'all_patient_details':all_patient_details,'session_details':session_details,'allR':allR})


def startsession(request,id):
    users_details = editProfile.objects.get(id=id)
    username = users_details.profile_user
    doc = len(Doctor.objects.filter(doctor_username=request.user))
    doc_present = False
    if doc>0:
        doc_present=True
    
    if request.method == "POST":
        patient_user = Session()
        patient_user.patient_username = users_details.profile_user;
        patient_user.required_sessions = request.POST.get('noofsessions')
        patient_user.doctor_username = request.user
        patient_user.save()
        users_details.doc_assigned = 1
        users_details.save()
        report_user = ReportDoc()
        report_user.patient_username = users_details.profile_user
        report_user.required_reports = request.POST.get('noofsessions')
        report_user.save()

        return redirect('/')
    return render(request, 'startsession.html',{'doc_present':doc_present,'username':username})


def usersession(request):
    session_present = len(Session.objects.filter(patient_username=request.user))
    report_present = len(ReportDoc.objects.filter(patient_username=request.user))
    session_p = False
    report_count = 0
    report_left = 0
    if session_present>0:
        session_p = True
        session_details = Session.objects.get(patient_username=request.user)
        doc_assigned = session_details.doctor_username
        doc_details = User.objects.get(username = doc_assigned)
        doc_details_id = doc_details.id
        doc_details = Doctor.objects.get(doctor_username = doc_assigned)
        doc_image = doc_details.doc_image
        session_count = session_details.required_sessions
        session_left = session_details.completed_sessions
        if report_present>0:
            report_details = ReportDoc.objects.get(patient_username = request.user)
            report_count = report_details.required_reports
            report_left = report_details.completed_reports
        else:
            ins = ReportDoc(patient_username = request.user, required_reports = session_count, completed_reports= 0)
            ins.save()



        return render(request,"session.html",{"doc_assigned":doc_assigned,"session_count":session_count,"doc_image":doc_image,"doc_details_id":doc_details_id,'session_present':session_present,'session_left':session_left,'report_count':report_count,'report_left':report_left})
    else:
        session_p = False
        return render(request,"session.html",{'session_present':session_present})


def getDetails(request):
    if request.method == "POST":
        print("IN")
        getSessionCount = request.POST.get('rangevalue')
        getReportCount = request.POST.get('reportrangevalue')
        getpatientusername = request.POST.get('patientusername')
        session = Session.objects.get(patient_username=getpatientusername)
        session.completed_sessions = getSessionCount
        doc_report = ReportDoc.objects.get(patient_username=getpatientusername)
        doc_report.completed_reports = getReportCount
        doc_report.save()
        session.save()
        print("Successfully updated reports as well as sessions")
        
        return redirect("/doctor/docsessions")
    return redirect("/doctor/docsessions")


def report(request):
    if request.method=='POST':
        post_username = request.user
        post_title = request.POST['content-title']
        post_content = request.POST['content-area']

        ins = Report(post_username=post_username,post_title=post_title,post_content=post_content)
        ins.save()

    return render(request,'report.html')


def viewReport(request,id):
    doc = len(Doctor.objects.filter(doctor_username=request.user))
    doc_present = False
    if doc>0:
        doc_present=True
    user_data = editProfile.objects.get(id=id)
    user_image = user_data.image
    allReports = Report.objects.filter(post_username= user_data.profile_user)
    print(allReports)
    return render(request,"viewReport.html",{'allReports':allReports,'user_image':user_image,'doc_present':doc_present})

