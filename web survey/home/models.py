from django.db import models

# Create your models here.
class Csv(models.Model):
    name = models.CharField(max_length=224)
    file = models.FileField(upload_to='media/csv', max_length=100)
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "{}.{}".format(self.id, self.name)

class CsvValue(models.Model):
    csv = models.ForeignKey('home.Csv',blank=True, null=True,on_delete=models.CASCADE)
    value = models.TextField()
    freq = models.IntegerField(default=1)
    def __str__(self):
        return "{}.{}".format(self.id, self.value)

class Survey(models.Model):
    name = models.CharField(max_length=225)
    date = models.DateField(auto_now_add=True)
    isOpen = models.BooleanField(default=True)
    def __str__(self):
        return "{}.{}".format(self.id, self.name)

class Question(models.Model):
    name = models.CharField(max_length=225)
    isText = models.BooleanField()
    def __str__(self):
        return "{}.{}".format(self.id, self.name)
    
class QuestionValue(models.Model):
    question = models.ForeignKey('home.Question',blank=True, null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=225)
    value = models.IntegerField(blank=True)

    def __str__(self):
        return "{}.{}".format(self.id, self.name)

class SurveyQuestion(models.Model):
    survey = models.ForeignKey('home.Survey',blank=True, null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=225)
    isText = models.BooleanField(default=False)
    value = models.ForeignKey('home.Question',blank=True, null=True,on_delete=models.CASCADE)
    def __str__(self):
        return "{}.{}".format(self.id, self.name)

class Responden(models.Model):
    user = models.ForeignKey('home.User',blank=True, null=True,on_delete=models.CASCADE)
    Survey = models.ForeignKey('home.Survey',blank=True, null=True,on_delete=models.CASCADE)
    def __str__(self):
        return "{}.{}={}".format(self.id, self.user, self.Survey)

class ResponSurvey(models.Model):
    respond =  models.ForeignKey('home.Responden',blank=True, null=True,on_delete=models.CASCADE)
    value = models.ForeignKey('home.SurveyQuestion',blank=True, null=True,on_delete=models.CASCADE)
    answer = models.ForeignKey('home.QuestionValue',blank=True, null=True,on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return "{}.{}={}".format(self.id, self.respond, self.answer)

class User(models.Model):
    name = models.CharField(max_length=225)
    age = models.IntegerField()
    sex = models.IntegerField(choices=((1,"Laki - Laki"),(2, "Perempuan")))
    email = models.EmailField()
    master = models.BooleanField(default=False)
    def __str__(self):
        return "{}.{}".format(self.id, self.name)

class Layanan(models.Model):
    csv = models.ForeignKey('home.Csv',blank=True, null=True,on_delete=models.CASCADE)
    layanan = models.CharField(max_length=225)
    setuju = models.IntegerField(default=0)
    sangat_setuju = models.IntegerField(default=0)
    tidak_setuju = models.IntegerField(default=0)
    sangat_tidak_setuju = models.IntegerField(default=0)
    def __str__(self):
        return "{}".format(self.layanan)

