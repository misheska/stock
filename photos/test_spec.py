"""
The tests in this file are disabled by default, via the exercise decorator (and manage command).
"""

from decimal import Decimal

from django.test import TestCase
from django.test.client import Client

from photos.tests import create_photo
from website.exercise import exercise 
from website.testing_util import SeleniumTestCase


class TestSpec(TestCase):
    @exercise(1, "First Push: Change the store's name.")
    def test_does_not_have_default_name(self):
        response = Client().get("/")
        self.assertNotContains(response, "MyCompany")

    @exercise(2, "Schema Change: Create the CouponCode model.")
    def test_CouponCode_has_correct_fields(self):
        from photos.models import CouponCode

        # Create a coupon
        CouponCode.objects.create(code="foobar", discount_percentage=99)

        # Fetch that coupon from the database
        code = CouponCode.objects.get(code="foobar")
        # Assert that it's what we just created
        self.assertEqual(code.discount_percentage, 99)

    @exercise(3, "Admin Page: Allow coupon code creation.")
    def test_can_create_coupon_code_via_admin_page(self):
        from photos.models import CouponCode

        client = Client()
        create_coupon = client.get('/admin/create_coupon')

        # Create a coupon by posting to the admin page
        client.post('/admin/create_coupon', { 'code': 'SAVE25', 'discount_percentage': '25'})

        # Assert that we got what was intended
        code = CouponCode.objects.get(code='SAVE25')
        self.assertEqual(code.discount_percentage, 25)

    @exercise(4, "Feature Flipper: Start building the Checkout GUI", stop=7)
    def test_coupon_code_ui_is_behind_a_feature_flipper(self):
        from photos.views import coupon_code_feature

        # We'll need a test photo for the tests from now on
        photo = create_photo()
        client = Client()

        # Assert that if the flipper is not enabled for us, we don't see the coupon code UI
        response = client.post("/checkout", { 'photo_id': photo.id })
        self.assertNotContains(response, "Have a coupon code?")

        # Assert that if the flipper is enabled, we do see the coupon code UI
        client.post("/feature/set_enabled", {'name': coupon_code_feature.name, 'enabled': 'True'})
        response = client.post("/checkout", { 'photo_id': photo.id })
        self.assertContains(response, "Have a coupon code?")

    @exercise(5, "Implementation: Update the checkout price.")
    def test_applying_coupon_code_updates_price(self):
        photo = create_photo()
        client = Client()

        # Create a coupon code
        client.post('/admin/create_coupon', {'code': 'TWENTYOFF', 'discount_percentage': '20'})

        # Apply it to the checkout page
        response = client.post("/checkout", { 'photo_id': photo.id, 'code': 'TWENTYOFF'})
        # Assert that the new price accurately reflects the coupon code
        self.assertContains(response, "Cost: $11.96")

    @exercise(6, "Implentation: Actually charge the reduced price.")
    def test_applied_coupon_code_charges_discounted_price(self):
        photo = create_photo()
        client = Client()

        # Create a coupon code
        client.post('/admin/create_coupon', {'code': 'FORTYOFF', 'discount_percentage': '40'})

        # Actually purchase a picture with the coupon code
        response = client.post("/buy", {'photo_id': photo.id, 'code': 'FORTYOFF'})
        # Assert that the price we were charged is right
        self.assertContains(response, "Price: $8.97")

        # Double check by fetching from the payment log
        from photos.models import PurchaseLog

        # Get the purchase log (ids always start)
        log = PurchaseLog.objects.get(id=1)
        # Assert that the logged price is also the correct amount
        self.assertEqual(log.amount, Decimal("8.97"))

class TestCouponCodePurchaseFlow(SeleniumTestCase):
    @exercise(7, "Push the feature live for everyone.")
    def test_purchase_flow(self):
        # Create a coupon code
        self.driver.get(self.live_server_url + "/admin/create_coupon")
        # Enter the code name
        self.wait_for(self.driver.find_element_by_css_selector, "input[name='code']").send_keys("SAVE20")
        # Enter the discount amount
        self.wait_for(self.driver.find_element_by_css_selector, "input[name='discount_percentage']").send_keys("20")
        # Submit the form
        self.wait_for(self.driver.find_element_by_css_selector, "input[type='submit']").click()


        # Create a photo to purchase
        photo = create_photo()

        # Start at the home page
        self.driver.get(self.live_server_url)
        # Click on the photo
        self.wait_for(self.driver.find_element_by_partial_link_text, photo.title).click()
        # Start purchase from details page
        self.wait_for(self.driver.find_element_by_css_selector, "input[value='Buy Photo']").click()

        # Find the coupon code form
        form = self.wait_for(self.driver.find_element_by_css_selector, "form[action='/checkout']")
        # Type in the code
        self.wait_for(form.find_element_by_css_selector, "input[name='code']").send_keys("SAVE20")
        # Apply the code
        self.wait_for(form.find_element_by_css_selector, "input[type='submit']").click()

        # Fill out checkout form and submit
        self.wait_for(self.driver.find_element_by_css_selector, "form[action='/buy'] input[type='submit']").click()

        # Make sure we get the confirmation page
        self.wait_for(self.driver.find_element_by_css_selector, ".thanks")

        # Make sure we get the discounted price
        price_text = self.wait_for(self.driver.find_element_by_css_selector, ".price").text
        self.assertEqual(price_text.strip(), "Price: $11.96")
