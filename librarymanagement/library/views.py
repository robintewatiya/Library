from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from . import forms,models
from django.contrib.auth.models import Group
from django.contrib import auth
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from .models import Book
from django.urls import reverse



def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/index.html')

#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/studentclick.html')

#for showing signup/login button for admin
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/adminclick.html')



def adminsignup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()


            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('adminlogin')
    return render(request,'library/adminsignup.html',{'form':form})


def studentsignup_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('studentlogin')
    return render(request,'library/studentsignup.html',context=mydict)


def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()


def afterlogin_view(request):
    if is_admin(request.user):
        return render(request,'library/adminafterlogin.html')
    else:
        return render(request,'library/studentafterlogin.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def addbook_view(request):
    #now it is empty book form for sending to html
    form=forms.BookForm()
    if request.method=='POST':
        #now this form have data from html
        form=forms.BookForm(request.POST)
        if form.is_valid():
            user=form.save()
        else:
            return render(request, 'library/addbook.html', {'alert_flag': True,'form':form})

        return render(request,'library/bookadded.html')
    return render(request,'library/addbook.html',{'form':form})


def viewbook_view(request):
    books=models.Book.objects.all()
    return render(request,'library/viewbook.html',{'books':books})

@login_required(login_url='studentlogin')
def viewlibrary_view(request):
    book_ids = list()

    pending_requests = models.PendingAddRequest.objects.filter(
    user_id=request.user.id)

    # Remove the requested books
    for book_request in pending_requests:
        book_ids.append(book_request.book_id)

    books = models.Book.objects.all().exclude(id__in=list(set(book_ids)))

    return render(request,'library/viewlibrary.html',{'books':books})

@login_required(login_url='studentlogin')
def viewrequestedbooks(request):
    book_ids = list()

    pending_requests = models.PendingAddRequest.objects.filter(
    user_id=request.user.id)

    # Remove the requested books
    for book_request in pending_requests:
        book_ids.append(book_request.book_id)

    books = models.Book.objects.filter(pk__in=list(set(book_ids)))

    return render(request,'library/viewrequestedbooks.html',{'books':books})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def issuebook_view(request):
    form=forms.IssuedBookForm()
    if request.method=='POST':
        #now this form have data from html
        form=forms.IssuedBookForm(request.POST)
        book_record = models.Book.objects.get(isbn = request.POST.get('isbn2'))
        if form.is_valid() and book_record.allotment_status == '0':
            book_record.allotment_status = '1'
            book_record.save()
            models.IssuedBook.objects.create(
    enrollment=request.POST.get('enrollment2'), isbn=request.POST.get('isbn2'))
            # obj.save()
            return render(request,'library/bookissued.html')
        else:
            return render(request, 'library/bookissued.html', {'alert_flag': True})


    return render(request,'library/issuebook.html',{'form':form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewissuedbook_view(request):
    issuedbooks=models.IssuedBook.objects.all()
    li=[]
    for ib in issuedbooks:
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=(date.today()-ib.issuedate)
        print(date.today())
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10


        books=list(models.Book.objects.filter(isbn=ib.isbn))
        students=list(models.StudentExtra.objects.filter(enrollment=ib.enrollment))
        i=0
        for l in books:
            t=(students[i].get_name,students[i].enrollment,books[i].name,books[i].author,issdate,expdate,fine, books[i].isbn)
            i=i+1
            li.append(t)

    return render(request,'library/viewissuedbook.html',{'li':li})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewstudent_view(request):
    students=models.StudentExtra.objects.all()
    return render(request,'library/viewstudent.html',{'students':students})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewpendingrequests(request):
    all_request = list()
    pending_requests = models.PendingAddRequest.objects.all()

    for pending in pending_requests:

        one_request = dict()
        one_request['book_name'] = models.Book.objects.get(id = pending.book_id).name
        user = models.User.objects.get(id=pending.user_id)
        one_request['user_name'] = user.first_name
        one_request['user_id'] = pending.user_id
        one_request['book_id'] = pending.book_id
        all_request.append(one_request)
        print(one_request)
    print(all_request)
    return render(request,'library/viewpendingrequests.html', {'all_request':all_request})


@login_required(login_url='studentlogin')
def viewissuedbookbystudent(request):
    student=models.StudentExtra.objects.filter(user_id=request.user.id)
    issuedbook=models.IssuedBook.objects.filter(enrollment=student[0].enrollment)

    li1=[]

    li2=[]
    for ib in issuedbook:
        books=models.Book.objects.filter(isbn=ib.isbn)
        for book in books:
            t=(request.user,student[0].enrollment,student[0].branch,book.name,book.author)
            li1.append(t)
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=(date.today()-ib.issuedate)
        print(date.today())
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10
        t=(issdate,expdate,fine)
        li2.append(t)

    return render(request,'library/viewissuedbookbystudent.html',{'li1':li1,'li2':li2})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_book(request, book_id):
    book_id = int(book_id)
    try:
        book_sel = models.Book.objects.get(id = book_id)
    except models.Book.DoesNotExist:
        return HttpResponseRedirect(reverse(viewbook_view))
    book_sel.delete()
    return HttpResponseRedirect(reverse(viewbook_view))

@login_required(login_url='studentlogin')
def request_add_book(request, book_id, user_id):
    book_id = int(book_id)
    user_id = int(user_id)
    try:

      book_ids = list()

      pending_requests = models.PendingAddRequest.objects.filter(user_id = request.user.id)

    # Remove the requested books
      for book_request in pending_requests:
          book_ids.append(book_request.book_id)

      books = models.Book.objects.all().exclude(id__in=list(set(book_ids)))
      book_record = models.Book.objects.get(id = book_id)
      if book_record.allotment_status == '0':
          models.PendingAddRequest.objects.create(user_id=user_id, book_id=book_id)
      else:
          return render(request, 'library/viewlibrary.html', {'alert_flag': True, 'books':books})

    except models.Book.DoesNotExist:
        return HttpResponseRedirect(reverse(viewlibrary_view))
    return HttpResponseRedirect(reverse(viewlibrary_view))

@login_required(login_url='studentlogin')
def request_delete_book(request, book_id, user_id):
    book_id = int(book_id)
    user_id = int(user_id)
    try:
        requested_book = models.PendingAddRequest.objects.filter(
    user_id=user_id, book_id=book_id)
    except models.Book.DoesNotExist:
        return HttpResponseRedirect(reverse(viewrequestedbooks))
    requested_book.delete()
    return HttpResponseRedirect(reverse(viewrequestedbooks))

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_request(request, book_id, user_id):
    book_id = int(book_id)
    user_id = int(user_id)
    try:
        requested_book = models.PendingAddRequest.objects.filter(
    user_id=user_id, book_id=book_id)
        student = models.StudentExtra.objects.get(user_id=user_id)
        book_record = models.Book.objects.get(id=book_id)

        book_record.allotment_status = '1'

        book_record.save()

        models.IssuedBook.objects.create(enrollment = student.enrollment, isbn = book_record.isbn)
        requested_book.delete()
    except Exception as e:
        return HttpResponseRedirect(reverse(viewpendingrequests))

    return HttpResponseRedirect(reverse(viewpendingrequests))

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def deny_request(request, book_id, user_id):
    book_id = int(book_id)
    user_id = int(user_id)
    try:
        requested_book = models.PendingAddRequest.objects.filter(
    user_id=user_id, book_id=book_id)

    except Exception as e:
        return HttpResponseRedirect(reverse(viewpendingrequests))
    requested_book.delete()
    return HttpResponseRedirect(reverse(viewpendingrequests))

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def deassociate_book(request, isbn):
    try:
        issue_record = models.IssuedBook.objects.filter(isbn = isbn)
        book_record = models.Book.objects.get(isbn = isbn)
        book_record.allotment_status = '0'
        book_record.save()
    except models.Book.DoesNotExist:
        return HttpResponseRedirect(reverse(viewissuedbook_view))
    issue_record.delete()
    return HttpResponseRedirect(reverse(viewissuedbook_view))
