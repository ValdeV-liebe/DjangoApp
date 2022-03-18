from store.models import Album , Artist
import secrets

# def run() :
#     for i in range(20) :
#         artist = Artist()
#         artist.name = secrets.token_hex(10)
#         artist.save()
#         album = Album()
#         album.title = secrets.token_hex(10)
#         #album.picture = secrets.token_hex(7)
#         album.save()
#         album.artists.add(artist)
#         album.save()