from django.db import models


class Sponsor(models.Model):
    name = models.CharField(max_length=128, help_text="Name of the sponsor", unique=True)
    website = models.CharField(max_length=256, help_text="URL of the sponsor's website")

    image = models.ImageField(upload_to="frontend/sponsors",
                              help_text="Supporter image for display on frontend")

    def __repr__(self):
        return f"<{self.__class__.__name__}> - {self.name}"

    def __str__(self):
        return self.__repr__()


class Supporter(models.Model):
    """ The same as a sponsor, but not paying - will be displayed below sponsors. Includes DUSA and Deakin"""
    name = models.CharField(max_length=128, help_text="Name of the supporter", unique=True)
    website = models.CharField(max_length=256, help_text="URL of the supporter's website")

    image = models.ImageField(upload_to="frontend/sponsors", null=True,
                              help_text="Supporter image for display on frontend")

    def __repr__(self):
        return f"<{self.__class__.__name__}> - {self.name}"

    def __str__(self):
        return self.__repr__()


class OfficialDocumentation(models.Model):
    """ For use on the About page"""
    class Meta:
        verbose_name = "Official Documentation"
        verbose_name_plural = "Official Documentation"

    name = models.CharField(max_length=256, help_text="Name of the document", unique=True)
    file = models.FileField(upload_to="official_documentation")
    publish_year = models.IntegerField()

    def __repr__(self):
        return f"<{self.__class__.__name__}> - {self.name}"

    def __str__(self):
        return self.__repr__()
