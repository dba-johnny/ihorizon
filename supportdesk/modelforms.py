from django import forms
from .models import Ticket

class CustomerTicketCreateForm(forms.ModelForm):

	class Meta:
		model = Ticket
		fields = ['summary', 'description', 'is_priority']
		widgets = {'description': forms.Textarea(attrs={'cols': 75, 'rows': 15})} 
		labels = {'summary' : 'Summary',
			  'description' : 'Description',
			  'is_priority' : 'Flag as high priority'}

class AgentTicketListForm(forms.ModelForm):

	class Meta:
		model = Ticket
		fields = ['agent', 'is_complete']


class AgentTicketUpdateForm(forms.ModelForm):

	class Meta:
		model = Ticket
		fields = ['is_complete']
