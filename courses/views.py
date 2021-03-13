from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from courses.models import Course, Video, Payment, UserCourse
from courses.forms import RegistrationForm, LoginForm
from django.views import View
from django.views.generic.edit import FormView
from django.contrib.auth import logout, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from codeWithRG.settings import *
from time import time
import razorpay

client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))


def home(request):
    courses = Course.objects.filter(active=True)
    return render(request, 'courses/home.html', context={'courses': courses})


def coursePage(request, slug):
    course = Course.objects.get(slug=slug)
    serial_number = request.GET.get('lecture')
    videos = course.video_set.all().order_by('serial_number')
    if serial_number is None:
        serial_number = 1
    video = Video.objects.get(serial_number=serial_number, course=course)
    if(video.is_preview is False):
        if(request.user.is_authenticated is False):
            return redirect('login')
        else:
            user = request.user
            try:
                user_course = UserCourse.objects.get(user=user, course=course)
            except:
                return redirect('checkout', slug=course.slug)
    context = {'course': course, 'video': video, 'videos': videos}
    return render(request, template_name='courses/course_page.html', context=context)


class signupView(FormView):
    template_name = 'courses/signup.html'
    form_class = RegistrationForm
    success_url = '/login'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# we use upper method for signUP page intead of this lengthy method
'''class signupView(View):
    def get(self, request):
        form = RegistrationForm()
        print('class view ececuted successfuly...')
        return render(request, 'courses/signup.html', context={'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if(form.is_valid()):
            user = form.save()
            if(user):
                return redirect('login')
        return render(request, 'courses/signup.html', context={'form': form})
'''


class loginView(FormView):
    template_name = 'courses/login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        login(self.request, form.cleaned_data)
        return super().form_valid(form)


'''class loginView(View):
    def get(self, request):
        form = LoginForm()
        context = {
            'form': form
        }
        return render(request, 'courses/login.html', context=context)

    def post(self, request):
        form = LoginForm(request=request, data=request.POST)
        context = {
            'form': form
        }
        if(form.is_valid()):
            return redirect('home')
        return render(request, 'courses/login.html', context=context)
'''


def signout(request):
    logout(request)
    return redirect('home')


def checkout(request, slug):
    course = Course.objects.get(slug=slug)
    user = None
    if(request.user.is_authenticated is False):
        return redirect('login')
    user = request.user
    action = request.GET.get('action')
    order = None
    payment = None
    error = None
    if(action == 'create_payment'):
        try:
            user_course = UserCourse.objects.get(user=user, course=course)
            error = 'You are already enrolled in this course'
        except:
            pass

        if(error is None):
            amount = (int(course.price - (course.price*course.discount*0.01)))*100
            currency = 'INR'
            notes = {
                'email': user.email,
                'name': f'{user.first_name} {user.last_name}'
            }
            receipt = f'codeWithRG-{int(time())}'

            order = client.order.create(
                {
                    'amount': amount,
                    'currency': currency,
                    'receipt': receipt,
                    'notes': notes
                }
            )
            payment = Payment()
            payment.user = user
            payment.course = course
            payment.order_id = order.get('id')
            payment.save()

    context = {'course': course, 'order': order,
               'payment': payment, 'user': user, 'error': error}
    return render(request, template_name='courses/check_out.html', context=context)


@csrf_exempt
def verifyPayment(request):
    if(request.method == 'POST'):
        data = request.POST
        try:
            client.utility.verify_payment_signature(data)
            print(data)
            razorpay_order_id = data['razorpay_order_id']
            razorpay_payment_id = data['razorpay_payment_id']
            payment = Payment.objects.get(order_id=razorpay_order_id)
            payment.payment_id = razorpay_payment_id
            payment.status = True
            userCourse = UserCourse(user=payment.user, course=payment.course)
            userCourse.save()
            payment.user_course = userCourse
            payment.save()
            return redirect('my_courses')
        except:
            return HttpResponse('invalid payment details')


@login_required(login_url='login')
def my_courses(request):
    user = request.user
    user_courses = UserCourse.objects.filter(user=user)
    context = {
        'user_course': user_courses
    }
    return render(request, 'courses/my_courses.html', context=context)
