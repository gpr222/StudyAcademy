from django import template
from courses.models import User,Course,UserCourse
import math

register = template.Library()


@register.simple_tag
def cal_sellPrice(price, discount):
    if discount is None or discount == 0:
        return price
    sellPrice = price
    sellPrice = price - (price * discount * 0.01)
    return math.floor(sellPrice)


@register.filter
def amount(price):
    return f'₹{price}'

@register.simple_tag
def is_enrolled(request,course):
    user = None
    if not request.user.is_authenticated:
        return False
    user = request.user
    try:
        user_course = UserCourse.objects.get(user=user,course=course)
        return True
    except:
        return False