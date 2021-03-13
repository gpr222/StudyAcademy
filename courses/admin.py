from django.contrib import admin
from courses.models import Course, Tag, Prerequisite, Learning, Video, UserCourse, Payment
from django.utils.html import format_html


class TagAdmin(admin.TabularInline):
    model = Tag


class VideoAdmin(admin.TabularInline):
    model = Video


class PrerequisiteAdmin(admin.TabularInline):
    model = Prerequisite


class LearningAdmin(admin.TabularInline):
    model = Learning


class CourseAdmin(admin.ModelAdmin):
    inlines = [TagAdmin, PrerequisiteAdmin, LearningAdmin, VideoAdmin]
    list_display = ['name', 'get_price', 'get_discount', 'active']
    list_filter = ['discount', 'active']

    def get_discount(self, course):
        return f'{course.discount}%'

    def get_price(self, course):
        return f'₹ {course.price}'

    get_discount.short_description = 'Discount'
    get_price.short_description = 'Price'


class PaymentAdmin(admin.ModelAdmin):
    model = Payment
    list_display = ['order_id', 'get_user', 'get_course', 'status']
    list_filter = ['course', 'status']

    def get_user(self, payment):
        return format_html(f'<a href="/admin/auth/user/{payment.user.id}">{payment.user}</a>')

    def get_course(self, payment):
        return format_html(f'<a href="/admin/courses/course/{payment.course.id}">{payment.course}</a>')

    get_user.short_description = 'User'
    get_course.short_description = 'Course'


class VideoAdmin(admin.ModelAdmin):
    model = Video
    list_display = ['title', 'get_course', 'is_preview']
    list_filter = ['course', 'is_preview']

    def get_course(self, payment):
        return format_html(f'<a href="/admin/courses/course/{payment.course.id}">{payment.course}</a>')

    get_course.short_description = 'Course'


class UserCourseAdmin(admin.ModelAdmin):
    model = UserCourse
    list_display = ['get_details', 'get_user', 'get_course']

    def get_details(self, UserCourse):
        return('Show Details')

    def get_user(self, UserCourse):
        return format_html(f'<a href="/admin/auth/user/{UserCourse.user.id}">{UserCourse.user}</a>')

    def get_course(self, UserCourse):
        return format_html(f'<a href="/admin/courses/course/{UserCourse.course.id}">{UserCourse.course}</a>')

    get_course.short_description = 'Course'
    get_user.short_description = 'User'
    get_details.short_description = 'UserCourse'


admin.site.register(Course, CourseAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(UserCourse, UserCourseAdmin)
admin.site.register(Payment, PaymentAdmin)
