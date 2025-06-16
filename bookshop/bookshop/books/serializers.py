from rest_framework import serializers
from .models import Author, Book, BookInstance, Publisher, Genre, Category


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = "__all__"


class BookInstanceSerializer(serializers.ModelSerializer):
    publisher = serializers.CharField(source="publisher.name")

    class Meta:
        model = BookInstance
        fields = ("publisher", "count")


class BookSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), many=True
    )
    book_instances = BookInstanceSerializer(many=True, read_only=True)
    total_amount = serializers.SerializerMethodField()

    def get_total_amount(self, instance):
        result = 0
        for book_instances in instance.book_instances.all():
            result += book_instances.count
        return result

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "genres",
            "category",
            "book_instances",
            "total_amount",
        )


class PriceSerializer(serializers.ModelSerializer):
    book = BookSerializer(many=False)

    class Meta:
        model = BookInstance
        fields = (
            "book",
            "price",
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
