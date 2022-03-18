from django.contrib.contenttypes.models import ContentType
from .models import Album , Artist , Booking , Contact
from django.utils.safestring import mark_safe
from django.contrib import admin
from django.urls import reverse

#admin.site.register(Album)
#admin.site.register(Booking)

class AdminURLMixin(object) :
    def get_admin_url(self , obj) :
        content_type = ContentType.objects.get_for_model(obj.__class__)
        return reverse("admin:store_%s_change" % (
            content_type.model) , 
            args = (obj.id,) )

#admin.TabularInline permet d'afficher les infos sur plusieurs lignes
class BookingInline(admin.TabularInline , AdminURLMixin) :
    model = Booking
    readonly_fields = [
        'created_at' ,
        'album' ,
        'contacted',
        'album_link'
        ]
    #fieldsets indique les chapms à afficher 
    fieldsets = (
        (None, {
            "fields": (
                'album_link' ,
                'contacted' 
            ),
        }),
    )
    extra = 0    # spcefie qu'on ne veut pas de ligne supplementaires
    verbose_name = "Réservation"
    verbose_name_plural = "Réservations"
    
    def has_add_permission(self , request , obj=None) :
        return False
    
    def album_link(self , booking) :
        url = self.get_admin_url(booking.album)
        return mark_safe("<a href = '{}'>{}</a>".format(url , booking.album.title))
    

@admin.register(Contact) #decorateur
class ContactAdmin(admin.ModelAdmin) :
    inlines = [BookingInline, ]      #permet d'afficher les infos sur plusieurs ligne avec des colonnes

class AlbumArtistInline(admin.TabularInline) :
    model = Album.artists.through   
    extra = 1   
    verbose_name = "Disque"
    verbose_name_plural = "Disques"

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin) :
    inlines = [AlbumArtistInline, ]

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin) :
    search_fields = ['reference' , 'title']
    """
    La ligne précedente permet d'afficher un formulaire de recherche
    dans la page d'administration. Le mot saisi dans ce formulaire
    sera comparer à ceux présents dans les entrées des attributs 
    reference et title 
    """

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin , AdminURLMixin):
    readonly_fields = [
        'created_at' ,
        'contact' ,
        'album' ,
        'album_link' ,
        'contact_link' 
        ]
    
    fields = ['created_at' , 'album_link' , 'contacted']
    list_filter = ['created_at' , 'contacted']
    """
    La ligne précedente permet d'afficher un filtre de recherche
    baser sur les champs passer en paramètres(ici created_at et contacted)
    dans la page d'administration
    """
    def has_add_permission(self , request) :
        return False
    
    def album_link(self , booking) :
        url = self.get_admin_url(booking.album)
        return mark_safe("<a href = '{}'>{}</a>".format(url , booking.album.title))
    
    def contact_link(self , booking) :
        url = self.get_admin_url(booking.contact)
        return mark_safe("<a href = '{}'>{}</a>".format(url , booking.contact.name))
    