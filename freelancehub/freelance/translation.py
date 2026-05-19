from modeltranslation.translator import register, TranslationOptions
from .models import Project, Category, Skill, Offer, Review, UserProfile

@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = ('title', 'description' ,'status')

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)

@register(Skill)
class SkillTranslationOptions(TranslationOptions):
    fields = ('skill_name',)


@register(Review)
class ReviewTranslationOptions(TranslationOptions):
    fields = ('comment',)

@register(UserProfile)
class UserProfileTranslationOptions(TranslationOptions):
    fields = ('bio',)
