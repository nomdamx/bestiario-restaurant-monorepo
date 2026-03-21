from fastapi import APIRouter, status

from src.core.api_response import APIResponse, build_response
from src.core.auth_dependency import StaffDependency, UserDependency
from src.core.dependency import PaginationDependency
from src.db.session import DbSession

from . import controller, dependency, schema

router = APIRouter(prefix="/ticket", tags=["ticket"])

RESPONSE_TYPE = "tickets"


@router.get("/", response_model=APIResponse[schema.ResponseTicket])
def route_get_all(
    db: DbSession,
    user: UserDependency,
    pagination: PaginationDependency,
    filters: dependency.FilterTicketDependency,
):
    tickets, pagination_meta = controller.get_all(
        db, pagination=pagination, filters=filters
    )
    return build_response(
        tickets, response_type=RESPONSE_TYPE, pagination=pagination_meta
    )


@router.get(
    "/{uuid}/orders", response_model=APIResponse[schema.ResponseTicketRelations]
)
def route_get_ticket_with_orders(
    db: DbSession,
    user: UserDependency,
    pagination: PaginationDependency,
    uuid: str,
):
    ticket = controller.get_ticket_with_orders(db, uuid=uuid)
    return build_response(ticket, response_type=RESPONSE_TYPE)


@router.post(
    "/",
    response_model=APIResponse[schema.ResponseTicket],
    status_code=status.HTTP_201_CREATED,
)
def route_register(db: DbSession, user: UserDependency, payload: schema.PayloadTicket):
    ticket = controller.register(db, user, payload=payload)
    return build_response(ticket, response_type=RESPONSE_TYPE)


@router.get("/{id_ticket}", response_model=APIResponse[schema.ResponseTicket])
def route_get_by_id(db: DbSession, user: UserDependency, id_ticket: int):
    category = controller.get_by_id(db, id_ticket=id_ticket)
    return build_response(category, response_type=RESPONSE_TYPE)


@router.patch("/{id_ticket}", response_model=APIResponse[schema.ResponseTicket])
def route_patch(
    db: DbSession,
    user: UserDependency,
    payload: schema.PayloadUpdateTicket,
    id_ticket: int,
):
    category = controller.patch(db, payload=payload, id_ticket=id_ticket)
    return build_response(category, response_type=RESPONSE_TYPE)


@router.delete("/{id_ticket}", status_code=status.HTTP_204_NO_CONTENT)
def route_delete(db: DbSession, user: StaffDependency, id_ticket: int):
    controller.delete(db, id_ticket=id_ticket)


@router.post("/{uuid}/print", status_code=status.HTTP_201_CREATED)
def route_print_ticket(
    db: DbSession,
    user: UserDependency,
    filter: dependency.FilterPrintPaymentDepndency,
    uuid: str,
):
    controller.print_ticket(db, filter=filter, uuid=uuid)


@router.patch(
    "/{uuid}/client",
    status_code=status.HTTP_200_OK,
    response_model=APIResponse[schema.ResponseTicket],
)
def route_patch_client(
    db: DbSession,
    user: UserDependency,
    payload: schema.PayloadUpdateClientTicket,
    uuid: str,
):
    ticket = controller.patch_client(db, payload=payload, uuid=uuid)
    return build_response(ticket, response_type=RESPONSE_TYPE)


@router.patch(
    "/{uuid}/comments",
    status_code=status.HTTP_200_OK,
    response_model=APIResponse[schema.ResponseTicket],
)
def route_patch_comments(
    db: DbSession,
    user: UserDependency,
    payload: schema.PayloadUpdateCommentsTicket,
    uuid: str,
):
    ticket = controller.patch_comments(db, payload=payload, uuid=uuid)
    return build_response(ticket, response_type=RESPONSE_TYPE)


@router.patch("/{uuid}/pay", status_code=status.HTTP_200_OK)
def route_paid_status(
    db: DbSession,
    user: UserDependency,
    payload: schema.PayloadUpdatePaidTicket,
    uuid: str,
):
    controller.patch_paid_status(db, payload=payload, uuid=uuid)
