from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
# from django.core.servers.basehttp import FileWrapper
from django.template import loader
from se1.models import Studentinfo
from se1.models import Project
from se1.models import Profinfo
from se1.models import Profemail
from se1.models import Studprojgrade
from se1.models import Studcontact
from se1.models import Studemail
from se1.models import *
from django.db import connection
from se1.models import Projprof
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db import transaction
import time
from django.core.files.base import ContentFile
from datetime import datetime
from django.http import JsonResponse
from django.core import serializers
import re, shutil


# Create your views here.

FILE_PATH = 'C:/Users/sneha kadham/Desktop/PMS/'

def rendersystem(request):
    title = "Welcome to Project Management System"
    return render(request, 'se1/dashboard/start.html', {'title': title})


@csrf_exempt
def renderindex(request):
    if (request.method == "POST"):
        data = request.POST  # data is now a dictionary
        usr_name = data['username']
        passwrd = data['passwrd']

        user = authenticate(username=usr_name, password=passwrd)

        if user is not None:
            request.session.clear_expired()
            request.session['member_id'] = user.username  # add username to the current session
            request.session['prof'] = 'none'
            request.session['guest'] = ''
            request.session.set_expiry(1200)
            return redirect(renderdashboard)
        else:
            template = loader.get_template('se1/dashboard/index.html')
            context = {'KEY': 1}
            return HttpResponse(template.render(context, request), status=200)
    else:
        template = loader.get_template('se1/dashboard/index.html')
        context = {'KEY': 0}
        return HttpResponse(template.render(context, request), status=200)


@csrf_exempt
def renderuser(request):
    if(request.session and request.session.get('member_id') and request.session.get('member_id') != '' and request.session.get('member_id') != 'guest'):
        u = request.session['member_id']
        all1 = list(Studprojgrade.objects.filter(usn=u))
        all_prof = list(Profinfo.objects.filter(name=u))
        if (len(all1) != 0):
            usr = User.objects.get(username=u)  # get django user object
            cursor = connection.cursor()
            name = Studentinfo.objects.filter(usn=u)  # get all details to display
            phnos = Studcontact.objects.filter(usn=u)
            emails = Studemail.objects.filter(usn=u)
            if (request.method == 'POST'):
                data = request.POST  # obtain the dictionary of submitted elements
                passwrd = data["passwrd"]
                passwrd2 = data["passwrd2"]
                if (passwrd == passwrd2):  # checking if entered passwords match -> to change passwords
                    if(len(passwrd) > 7):
                        usr.set_password(passwrd)  # change password and save
                        usr.save()
                        cursor.execute(
                            "update Studentinfo set passwd = '" + passwrd + "' where usn = '" + u + "'")  # update in database
                        template = loader.get_template('se1/dashboard/user.html')
                        return HttpResponse(template.render(
                            {'KEY': 1, 'name': name[0].name, 'usn': u, 'phnos': phnos[0].phno, 'emails': emails[0].email},
                            request),
                            status=200)
                    else:
                        template = loader.get_template('se1/dashboard/user.html')
                        return HttpResponse(template.render(
                            {'KEY': 3, 'name': name[0].name, 'usn': u, 'phnos': phnos[0].phno, 'emails': emails[0].email},
                            request),
                            status=200)

                else:
                    template = loader.get_template('se1/dashboard/user.html')
                    return HttpResponse(template.render(
                        {'KEY': 2, 'name': name[0].name, 'usn': u, 'phnos': phnos[0].phno, 'emails': emails[0].email},
                        request), status=200)
            else:
                return render(request, 'se1/dashboard/user.html',
                              {'name': name[0].name, 'usn': u, 'phnos': phnos[0].phno, 'emails': emails[0].email})
        else:
            usr = User.objects.get(username=u)  # get django user object
            cursor = connection.cursor()
            name = Profinfo.objects.filter(name=u)  # get all details to display
            prof_id = name[0].profid
            print(type(prof_id))
            prof_id = int(prof_id)
            phnos = Profcontact.objects.filter(profid=prof_id)
            emails = Profemail.objects.filter(profid=prof_id)
            if (request.method == 'POST'):
                data = request.POST  # obtain the dictionary of submitted elements
                passwrd = data["passwrd"]
                passwrd2 = data["passwrd2"]
                if (passwrd == passwrd2):  # checking if entered passwords match -> to change passwords
                    if(len(passwrd) > 7):
                        usr.set_password(passwrd)  # change password and save
                        usr.save()
                        cursor.execute("update profinfo set passwd = '" + passwrd + "' where profid = {} ".format(prof_id))
                        # update in database
                        template = loader.get_template('se1/dashboard/user_prof.html')
                        return HttpResponse(template.render(
                            {'KEY': 1, 'name': name[0].name, 'profid': prof_id, 'phnos': phnos[0].phno,
                             'emails': emails[0].email}, request),
                            status=200)
                    else:
                        template = loader.get_template('se1/dashboard/user_prof.html')
                        return HttpResponse(template.render(
                            {'KEY': 3, 'name': name[0].name, 'profid': prof_id, 'phnos': phnos[0].phno,
                             'emails': emails[0].email}, request),
                            status=200)
                else:
                    template = loader.get_template('se1/dashboard/user_prof.html')
                    return HttpResponse(template.render(
                        {'KEY': 2, 'name': name[0].name, 'profid': prof_id, 'phnos': phnos[0].phno,
                         'emails': emails[0].email}, request),
                        status=200)

            else:
                return render(request, 'se1/dashboard/user_prof.html',
                              {'name': name[0].name, 'profid': prof_id, 'phnos': phnos[0].phno,
                               'emails': emails[0].email})
    else:
        return redirect(rendersystem)


