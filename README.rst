==================
collective.netopia
==================

`Netopia Payments <https://netopia-payments.com>`_ for `Plone <https://plone.org/>`_

See also `volto-netopia <https://github.com/avoinea/volto-netopia>`_
if you intend to use with `Volto <https://6.dev-docs.plone.org/volto/>`_ Plone Frontend.

Features
--------

1. Control Panel entry to store Netopia Payments secrets **/@@netopia.controlpanel**
2. Order behaviors:

   - **collective.netopia.order**
   - **collective.netopia.price**
   - **collective.netopia.billing**
   - **collective.netopia.shipping**

3. Sign Order Utility **getUtility(ICollectiveNetopiaSignedOrder)**
4. Sign Order Browser View **order/@@netopia.sign**
5. Payment Browser View **order/@@netopia.pay**
6. Payment Confirmation Browser View **order/@@netopia.confirm**
7. Custom events and content-rules trigger actions:

   - **IPaymentEvent**
   - **IPaymentConfirmedEvent**
   - **IPaymentConfirmedPendingEvent**
   - **IPaymentPaidPendingEvent**
   - **IPaymentPaidEvent**
   - **IPaymentCancelledEvent**
   - **IPaymentCreditEvent**
   - **IPaymentRejectedEvent**

8. RestAPI endpoints:

   - **order/@netopia.sign**

Translations
------------

This product has been translated into

- Romanian


Getting started
---------------

1. Within your Plone 6 pip based environment run::

    bin/pip install collective.netopia

2. Restart Plone
3. Go to Site Setup > Add-ons and install collective.netopia
4. Go to Site Setup > Netopia Payments and provided required information
5. Go to Site Setup > Content Types and add a new content-type called Order
6. Via behaviors Tab enable Order, Price, Billing and Shipping behaviors
7. Go to Site root and add a new Order
8. Go to /my-order/netopia.pay and click **Continue to payment**

Testing Cards
-------------

- https://support.netopia-payments.com/en-us/article/52-carduri-de-test

Troubleshooting
---------------

1. locale.Error: unsupported locale setting::

      Module collective.netopia.utilities.order, line 106, in __call__
      Module collective.netopia.mobilpay.payment.request.card, line 60, in encrypt
      Module collective.netopia.mobilpay.invoice, line 116, in create_xml_element
      Module locale, line 610, in setlocale
      locale.Error: locale.Error: unsupported locale setting

- See https://stackoverflow.com/questions/59633558/python-based-dockerfile-throws-locale-error-unsupported-locale-setting

      apt-get update && \
      apt-get install -y locales && \
      sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
      dpkg-reconfigure --frontend=noninteractive locales

- After dpkg-reconfigure, the locale should be available as en_US.UTF-8.
- You can also add the following to .bashrc::

      export LANG en_US.UTF-8
      export LC_NUMERIC en_US.UTF-8


Authors
-------

Alin Voinea


Contributors
------------

Put your name here, you deserve it!

- ?


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.netopia/issues
- Source Code: https://github.com/collective/collective.netopia


Support
-------

If you are having issues, please let us know.
We have a mailing list located at: project@example.com


License
-------

The project is licensed under the GPLv2.
