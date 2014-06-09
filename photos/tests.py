import random
import string

from django.conf import settings
from django.test import TestCase
from django.test.client import Client

from photos.models import Photo, PurchaseLog
from website.testing_util import SeleniumTestCase

rand_str = lambda: "".join(random.choice(string.lowercase) for x in range(32))

def create_photo():
    return Photo.objects.create(
        filename=rand_str() + ".jpg",
        title=rand_str(),
        description=rand_str(),
    )

class PurchaseTests(TestCase):
    def test_purchase_logs_photo(self):
        photo = create_photo()
        response = Client().post("/buy", {'photo_id': photo.id})

        log, = PurchaseLog.objects.all()

        self.assertEqual(log.photo, photo)

    def test_purchase_logs_amount(self):
        photo = create_photo()
        response = Client().post("/buy", {'photo_id': photo.id})

        log, = PurchaseLog.objects.all()

        self.assertEqual(log.amount, settings.PHOTO_PRICE)

    def test_purchase_shown_on_log_page(self):
        photo = create_photo()
        Client().post("/buy", {'photo_id': photo.id})
        response = Client().get('/admin/purchase_log')

        self.assertContains(response, photo.filename)

    def test_purchase_price_shown_on_log_page(self):
        photo = create_photo()
        Client().post("/buy", {'photo_id': photo.id})
        response = Client().get('/admin/purchase_log')

        self.assertContains(response, settings.PHOTO_PRICE)

class PageTests(TestCase):
    def test_index_contains_multiple_thumbnails(self):
        photos = [create_photo() for n in range(3)]

        response = Client().get("/")

        for photo in photos:
            self.assertContains(response, "/static/thumbnail/" + photo.filename)

    def test_details_page_contains_watermarked_photo(self):
        photo = create_photo()
        response = Client().get("/details/" + str(photo.id))
        self.assertContains(response, "/static/watermark/" + photo.filename)

    def test_details_page_does_not_contain_original_photo(self):
        photo = create_photo()
        response = Client().get("/details/" + str(photo.id))
        self.assertNotContains(response, "/static/original/" + photo.filename)

class TestPurchaseFlow(SeleniumTestCase):
    def test_purchase_flow(self):
        photo = create_photo()
        self.driver.get(self.live_server_url)
        self.wait_for(self.driver.find_element_by_partial_link_text, photo.title).click()

        # Start purchase from details page
        self.wait_for(self.driver.find_element_by_css_selector, "input[value='Buy Photo']").click()

        # Fill out checkout form and submit
        self.wait_for(self.driver.find_element_by_css_selector, "form[action='/buy'] input[type='submit']").click()

        # Make sure we get the confirmation page
        self.wait_for(self.driver.find_element_by_css_selector, ".thanks")
