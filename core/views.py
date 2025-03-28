

from .models import CustomUser, Idea, InvestorInterest, Event, Connection, Company

from .forms import CustomUserCreationForm, IdeaForm, EventForm

from .models import Event
from .forms import EventForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from .models import Profile, Connection, Invention, Patent, Group, Page, Event
from .models import InvestorProposal

from .models import Post, Comment
from .forms import PostForm, CommentForm
from .models import ProfileView


from django.db.models import Q
from .models import Post, Idea, Topic, Inventor, Industry


from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm

# from .views import contact
# from core.forms import ProfileEditForm
# from oduma_platform.core.forms import ProfileEditForm

##proposals
@login_required
def investor_proposals(request):
    proposals = InvestorProposal.objects.filter(post__user=request.user)
    return render(request, "proposals.html", {"proposals": proposals})

def investor_proposals(request):
    proposals = InvestorProposal.objects.all().order_by("-timestamp")
    return render(request, "proposals.html", {"proposals": proposals})


##user posts
@login_required
def user_posts(request):
    user_posts = Post.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "user_posts.html", {"user_posts": user_posts})

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

    return render(request, "edit_profile.html", {"form": form})

@login_required
def app_view(request):
    user = request.user  # Get logged-in user
    profile = Profile.objects.get(user=user)

    context = {"page_title": "App Center"}
    
    context = {
        "user": user,
        "profile": profile,
        "profile_views": profile.views_count,  # Assuming a field exists
        "connections_count": Connection.objects.filter(user=user).count(),
        "inventions_count": Invention.objects.filter(user=user).count(),
        "patents_count": Patent.objects.filter(user=user).count(),
        "groups_count": Group.objects.filter(members=user).count(),
        "pages_count": Page.objects.filter(owner=user).count(),
        "events_count": Event.objects.filter(organizer=user).count(),
    }
    
    return render(request, "app.html", context)






##post list
def post_list(request):
    posts = Post.objects.all().order_by("-created_at")
    post_form = PostForm()
    comment_form = CommentForm()
    
    return render(request, "post_list.html", {
        "posts": posts,
        "post_form": post_form,
        "comment_form": comment_form
    })

##create post
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("post_list")
    return redirect("post_list")

def add_comment(request, post_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post_id = post_id
            comment.save()
    return redirect("post_list")



##track user visitors

def profile_view(request, username):
    viewed_user = get_object_or_404(CustomUser, username=username)

    # Track profile visit (but not if user views their own profile)
    if request.user.is_authenticated and request.user != viewed_user:
        ProfileView.objects.update_or_create(viewer=request.user, viewed=viewed_user)

    # Fetch recent profile viewers
    recent_viewers = ProfileView.objects.filter(viewed=viewed_user).select_related("viewer")[:10]

    return render(request, "profile.html", {
        "viewed_user": viewed_user,
        "recent_viewers": recent_viewers
    })


##fetch data from suggestions


# def suggestions_view(request):
#     user = request.user

#     # 1️⃣ Node Suggestions: Random users (excluding current user and existing connections)
#     connected_users = Connection.objects.filter(user=user).values_list("connected_user", flat=True)
#     node_suggestions = CustomUser.objects.exclude(id__in=[user.id] + list(connected_users))[:6]

#     # 2️⃣ Companies to Look At: Fetch random companies
#     companies = Company.objects.all()[:6]

#     # 3️⃣ Nodes in Your Community: Fetch users with common connections
#     community_nodes = CustomUser.objects.filter(connections_received__user=user).exclude(id=user.id)[:6]

#     # 4️⃣ Profile-Based Suggestions: Fetch companies based on user's industry
#     profile_based_companies = Company.objects.filter(industry=user.profile.industry)[:6]

#     return render(request, "suggestions.html", {
#         "node_suggestions": node_suggestions,
#         "companies": companies,
#         "community_nodes": community_nodes,
#         "profile_based_companies": profile_based_companies
#     })


##part 2 suggestions


def home_view(request):
    user = request.user

    # Fetch Node Suggestions
    connected_users = Connection.objects.filter(user=user).values_list("connected_user", flat=True)
    node_suggestions = User.objects.exclude(id__in=[user.id] + list(connected_users))[:6]

    # Fetch Companies
    companies = Company.objects.all()[:6]

    # Fetch Nodes in Community
    community_nodes = User.objects.filter(connections_received__user=user).exclude(id=user.id)[:6]

    # Fetch Profile-Based Companies
    profile_based_companies = Company.objects.filter(industry=user.profile.industry)[:6]

    return render(request, "app.html", {
        "node_suggestions": node_suggestions,
        "companies": companies,
        "community_nodes": community_nodes,
        "profile_based_companies": profile_based_companies
    })





# Views
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

##app.html
def app_view(request):
    context = {"page_title": "App Center"}
    return render(request, 'app.html', context)

##event.html
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'add_event.html', {'form': form})


