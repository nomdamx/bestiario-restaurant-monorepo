from flask import Blueprint

from app.controllers import CategoryController

from app.routes.base_route import BaseRoute


category_bp = Blueprint("category",__name__)
category_controller = CategoryController()

class CategoryRoute(BaseRoute):
    def __init__(self):
        super().__init__(category_bp, category_controller)