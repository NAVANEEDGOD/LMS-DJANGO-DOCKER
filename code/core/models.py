from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.TextField("bio",default='-')
#     birth_date = models.DateField("tanggal lahir",null=True,blank=True)
#     profile_picture = models.ImageField("gambar profil", null=True,blank=True)

#     class Meta:
#         verbose_name = "Profil"
#         verbose_name_plural = "Profil"
#     def __str__(self)->str:
#         return self.user.username


class Course(models.Model):
    name = models.CharField("nama matkul", max_length=100)
    description = models.TextField("deskripsi", default='-')
    price = models.IntegerField("harga", default=10000)
    image = models.ImageField("gambar", null=True, blank=True)
    teacher = models.ForeignKey(User, verbose_name="pengajar", on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Mata Kuliah"
        verbose_name_plural = "Mata Kuliah"

    def __str__(self) -> str:
        return f"{self.name} : {self.price}"