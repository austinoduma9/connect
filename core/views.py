

from .models import CustomUser, Company

from .forms import CustomUserCreationForm


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile,  Group, Page
from .models import Post, Comment
from django.db.models import Q
from .models import Post
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm
from .models import Project
from .forms import ProjectForm
from django.utils.timezone import now
from .forms import CustomLoginForm

##proposals



##user posts


##edit profile
@login_required
def edit_profile(request):
    user = request.user

    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile")  # Change to your profile page URL
    else:
        form = ProfileEditForm(instance=user)

    return render(request, "profile.html", {"form": form})


##profile page

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    # profile = Profile.objects.get(user=request.user)  # Fetch the profile for logged-in user

    context = {
        'profile': profile,
        'profile_views': profile.profile_views if profile.profile_views else 0,
        # 'inventions_count': profile.inventions.count() if profile.inventions else 0,
        # 'patents_count': profile.patents.count() if profile.patents else 0,
        # 'groups_count': profile.groups.count() if profile.groups else 0,
        # 'pages_count': profile.pages.count() if profile.pages else 0,
        # 'events_count': profile.events.count() if profile.events else 0,
    }
    # return render(request, 'profile.html', context)
    return render(request, 'profile.html', {'user': request.user, 'profile': profile})

##############
###############


##view user app
@login_required
def app_view(request):
    user = request.user  # Get logged-in user
    profile = Profile.objects.get(user=user)

    context = {"page_title": "App Center"}
    
    context = {
        "user": user,
        "profile": profile,
        # "profile_views": profile.views_count,  # Assuming a field exists
        # "connections_count": Connection.objects.filter(user=user).count(),
        # "inventions_count": Invention.objects.filter(user=user).count(),
        # "patents_count": Patent.objects.filter(user=user).count(),
        "groups_count": Group.objects.filter(members=user).count(),
        "pages_count": Page.objects.filter(owner=user).count(),
        # "events_count": Event.objects.filter(organizer=user).count(),
    }
    
    return render(request, "app.html", context)



##post list


##create post


##track user visitors




##fetch data from suggestions



##part 2 suggestions


def home_view(request):
    user = request.user

    # Fetch Node Suggestions
    # connected_users = Connection.objects.filter(user=user).values_list("connected_user", flat=True)
    # node_suggestions = CustomUser.objects.exclude(id__in=[user.id] + list(connected_users))[:6]

    # Fetch Companies
    companies = Company.objects.all()[:6]

    # Fetch Nodes in Community
    community_nodes = CustomUser.objects.filter(connections_received__user=user).exclude(id=user.id)[:6]

    # Fetch Profile-Based Companies
    profile_based_companies = Company.objects.filter(industry=user.profile.industry)[:6]

    return render(request, "app.html", {
        # "node_suggestions": node_suggestions,
        "companies": companies,
        "community_nodes": community_nodes,
        "profile_based_companies": profile_based_companies
    })

# Views pages
##index.html
def index(request):
    # context = {"page_title": "Home"}
    return render(request, 'index.html',{"hide_navbar": True})
##about.html
def about(request):
    context = {"page_title": "About" , "page_name": "About"}
    return render(request, 'about.html', context)
##services.html
def services(request):
    context = {"page_title": "Services", "page_name": "Services"}
    return render(request, 'services.html', context)
##dashboard.html
def dashboard(request):
    context = {"page_title": "Dashboard", "page_name": "Dashboard"}
    return render(request, 'dashboard.html', context)
##events.html
def events(request):
    context = {"page_title": "Event and News", "page_name": "Event and News"}
    return render(request, 'events.html', context)
##jobs.html
def jobs(request):
    context = {"page_title": "Jobs", "page_name": "Jobs"}
    return render(request, 'jobs.html', context)
##messages.html
def user_messages(request):
    context = {"page_title": "Messages", "page_name": "Messages"}
    return render(request, 'messages.html', context)
##networks.html
def networks(request):
    context = {"page_title": "Networks", "page_name": "Networks"}
    return render(request, 'networks.html', context)
##notifications.html
def notifications(request):
    context = {"page_title": "Notifications", "page_name": "Notifications"}
    return render(request, 'notifications.html', context)

##inventor_page.html
def inventor_page(request):
    context = {"page_title": "Inventor_page", "page_name": "Inventor_page"}
    return render(request, 'inventor_page.html', context)
##contact
def contact(request):
    context = {"page_title": "contact", "page_name": "contact"}
    return render(request, 'contact.html', context)

##app.html
def app_view(request):
    context = {"page_title": "App Center"}
    return render(request, 'app.html', context)

##event.html



##post_list

from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm  # Ensure you have imported your PostForm


