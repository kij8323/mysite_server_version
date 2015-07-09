from django.contrib import admin

# Register your models here.
from .models import Video, Category, TaggedItem
from django.contrib.contenttypes.admin import GenericTabularInline


class TaggedItemInline(GenericTabularInline):
	model = TaggedItem

class VideoInline(admin.TabularInline):
	model = Video

class VideoAdmin(admin.ModelAdmin):
	inlines = [TaggedItemInline]
	list_display = ["__unicode__", 'slug']
	fields = ['title', 'order','share_message', 'embed_code','active','slug',
			'featured', 'free_preview',
			 'category']
	prepopulated_fields = {
		'slug': ["title"], 
	}
	class Meta:
		model = Video



class CategoryAdmin(admin.ModelAdmin):
	inlines = [VideoInline, TaggedItemInline]
	class Meta:
		model = Category

admin.site.register(Video, VideoAdmin)

admin.site.register(Category, CategoryAdmin)

#admin.site.register(TaggedItem)