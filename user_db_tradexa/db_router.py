class CoreRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label in ('auth', 'contenttypes', 'admin', 'sessions'):
            return 'default'
        if model._meta.app_label == 'user_db_tradexa':
            return 'users'
        # add more custom logic
        return None

    def db_for_write(self, model, **hints):
        return self.db_for_read(model, **hints)

    def allow_relation(self, obj1, obj2, **hints):
        return True  # or customize logic here

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in ('auth', 'contenttypes', 'admin', 'sessions'):
            return db == 'default'
        if app_label == 'user_db_tradexa':
            return db == 'users'
        return None
