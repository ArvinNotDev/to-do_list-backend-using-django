from django.db import models
from accounts.models import User
from django.utils.translation import gettext_lazy as _

class Task(models.Model):

    class Status(models.IntegerChoices):
        SCHEDULED = 0, _("Scheduled")
        CANCELLED = 1, _("Cancelled")
        COMPLETED = 2, _("Completed")

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    title = models.CharField(max_length=100, verbose_name=_("Title"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    status = models.SmallIntegerField(choices=Status.choices, default=Status.SCHEDULED, verbose_name=_("Status"))
    due_date = models.DateField(blank=True, null=True, verbose_name=_("Due Date"))
    done_at = models.DateTimeField(blank=True, null=True, verbose_name=_("Completion Date"))

    def save(self, *args, **kwargs):
        # Automatically set `done_at` when status is marked as completed
        if self.status == self.Status.COMPLETED and not self.done_at:
            self.done_at = models.functions.Now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['status', 'due_date']
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
