from django.db.models.fields.files import ImageFieldFile, ImageField


class CustomImageFieldFile(ImageFieldFile):
    @property
    def url(self):
        try:
            return super().url
        except ValueError:
            return 'fdsfasd'


class CustomImageField(ImageField):
    attr_class = CustomImageFieldFile
