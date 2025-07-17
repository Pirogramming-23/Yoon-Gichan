from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Idea, IdeaStar
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import DevTool, Idea

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

@login_required
def toggle_star(request, id):
    idea = Idea.objects.get(id=id)
    star, created = IdeaStar.objects.get_or_create(user=request.user, idea=idea)

    if not created:
        star.delete()
        result = 'unstarred'
    else:
        result = 'starred'

    return JsonResponse({'result': result})

def idea_list(request):
    sort = request.GET.get('sort', 'recent')
    page = request.GET.get('page', 1)

    if sort == 'interest':
        ideas = Idea.objects.all().order_by('-interest')
    elif sort == 'name':
        ideas = Idea.objects.all().order_by('name')
    else:
        ideas = Idea.objects.all().order_by('-created_at')

    paginator = Paginator(ideas, 4)
    page_obj = paginator.get_page(page)

    starred_ideas = []
    if request.user.is_authenticated:
        starred_ideas = IdeaStar.objects.filter(user=request.user).values_list('idea_id', flat=True)

    return render(request, 'idea_list.html', {'page_obj': page_obj, 'sort': sort, 'starred_ideas': starred_ideas})

def idea_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        devtool_id = request.POST.get('devtool')
        image = request.FILES.get('image')

        devtool = DevTool.objects.get(id=devtool_id)
        Idea.objects.create(name=name, description=description, devtool=devtool, image=image)

        return redirect('idea_list')

    devtools = DevTool.objects.all()
    return render(request, 'idea_form.html', {'devtools': devtools, 'idea': {}})

def idea_detail(request, id):
    idea = Idea.objects.get(id=id)
    starred = False
    if request.user.is_authenticated:
        starred = IdeaStar.objects.filter(user=request.user, idea=idea).exists()
    return render(request, 'idea_detail.html', {'idea': idea, 'starred': starred})

def idea_update(request, id):
    idea = Idea.objects.get(id=id)
    if request.method == 'POST':
        idea.name = request.POST.get('name')
        idea.description = request.POST.get('description')
        devtool_id = request.POST.get('devtool')
        image = request.FILES.get('image')

        idea.devtool = DevTool.objects.get(id=devtool_id)
        if image:
            idea.image = image
        idea.save()
        return redirect('idea_list')

    devtools = DevTool.objects.all()
    return render(request, 'idea_form.html', {'idea': idea, 'devtools': devtools})

def idea_delete(request, id):
    idea = Idea.objects.get(id=id)
    idea.delete()
    return redirect('idea_list')

def devtool_list(request):
    devtools = DevTool.objects.all()
    return render(request, 'devtools_list.html', {'devtools': devtools})

def devtool_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        kind = request.POST.get('kind')
        description = request.POST.get('description')
        DevTool.objects.create(name=name, kind=kind, description=description)
        return redirect('devtool_list')
    return render(request, 'devtool_form.html', {'devtool': {'name': '', 'kind': '', 'description': ''}})

def devtool_detail(request, id):
    devtool = DevTool.objects.get(id=id)
    ideas = Idea.objects.filter(devtool=devtool)
    return render(request, 'devtool_detail.html', {'devtool': devtool, 'ideas': ideas})

def devtool_update(request, id):
    devtool = DevTool.objects.get(id=id)
    if request.method == 'POST':
        devtool.name = request.POST.get('name')
        devtool.kind = request.POST.get('kind')
        devtool.description = request.POST.get('description')
        devtool.save()
        return redirect('devtool_list')
    return render(request, 'devtool_form.html', {'devtool': devtool})

def devtool_delete(request, id):
    devtool = DevTool.objects.get(id=id)
    devtool.delete()
    return redirect('devtool_list')

@require_POST
def adjust_interest(request, id):
    idea = Idea.objects.get(id=id)
    action = request.POST.get('action')

    if action == 'up':
        idea.interest += 1
    elif action == 'down' and idea.interest > 0:
        idea.interest -= 1

    idea.save()
    return redirect('idea_detail', id=id)


# AJAX: Toggle star
@require_POST
@csrf_exempt
def toggle_star_ajax(request, id):
    idea = Idea.objects.get(id=id)
    star, created = IdeaStar.objects.get_or_create(user=request.user, idea=idea)

    if not created:
        star.delete()
        result = 'unstarred'
    else:
        result = 'starred'

    return JsonResponse({'result': result})


# AJAX: Adjust interest
@require_POST
@csrf_exempt
def adjust_interest_ajax(request, id):
    idea = Idea.objects.get(id=id)
    action = request.POST.get('action')

    if action == 'up':
        idea.interest += 1
    elif action == 'down' and idea.interest > 0:
        idea.interest -= 1

    idea.save()
    return JsonResponse({'interest': idea.interest})