@csrf_exempt
def renderadd_project(request):
    print("$********", request.session.get('member_id'))
    if(request.session and request.session.get('member_id') and request.session.get('member_id') != '' and request.session.get('member_id') != 'guest'):
        u = request.session['member_id']
        cursor = connection.cursor()
        usr = User.objects.get(username=u)
        name = Studentinfo.objects.filter(usn=u)
        logged_user_usn = name[0].usn
        error = 0
        print(logged_user_usn)
        if (request.method == 'POST'):
            try:
                with transaction.atomic():
                    data = request.POST
                    EnteredNames = data.get("namelist")
                    EnteredUSNs = data.get("usnlist").split(',')
                    NameUsn = zip(EnteredNames, EnteredUSNs)
                    enteredTitle = data["title"]
                    enteredMentor = data.get("mentorselect").split(',')
                    doms = data.get("dom").split(',')
                    enteredDesc = data.getlist("desc")
                    Stat = data.get("dropdown")
                    if (Stat == "Ongoing"):
                        complete = 'false'
                    else:
                        complete = 'true'
                    # print("Heolo",type(enteredDesc[0]))
                    print("dfhgfhgfhgf", data)
                    # print(enteredTitle,enteredMentor)(Title,DateOfReg,Status,Synopsis,Complete)
                    # id1 = cursor.execute("SELECT projid FROM project ORDER BY projid DESC LIMIT 1")
                    idmax = Project.objects.all().order_by("-projid")[0]
                    newid = idmax.projid + 1
                    newid1 = str(newid)
                    # dat = datetime.now().date()
                    # dat = dat.strftime('%Y-%m-%d')
                    dat1 = time.strftime('%Y-%m-%d')
                    # print(type())
                    cursor.execute(
                        "insert into  Project  values (" + newid1 + ",'" + enteredTitle + "','" + dat1 + "','" + Stat + "','" +
                        enteredDesc[0] + "','" + complete + "')")
                    for i in doms:
                        domain_id = (Domains.objects.filter(domainname=i))[0].domid
                        domain_id1 = str(domain_id)
                        cursor.execute("insert into Projdom values(" + newid1 + "," + domain_id1 + ")")
                    for i in enteredMentor:
                        Mentor = Profinfo.objects.filter(name=i)
                        MentorID = str(Mentor[0].profid)
                        cursor.execute("insert into Projprof values(" + newid1 + "," + MentorID + ")")
                    for i in EnteredUSNs:
                        if i != logged_user_usn and (Studentinfo.objects.filter(usn=i)):
                            cursor.execute("insert into Studprojgrade values('" + i + "'," + newid1 + ",'-')")
                    cursor.execute("insert into Studprojgrade values('" + logged_user_usn + "'," + newid1 + ",'-')")
                    error = 2
                    # return HttpResponseRedirect('/dashboard.html')

            except Exception as e:
                print(e)
                error = 1

                # ProjFiles
                # ProjProfCom
        domains = Domains.objects.filter()
        prof = Profinfo.objects.filter()
        return render(request, 'se1/dashboard/add_project.html', {'ERROR': error, 'DOM': domains, "prof": prof})

    else:
        return redirect(rendersystem)




