# -*- encoding: utf-8 -*-
"""
@File Name      :   database_router.py    
@Create Time    :   2021/12/7 21:42
@Description    :   
@Version        :   
@License        :   
@Author         :   diklios
@Contact Email  :   diklios5768@gmail.com
@Github         :   https://github.com/diklios5768
@Blog           :   
@Motto          :   All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
"""
__auth__ = 'diklios'

from django.conf import settings

DATABASE_MAPPING = settings.DATABASE_APPS_MAPPING
CACHE_DATABASE = settings.CACHE_DATABASE


class DatabaseRouter:
    """
    A router to control all database operations on models for different
    databases.

    In case an app is not set in settings.DATABASE_APPS_MAPPING, the router
    will fallback to the `default` database.

    Settings example:

    DATABASE_APPS_MAPPING = {'app1': 'db1', 'app2': 'db2'}
    """
    database_mapping=DATABASE_MAPPING

    def db_for_read(self, model, **hints):
        """
        Point all read operations to the specific database.
        """
        if model._meta.app_label in self.database_mapping:
            return self.database_mapping[model._meta.app_label]
        return None

    def db_for_write(self, model, **hints):
        """
        Point all write operations to the specific database.
        """
        if model._meta.app_label in self.database_mapping:
            return self.database_mapping[model._meta.app_label]
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow any relation between apps that use the same database.
        """
        db_obj1 = self.database_mapping.get(obj1._meta.app_label)
        db_obj2 = self.database_mapping.get(obj2._meta.app_label)
        if db_obj1 and db_obj2:
            if db_obj1 == db_obj2:
                return True
            else:
                return False
        return None

    def allow_syncdb(self, db, model):
        """
        Make sure that apps only appear in the related database.
        """
        if db in self.database_mapping.values():
            return self.database_mapping.get(model._meta.app_label) == db
        elif model._meta.app_label in self.database_mapping:
            return False
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db' database.
        """
        if db in self.database_mapping.values():
            return self.database_mapping.get(app_label) == db
        elif app_label in self.database_mapping:
            return False
        return None


class CacheRouter:
    """A router to control all database cache operations"""
    cache_database=CACHE_DATABASE

    def db_for_read(self, model, **hints):
        """All cache read operations go to the replica"""
        if model._meta.app_label =='django_cache':
            return self.cache_database
        return None

    def db_for_write(self, model, **hints):
        """All cache write operations go to primary"""
        if model._meta.app_label =='django_cache':
            return self.cache_database
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Only install the cache model on primary"""
        # 无论有多少个缓存表，都指向一个数据库
        if app_label =='django_cache':
            return db==self.cache_database
        return None