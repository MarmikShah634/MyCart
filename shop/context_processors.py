from .models import UserRegistration, Category

def session_data(request):
    email = request.session.get('email')
    user_registration = None
    if email:
        user_registration = UserRegistration.objects.filter(email=email).first()
    return {
        'email': email,
        'user_registration': user_registration,
    }

def categories_processor(request):
    root_categories = Category.objects.filter(parent_category__isnull=True)
    level1_category_items = Category.objects.filter(level=1)
    level2_category_items = Category.objects.filter(level=2)

    level1_category = {}
    level2_category = {}

    for category in root_categories:
        level1_category[category] = Category.objects.filter(parent_category=category)
    
    for category in level1_category_items:
        level2_category[category] = Category.objects.filter(parent_category=category)

    return {
        'root_categories': root_categories,
        'level1_category': level1_category,
        'level2_category': level2_category
    }