@csrf_exempt
def renderdashboard(request):
    # render current project details
    print("*******************", request.session.get('member_id'))
    if(request.session and request.session.get('member_id') and request.session.get('member_id') != '' and request.session.get('member_id') != 'guest'):
        u = request.session.get('member_id')
        all1 = list(Studprojgrade.objects.filter(usn=u))
        all_prof = list(Profinfo.objects.filter(name=u))
        data = request.POST
        if (request.method == "POST"):
            if (data.get("student") == "student"):
                if request.POST.get('remove'):
                    proj = request.POST.get('remove')
                    print(proj)
                    ins = Studprojgrade.objects.filter(projid=proj)
                    ins.delete()
                    print("del grade")
                    ins = Projprof.objects.filter(projid=proj)
                    ins.delete()
                    print("del prof")
                    ins = Projdom.objects.filter(projid=proj)
                    ins.delete()
                    print("del dom")
                    ins = Projfiles.objects.filter(projid=proj)
                    ins.delete()
                    ins = Projprofcom.objects.filter(projid=proj)
                    ins.delete()
                    print("del projfiles")
                    ins = FilesUpload.objects.filter(projid=proj)
                    ins.delete()
                    print("del filesupload")
                    ins = Chat.objects.filter(projid=proj)
                    ins.delete()
                    print("del chat")
                    ins = Project.objects.filter(projid=proj)
                    ins.delete()
                    print("all deleted")
                    if os.path.isdir(FILE_PATH + proj):
                        shutil.rmtree(FILE_PATH + proj)
                    return HttpResponseRedirect('/pmsystem/dashboard.html')
                request.session['proj_name'] = request.POST.get('proj_name')  # set proj_name in session variable
                request.session['from_page'] = "own"  # indicating where it comes from
                return redirect(renderproject_details_view)
            elif (data.get("prof") == "prof"):
                request.session['proj_name'] = request.POST.get('proj_name')  # set proj_name in session variable
                if (len(all1) != 0):
                    request.session['from_page'] = "own"  # indicating where it comes from
                else:
                    request.session['from_page'] = 'table'
                    request.session['prof'] = 'prof'
                return redirect(renderproject_details_view)


        else:
            if (len(all1) > 0):
                final_current_projs = find_projects(u, complete="Ongoing")
                # print("*****",final_current_projs)
                return render(request, 'se1/dashboard/dashboard.html', {'final_current_projs': final_current_projs})
            elif (len(all_prof) > 0):
                all1 = list(Studprojgrade.objects.filter(usn=u))
            all_prof = list(Profinfo.objects.filter(name=u))
            all2 = []
            all3 = []
            all4 = []
            print(request.session.get('prof') + 'indide student')
            if (len(all1) != 0):
                for i in all1:
                    all5 = []
                    x = i.projid
                    l = list(Project.objects.filter(projid=x))
                    if (not l[0].complete):
                        all4 = list(Projprof.objects.filter(projid=x))
                        for ii in all4:
                            xx = ii.profid
                            # print(xx)
                            all6 = []
                            all6 = list(Profinfo.objects.filter(profid=xx))
                            all5.append(all6[0])
                        l1 = list(Studprojgrade.objects.filter(projid=x))
                        l.append(l1)
                        l.append(all5)
                        all2.append(l)
                return render(request, 'se1/dashboard/dashboard.html', {'all2': all2})
            elif (len(all_prof) != 0):
                all1 = []
                all2 = []
                prof_details = list(Profinfo.objects.filter(name=u))
                name = u
                com_stu_prof = []

                prof_id = 0
                for i in prof_details:
                    x = i.profid
                    all1 = list(Projprof.objects.filter(profid=x))
                    prof_id = x
                for i in all1:
                    usn_s = []
                    com_stu_prof = []
                    x = i.projid
                    l = Project.objects.filter(projid=x)
                    s = list(Studprojgrade.objects.filter(projid=x))
                    if (l[0].status == 'Ongoing'):
                        com_stu_prof.append(l)
                        com_stu_prof.append(s)
                        all2.append(com_stu_prof)
                return render(request, 'se1/dashboard/dashboard_prof.html', {'all2': all2})
            else:
                return redirect(rendersystem)
    else:
        return redirect(rendersystem)


