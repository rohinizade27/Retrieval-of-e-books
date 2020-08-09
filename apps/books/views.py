from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import (BooksAuthor,BooksBook, BooksBookAuthors, BooksBookBookshelves,
                     BooksBookLanguages, BooksSubject, BooksBookSubjects, BooksBookshelf,
                     BooksFormat,BooksLanguage)
import operator
import json


class BookDetails(View):
    def get_objs(self, book_obj):
        author_objs = BooksBookAuthors.objects.select_related('book', 'author').filter(book=book_obj)
        subject_objs = BooksBookSubjects.objects.select_related('book', 'subject').filter(book=book_obj)
        language_objs = BooksBookLanguages.objects.select_related('book', 'language').filter(book=book_obj)
        bookshelf_objs = BooksBookBookshelves.objects.select_related('book', 'bookshelf').filter(book=book_obj)
        bookformat_objs = BooksFormat.objects.select_related('book').filter(book=book_obj)
        return author_objs, subject_objs, language_objs, bookshelf_objs, bookformat_objs

    def create_book_info_dict(self, book):
        url_list,lang_list,sub_list,shelf_list =[], [], [], []
        author_info, subject_info, language_info, bookshelf_info, bookformat_info = self.get_objs(book)
        for ele in bookformat_info:
            url_list.append(ele.url)

        # for lang in language_info:
        #     lang_list.append(lang.language.code)

        for sub in subject_info:
            sub_list.append(sub.subject.name)

        for shelf in shelf_list:
            shelf_list.append(shelf.bookshelf.name)

        # A list of book objects contains title of book information about author,
        # Language,subjects,bookshelfs,
        # A list of links to download the book in the available formats (mime-types)
        book_info_dict = {
            'book_title': book.title,
            'book_download_count':book.download_count,
            'book_author_info': author_info[0].author.as_dict() if author_info else "",
            'book_subject': sub_list,
            'book_language': language_info[0].language.code if language_info else "",
            'book_shelf': shelf_list,
            'book_download_urls': url_list
        }
        return book_info_dict

    def get(self, request):
        res_data = {}
        book_info_list = []

        # get request query parameters
        book_id = request.GET.get('book_id','')
        book_title = request.GET.get('title','')
        book_author = request.GET.get('author', '')
        book_mime_type = request.GET.get('mime_type', '')
        book_topic = request.GET.get('topic', '')
        book_language = request.GET.get('language', '')

        # filter books based on Book ID numbers specified as Project Gutenberg ID numbers
        if book_id:
            books = BooksBook.objects.filter(gutenberg_id=book_id)
            if books:
                for book in books:
                    book_info_dict = self.create_book_info_dict(book)
                    book_info_list.append(book_info_dict.copy())

        # filter books based on Title.
        if book_title:
            # Case insensitive partial matches
            books = BooksBook.objects.filter(title__icontains=book_title)
            if books:
                for book in books:
                    book_info_dict = self.create_book_info_dict(book)
                    book_info_list.append(book_info_dict.copy())

        # filter books based on Author.
        if book_author:
            try:
                # Case insensitive partial matches
                author = BooksAuthor.objects.get(name__icontains=book_author)
                author_objs = BooksBookAuthors.objects.\
                    select_related('book','author').filter(author=author)
                for auth in author_objs:
                    book_info_dict = self.create_book_info_dict(auth.book)
                    book_info_list.append(book_info_dict.copy())
            except ObjectDoesNotExist:
                pass

        # filter books based on language.
        if book_language:
            # multiple filter
            # if book_language = en,fr then for en and fr criteria check.
            # by splitting string we get two language code
            lang_list = book_language.split(',')
            for l in lang_list:
                try:
                    language = BooksLanguage.objects.get(code=l)
                    language_objs = BooksBookLanguages.objects.\
                        select_related('book','language').filter(language=language)
                    for lang in language_objs:
                        book_info_dict = self.create_book_info_dict(lang.book)
                        book_info_list.append(book_info_dict.copy())
                except ObjectDoesNotExist:
                    pass

        # book filter on the basis of Mime-type.
        if book_mime_type:
            try:
                bookformat_objs = BooksFormat.objects.select_related('book').\
                    filter(mime_type=book_mime_type)
                for bf in bookformat_objs:
                    book_info_dict = self.create_book_info_dict(bf.book)
                    book_info_list.append(book_info_dict.copy())
            except ObjectDoesNotExist:
                pass

        # book filter on the basis of topic.
        if book_topic:
            try:
                # Topic should filter on either subject
                # Case insensitive partial matches
                bookshelf = BooksBookshelf.objects.get(name__icontains=book_topic)
                bookshelf_objs = BooksBookBookshelves.objects.\
                    select_related('book','bookshelf').filter(bookshelf=bookshelf)
                for bshelf in bookshelf_objs:
                    book_info_dict = self.create_book_info_dict(bshelf.book)
                    book_info_list.append(book_info_dict.copy())
            except ObjectDoesNotExist:
                try:
                    # or Topic should filter on bookshelf
                    # Case insensitive partial matches
                    booksubject = BooksSubject.objects.get(name__icontains=book_topic)
                    booksubject_objs = BooksBookSubjects.objects. \
                        select_related('book', 'subject').filter(subject=booksubject)
                    for bsub in booksubject_objs:
                        book_info_dict = self.create_book_info_dict(bsub.book)
                        book_info_list.append(book_info_dict.copy())
                except ObjectDoesNotExist:
                    pass

        res_data['total_books'] = len(book_info_list) # number of books meeting the criteria

        # display book list based on the number of downloads. decreasing order of popularity
        book_info_list.sort(key=operator.itemgetter('book_download_count'), reverse=True)

        # pagination in case the number of books that meet the criteria exceeds 25,
        # return only 25 books at a time
        page = request.GET.get('page', 1) # 1st page
        paginator = Paginator(book_info_list, 25) # 1st page contains only 25 records
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
        except EmptyPage:
            books = paginator.page(paginator.num_pages)
        res_data['book_list'] = books.__dict__.get("object_list")
        # with help of paginator object we can access next page
        res_data['paginator']= books.__dict__.get("paginator")
        res_data['page'] = books

        json_data = json.dumps(res_data, indent=4, default=str)
        # returning data in json format
        return HttpResponse(json_data, content_type='application/json', status=200)






