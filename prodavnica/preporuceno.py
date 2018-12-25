import redis
from .models import Proizvod
from django.conf import settings

# konekcija redis
r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


class Preporucivac(object):
    def dobij_proizvod_key(self, id):
        return 'prozivod:{}:kupljen_sa'.format(id)

    def kupljeni_proizvodi(self, proizvodi):
        proizvod_ids = [p.id for p in proizvodi]
        for proizvod_id in proizvod_ids:
            for sa_id in proizvod_ids:
                if proizvod_id != sa_id:
                    r.zincrby(self.dobij_proizvod_key(proizvod_id), 1, sa_id)

    def preporuci_proizvode_za(self, prozivodi, broj_proizvoda=5):
        prozivod_ids = [p.id for p in prozivodi]
        if len(prozivod_ids) == 1:
            preporuceno = r.zrange(self.dobij_proizvod_key(
                prozivod_ids[0]), 0, -1, desc=True)[:broj_proizvoda]
        else:
            flat_ids = ''.join([str(id) for id in prozivod_ids])
            tmp_key = 'tmp_{}'.format(flat_ids)
            keys = [self.dobij_proizvod_key(id) for id in prozivod_ids]
            r.zunionstore(tmp_key, keys)
            r.zrem(tmp_key, *prozivod_ids)
            preporuceno = r.zrange(tmp_key, 0, -1, desc=True)[:broj_proizvoda]
            r.delete(tmp_key)
        preporuceni_proizvodi_ids = [int(id) for id in preporuceno]
        preporuceni_proizvodi = list(
            Proizvod.objects.filter(id__in=preporuceni_proizvodi_ids))
        preporuceni_proizvodi.sort(key=lambda x: preporuceni_proizvodi_ids.index(x.id))
        return preporuceni_proizvodi

    def ocisti_kupljene(self):
        for id in Proizvod.objects.value_list('id', flat=True):
            r.delete(self.dobij_proizvod_key(id))
