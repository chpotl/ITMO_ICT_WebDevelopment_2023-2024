from rest_framework.permissions import BasePermission
# Импортировать базовый класс для определения пользовательских разрешений

class ProfilePermissions(BasePermission):
    # Создание пользовательского класса разрешений, основанного на BasePermission

    def has_object_permission(self, request, view, obj):
        # Определение метода проверки разрешений для объекта
        print(obj)  # Вывести объект для отладки
        
        # Проверить, равен ли пользователь, отправивший запрос, объекту
        if request.user == obj:
            return True  # Вернуть True, если пользователь имеет доступ к объекту
        return False  # В противном случае вернуть False

class RegistrationsPermissions(BasePermission):
    # Создание другого пользовательского класса разрешений, также основанного на BasePermission

    def has_object_permission(self, request, view, obj):
        # Определение метода проверки разрешений для объекта
        
        # Проверить, является ли пользователь, отправивший запрос, владельцем объекта регистрации
        if request.user == obj.user:
            return True  # Вернуть True, если пользователь имеет доступ к объекту регистрации
        return False  # В противном случае вернуть False