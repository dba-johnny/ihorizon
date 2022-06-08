from django.urls import path
from .views import TicketList, CustomerTicketCreate, AgentTicketUpdate

urlpatterns = [
    path("tickets/", TicketList.as_view(), name="supportdesk_tickets"),
    path("tickets/create/", CustomerTicketCreate.as_view(), name="supportdesk_ticket_create"),
    path("tickets/<int:pk>/", AgentTicketUpdate.as_view(), name="supportdesk_ticket_update"),
]
