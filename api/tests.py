"""
A few test to verify basic functionality. The encoder should probably be tested directly

This file demonstrates writing tests using the unittest module. These shoud pass
when you run "manage.py test".
"""
from opendata.models import *
from suggestions.models import *

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from datetime import datetime

import simplejson as j
import base64

class RestTestCase(TestCase):
    def setUp(self):
        self.c = Client()
        self.password = "password"
        self.u = User.objects.create(username="testuser")
        self.u.set_password(self.password)
        self.u.save()

        self.u2 = User.objects.create(username="testuser2")
        self.u2.set_password(self.password)
        self.u2.save()

    def mkrsrc(self,name,**kwargs):
        return Resource.objects.create(
            name = name,
            created_by = self.u,
            last_updated_by=self.u,
            created = datetime.now(),
            **kwargs)

    def mkidea(self,title,**kwargs):
        return Idea.objects.create(
            title = title,
            created_by = self.u,
            created_by_date = datetime.now(),
            updated_by = self.u,
            **kwargs)

    def mktag(self,tag_name,**kwargs):
        return Tag.objects.create(
            tag_name = tag_name,
            **kwargs)

    def mksug(self,text, **kwargs):
        return Suggestion.objects.create(
            text = text,
            suggested_by = self.u,
            **kwargs)

    def verify_ids(self, objdict, objlist, dict_key="id", list_key = "pk"):
        self.assertEquals(
            set(map(lambda obj: obj[dict_key], objdict)),
            set(map(lambda obj: getattr(obj, list_key), objlist)))

    def get(self, url):
        return j.loads(self.c.get(url).content)

    def assertCode(self, resp, code):
        self.assertEquals(resp.status_code, code)

    def assertEmptyList(self, url):
        self.assertEquals(self.get(url), list())

    def auth_pair(self, user, password = None):
        if not password:
            password = self.password

        base64_auth = base64.encodestring(user.username + ":" + password)
        return {"HTTP_AUTHORIZATION" : "Basic " + base64_auth}

class SuggestionsTest(RestTestCase):
    def test_empty_case(self):
        self.assertEmptyList("/api/suggestions/")

    def test_many(self):
        sug1 = self.mksug("sug1")
        sug2 = self.mksug("sug2")

        self.verify_ids(self.get("/api/suggestions/"), [sug1,sug2])

    def test_one(self):
        sug1 = self.mksug("sug1")
        sug2 = self.mksug("sug2")

        self.assertEquals(self.get("/api/suggestions/%d/" % sug1.pk)["id"], sug1.pk)
        self.assertEquals(self.get("/api/suggestions/%d/" % sug2.pk)["id"], sug2.pk)

    def test_search(self):
        sug1 = self.mksug("sug_a_b")
        sug2 = self.mksug("sug_c_b")
        sug3 = self.mksug("a_sug_c")

        # All results
        self.verify_ids(self.get("/api/suggestions/search?qs="), [sug1,sug2,sug3])

        # Basic searches
        self.verify_ids(self.get("/api/suggestions/search?qs=sug_a"), [sug1])
        self.verify_ids(self.get("/api/suggestions/search?qs=sug_"), [sug1,sug2,sug3])
        self.verify_ids(self.get("/api/suggestions/search?qs=_c"), [sug2,sug3])

        # No results
        self.assertEqual(self.get("/api/suggestions/search?qs=fail"), [])

    def test_invalid_url(self):
        self.assertCode(self.c.get("/api/suggestions/22/"), 404)
        self.assertCode(self.c.get("/api/suggestions/f/"), 404)

    def test_invalid_login(self):
        sug1 = self.mksug("sug1")

        resp = self.c.put("/api/suggestions/%s/vote"%sug1.pk, {}, **self.auth_pair(self.u,"fail"))
        self.assertEquals(resp.status_code, 401)


    def test_vote(self):
        sug1 = self.mksug("sug1")

        self.assertEqual(sug1.rating.votes, 0)

        # Single vote
        self.c.put("/api/suggestions/%s/vote"%sug1.pk, {}, **self.auth_pair(self.u))
        self.assertEqual(Suggestion.objects.all()[0].rating.votes, 1)

        # Only allow 1 vote
        self.c.put("/api/suggestions/%s/vote"%sug1.pk, {}, **self.auth_pair(self.u))
        self.assertEqual(Suggestion.objects.all()[0].rating.votes, 1)

        # Remove vote (does not exist)
        self.c.delete("/api/suggestions/%s/vote"%sug1.pk, {}, **self.auth_pair(self.u2))
        self.assertEqual(Suggestion.objects.all()[0].rating.votes, 1)

        # Second vote
        self.c.put("/api/suggestions/%s/vote"%sug1.pk, {}, **self.auth_pair(self.u2))
        self.assertEqual(Suggestion.objects.all()[0].rating.votes, 2)

        # Only allow 1 vote
        self.c.put("/api/suggestions/%s/vote"%sug1.pk, {}, **self.auth_pair(self.u2))
        self.assertEqual(Suggestion.objects.all()[0].rating.votes, 2)

        # Remove vote
        self.c.delete("/api/suggestions/%s/vote"%sug1.pk, {}, **self.auth_pair(self.u))
        self.assertEqual(Suggestion.objects.all()[0].rating.votes, 1)

        # Only remove once
        self.c.delete("/api/suggestions/%s/vote"%sug1.pk, {}, **self.auth_pair(self.u))
        self.assertEqual(Suggestion.objects.all()[0].rating.votes, 1)

        # Back to zero
        self.c.delete("/api/suggestions/%s/vote"%sug1.pk, {}, **self.auth_pair(self.u2))
        self.assertEqual(Suggestion.objects.all()[0].rating.votes, 0)
        
