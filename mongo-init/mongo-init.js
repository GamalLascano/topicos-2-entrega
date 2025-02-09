db = db.getSiblingDB('subscriptions');
db.createCollection('users');
db.createCollection('logs');
db.users.createIndex({apiKey: "text"}, {unique: true});
db.users.insertMany([{
    "apiKey": "3a30a7f7-5374-4ffc-b061-5aa3145ad4ce",
    "subscription": "freemium"
  },
  {
    "apiKey": "d10aa37e-d9bc-44e7-aba4-79feab1e822b",
    "subscription": "premium"
  }]);

print('Database set up complete!');