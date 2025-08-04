class CoreRouter:
    def db_for_read(self, model, **hints):
        if model.__name__ == 'User':
            return 'users'
        elif model.__name__ == 'Product':
            return 'products'
        elif model.__name__ == 'Order':
            return 'orders'
        return None

    def db_for_write(self, model, **hints):
        return self.db_for_read(model)

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name == 'user' and db == 'users':
            return True
        elif model_name == 'product' and db == 'products':
            return True
        elif model_name == 'order' and db == 'orders':
            return True
        return False
