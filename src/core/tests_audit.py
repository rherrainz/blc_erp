from django.test import TestCase, Client as DjangoTestClient
from django.urls import reverse
from django.contrib.auth import get_user_model

from core.models import AuditLog
from clients.models import Client


class AuditLogTests(TestCase):
    def setUp(self):
        self.http = DjangoTestClient()
        User = get_user_model()
        self.user = User.objects.create_user(username='tester', password='pass')

    def test_create_client_generates_auditlog(self):
        # autenticamos para que el middleware capture el user
        self.http.login(username='tester', password='pass')
        resp = self.http.post(reverse('clients:add'), {
            'company_name': 'Audit Co',
            'name': 'Audit Contact'
        })
        # debería haberse creado un cliente
        self.assertEqual(Client.objects.filter(company_name='Audit Co').count(), 1)
        # y al menos una entrada de auditlog
        self.assertTrue(AuditLog.objects.filter(action__in=['create','update']).exists())

    def test_delete_client_generates_auditlog(self):
        client = Client.objects.create(company_name='ToDelete', name='X')
        self.http.login(username='tester', password='pass')
        resp = self.http.post(reverse('clients:delete', args=[client.id]))
        self.assertFalse(Client.objects.filter(id=client.id).exists())
        self.assertTrue(AuditLog.objects.filter(action='delete', object_pk=str(client.id)).exists())
