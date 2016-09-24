from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
import datetime

class UserManager(models.Manager):
    def register(self, data):
        response = {}
        validationErrors = self.validateAllFields(data)

        if len(validationErrors) > 0:
            response["validated"] = False
            response["errors"] = validationErrors
            response["registered"] = False
        else:
            response["validated"] = True

            # Validation passed. Save the new user to the database,
            # but first check if the user already exists.
            if not len(User.objects.filter(email = data["Email"])) > 0:
                newUser = User.objects.create(
                    name = data['Name'],
                    alias = data['Alias'],
                    email = data['Email'],
                    password = bcrypt.hashpw(data['Password'].encode(), bcrypt.gensalt()),
                    birthday = data['Birthday']
                )

                response["registered"] = True
                response["user"] = newUser
            else:
                response["registered"] = False
                response["errors"] = [ "User already exists. Please login instead." ]
        return response

    def login(self, data):
        response = {}
        badLoginMsg = "Unknown email or bad password."
        existingUser = None
        try:
            existingUser = User.objects.filter(email = data['Email'])
            if bcrypt.hashpw(data['Password'].encode(), existingUser[0].password.encode()) != existingUser[0].password:
                response["logged_in"] = False
                response["errors"] = [ badLoginMsg ]
                return response
        except Exception, e:
              # Handle situation when the salt is bad, etc.
              response["logged_in"] = False
              response["errors"] = [ badLoginMsg ]
              print "Unexpected error: " + e.message
              return response

        # Login succeeded.
        response["logged_in"] = True
        response["user"] = existingUser[0]
        return response

    ####### Validation Helper Methods #######

    def validateAllFields(self, data):
        response = []

        self.validateNotBlank(data, response)
        self.validateNames(data, response)
        self.validatePasswords(data, response)
        self.validateEmail(data, response)
        self.validateBirthday(data, response)

        return response

    def validateNotBlank(self, data, errors):
        for key in data:
            if len(data[key]) < 1:
                errors.append(key + " is empty but is required.")

    def validateNames(self, data, errors):
        MIN_NAME_LEN = 2
        #if all(c.isalpha() or c.isspace() for c in data["Name"]):
        #if not data["Name"].isalpha() or not data["Alias"].isalpha():
            #errors.append("Only alphamumeric characters are allowed for the name and alias.")

        if len(data["Name"]) < MIN_NAME_LEN or len(data["Alias"]) < MIN_NAME_LEN:
            errors.append("Name and Alias must contain at least two characters.")

    def validatePasswords(self, data, errors):
        MIN_PASSWORD = 8
        if len(data["Password"]) < MIN_PASSWORD:
            errors.append("The password must be at least " + str(MIN_PASSWORD) + " characters. Yours is only " + str(len(data["Password"])) + ".")

        if len(data["Password"]) != len(data["Confirmed Password"]):
            errors.append("The password and confirmed password do not match.")

    def validateEmail(self, data, errors):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(data["Email"]):
            errors.append("The email is invalid.")

    def validateBirthday(self, data, errors):
        MIN_BIRTHDAY = '1900-01-01'
        MAX_BIRTHDAY = str(datetime.datetime.now())
        if data["Birthday"] < MIN_BIRTHDAY or data["Birthday"] > MAX_BIRTHDAY:
            errors.append("Invalid birthday.")

    ####### Validation Helper Methods Ends #######


class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