# User Registration
def register(request):
    context = {"page_title": "App Center"}
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("dashboard")
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
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid credentials, try again.")
    return render(request, "login.html")

# User Logout
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect("login")

# User Dashboard
@login_required
def dashboard(request):
    user_ideas = Idea.objects.filter(created_by=request.user)
    events = Event.objects.all().order_by("-date")[:5]
    return render(request, "dashboard.html", {"user_ideas": user_ideas, "events": events} )

# User Profile
@login_required
def profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    user_ideas = Idea.objects.filter(created_by=user)
    return render(request, "profile.html", {"profile_user": user, "user_ideas": user_ideas})

# Submit an Idea
@login_required
def submit_idea(request):
    if request.method == "POST":
        form = IdeaForm(request.POST)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.created_by = request.user
            idea.save()
            messages.success(request, "Idea submitted successfully!")
            return redirect("dashboard")
    else:
        form = IdeaForm()
    return render(request, "ideas/submit_idea.html", {"form": form})

@login_required
def create_idea(request):
    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.user = request.user
            idea.save()
            return redirect('dashboard')  # Redirect to a dashboard or another page
    else:
        form = IdeaForm()
    return render(request, 'create_post.html', {'form': form})



# Investor Expresses Interest in an Idea
@login_required
def express_interest(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)
    if request.user.user_type == "investor":
        existing_interest = InvestorInterest.objects.filter(investor=request.user, idea=idea).exists()
        if not existing_interest:
            InvestorInterest.objects.create(investor=request.user, idea=idea)
            messages.success(request, "Interest registered successfully!")
        else:
            messages.warning(request, "You have already shown interest in this idea.")
    else:
        messages.error(request, "Only investors can express interest.")
    return redirect("dashboard")

# Event Listing
def event_list(request):
    events = Event.objects.all().order_by("-date")
    return render(request, "events/event_list.html", {"events": events})

# Send Connection Request
@login_required
def send_connection_request(request, user_id):
    receiver = get_object_or_404(CustomUser, id=user_id)
    if request.user != receiver:
        existing_request = Connection.objects.filter(sender=request.user, receiver=receiver).exists()
        if not existing_request:
            Connection.objects.create(sender=request.user, receiver=receiver, status="pending")
            messages.success(request, "Connection request sent!")
        else:
            messages.warning(request, "You have already sent a request to this user.")
    return redirect("dashboard")

# Manage Connection Requests (Accept/Reject)
@login_required
def manage_connection_request(request, request_id, action):
    connection = get_object_or_404(Connection, id=request_id, receiver=request.user)
    if action == "accept":
        connection.status = "accepted"
        messages.success(request, "Connection request accepted!")
    elif action == "reject":
        connection.status = "rejected"
        messages.info(request, "Connection request rejected.")
    connection.save()
    return redirect("dashboard")



##to query on search bar

def search(request):
    query = request.GET.get('q')
    results = []

    if query:
        results.extend(Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)))
        results.extend(Idea.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)))
        results.extend(Topic.objects.filter(name__icontains=query))
        results.extend(Inventor.objects.filter(Q(name__icontains=query) | Q(bio__icontains=query)))
        results.extend(Industry.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)))
        results.extend(Post.objects.filter(Q(content__icontains=query))) 

    return render(request, 'search_results.html', {'query': query, 'results': results})

# @login_required
# def post_list(request):
#     return render(request, "posts/post_list.html")

@login_required
def create_post(request):
    # Your form processing logic...
    return redirect("post_list")




def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Example: Send an email (optional)
            send_mail(
                subject=f"Contact Form Message from {name}",
                message=message,
                from_email=email,
                recipient_list=["odumacorp@gmail.com"],  # Change to your email
            )

            messages.success(request, "Your message has been sent successfully!")
            form = ContactForm()  # Clear the form after submission
        else:
            messages.error(request, "There was an error with your submission.")
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})
