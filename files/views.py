from django.views.generic import ListView
from files.models import File


# Create your views here.
class FilesListView(ListView):
    model = File
    template_name = "files/files.html"
    # context_object_name = "file"

    # def get(self, request, *args, **kwargs):
    #     if "del" in request.GET:
    #         delete_book(request)
    #     return super().get(self, *args, *kwargs)
    #
    # def post(self, request, *args, **kwargs):
    #     return super().get(self, *args, *kwargs)
    #
    # def get_queryset(self):
    #     lib = library_to_view(self.request)
    #     req = ArgsLibrary()
    #     if self.request.method == "POST":
    #         req = get_args_library(self.request)
    #     books_cards_sorted = sort_books(req, library_books=lib.books_cards)
    #     lib.books_cards = books_cards_sorted
    #     info_sort_library(self.request, req)
    #     return lib
    #
    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #
    #     # book image size: width, height
    #     context["width"] = 105
    #     context["height"] = 150
    #
    #     return context
