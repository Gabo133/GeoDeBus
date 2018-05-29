from django.shortcuts import render

# Create your views here.
def index(request):
	template_name = "index.html"
	data = {}
	return render(request, template_name, data)