def post_list(request):
    context = {"page_title": "Posts", "page_name": "Posts"}  # ✅ Always initialize context
    form = PostForm(request.POST or None, request.FILES or None)  # ✅ Initialize form at the start

    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)  # ✅ Don't save yet
            post.user = request.user  # ✅ Assign the logged-in user
            post.save()  # ✅ Save to DB
            return redirect("post_list")  # ✅ Redirect to avoid duplicate submissions

    posts = Post.objects.all().order_by("-created_at")  # ✅ Fetch posts from newest to oldest
    context["posts"] = posts
    context["form"] = form

    return render(request, "post_list.html", context)  # ✅ Pass the context correctly



##intentor page

def dashboard(request):
    user_ideas = Project.objects.filter(user=request.user)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('dashboard')  # Redirect to refresh the page
    
    else:
        form = ProjectForm()
    
    context = {
        'form': form,
        'user_ideas': user_ideas,
        # 'events': events,
    }
    return render(request, 'dashboard.html', context)

##inventor page inputs
def inventor_page(request):
    user_ideas = Project.objects.filter(user=request.user)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('inventor_page')  # Redirect to refresh the page
    
    else:
        form = ProjectForm()
        footer_message = "Thanks for visiting your inventor page! Keep innovating!"
        context = {
            'form': form,
            'user_ideas': user_ideas,
            'footer_message': footer_message
            # 'events': events,
        }
    return render(request, 'inventor_page.html', context)

###Edit Project
from django.shortcuts import render, redirect, get_object_or_404
from .models import Project
from .forms import ProjectForm

# Edit Project
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('inventor_page')  # Redirect back to the inventor page
    else:
        form = ProjectForm(instance=project)

    context = {
        'form': form,
        'project': project,
    }
    return render(request, 'edit_project.html', context)

# Delete Project
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == "POST":
        project.delete()
        return redirect('inventor_page')  # Redirect back to the inventor page
    return render(request, 'confirm_delete.html', {'project': project})


#####Edit from dashboard
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('inventor_page')  # Redirect back to the inventor page
    else:
        form = ProjectForm(instance=project)

    context = {
        'form': form,
        'project': project,
    }
    return render(request, 'inventor_page.html', context)

# Delete Project
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == "POST":
        project.delete()
        return redirect('dashboard')  # Redirect back to the inventor page
    return render(request, 'confirm_delete.html', {'project': project})





# User Registration
def register(request):
    context = {"page_title": "App Center"}
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("app")
        else:
            messages.error(request, "Registration failed. Please check your details.")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})

# User Login
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("app")
        else:
            messages.error(request, "Invalid credentials, try again.")
    return render(request, "login.html")



def login_view(request):
    form = CustomLoginForm(data=request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('app')  # Redirect to a  home page
        else:
            messages.error(request, "Invalid credentials, try again.")

    return render(request, 'login.html', {'form': form})

# User Logout
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect("login")

# User Dashboard
# @login_required
# def dashboard(request):
#     user_ideas = Idea.objects.filter(created_by=request.user)
#     events = Event.objects.all().order_by("-date")[:5]
#     return render(request, "dashboard.html", {"user_ideas": user_ideas, "events": events} )

# User Profile



# Investor Expresses Interest in an Idea


# Event Listing


# Send Connection Request


# Manage Connection Requests (Accept/Reject)



##create Project

def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Saves to SQLite
            return redirect("dashboard")  # Update with your actual dashboard URL
        else:
            print(form.errors)  # Debugging: Show errors if form fails to save
    else:
        form = ProjectForm()

    return render(request, "create_project.html", {"form": form})



##to query on search bar

def search(request):
    query = request.GET.get('q')
    results = []

    if query:
        results.extend(Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)))
        # results.extend(Idea.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)))
        # results.extend(Topic.objects.filter(name__icontains=query))
        # results.extend(Inventor.objects.filter(Q(name__icontains=query) | Q(bio__icontains=query)))
        # results.extend(Industry.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)))
        results.extend(Post.objects.filter(Q(content__icontains=query))) 

    return render(request, 'search_results.html', {'query': query, 'results': results})

##feedback form


###
import logging
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render
from .forms import ContactForm

logger = logging.getLogger(__name__)

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            logger.info(f"Received contact form: Name={name}, Email={email}, Message={message}")

            try:
                send_mail(
                    subject=f"Contact Form Message from {name}",
                    message=message,
                    from_email=email,
                    recipient_list=["odumacorp@gmail.com"],
                )
                messages.success(request, "Your message has been sent successfully!")
            except Exception as e:
                logger.error(f"Email sending failed: {e}")
                messages.error(request, "There was an error sending your message.")
            
            form = ContactForm()  # Clear the form after submission
        else:
            messages.error(request, "There was an error with your submission.")
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})

