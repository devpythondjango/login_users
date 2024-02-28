from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.http import HttpResponseNotFound


# @csrf_protect
# @ensure_csrf_cookie
# @login_required(login_url="login")
# def index(request):
#     context = {'segment': 'index'}

#     html_template = loader.get_template('layouts/index.html')
#     return HttpResponse(html_template.render(context, request))


@csrf_protect
@ensure_csrf_cookie
@login_required(login_url="login")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template      = request.path.split('%/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:
        html_template = loader.get_template( '404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template( '404.html' )
        return HttpResponse(html_template.render(context, request))

def handle_unknown_path(request, unknown_path):
    context = {'segment': unknown_path}
    
    try:
        load_template = unknown_path.replace("/", "-") + '.html'
        html_template = loader.get_template(load_template)
        return render(request, load_template, context)
    except loader.TemplateDoesNotExist:
        html_template = loader.get_template('page-404.html')
        return render(request, 'page-404.html', context, status=404)
    except:
        html_template = loader.get_template('page-505.html')
        return render(request, 'page-505.html', context, status=500)