@csrf_exempt
def rendertable(request):
    # render previous project details
    if(request.session and request.session.get('member_id') and request.session.get('member_id') != ''):
        u = request.session.get('member_id')
        if (request.method == "POST"):
            request.session['proj_name'] = request.POST.get('proj_name')  # set proj_name in session variable
            request.session['from_page'] = "table"  # indicating where it comes from
            return redirect(renderproject_details_view)
        else:
            final_previous_projs = find_projects(u, complete="Completed")
            return render(request, 'se1/dashboard/table.html', {'final_previous_projs': final_previous_projs})
    else:
        return redirect(rendersystem)

@csrf_exempt
def rendertable1(request):
    # render all project details
    if(request.session and request.session.get('member_id') and request.session.get('member_id') != ''):
        u = request.session.get('member_id')
        if (request.method == "POST"):
            request.session['proj_name'] = request.POST.get('proj_name')  # set proj_name in session variable
            request.session['from_page'] = "other"  # indicating where it comes from
            print("kk", request.POST.get('proj_name'))
            return redirect(renderproject_details_view)

        final_all_projs = find_projects()
        return render(request, 'se1/dashboard/table1.html', {'final_all_projs': final_all_projs})
    else:
        return redirect(rendersystem)


@csrf_exempt
def renderproject_details_view(request):
    if(request.session and request.session.get('member_id') and request.session.get('member_id') != ''):
        proj_name = request.session.get('proj_name')
        project = Project.objects.filter(title=proj_name)
        member_usns = []
        member_emails = []
        member_names = []
        member = []
        profs_id = []
        profs_name = []
        profs_email = []
        prof = []
        members = Studprojgrade.objects.filter(projid=project[0].projid)  # team members table
        profs = Projprof.objects.filter(projid=project[0].projid)  # guides table
        for i in project:  # obtain synopsis of projects using each row
            synopsis = i.synopsis
        for i in members:  # obtain members of projects
            member_usns.append(i.usn)
        for i in profs:  # obtain all the guides
            profs_id.append(i.profid)
        for i in profs_id:  # obtain name and email id using prof id
            profs_name.append(Profinfo.objects.filter(profid=i)[0].name)
            profs_email.append(Profemail.objects.filter(profid=i)[0].email)
        for i in member_usns:  # obtain the names and email addresses of the members
            member_names.append(Studentinfo.objects.filter(usn=i)[0].name)
            member_emails.append(Studemail.objects.filter(usn=i)[0].email)

        guest = 'none'
        if (request.session.get('guest')):
            guest = request.session.get('guest')
        if (request.session.get('prof')):
            prof = request.session.get('prof')

        prof = zip(profs_name, profs_email)
        inter = zip(member_usns, member_emails)
        student = zip(member_names, inter)

        if (guest == 'guest') or (request.session.get('member_id') in profs_name):
            grade = Studprojgrade.objects.filter(usn=member_usns[0], projid=project[0].projid)[0].grade
        elif request.session.get('member_id') not in profs_name:
            grade1 = Studprojgrade.objects.filter(usn=request.session['member_id'], projid=project[0].projid)
            if (grade1):
                grade = grade1[0].grade
            else:
                grade = '-'  # project grade

        stud_proj_grade_objs = Studprojgrade.objects.filter(usn=request.session.get('member_id'), projid=project[0].projid)
        if (stud_proj_grade_objs):
            grade = stud_proj_grade_objs[0].grade  # project grade
        else:
            grade = "-"

        # get list of files for the project
        file_names = get_files(project[0].projid)
        if (len(file_names) == 0):
            file_names.append("-")

        if (request.session["from_page"] == "own"):  # check if it's coming from dashboard
            template = 'se1/dashboard/project_view.html'
        elif (request.session["from_page"] == "other"):
            template = 'se1/dashboard/others_view.html'
        else:
            if (request.session['member_id'] not in profs_name and (guest == '' or guest == 'none')):
                template = 'se1/dashboard/previous_projects_view.html'
            elif (guest == 'guest'):
                template = 'se1/dashboard/project_view_guest.html'
            elif (request.session['member_id'] in profs_name and guest == 'none'):
                template = 'se1/dashboard/project_view_prof.html'
        cursor = connection.cursor()
        if (request.method == "POST"):
            print("**********POST")
            try:
                error = 1
                if (request.POST.get("upload")):  # uploading a file
                    f = request.FILES['myfile']
                    '''for s in f.chunks():
                        print(s)'''
                    name = f.name
                    fileid = FilesUpload.objects.all().order_by("-fileid")
                    print("length**************", len(fileid))
                    if (len(fileid) != 0):
                        # fileid = idmax[0]
                        print("fileid************", fileid[0].fileid)
                        newid = fileid[0].fileid + 1
                        uploadTrue = FilesUpload.objects.filter(projid=project[0].projid).filter(filename=name)
                        if (len(uploadTrue) == 0):
                            u = FilesUpload(projid=project[0].projid, fileid=newid, filename=name, file=f)
                            u.save()
                        else:
                            error = 2
                            raise Exception
                        print("herenewid******", newid)
                    elif (len(fileid) == 0):
                        print("len is zero!!********")
                        u = FilesUpload(projid=project[0].projid, fileid=1, filename=name, file=f)
                        u.save()
                    # newid = fileid + 1
                    print(type(f))
                    # cursor.execute("insert into filesupload values("+str(project[0].projid)+","+str(newid)+", '"+name+"',"+str(f)+")")
                    # print("newid***************", newid)

                    template = loader.get_template('se1/dashboard/project_view.html')
                    context = {}
                    return redirect(renderproject_details_view)
                elif (request.POST.get("download")):  # downloading a file
                    # print("hi")
                    print("FileName************", request.POST.get("filename"))
                    file_path = FILE_PATH + str(project[0].projid) + '/' + request.POST.get(
                        "filename")
                    file = open(file_path, 'r')
                    my_data = file.readlines()
                    response = HttpResponse(my_data, content_type='text/plain')
                    response['X-Sendfile'] = file_path
                    response['Content-Length'] = os.stat(file_path).st_size
                    response['Content-Disposition'] = 'attachment; filename= ' + request.POST.get("filename")
                    return response
                    # return redirect(renderproject_details_view)
                elif (request.POST.get("view")):
                    file_path = FILE_PATH + str(project[0].projid) + '/' + request.POST.get(
                        "filename")
                    file = open(file_path, 'r')
                    # request.session['file']=file
                    request.session['name'] = request.POST.get("filename")
                    # my_data = file.readlines()
                    my_data = ""
                    for line in file:
                        my_data = my_data + line
                    request.session['mydata'] = my_data
                    # print my_data
                    # return render(request, 'se1/dashboard/txt-editor.html', {"mydata":my_data})
                    return redirect(txtEditor)
                elif (request.POST.get("del")):
                    file_path = FILE_PATH + str(project[0].projid) + '/' + request.POST.get(
                        "filename")
                    os.remove(file_path)
                    instance = FilesUpload.objects.filter(filename=request.POST.get("filename")).filter(
                        projid=project[0].projid)
                    instance.delete()
                    return redirect(renderproject_details_view)

            except Exception as e:
                print(e)
                return render(request, template,
                              {'KEY': error, 'FILES': file_names, 'GRADE': grade, 'STUDENT': student, 'PROF': prof,
                               'NAME': proj_name,
                               'SYNOPSIS': synopsis})
        else:
            return render(request, template,
                          {'KEY': 0, 'FILES': file_names, 'GRADE': grade, 'STUDENT': student, 'PROF': prof,
                           'NAME': proj_name,
                           'SYNOPSIS': synopsis})
    else:
        return redirect(rendersystem)


