from relations import *

persion1 = Person(name='Tom')
add1 = Address(email='Tom@gmail.com', person=persion1)
add2 = Address(email='John@gmail.com')
persion1.addresses.append(add2)

db.session.add(persion1)
db.session.commit()


#User.query.all()