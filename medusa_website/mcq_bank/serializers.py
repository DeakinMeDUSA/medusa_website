from rest_framework import serializers

from medusa_website.mcq_bank.models import Answer, Question


class AnswerSerializer(serializers.ModelSerializer):
    question_id = serializers.CharField()  # no corresponding model property.

    class Meta:
        model = Answer
        fields = ["id", "answer_text", "explanation_text", "is_correct", "question_id"]

    # def validate(self, data):
    #     for req_field in ["answer_text", "is_correct", "question_id"]:
    #         if req_field not in data:
    #             raise serializers.ValidationError(f"Must include {req_field}")
    #     return data

    #
    def create(self, validated_data):
        print(f"validated_data = {validated_data}")
        return Answer.objects.create(
            question=Question.objects.get(id=validated_data["question_id"]),
            explanation_text=validated_data.get("explanation_text", None),
            is_correct=validated_data.get("is_correct"),
            answer_text=validated_data.get("answer_text"),
        )


# #         if 'text' not in validated_data:
# #             assert validated_data.get('not_present', False) and 'rectangles' not in validated_data
# #
# #         annotation = Annotation.objects.create(
# #             page=validated_data['page'],
# #             data_point=validated_data['data_point'],
# #             text=validated_data.get('text', None),
# #             not_present=validated_data.get('not_present', False),
# #             verified=validated_data['verified'],
# #             verified_by=validated_data['verified_by'],
# #             area_image=validated_data.get('area_image', None)
# #         )


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "question_text", "category", "author", "image"]


#
# from affinda.main.models import Document, Page, Annotation, Rectangle, DataPoint, ParseRequest, GeoRequest, \
#     BoundingRectangle
#
#
# class PageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Page
#         fields = ["id", "page_index"]
#
# class InternalDocumentSerializer(serializers.ModelSerializer):
#     pages = PageSerializer(many=True, read_only=True)
#
#     def save(self, **kwargs):
#         document = super().save(**kwargs)
#         # tagger.predict_document(document, restrict_to_indices=(0,))
#         return document
#
#     class Meta:
#         model = Document
#         fields = ["pdf", "id", "url", "pages"]
#
#         extra_kwargs = {
#             "url": {"view_name": "api:document-detail", "lookup_field": "id"}
#         }
#
#
# class DataPointSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DataPoint
#         fields = ["id", "slug"]
#
#
# class RectangleSerializer(serializers.ModelSerializer):
#     height = serializers.FloatField(write_only=True)
#     width = serializers.FloatField(write_only=True)
#
#     class Meta:
#         model = Rectangle
#         fields = ["id", "x0", "y0", "x1", "y1", "height", "width"]
#
#
# class BoundingRectangleSerializer(RectangleSerializer):
#     class Meta:
#         model = BoundingRectangle
#         fields = ["id", "x0", "y0", "x1", "y1", "height", "width"]
#
#
# class VerifyAnnotationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Annotation
#         fields = ["id", "verified", "verified_by"]
#
#
# class ConfirmAnnotationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Annotation
#         fields = ["id", "verified_twice", "second_verification_by"]
#
#
# class AnnotationSerializer(serializers.ModelSerializer):
#     rectangles = RectangleSerializer(many=True, required=False)
#     bounding_rectangle = BoundingRectangleSerializer(many=False, read_only=True)
#     data_point_slug = serializers.ReadOnlyField(source='data_point.slug')
#     page_number = serializers.ReadOnlyField(source='page.page_index')
#     page_height = serializers.ReadOnlyField(source='page.height')
#     page_width = serializers.ReadOnlyField(source='page.width')
#
#     class Meta:
#         model = Annotation
#         partial = True
#         fields = ["id", "data_point", "rectangles", "data_point_slug", "page_number", "bounding_rectangle",
#                   "page_height", "page_width", "page", "text", "verified", "verified_by", "not_present",
#                   'requires_second_verification', 'verified_twice', 'area_image']
#
#     def create(self, validated_data):
#         if 'text' not in validated_data:
#             assert validated_data.get('not_present', False) and 'rectangles' not in validated_data
#
#         annotation = Annotation.objects.create(
#             page=validated_data['page'],
#             data_point=validated_data['data_point'],
#             text=validated_data.get('text', None),
#             not_present=validated_data.get('not_present', False),
#             verified=validated_data['verified'],
#             verified_by=validated_data['verified_by'],
#             area_image=validated_data.get('area_image', None)
#         )
#         for rect in validated_data.get('rectangles', []):
#             Rectangle.objects.create(
#                 annotation=annotation,
#                 x0=rect['x0'] * annotation.page.width / rect['width'],
#                 y0=rect['y0'] * annotation.page.height / rect['height'],
#                 x1=rect['x1'] * annotation.page.width / rect['width'],
#                 y1=rect['y1'] * annotation.page.height / rect['height'],
#             )
#         if not annotation.not_present:
#             annotation.populate_bounding_rectangle()
#             annotation.populate_image()
#             annotation.save()
#         return annotation
#
#
# class DocumentSerializer(serializers.ModelSerializer):
#     output = serializers.JSONField(read_only=True)
#
#     class Meta:
#         model = Document
#         fields = ["pdf", "output"]
#
#
# class ParseRequestSerializer(serializers.ModelSerializer):
#     documents = DocumentSerializer(many=True, required=False, read_only=True)
#     proportion_complete = serializers.ReadOnlyField()
#     processing = serializers.ReadOnlyField()
#     identifier = serializers.ReadOnlyField()
#
#     class Meta:
#         model = ParseRequest
#         fields = ["identifier", "documents", "ready", "email", "proportion_complete", "processing"]
#
#
# class GeoRequestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = GeoRequest
#         fields = ["id", "raw_input", "geocode"]