def get_files(projid):
    file_names = []
    files = FilesUpload.objects.filter(projid=projid)
    for i in files:
        file_names.append(i.filename)
    return file_names


def rendernotifications(request):
    # TODO
    u = request.session['member_id']
    return render(request, 'se1/dashboard/notifications.html', {})


def rendertemplate(request):
    # TODO
    u = request.session['member_id']
    return render(request, 'se1/dashboard/template.html', {})


@csrf_exempt
def rendertable2(request):
    # TODO
    u = request.session['member_id']
    return render(request, 'se1/dashboard/table2.html', {})


## Utility Functions

# Function to find details of projects
def find_projects(user="Not Required", complete="Not Required"):
    if (user == "Not Required"):
        stud_projs = set(Studprojgrade.objects.filter())
    else:
        stud_projs = set(
            Studprojgrade.objects.filter(usn=user))  # Find all the projects and their details for the given user.
    final_projs = []  # Final list of projects with all the details

    ## Find details(Project,Students,professors) of each of the projects
    for i in stud_projs:
        pid = i.projid
        all_proj_details = []
        proj_details = list(Project.objects.filter(projid=pid))  # Find the project with the given project id
        prof_details = []
        stud_details = []
        if (complete == "Not Required" or proj_details[0].status == complete):
            prof_id_list = list(Projprof.objects.filter(projid=pid))
            for i1 in prof_id_list:
                prof_id = i1.profid
                prof_details.append(list(Profinfo.objects.filter(profid=prof_id))[0])
            stud_details = list(Studprojgrade.objects.filter(projid=pid))  # Student details for the project
            all_proj_details.append(proj_details[0])  # Add project details
            all_proj_details.append(prof_details)  # Add professor details
            all_proj_details.append(stud_details)  # Add student details
            final_projs.append(all_proj_details)  # Add details to the final list
    return final_projs


