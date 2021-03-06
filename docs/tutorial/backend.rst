Building The Backend
====================

Before You Start
----------------

This guide assumes you already have a Django-based website where your users can
browse around whatever it is you're selling. If you haven't, go ahead and build
one, we'll be here when you get back!

For the examples in this guide, we'll assume the products in your store are
modelled using the following model.

.. code:: python

    from django.db import models

    class Product(models.Model):
        name = models.CharField(max_length=255)
        unit_price = models.DecimalField(max_digits=7, decimal_places=2)

.. note::

    Lorikeet doesn't require that you create a ``Product`` model. You can model your products however you like; this is just how we've chosen to do it in this tutorial.

Line Items
----------

In Lorikeet, a shopping cart is made up of line items;
subclasses of :class:`lorikeet.models.LineItem`, with a ``get_total`` method
that returns how much they cost. Here's a simple one:

.. code:: python

    from django.db import models
    from lorikeet.models import LineItem

    class MyLineItem(LineItem):
        product = models.ForeignKey(Product, on_delete=models.PROTECT)
        quantity = models.PositiveSmallIntegerField()

        def get_total(self):
            return self.quantity * self.product.unit_price

Every line item type needs a serializer, so that your frontend can create new
LineItems and add things to your users' carts. You should subclass these from
:class:`lorikeet.api_serializers.LineItemSerializer`, but otherwise write them
as you would a normal Django REST Framework serializer.

.. code:: python

    from rest_framework import fields
    from lorikeet.api_serializers import (LineItemSerializer,
                                          PrimaryKeyModelSerializer)

    from . import models


    class ProductSerializer(PrimaryKeyModelSerializer):
        class Meta:
            model = models.Product
            fields = ('id', 'name', 'unit_price')


    class MyLineItemSerializer(LineItemSerializer):
        product = ProductSerializer()
        class Meta:
            model = models.MyLineItem
            fields = ('product', 'quantity',)


.. note::

    We've also made a simple serializer for our ``Product`` class. Notice that we've subclassed :class:`lorikeet.api_serializers.PrimaryKeyModelSerializer`; we'll talk about what this serializer class does when we get to the frontend.

The last thing we need to do is link the two together when Django starts up.
The easiest place to do this is in the `ready` method of your app's `AppConfig`:

.. code:: python

    from django.apps import AppConfig

    class MyAppConfig(AppConfig):
        # ...

        def ready(self):
            from . import models, api_serializers
            from lorikeet.api_serializers import registry

            registry.register(models.MyLineItem,
                              api_serializers.MyLineItemSerializer)

.. warning::

    If you're newly setting up an app config for use with Lorikeet, make sure
    Django actually loads it!

    You can do this by either changing your app's entry in `INSTALLED_APPS` to
    the dotted path to your AppConfig (e.g. ``myapp.apps.MyAppConfig``), or
    by adding a line like ``default_app_config = "myapp.apps.MyAppConfig"`` in
    your app's ``__init__.py``.

    For more on app configs, check out the `Django documentation <https://docs.djangoproject.com/en/1.10/ref/applications/#application-configuration>`_.

Delivery Addresses
------------------

Now that Lorikeet knows about the things you're selling, it needs to know where you plan to send them after they've been sold, whether that's a postal address, an email, or something totally different.

.. note::

    There are `plans to eventually add an optional pre-built postal addressing plugin <https://github.com/excitedleigh/lorikeet/issues/1>`_, which will mean you'll be able to skip this section in the future if you're delivering to postal addresses.

Just like with line items, we need a model subclassing :class:`lorikeet.models.DeliveryAddress`, a serializer, and a ``registry.register`` call to connect the two. Delivery addresses are even eaiser, though; there's no special methods you need to define.

.. code:: python

    class AustralianDeliveryAddress(DeliveryAddress):
        addressee = models.CharField(max_length=255)
        address = models.TextField()
        suburb = models.CharField(max_length=255)
        state = models.CharField(max_length=3, choices=AUSTRALIAN_STATES)
        postcode = models.CharField(max_length=4)

.. code:: python

    class AustralianDeliveryAddressSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.AustralianDeliveryAddress
            fields = ('addressee', 'address', 'suburb', 'state', 'postcode')

.. code:: python

    registry.register(models.AustralianDeliveryAddress,
                      api_serializers.AustralianDeliveryAddressSerializer)

Payment Methods
---------------

Now Lorikeet knows what we're buying, and where it's going, but it needs to be able to collect payment. By now, you probably won't be surprised to find that you need to provide a model subclassing :class:`lorikeet.models.PaymentMethod`, a serializer, and link the two with ``registry.register``.

.. tip::

    If you're planning to accept payments via Stripe, you can skip this section; Lorikeet comes built-in with an optional Stripe payment method. See the section on :doc:`stripe`.

For this example, we'll use the fictional payment provider Pipe, which just so happens to have a similar API to Stripe, although slightly simplified.

.. code:: python

    class PipeCard(PaymentMethod):
        card_id = models.CharField(max_length=30)

With most payment providers, the data you want to send to the server on creation is totally different to the data you want to receive when viewing the payment method. Usually, you have some sort of opaque token returned by a JavaScript library, which you want to pass to your payment provider and store the result; when you read it back you want to know that it's a Visa that ends in 4242.

We've accomplished that by using a ``write_only`` field and a pair of ``SerializerMethodField`` instances (which defualt to read-only), and a ``create()`` method to communicate with the payment provider.

.. code:: python

    class PipeCardSerializer(serializers.ModelSerializer):
        card_token = fields.CharField(max_length=30, write_only=True)
        brand = fields.SerializerMethodField()
        last4 = fields.SerializerMethodField()

        class Meta:
            model = models.PipeCard
            fields = ('card_token', 'brand', 'last4')

        def get_brand(self, object):
            return pipe.get_card(object.card_id)['brand']

        def get_last4(self, object):
            return pipe.get_card(object.card_id)['last4']

        def create(self, validated_data):
            card_token = validated_data.pop('card_token')
            validated_data['card_id'] = pipe.create_card(card_token)['id']
            return super().create(validated_data)

Now that we can create payment methods, let's look at what happens when we charge them. We'll need a model to store details about a charge, which should be a subclass of :class:`lorikeet.models.Payment`.

.. code:: python

    class PipePayment(Payment):
        payment_id = models.CharField(max_length=30)

Then, we'll need to add a ``make_payment`` method to our ``PipeCard`` class. This should either return an instance of our ``PipePayment`` class, or raise :class:`lorikeet.exceptions.PaymentError` if the payment is unsuccessful.

.. note::

    The :class:`~lorikeet.models.Payment` model has a mandatory ``method`` field, which you'll need to fill with ``self`` when you create new instances.

.. code:: python

    class PipeCard(PaymentMethod):
        card_id = models.CharField(max_length=30)

        def make_payment(self, order, amount):
            try:
                payment_id = pipe.charge_card(self.card_id, amount)
            except pipe.ChargeError as e:
                raise PaymentError(e.user_info)
            else:
                return PipePayment.objects.create(method=self, payment_id=payment_id)
