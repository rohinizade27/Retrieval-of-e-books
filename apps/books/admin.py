from django.contrib import admin
from .models import (BooksAuthor,BooksBook, BooksBookAuthors, BooksBookBookshelves,
                     BooksBookLanguages, BooksSubject, BooksBookSubjects, BooksBookshelf,
                     BooksFormat,BooksLanguage)


class BooksAuthorAdmin(admin.ModelAdmin):
    list_display = ('id','birth_year', 'death_year','name')


admin.site.register(BooksAuthor, BooksAuthorAdmin)


class BooksBookAdmin(admin.ModelAdmin):
    list_display = ('id', 'download_count','gutenberg_id','media_type','title')


admin.site.register(BooksBook, BooksBookAdmin)


class BooksBookAuthorsAdmin(admin.ModelAdmin):
    list_display = ('id','book', 'author')


admin.site.register(BooksBookAuthors, BooksBookAuthorsAdmin)


class BooksBookBookshelvesAdmin(admin.ModelAdmin):
    list_display = ('id','book', 'bookshelf')


admin.site.register(BooksBookBookshelves, BooksBookBookshelvesAdmin)


class BooksBookLanguagesAdmin(admin.ModelAdmin):
    list_display = ('id','book', 'language')


admin.site.register(BooksBookLanguages, BooksBookLanguagesAdmin)


class BooksBookSubjectsAdmin(admin.ModelAdmin):
    list_display = ('id','book','subject')


admin.site.register(BooksBookSubjects, BooksBookSubjectsAdmin)


class BooksBookshelfAdmin(admin.ModelAdmin):
    list_display = ('id','name',)


admin.site.register(BooksBookshelf, BooksBookshelfAdmin)


class BooksFormatAdmin(admin.ModelAdmin):
    list_display = ('id','mime_type','url','book')


admin.site.register(BooksFormat, BooksFormatAdmin)


class BooksLanguageAdmin(admin.ModelAdmin):
    list_display = ('id','code')


admin.site.register(BooksLanguage, BooksLanguageAdmin)


class BooksSubjectAdmin(admin.ModelAdmin):
    list_display = ('id','name')


admin.site.register(BooksSubject, BooksSubjectAdmin)
