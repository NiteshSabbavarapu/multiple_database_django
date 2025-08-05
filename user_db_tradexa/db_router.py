class CoreRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label in ('auth', 'contenttypes', 'admin', 'sessions'):
            return 'default'
        if model._meta.app_label == 'user_db_tradexa':
            if model.__name__ == 'User':
                return 'users'
            elif model.__name__ == 'Product':
                return 'products'
            elif model.__name__ == 'Order':
                return 'orders'
        return None

    def db_for_write(self, model, **hints):
        return self.db_for_read(model, **hints)

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in ('auth', 'contenttypes', 'admin', 'sessions'):
            return db == 'default'
        if app_label == 'user_db_tradexa':
            if model_name == 'user':
                return db == 'users'
            elif model_name == 'product':
                return db == 'products'
            elif model_name == 'order':
                return db == 'orders'
        return None