@csrf_exempt
def txtEditor(request):
    # TODO
    if(request.session and request.session.get('member_id') and request.session.get('member_id') != '' and request.session.get('member_id') != 'guest'):
        guest = 'none'
        if (request.session['guest']):
            guest = request.session['guest']
        if (request.session['prof']):
            prof = request.session['prof']
        if (guest == 'guest') or prof != 'none':
            print(prof)
            my_data = request.session['mydata']
        else:
            prof = ""
            guest = ""
        u = request.session['member_id']
        proj_name = request.session['proj_name']
        project = Project.objects.filter(title=proj_name)
        name = request.session['name']
        my_data = request.session['mydata']
        fileid = FilesUpload.objects.all().order_by("-fileid")
        if request.POST.get("save"):
            if (request.POST.get("filename") != ""):
                name = request.POST.get("filename")
            file_path = FILE_PATH + str(project[0].projid) + '/' + name
            f = open(file_path, 'w+')
            f.write(request.POST.get("textdata"))
            my_data = request.POST.get("textdata")
            content = ContentFile(f.read())
            # print request.POST.get("textdata")
            newid = fileid[0].fileid + 1
            if (request.POST.get("filename") != ""):
                name = request.POST.get("filename")
                a = FilesUpload(projid=project[0].projid, fileid=newid, filename=name, file=content)
            else:
                instance = FilesUpload.objects.filter(filename=name).filter(projid=project[0].projid)
                newid = instance[0].fileid
                instance.delete()
                a = FilesUpload(projid=project[0].projid, fileid=newid, filename=name, file=content)
            '''instance = FilesUpload.objects.filter(filename=name).filter(projid=project[0].projid)
            instance.delete()
            a = FilesUpload(projid=project[0].projid, fileid=newid, filename=name, file=content)'''
            a.save()
        return render(request, 'se1/dashboard/txt-editor.html', {"mydata": my_data, "prof": prof, "guest": guest})
    else:
        return redirect(rendersystem)


