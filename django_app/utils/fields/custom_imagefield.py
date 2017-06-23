from django.db.models.fields.files import ImageFieldFile, ImageField


# ImageFieldFile 클래스를 오버라이드
# img_profile 이미지가 없을 경우 profile.png 파일이 보이게 CustomImageField를 오버라이드
class CustomImageFieldFile(ImageFieldFile):
    @property
    def url(self):
        try:
            return super().url
        except ValueError:
            from django.contrib.staticfiles.storage import staticfiles_storage
            return staticfiles_storage.url(self.field.static_image_path)


# img_profile 이미지가 없을 경우 profile.png 파일이 보이게 CustomImageField를 오버라이드
class CustomImageField(ImageField):
    attr_class = CustomImageFieldFile

    # 초기 설정값의 static_image_path를 오버라이드
    def __init__(self, *args, **kwargs):
        # ImageField는 default_static_image 키워드인자를 받지 않으므로 삭제
        self.static_image_path = kwargs.pop('default_static_image', 'images/no_image.png')
        super().__init__(*args, **kwargs)
