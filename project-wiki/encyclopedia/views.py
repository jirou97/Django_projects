from django.shortcuts import render
from django.http  import HttpResponseRedirect
from django.urls  import reverse
from . import util
from random import randint
from django import forms
from django.utils.safestring import mark_safe


class NewPageForm(forms.Form):
    title = forms.CharField(label = "Title", max_length = 100 )
    text = forms.CharField(label = 'Text', widget=forms.Textarea(attrs={'width':"25%" , 'height':"25%", 'cols' : "80", 'rows': "20", }))
    
    
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request , name):
    if (name in util.list_entries()):
        return render(request, "encyclopedia/entry.html", {
            "entry": name,
            "text": markdown2.markdown(util.get_entry(name))
        })
    else :
        return render(request, "encyclopedia/error.html", {
                    "message": "Entry doesn't exist"
                })

def search(request):
    if request.method == "POST" :
        title = request.POST["q"]
        y = util.list_entries()
        if title in y:
            return render(request, "encyclopedia/search.html", {
                "entries": [title]
            })
        else :
            results=[]
            for name in y:
                if title in name:
                    results+=[name]
            return render(request, "encyclopedia/search.html", {
                "entries": results
            })

def random(request):
    y = util.list_entries()
    rand = randint(0,len(y)-1)
    return entry(request,y[rand])
    
def new_entry(request):
    if request.method == "POST" :
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            if title not in util.list_entries() :
                util.save_entry(title,text)
                return entry(request,title)
            else :
                return render(request, "encyclopedia/error.html", {
                    "message": "Entry already exists"
                })
        else :
            return render(request, "encyclopedia/new_entry.html" , {
            "form" : form
            })
        
    return render(request, "encyclopedia/new_entry.html" , {
            "form" : NewPageForm()
            })
 
