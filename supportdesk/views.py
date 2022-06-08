from random import choice

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.views.generic import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Ticket
from .modelforms import CustomerTicketCreateForm, AgentTicketListForm, AgentTicketUpdateForm

GROUP_CUSTOMER = 'Customer'
GROUP_AGENT = 'Agent'

class TicketList(LoginRequiredMixin, ListView):
	model = Ticket
	login_url = reverse_lazy('login')

	def get_queryset(self):
		user = self.request.user
		if user.groups.filter(name=GROUP_CUSTOMER).count():
			queryset = Ticket.objects.select_related('agent').filter(customer=user)
			self.template_name = 'supportdesk/customer_ticket_list.html'
		elif user.groups.filter(name=GROUP_AGENT).count(): 
			queryset = Ticket.objects.filter(agent=user, is_complete=False)
			self.template_name = 'supportdesk/agent_ticket_list.html'
		else:
			queryset = None
	
		self.n_tickets = queryset.count() if queryset else 0
		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update({'n_tickets': self.n_tickets})
		return context
	

class CustomerTicketCreate(LoginRequiredMixin, CreateView):
	model = Ticket
	form_class = CustomerTicketCreateForm
	template_name = 'supportdesk/customer_ticket_create.html'
	success_url = reverse_lazy('supportdesk_tickets')
	login_url = reverse_lazy('login')

	def get_random_agent(self):
		all_agents = User.objects.filter(groups__name='Agent').prefetch_related('groups')
		return choice(all_agents)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update({'n_tickets': Ticket.objects.filter(customer=self.request.user).count()})
		return context

	def form_valid(self, mform):
		mform.instance.customer = self.request.user
		mform.instance.agent = self.get_random_agent()
		return super().form_valid(mform)

	def dispatch(self, request, *args, **kwargs):
		if request.user.groups.filter(name=GROUP_CUSTOMER).count() != 1:
			return HttpResponseRedirect(self.login_url)
		return super().dispatch(request, *args, **kwargs)


class AgentTicketUpdate(LoginRequiredMixin, UpdateView):
	model = Ticket
	form_class = AgentTicketUpdateForm
	template_name = 'supportdesk/agent_ticket_update.html'
	success_url = reverse_lazy('supportdesk_tickets')
	login_url = reverse_lazy('login')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update({'n_tickets': Ticket.objects.filter(agent=self.request.user, is_complete=False).count()})
		return context

	def dispatch(self, request, *args, **kwargs):
		if request.user.groups.filter(name=GROUP_AGENT).count() != 1:
			return HttpResponseRedirect(self.login_url)
		return super().dispatch(request, *args, **kwargs)
