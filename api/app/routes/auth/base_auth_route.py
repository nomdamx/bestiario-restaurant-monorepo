from flask import Blueprint,request, Response
from app.controllers.auth.base_auth_controller import BaseAuthController
from app.decorators import requires_auth

class BaseAuthRoute:
    def __init__(self,blueprint:Blueprint,controller:BaseAuthController):
        self._blueprint = blueprint
        self._controller = controller
        
        self._create_routes()
        
    def _create_routes(self):
        
        @self._blueprint.route("/",methods=["POST"],strict_slashes=False)
        def route_register_user():
            json_request = request.get_json()
            return self._controller.register_user(
                data=json_request,
                request=request
            )

        @self._blueprint.route("/",methods=["GET"],strict_slashes=False)
        def route_get_users():
            return self._controller.get_all(
                request=request
            )
        
        @self._blueprint.route("/<int:id>",methods=["GET"],strict_slashes=False)
        @requires_auth(["admin"])
        def route_get_by_id_user(id):
            return self._controller.get_by_id(
                id=id,
                request=request
            )
        
        @self._blueprint.route("/user-validation",methods=["POST"],strict_slashes=False)
        def route_user_validation_user():
            json_request = request.get_json()
            return self._controller.validate_user(
                data=json_request,
                request=request
            )
        
        @self._blueprint.route("/need_password", methods=["GET"],strict_slashes=False)
        def route_check_user_need_password():
            value = self._controller.controller_check_username_need_password()
            return {
                "value":str(value)
            }
        
        @self._blueprint.route("/admin_see_config", methods=["GET"],strict_slashes=False)
        def route_check_admin_see_config():
            value = self._controller.controller_check_admin_see_config()
            return {
                "value":str(value)
            }
        
        @self._blueprint.route("/need_password", methods=["POST"],strict_slashes=False)
        @requires_auth(["admin","manager"])
        def route_change_user_need_password():
            self._controller.controller_change_username_need_password(request.get_json())
            return Response(status=201)
        
        @self._blueprint.route("/change_password", methods=["POST"],strict_slashes=False)
        # @requires_auth(["admin","manager"])
        def route_change_password():
            self._controller.controller_change_user_password(request.get_json())
            return Response(status=200)

        @self._blueprint.route("/<int:id>",methods=["DELETE"],strict_slashes=False)
        def route_delete_by_id(id):
            return self._controller.delete_user_by_id(id)

        @self._blueprint.route("/session-token",methods=["GET"],strict_slashes=False)
        def route_session_token():
            return self._controller.generateSessionToken()

        @self._blueprint.route("/create-session/<int:id>",methods=["POST"],strict_slashes=False)
        def route_test_user(id):
            json_request = request.get_json()
            return self._controller.createSessionToken(json_request,id)

        @self._blueprint.route("/session-validation",methods=["POST"],strict_slashes=False)
        def route_test_validation_user():
            json_request = request.get_json()
            return self._controller.validateSessionToken(json_request["token"])

        @self._blueprint.route("/session-invalidation",methods=["POST"],strict_slashes=False)
        def route_test_invalidation_user():
            json_request = request.get_json()
            return self._controller.invalidateSession(json_request["session"])
        
    def get_blueprint(self):
        return self._blueprint