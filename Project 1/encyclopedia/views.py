from django.shortcuts import render, redirect
from . import util
from markdown2 import Markdown

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
            "content": content
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
        mod_entries = [item.lower() for item in entries]
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
