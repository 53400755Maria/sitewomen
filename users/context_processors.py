from women.views import menu

def get_women_context(request):
    return {'mainmenu': menu}