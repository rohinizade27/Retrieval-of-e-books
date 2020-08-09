from django.db import models


class BooksAuthor(models.Model):
    id = models.IntegerField(primary_key=True)
    birth_year = models.SmallIntegerField(blank=True, null=True)
    death_year = models.SmallIntegerField(blank=True, null=True)
    name = models.CharField(max_length=128)

    class Meta:
        db_table = 'books_author'

    def as_dict(self):
        dict = {
            'name':self.name,
            'birth_year':self.birth_year,
            'death_year':self.death_year,
            }
        return  dict


class BooksBook(models.Model):
    id = models.IntegerField(primary_key=True)
    download_count = models.IntegerField(blank=True, null=True)
    gutenberg_id = models.IntegerField()
    media_type = models.CharField(max_length=16)
    title = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'books_book'


class BooksBookAuthors(models.Model):
    id = models.IntegerField(primary_key=True)
    book = models.ForeignKey(BooksBook, on_delete=models.CASCADE)
    author =  models.ForeignKey(BooksAuthor, on_delete=models.CASCADE)

    class Meta:
        db_table = 'books_book_authors'


class BooksBookshelf(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)

    class Meta:
        db_table = 'books_bookshelf'


class BooksBookBookshelves(models.Model):
    id = models.IntegerField(primary_key=True)
    book = models.ForeignKey(BooksBook, on_delete=models.CASCADE)
    bookshelf = models.ForeignKey(BooksBookshelf, on_delete=models.CASCADE)

    class Meta:
        db_table = 'books_book_bookshelves'


class BooksLanguage(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=4)

    class Meta:
        db_table = 'books_language'


class BooksBookLanguages(models.Model):
    id = models.IntegerField(primary_key=True)
    book = models.ForeignKey(BooksBook, on_delete=models.CASCADE)
    language = models.ForeignKey(BooksLanguage, on_delete=models.CASCADE)

    class Meta:
        db_table = 'books_book_languages'


class BooksSubject(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()

    class Meta:
        db_table = 'books_subject'


class BooksBookSubjects(models.Model):
    id = models.IntegerField(primary_key=True)
    book = models.ForeignKey(BooksBook, on_delete=models.CASCADE)
    subject = models.ForeignKey(BooksSubject, on_delete=models.CASCADE)

    class Meta:
        db_table = 'books_book_subjects'


class BooksFormat(models.Model):
    id = models.IntegerField(primary_key=True)
    mime_type = models.CharField(max_length=32)
    url = models.TextField()
    book =  models.ForeignKey(BooksBook, on_delete=models.CASCADE)

    class Meta:
        db_table = 'books_format'