@csrf_exempt
def tryAjax(request):
    if request.method == 'POST':
        x = request.POST['client_response']
        print(request.session['member_id'])
        y = Studentinfo.objects.filter(usn=x)
        print(x)
        # response_dict = {}
        # response_dict.update({'server_response': y })
        posts_serialized = serializers.serialize('json', y)
        return JsonResponse(posts_serialized, safe=False)
        # return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
    else:
        return render(request, 'tryingAjax.html')


@csrf_exempt
def chat_table(request):
    if(request.session and request.session.get('member_id') and request.session.get('member_id') != '' and request.session.get('member_id') != 'guest'):
        print("hi")
        person = request.session['member_id']
        stud = False
        prof = False
        print("************HERE")
        if request.method == 'POST':
            print("****************CHAT")
            if request.is_ajax():
                print("***********INSIDE")
                chat_content = request.POST['client_response']
                # print("*************", chat_content)
                chat_content = re.sub(r"\n", " ", chat_content);
                # print("*************", chat_content)
                if (len(Studentinfo.objects.filter(usn=person)) > 0):
                    namePerson = Studentinfo.objects.filter(usn=person)[0].name
                    stud = True

                elif (len(Profinfo.objects.filter(name=person)) > 0):
                    namePerson = Profinfo.objects.filter(name=person)[0].name
                    prof = True

                name = {"name": namePerson}
                idmax = Chat.objects.all().order_by("-chatid")
                if (len(idmax) > 0):
                    idmax = idmax[0]
                    newid = idmax.chatid + 1
                else:
                    newid = 1

                chatid = str(newid)
                p_name = request.session['proj_name']
                p_id = str(Project.objects.filter(title=p_name)[0].projid)
                print("in chat")
                nowtim = str(timezone.now())
                cursor = connection.cursor()
                if (stud):
                    cursor.execute(
                        "insert into Chat values ('" + chatid + "','" + person + "',null,'" + p_id + "','" + chat_content + "','" + nowtim + "')")
                elif (prof):
                    cursor.execute(
                        "insert into Chat values ('" + chatid + "',null,'" + person + "','" + p_id + "','" + chat_content + "','" + nowtim + "')")
                return JsonResponse(name)
        else:
            print("bye")
            s = request.session['member_id']
            p_name = request.session['proj_name']
            print(s)
            print(p_name)
            p_id = str(Project.objects.filter(title=p_name)[0].projid)
            dic = {}
            msgs = []
            chat_obj = Chat.objects.filter(projid=p_id)
            for i in chat_obj:
                print(i)
                if i.usn == s:
                    place = "right"
                    qwe = i.usn
                    name = Studentinfo.objects.filter(usn=qwe)
                    print(name)
                    name = name[0].name
                elif i.name == s:
                    place = "right"
                    qwe = i.name
                    name = Profinfo.objects.filter(name=qwe)
                    print(name)
                    name = name[0].name
                else:
                    place = "left"
                    stList = Studentinfo.objects.filter(usn=i.usn)
                    # print(name)
                    if (len(stList) > 0):
                        name = stList[0].name
                    pfList = Profinfo.objects.filter(name=i.name)
                    if (len(pfList) > 0):
                        name = pfList[0].name

                dic[i.time_stamp] = [name, i.chatcontent, place, i.time_stamp]
            time = sorted(dic)
            for i in time:
                msgs.append(dic[i])
            context = {"dic": msgs}
            dic = {}
            print("hello")
            return render(request, "se1/dashboard/chat_table.html", context)
    else:
        return redirect(rendersystem)


