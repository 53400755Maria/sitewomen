from django.contrib import admin
from django.contrib import messages
from django.utils.html import mark_safe
from .models import Women, Category, TagPost


# Регистрация модели Women с настройками
@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    # Отображаемые поля в списке
    list_display = ('title', 'post_photo', 'time_create', 'is_published', 'category')
    # Поля-ссылки для перехода к редактированию
    list_display_links = ('title',)
    # Сортировка в списке (новые сверху)
    ordering = ['-time_create', 'title']
    # Поля, которые можно редактировать прямо в списке
    list_editable = ('is_published',)
    # Количество записей на странице
    list_per_page = 5
    # Фильтры справа
    list_filter = ('is_published', 'category')
    # Поля, по которым работает поиск
    search_fields = ('title', 'category__name')
    # Поля, отображаемые на форме редактирования (в нужном порядке)
    fields = ['title', 'slug', 'content', 'photo', 'post_photo', 'category', 'tags', 'is_published']
    # Поля только для чтения
    readonly_fields = ['post_photo']
    # Автоматическое заполнение слага из заголовка
    prepopulated_fields = {"slug": ("title",)}
    # Удобный виджет для выбора тегов (с двумя колонками)
    filter_horizontal = ['tags']
    # Действия в выпадающем списке
    actions = ['set_published', 'set_draft']

    # Отображение миниатюры в списке и на форме
    @admin.display(description="Изображение")
    def post_photo(self, women: Women):
        if women.photo:
            return mark_safe(f"<img src='{women.photo.url}' width=50>")
        return "Без фото"

    # Пользовательское поле (краткое описание) – опционально, можно оставить или удалить
    @admin.display(description="Краткое описание")
    def brief_info(self, women: Women):
        return f"Описание {len(women.content)} символов."

    # Действие: опубликовать выбранные записи
    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записи(ей).")

    # Действие: снять с публикации выбранные записи
    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f"{count} записи(ей) сняты с публикации!", messages.WARNING)


# Регистрация модели Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}


# Регистрация модели TagPost
@admin.register(TagPost)
class TagPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'slug')
    list_display_links = ('id', 'tag')
    prepopulated_fields = {'slug': ('tag',)}