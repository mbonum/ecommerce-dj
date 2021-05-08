# import array
from django import template
from products.models import Product

register = template.Library()

# @register.inclusion_tag('products/pdetail.html')
# def get_obj(slug):
#     obj = Product.objects.filter(slug=slug, active=True)
#     o = obj.first()
#     qty = o.quantity
#     return qty

# @register.inclusion_tag('products/pdetail.html')
# def rangeqty(qty):
#     print('****** ', qty)
#     if qty > 1:
#         q = [i for i in range(1,qty)]#[0,..,qty]
#     else:
#         q = 1
#     # for i in range(1, qty):
#     #     q[i-1] = i#q.insert(i, i)array.array('i',(1 for i in range(1,qty)))
#     print(q)
#     return q
# from django.template.loader import get_template
# t = get_template('products/pdetail.html')
# register.inclusion_tag(t)(rangeqty)