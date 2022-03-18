from django.db import models

class Artist(models.Model) :
    name = models.CharField('Nom', max_length = 200 , unique = True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Artiste'
        verbose_name_plural = 'Artistes'


class Contact(models.Model) :
    email = models.EmailField('Email',max_length = 100)
    name = models.CharField('Nom',max_length=200)

    def __str__(self):
        return self.name
      
    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'  


class Album(models.Model) :
    reference = models.IntegerField('Référence',null = True)
    created_at = models.DateTimeField('Date de création',auto_now_add = True)
    available = models.BooleanField('Disponible',default = True)
    title = models.CharField('Titre',max_length = 200)
    #picture = models.URLField()
    image = models.ImageField('Image',null = True , blank = True)
    artists = models.ManyToManyField(Artist , related_name = 'albums' , blank = True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Album'
        verbose_name_plural = 'Albums'


class Booking(models.Model) :
    created_at = models.DateTimeField("Date d'envoi",auto_now_add = True)
    contacted = models.BooleanField('Demande traitée?',default = False)
    contact = models.ForeignKey(Contact , on_delete = models.CASCADE)
    album = models.OneToOneField(Album , on_delete = models.CASCADE)

    def __str__(self):
        return self.contact.name
    
    class Meta:
        verbose_name = 'Réservation'
        verbose_name_plural = 'Réservations'