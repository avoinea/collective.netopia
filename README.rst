==================
collective.netopia
==================

`Netopia Payments <https://netopia-payments.com>`_ for Plone

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
7. RestAPI endpoints:

   - **order/@netopia.sign**
   - **order/@netopia.confirm**

Translations
------------

This product has been translated into

- Romanian


Installation
------------

1. Within your Plone 6 pip based environment run::

    bin/pip install collective.netopia

2. Restart Plone
3. Go to Site Setup > Add-ons and install collective.netopia
4. Go to Site Setup > Netopia Payments and provided required information
5. Go to Site Setup > Content Types and add a new content-type called Order
6. Via behaviors Tab enable Order, Price, Billing and Shipping behaviors
7. Go to Site root and add a new Order
8. Go to /my-order/netopia.pay and click **Continue to payment**

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
