from flask_caching import Cache

cache = Cache()

def invalidate_trek_cache():

    cache.delete("admin_treks_list_v1")