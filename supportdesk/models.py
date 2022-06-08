from django.db import models
from django.conf import settings

from datetime import datetime, timezone


# Create your models here.

class Ticket(models.Model):
	customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="customer_set", related_query_name="customer")
	agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="agent_set", related_query_name="agent")
	created = models.DateTimeField(auto_now_add=True, null=True)
	resolved = models.DateTimeField(null=True)
	is_complete = models.BooleanField(default=False)
	is_priority = models.BooleanField(default=False)
	summary = models.CharField(max_length=255)
	description = models.TextField()

	def get_id(self):
		return "T_%s" % str(self.id)

	def verbal_offset(self):
		now = datetime.now(timezone.utc)
		td = now - self.created
		days = td.days
		hours, remainder = divmod(td.seconds, 3600)
		minutes, seconds = divmod(remainder, 60)

		verbal_offset = "moments"
		if days: verbal_offset = "%s days" % str(days) if days>1 else "%s day" % str(days)
		elif hours: verbal_offset = "%s hours" % str(hours) if hours>1 else "%s hour" % str(hours)
		elif minutes: verbal_offset = "%s minutes" % str(minutes) if minutes>1 else "%s minutes" % str(minutes)

		return verbal_offset

	def __str__(self):
		return self.get_id()
