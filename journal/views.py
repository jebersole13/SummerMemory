from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
def index(request):
    """ Homepage for ll """
    return render(request,'journal/index.html')

@login_required
def topics(request):
   

    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics':topics}
    return render(request, 'journal/topics.html',context)
@login_required
def topic(request, topic_id):

    topic = get_object_or_404(Topic,id=topic_id)
    if topic.owner != request.user:
        raise  Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic, 'entries':entries}
    return render (request,'journal/topic.html', context)

@login_required
def new_topic(request):

    if request.method != 'POST':
        #No data submitted; create a blank form.
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('journal:topics')
    context = {'form':form}
    return render(request, 'journal/new_topic.html', context)

@login_required
def new_entry(request, topic_id):

    topic = get_object_or_404(Topic,id=topic_id)
    if topic.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        form= EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('journal:topic', topic_id=topic_id)
    context = {'topic':topic, 'form': form}
    return render(request, 'journal/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
 
    entry = get_object_or_404(Entry,id=entry_id)
    topic = entry.topic
    if topic.owner !=request.user:
        raise Http404
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('journal:topic', topic_id=topic.id)
    context ={'entry':entry, 'topic':topic, 'form':form}
    return render(request, 'journal/edit_entry.html', context)

@login_required
def delete_topic(request,topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if topic.owner != request.user:
        raise Http404
        
    if request.method == 'POST':
        topic.delete()
        return redirect('journal:topics')
    return render(request,'journal/delete_topic.html', {'topic':topic,  'warning': f"You're about to permanently delete topic from {topic.date_added}"})

@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    
    if topic.owner != request.user:
        raise Http404
    
    if request.method == 'POST':
        entry.delete()
        return redirect('journal:topic', topic_id=topic.id)
    return render(request, 'journal/delete_entry.html', {'entry':entry, 'topic':topic,   'warning': f"You're about to permanently delete entry from {entry.date_added}"})