from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
	return '{:.5f}'.format(value*arg)
	
@register.filter
def sub(value, arg):
	return value - arg
	
@register.simple_tag
def div_and_mult(a, b, c):
	return (a / b)*c
	
#@register.simple_tag
#def mult(a, b, c):
#	return int(a)*int(b)*int(c)