@csrf_exempt
def chat_page(request):
    # TODO
    u = request.session['member_id']
    return render(request, 'chat_page.html', {})


@csrf_exempt
def renderguest(request):
    if (request.method == "POST"):
        try:
            request.session['prof'] = ''
            del request.session['member_id']
        except KeyError:
            pass

        request.session['member_id'] = 'guest'
        request.session['proj_name'] = request.POST.get('proj_name')

        # set proj_name in session variable
        request.session['from_page'] = "others"
        request.session['guest'] = "guest"  # indicating where it comes from

        return redirect(renderproject_details_view)
    else:
        try:
            request.session['prof'] = ''
            del request.session['member_id']
        except KeyError:
            pass
        all1 = []
        all1 = list(Project.objects.all())
        all2 = []
        all3 = []
        l = []
        total = []
        for i in all1:
            l = []
            x = i.projid
            all2 = list(Studprojgrade.objects.filter(projid=x))
            all3 = list(Projprof.objects.filter(projid=x))
            all4 = list(Project.objects.filter(projid=x))
            l.append(all4)
            l.append(all2)
            l.append(all3)
            total.append(l)

        return render(request, "se1/dashboard/guest.html", {'total': total})


@csrf_exempt
def rendernewtable(request):
    if(request.session and request.session.get('member_id') and request.session.get('member_id') != ''):
        u = request.session['member_id']
        if (request.method == "POST"):
            request.session['proj_name'] = request.POST.get('proj_name')  # set proj_name in session variable
            request.session['prof'] = 'prof'
            request.session['from_page'] = "others"  # indicating where it comes from
            return redirect(renderproject_details_view)
        all1 = []
        all2 = []
        prof_details = list(Profinfo.objects.filter(name=u))
        name = u
        com_stu_prof = []

        prof_id = 0
        for i in prof_details:
            x = i.profid
            all1 = list(Projprof.objects.filter(profid=x))
            prof_id = x
        for i in all1:
            usn_s = []
            com_stu_prof = []
            x = i.projid
            l = Project.objects.filter(projid=x)
            s = list(Studprojgrade.objects.filter(projid=x))
            if (l[0].status == 'Completed'):
                com_stu_prof.append(l)
                com_stu_prof.append(s)
                all2.append(com_stu_prof)
        return render(request, 'se1/dashboard/newtable.html', {'all2': all2, 'name': name, 'prof_id': prof_id})
    else:
        return redirect(rendersystem)


def renderlogout(request):
    print(request.session['member_id'])
    try:
        request.session['prof'] = ''
        del request.session['member_id']
    except KeyError:
        pass
    '''request.session['member_id'] = ''
    request.session['prof'] = '''''
    return redirect(rendersystem)