class TagTest(RestTestCase):
    def test_empty_case(self):
        self.assertEmptyList("/api/tags/")

    def test_many(self):
        tag1 = self.mktag("tag1")
        tag2 = self.mktag("tag2")

        self.verify_ids(self.get("/api/tags/"), [tag1, tag2], "name", "tag_name")

    def test_one_empty(self):
        tag1 = self.mktag("tag1")

        self.assertEmptyList("/api/tags/%s/" % tag1.tag_name)

    def test_one(self):
        tag1 = self.mktag("tag1")
        tag2 = self.mktag("tag2")

        rsrc1 = self.mkrsrc("rsrc1")
        rsrc2 = self.mkrsrc("rsrc2")
        rsrc3 = self.mkrsrc("rsrc3")

        rsrc1.tags.add(tag1)
        rsrc2.tags.add(tag1)
        rsrc2.tags.add(tag2)
        rsrc3.tags.add(tag2)
        
        self.verify_ids(self.get("/api/tags/%s/" % tag1.tag_name),[rsrc1,rsrc2])
        self.verify_ids(self.get("/api/tags/%s/" % tag2.tag_name),[rsrc2,rsrc3])

class IdeaTest(RestTestCase):
    def test_empty_case(self):
        self.assertEmptyList("/api/ideas/")

    def test_many(self):
        idea1 = self.mkidea("idea1")
        idea2 = self.mkidea("idea2")
        
        self.verify_ids(self.get("/api/ideas/"), [idea1,idea2])

    def test_single_case(self):
        idea1 = self.mkidea("idea1")

        self.assertEquals(self.get("/api/ideas/%d/" % idea1.pk)["id"], idea1.pk)

    def test_invalid_url(self):
        self.assertCode(self.c.get("/api/ideas/22/"), 404)
        self.assertCode(self.c.get("/api/ideas/f/"), 404)

        

class ResourceTest(RestTestCase):

    def test_empty_json_case(self):
        self.assertEmptyList("/api/resources/")
        
    def test_search(self):
        # Search fields:
        # name, description, org, div
        
        rsrc1 = self.mkrsrc("rsrc_a")
        rsrc2 = self.mkrsrc("rsrc_a", description = "descr_a")
        rsrc3 = self.mkrsrc("rsrc_b", description = "descr_b")
        rsrc4 = self.mkrsrc("f_rsrc_c", description = "descr_b", organization = "org_a")
        rsrc5 = self.mkrsrc("f_rsrc_d", organization = "org_a", division = "div_a")
        rsrc6 = self.mkrsrc("f_rsrc_e", division = "div_a", organization = "orb_c")

        # Empty search - return everything
        self.verify_ids(self.get("/api/resources/search?qs="), [rsrc1,rsrc2, rsrc3, rsrc4, rsrc5, rsrc6])

        # No search match
        self.assertEquals(self.get("/api/resources/search?qs=fail"), list())

        # Name partial search
        self.verify_ids(self.get("/api/resources/search?qs=f_rsrc_"), [rsrc4,rsrc5,rsrc6])

        # Name exact search
        self.verify_ids(self.get("/api/resources/search?qs=rsrc_c"), [rsrc4])

        # Description search
        self.verify_ids(self.get("/api/resources/search?qs=descr_b"), [rsrc3,rsrc4])

        # Organization search
        self.verify_ids(self.get("/api/resources/search?qs=org_a"), [rsrc4,rsrc5])

        # Division search
        self.verify_ids(self.get("/api/resources/search?qs=div_a"), [rsrc5,rsrc6])

    def test_multi_case(self):

        rsrc1 = self.mkrsrc("rsrc1")
        rsrc2 = self.mkrsrc("rsrc2")
        rsrc3 = self.mkrsrc("rsrc3", is_published=False)

        # Don't show non-published data
        self.verify_ids(self.get("/api/resources/"), [rsrc1, rsrc2])

        rsrc3.is_published = True
        rsrc3.save()

        self.verify_ids(self.get("/api/resources/"), [rsrc1, rsrc2, rsrc3])
    
    def test_single_case(self):
        rsrc1 = self.mkrsrc("rsrc1")

        self.assertEquals(self.get("/api/resources/%d/" % rsrc1.pk)["id"], rsrc1.pk)

    def test_invalid_url(self):
        self.assertCode(self.c.get("/api/resources/22/"), 404)
        self.assertCode(self.c.get("/api/resources/f/"), 404)

        

