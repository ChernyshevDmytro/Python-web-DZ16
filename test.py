"""
Tests
"""
# from app import .
from datetime import datetime
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Person, Phones

engine = create_engine(
    "sqlite:///test_new.db", connect_args={"check_same_thread": False}
)
DBSession = sessionmaker(bind=engine)
session = DBSession()


class TestStringMethods(unittest.TestCase):
    """Models testing"""

    def test_class_person_and_phone(self):
        """Models data testing"""
        person = Person(name="Jack")
        person.phones.append(Phones(phone=380976646239))
        birthday = "2022-11-11"
        dt_birthday = datetime(
            year=int(birthday[0:4]), month=int(birthday[5:7]), day=int(birthday[8:])
        )
        person.birthday = dt_birthday.date()
        self.assertEqual(person.name, "Jack")
        self.assertEqual(person.phones[0].phone, 380976646239)
        self.assertEqual(birthday, str(person.birthday))

    def test_add_contact_to_db(self):
        """Contact adding testing"""
        addedperson = Person(name="Jack")
        addedperson.phones = [Phones(phone=380976646239)]
        birthday = "2022-11-11"
        dt_birthday = datetime(
            year=int(birthday[0:4]), month=int(birthday[5:7]), day=int(birthday[8:])
        )
        addedperson.birthday = dt_birthday.date()
        session.add(addedperson)
        session.commit()
        for person in session.query(Person).all():
            if "Jack" == str(person.name):
                self.assertTrue("Jack" == person.name)
                self.assertEqual(birthday, str(person.birthday.date()))
                for phone in session.query(Phones).all():
                    if person.id == phone.person_id:
                        self.assertTrue(380976646239 == phone.phone)
                session.query(Person).filter(Person.name == "Jack").delete()
                session.commit()

    def test_del_contact_from_db(self):
        """Contact deleting from db testing"""
        session.query(Person).filter(Person.name == "Jack").delete()
        session.commit()
        for person in session.query(Person).all():
            if "Jack" == str(person.name):
                self.assertRaises(TypeError)

    def test_edit_contact_phone_to_db(self):
        """Contact eddition testing"""
        person = Person(name="Jack")
        person.phones = [Phones(phone=380976646239)]
        birthday = "2022-11-11"
        dt_birthday = datetime(
            year=int(birthday[0:4]), month=int(birthday[5:7]), day=int(birthday[8:])
        )
        person.birthday = dt_birthday.date()
        session.add(person)
        session.commit()
        for searchedperson in session.query(Person).all():
            if "Jack" == str(person.name):
                session.query(Phones).filter(
                    Phones.person_id == searchedperson.id
                ).delete()
                new_phone_number = 380976646240
                new_phone = Phones(
                    phone=int(new_phone_number), person_id=searchedperson.id
                )
                session.add(new_phone)
                session.commit()
                for person in session.query(Person).all():
                    if "Jack" == str(person.name):
                        self.assertTrue("Jack" == person.name)
                        for i in session.query(Phones).all():
                            if i.person_id == person.id:
                                self.assertEqual(380976646240, i.phone)
                                self.assertEqual(birthday, str(person.birthday.date()))
                                session.query(Phones).filter(
                                    Phones.person_id == searchedperson.id
                                ).delete()
                                session.query(Person).filter(
                                    Person.name == "Jack"
                                ).delete()
                                session.commit()

    def test_del_contact_phone_from_db(self):
        """Contact deleting from db testing"""
        person = Person(name="Jack")
        person.phones.append(Phones(phone=380976646239))
        birthday = "2022-11-11"
        dt_birthday = datetime(
            year=int(birthday[0:4]), month=int(birthday[5:7]), day=int(birthday[8:])
        )
        person.birthday = dt_birthday.date()
        session.add(person)
        session.commit()
        for person in session.query(Person).all():
            if "Jack" == str(person.name):
                session.query(Phones).filter(Phones.person_id == person.id).delete()
                session.add(person)
                session.commit()
                for person in session.query(Person).all():
                    if "Jack" == str(person.name):
                        self.assertFalse(person.phones)
                        session.query(Person).filter(Person.name == "Jack").delete()
                        session.commit()


if __name__ == "__main__":
    unittest.main()
