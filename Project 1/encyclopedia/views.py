from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from . import util
from markdown2 import Markdown
import random

def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)
    
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = convert_md_to_html(title)
    if content == None:
        return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/entry.html", {
            "content": content,
            "title": title
        })

def search(request): 
    # Get the value of 'q' input field
    # .get() method returns none if the key doesn't exist
    query = request.GET.get('q') 
    # If value exists
    if query:
        # modified query
        mod_query = query.strip().lower()
        entries = util.list_entries()
        # everything lowercased in entries for comparison
        # check if string is empty
        if mod_query == "":
            return redirect("index")
        # exact match
        match = next(
            (entry for entry in entries if (entry.lower()) == mod_query),
            None
        )
        if match:
            return redirect("entry", title=match)
        # substring match - return list
        else:
            results = [entry for entry in entries if mod_query in entry.lower()]
            if results == []:
                return redirect("index")
            return render(request, "encyclopedia/results.html", {
                "results": results
            })
    else:
    # if value does not exist
        return redirect("index")

def create(request):
    if request.method == "POST":
        title = request.POST.get("title", "")
        content = request.POST.get("content", "")
        
        clean_title = title.strip()
        clean_content = content.strip()
        
        entries = util.list_entries()

        # verify - no whitespaces, and if title already exists
        if clean_title == "" or clean_content == "":
            return render(request, "encyclopedia/error.html", {
                "error_message": "You must include both title and content."
            }) 
        elif title.strip().lower() in [entry.lower() for entry in entries]:
            return render(request, "encyclopedia/error.html", {
                "error_message": "Page already exists!"
            }) 
        else:
            md_title = "# " + clean_title
            md_content = md_title + "\n" + "\n" + clean_content
            util.save_entry(clean_title, md_content)
            return redirect("entry", title=clean_title)
    else:
        return render(request, "encyclopedia/create.html")
    
def edit(request, title):
    content = util.get_entry(title)

    # check if page exists
    if content == None:
        return render(request, "encyclopedia/error.html", {
               "error_message": "Page not found."
           })
    
    # GET logic
    if request.method == "GET":
        split_content = content.splitlines()
        remaining_lines = split_content[1:]
        spliced_content = '\n'.join(remaining_lines)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": spliced_content
        })
    
    # POST logic
    else:
      edited_content = request.POST.get("content", "").strip()
      if edited_content == "":
        return render(request, "encyclopedia/error.html", {
            "error_message": "The text field is empty!"
        })
      
      # If valid, save user input
      else:
        # append title
        full_entry = "# " + title + "\n" + edited_content
        util.save_entry(title, full_entry)
        return redirect("entry", title=title)
        
def random_page(request):
    entries = util.list_entries()
    if entries:
        random_entry = random.choice(entries)
        return redirect("entry", title=random_entry) 
    else:
        return redirect('index')


   