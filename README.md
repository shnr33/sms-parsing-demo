# sms-parsing-demo
A Flask app which parses a JSON dump of SMS data and provides a dashboard with collated data.

The app is designed to be deployed on Google App Engine. A demo of it can be seen here - [https://ele-cc-darshan.appspot.com/](https://ele-cc-darshan.appspot.com/)

Once a JSON file is submitted to the system, the server parses the SMS data, collates it according to sender, differentiating between Transactional and Promotional messages and provides a dashboard with a tabulated form of the collated data.

This currently works on the JSON file obtained from Android phone through the app - [Conversation Backup](https://play.google.com/store/apps/details?id=net.ugorji.android.conversationbackup)

### Uses

- [Flask](http://flask.pocoo.org/): to serve as the application server
- [Bootstrap](http://getbootstrap.com/)
- [jQuery](https://jquery.com/)
- [FooTables](https://fooplugins.github.io/FooTable/index.html): a plug-in based on jQuery and Bootstrap to render the data in a responsive, searchable, paginated table.
