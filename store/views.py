from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage
from django.shortcuts import render , redirect , reverse , get_object_or_404
from .forms import ContactForm , ArtistForm , ParagraphErrorList
from .models import Album , Artist , Contact , Booking
from django.db import transaction , IntegrityError
from django.views.generic import ListView
from django.http import HttpResponse
from django.contrib import messages
from django.template import loader


"""class AlbumListView(ListView) :
    paginate_by = 2
    model = Album"""

def liste(request) :
    album_list = Album.objects.all()
    paginator = Paginator(album_list , 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'store/album.html' , {'page_obj' : page_obj})
 
def index(request) :
    albums = Album.objects.filter(available = True).order_by('-created_at')[:6]
    formatted_albums = ["<li>{}</li>".format(album.title ) for album in albums]
    #template = loader.get_template('/store/templates/store/index.html')
    context = {'albums' : albums}
    return render(request , 'store/index.html' , context)

def listing(request) :
    albums_list = Album.objects.filter(available = True)
    paginator = Paginator(albums_list , 3)
    page = request.GET.get('page')
    try :
        albums = paginator.get_page(page)
    except PageNotAnInteger :
        albums = paginator.get_page(1)
    except EmptyPage :
        albums = paginator.get_page(paginator.num_pages)
    
    context = {
        'albums' : albums,
        'paginate' : True
        }
    return render(request , 'store/listing.html' , context)


def artist(request) :
    if request.method == 'POST' :
        form = ArtistForm(request.POST)
        if form.is_valid() :
            name = request.POST.get('name')
            artist = Artist.objects.create(name = name)
            return redirect("hello")
        
        msg = messages.add_message(request , message.ERROR , "Le nom doit contenir au moins 5 caracteres")
        context = {
            "messages" : msg ,
            "form" : form
        }
        return render(request , 'store/album.html' , context)
    
    else :
        return render(request , 'store/album.html' , {"form" : ArtistForm()})

@transaction.atomic
def detail(request , album_id) :
    album = get_object_or_404(Album , pk = album_id)
    #artists = " ".join([artist.name for artist in album.artists.all()])
    context = {
            'album_title' : album.title ,
            'artists_name' : album.artists.all ,
            'album_id' : album.id ,
            'image' : album.image ,
        }
    if request.method == 'POST' :
        form = ContactForm(request.POST , error_class = ParagraphErrorList)
        if form.is_valid() :
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
        
            try :
                with transaction.atomic() :
                
                    contact = Contact.objects.filter(email = email)
                    if not contact.exists() :
                        contact = Contact.objects.create(
                            email = email ,
                            name = name
                        )
                    else :
                        contact = contact.first()
                    album = get_object_or_404(Album , id = album_id)
                    booking = Booking.objects.create(
                        contact = contact ,
                        album = album
                    )
                    album.available = False
                    album.save()
                    context = {
                        'album_title' : album.title
                    }
                
                    return render(request , 'store/merci.html', context)
            except IntegrityError :
                form.errors['internal'] = "Une erreur interne est apparue. Merci de recommencer votre requete"
                context['form'] = form
                return render(request , 'store/detail.html' , context)
    else :
        form = ContactForm()    
        context['form'] = form
        context['errors'] = form.errors.items()
        return render(request , 'store/detail.html' , context)

def search(request) :
    query = request.GET.get('query')
    
    if not query :
        albums = Album.objects.all()
    else :
        albums = Album.objects.filter(title__icontains = query)

        if not albums.exists() :
            albums = Album.objects.filter(artists__name__icontains = query)
        
    
    title = "Resultats pour la recherche %s"%query
    context = {
        'albums' : albums ,
        'title' : title
    }
    
    return render(request , 'store/search.html' , context)

