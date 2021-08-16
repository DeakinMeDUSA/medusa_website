from django.core.files.base import ContentFile
from django.db import models
from wand.color import Color
from wand.image import Image


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


class Publication(models.Model):
    """ Represents a MeDUSA Publication file, etc. The Pulse 2021"""
    # Note the name is not unique, useful to get all publications of the same name (e.g. all editions of The Pulse)
    name = models.CharField(max_length=256, help_text="Name of the publication", unique=False)
    pdf = models.FileField(upload_to="publications")
    pub_date = models.DateField(help_text="Publication date, generally the 1st of a month")
    thumbnail = models.ImageField(upload_to="publication_thumbnails", blank=True, null=True)

    def __repr__(self):
        return f"<{self.__class__.__name__}> - {self.name}"

    def __str__(self):
        return self.__repr__()

    def save(self, **kwargs):
        super(Publication, self).save(**kwargs)
        if self.has_thumbnail is False:
            self.gen_pdf_thumbnail(page_num=0)

    @property
    def has_thumbnail(self):
        return self.thumbnail.name is not None and self.thumbnail.name != ""

    def gen_pdf_thumbnail(self, page_num=0):
        """

        Creates images for a page of the input pdf document and saves it
        at img_path.

        :param page_num: page number to create image from in the pdf file.
        :return:
        """
        pdf_img = Image(filename=f"{self.pdf.path}[{page_num}]")

        with pdf_img.convert("png") as converted:
            converted.background_color = Color("white")
            converted.alpha_channel = "remove"
            # scale height and preserve aspect ratio
            converted.transform(resize='x400')
            f = ContentFile(content=converted.make_blob(format="png"))
            self.thumbnail.save(name=f"{self.name}_{self.pub_date}.png", content=f)
