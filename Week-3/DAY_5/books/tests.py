from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Book, BorrowRecord
from django.utils import timezone


class PermissionsAndBorrowTests(TestCase):
	def setUp(self):
		self.librarian = User.objects.create_user('lib', password='pass')
		self.librarian.is_staff = True
		self.librarian.save()

		self.member = User.objects.create_user('member', password='pass')

		self.cat = Category.objects.create(name='Fiction', description='Fictional books')
		self.book = Book.objects.create(
			title='Sample', author='Author', isbn='1234567890', category=self.cat, published_date='2020-01-01'
		)

		self.client = Client()

	def test_librarian_can_create_book(self):
		self.client.login(username='lib', password='pass')
		url = reverse('book-create')
		resp = self.client.post(url, data={
			'title': 'New Book',
			'author': 'A',
			'isbn': '1234567890',
			'category': self.cat.pk,
			'published_date': '2021-01-01'
		})
		self.assertEqual(resp.status_code, 302)
		self.assertTrue(Book.objects.filter(title='New Book').exists())

	def test_member_cannot_create_book(self):
		self.client.login(username='member', password='pass')
		url = reverse('book-create')
		resp = self.client.get(url)
		# Should redirect to login because user_passes_test redirects unauthorized to login
		self.assertEqual(resp.status_code, 302)

	def test_librarian_can_edit_and_delete(self):
		self.client.login(username='lib', password='pass')
		edit_url = reverse('book-edit', args=[self.book.pk])
		resp = self.client.post(edit_url, data={
			'title': 'Sample Edited', 'author': 'Author', 'isbn': '1234567890', 'category': self.cat.pk, 'published_date': '2020-01-01'
		})
		self.assertEqual(resp.status_code, 302)
		self.book.refresh_from_db()
		self.assertEqual(self.book.title, 'Sample Edited')

		delete_url = reverse('delete_book', args=[self.book.pk])
		resp = self.client.post(delete_url)
		self.assertEqual(resp.status_code, 302)
		self.assertFalse(Book.objects.filter(pk=self.book.pk).exists())

	def test_member_can_borrow_and_return(self):
		self.client.login(username='member', password='pass')
		borrow_url = reverse('borrow_book', args=[self.book.pk])
		resp = self.client.post(borrow_url)
		self.assertEqual(resp.status_code, 302)

		br = BorrowRecord.objects.filter(user=self.member, book=self.book, returned_at__isnull=True).first()
		self.assertIsNotNone(br)
		self.book.refresh_from_db()
		self.assertFalse(self.book.available)

		return_url = reverse('return_book', args=[self.book.pk])
		resp = self.client.post(return_url)
		self.assertEqual(resp.status_code, 302)

		br.refresh_from_db()
		self.assertIsNotNone(br.returned_at)
		self.book.refresh_from_db()
		self.assertTrue(self.book.available)

	def test_unauthenticated_cannot_borrow(self):
		borrow_url = reverse('borrow_book', args=[self.book.pk])
		resp = self.client.post(borrow_url)
		self.assertEqual(resp.status_code, 302)

	def test_logout_clears_session(self):
		# login then logout via POST
		self.client.login(username='member', password='pass')
		resp = self.client.post(reverse('logout'))
		# after logout, client should not have a logged-in user
		response = self.client.get(reverse('book-list'))
		user = response.wsgi_request.user
		self.assertFalse(user.is_authenticated)
