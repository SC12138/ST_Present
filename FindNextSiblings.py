import unittest
import bs4
from hypothesis import given, example, settings, Verbosity
from hypothesis.internal.conjecture.utils import boolean
from hypothesis.strategies import *
import re

from bs4.element import SoupStrainer

class TestFindNextSiblings(unittest.TestCase):   
    """
    This class contains all blackbox testcases for function find_next_siblings() of class BeautifulSoup(inherited from class PageElement)

    Signature of function find_next_siblings:
    find_next_siblings(self, name=None, attrs={}, text=None, limit=None, **kwargs)

    Find all siblings of this PageElement that match the given criteria and appear later in the document.

    :param name: A filter on tag name.
    :param attrs: A dictionary of filters on attribute values.
    :param text: A filter for a NavigableString with specific text.
    :param limit: Stop looking after finding this many results.
    :kwargs: A dictionary of filters on attribute values.

    :return: A ResultSet of PageElements.
    :rtype: bs4.element.ResultSet

    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_html_page_element = bs4.BeautifulSoup(
        """
        <html><head><title>The Dormouse's story</title></head>
        <body>
        
        <p class="title"><b>The Dormouse's story</b></p>

        <div class="wrapper_div">
            <div class="wrapper_div">
                <p class="wrapper">
                    <p class="story">
                        Once upon a time there were three little sisters; and their names were
                        <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
                        <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
                        <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
                        and they lived at the bottom of a well.
                        <p class="brother">Tom</p>    
                        <p class="brother">Bob</p>    
                    </p>
                </p>
            </div>
        </div>

        <p class="story">...</p>
        """
        , "html.parser")
    
    @composite
    def input_and_r_1(draw):
        num_attr = 1
        input_name_filter = draw(one_of([sampled_from(["a", "p"]),  # string filter
                                         sampled_from([re.compile("^a"), re.compile("^p")]), # re filter
                                         permutations(["a", "p"]).map(lambda x: x[:num_attr]), # list of filter
                                         sampled_from([True]), # boolean True
                                         ]))
        input_attrs_filter = draw(dictionaries(keys=sampled_from(["class"]), values=sampled_from(["sister"]), min_size=1))
        input_text_filter = draw(one_of([sampled_from(["Lacie"]),  # string filter
                                         sampled_from([re.compile("^Lacie")]), # re filter
                                         permutations(["Lacie"]).map(lambda x: x[:num_attr]), # list of filter
                                         sampled_from([True]), # boolean True
                                         ]))
        input_limit = draw(integers(min_value=1, max_value=5))     # seems that behavior is not deterministic if limit<=0                              

        # set expected result based on attrs_filter
        if ( input_name_filter=="a" or 
             input_name_filter==re.compile("^a") or 
             input_name_filter==["a"] ):
            if input_text_filter==True: r_exp=2
            else: r_exp=1
        elif input_name_filter==True:
            if input_text_filter==True: r_exp=2
            else: r_exp=1
        else: r_exp=0
        # set expected result to input_limit if 0<input_limit<r_exp 
        if (input_limit>0 and input_limit<r_exp): r_exp=input_limit 

        return (input_name_filter, input_attrs_filter, input_text_filter, input_limit, r_exp)
    @given(input=input_and_r_1())
    def test_black_1(self, input):
        """ Testcase for following block:
                name: non-empty filter that match some tags (including string, re, list, function, True)
                attrs: non-empty dict of filter that match some tags
                text: non-empty filter that match some tags 
                limit: integer in range [1, 5] 
        """
        (input_name_filter, input_attrs_filter, input_text_filter, input_limit, r_exp) = input
        tag = self.test_html_page_element.a # get first tag <a>
        r = tag.find_next_siblings(name=input_name_filter, attrs=input_attrs_filter, text=input_text_filter, limit=input_limit)
        self.assertTrue(len(r)==r_exp)


    @composite
    def input_and_r_2(draw):
        num_attr = 1
        input_name_filter = draw(one_of([sampled_from(["a", "p"]),  # string filter
                                         sampled_from([re.compile("^a"), re.compile("^p")]), # re filter
                                         permutations(["a", "p"]).map(lambda x: x[:num_attr]), # list of filter
                                         sampled_from([True]), # boolean True
                                         ]))
        input_attrs_filter = draw(dictionaries(keys=sampled_from(["class"]), values=sampled_from(["sister"]), min_size=1))
        input_text_filter = draw(one_of([sampled_from(["Lacie_not_exist"]),  # string filter
                                         sampled_from([re.compile("^Lacie_not_exist")]), # re filter
                                         permutations(["Lacie_not_exist"]).map(lambda x: x[:num_attr]), # list of filter
                                         # sampled_from([True]), # boolean True
                                         ]))
        input_limit = draw(integers(min_value=1, max_value=5))     # seems that behavior is not deterministic if limit<=0                              

        # set expected result based on attrs_filter
        r_exp=0
        # set expected result to input_limit if 0<input_limit<r_exp 
        if (input_limit>0 and input_limit<r_exp): r_exp=input_limit 

        return (input_name_filter, input_attrs_filter, input_text_filter, input_limit, r_exp)
    @given(input=input_and_r_2())
    def test_black_2(self, input):
        """ Testcase for following block:
                name: non-empty filter that match some tags (including string, re, list, function, True)
                attrs: non-empty dict of filter that match some tags
                text: non-empty filter that NOT match any tags 
                limit: integer in range [1, 5] 
        """
        (input_name_filter, input_attrs_filter, input_text_filter, input_limit, r_exp) = input
        tag = self.test_html_page_element.a # get first tag <a>
        r = tag.find_next_siblings(name=input_name_filter, attrs=input_attrs_filter, text=input_text_filter, limit=input_limit)
        self.assertTrue(len(r)==r_exp)


    @composite
    def input_and_r_3(draw):
        num_attr = 1
        input_name_filter = draw(one_of([sampled_from(["a", "p"]),  # string filter
                                         sampled_from([re.compile("^a"), re.compile("^p")]), # re filter
                                         permutations(["a", "p"]).map(lambda x: x[:num_attr]), # list of filter
                                         sampled_from([True]), # boolean True
                                         ]))
        input_attrs_filter = draw(dictionaries(keys=sampled_from(["class"]), values=sampled_from(["sister_not_exist"]), min_size=1))
        input_text_filter = draw(one_of([sampled_from(["Lacie_not_exist"]),  # string filter
                                         sampled_from([re.compile("^Lacie_not_exist")]), # re filter
                                         permutations(["Lacie_not_exist"]).map(lambda x: x[:num_attr]), # list of filter
                                         # sampled_from([True]), # boolean True
                                         ]))
        input_limit = draw(integers(min_value=1, max_value=5))     # seems that behavior is not deterministic if limit<=0                              

        # set expected result based on attrs_filter
        r_exp=0
        # set expected result to input_limit if 0<input_limit<r_exp 
        if (input_limit>0 and input_limit<r_exp): r_exp=input_limit 

        return (input_name_filter, input_attrs_filter, input_text_filter, input_limit, r_exp)
    @given(input=input_and_r_3())
    def test_black_3(self, input):
        """ Testcase for following block:
                name: non-empty filter that match some tags (including string, re, list, function, True)
                attrs: non-empty dict of filter that NOT match any tags
                text: non-empty filter that NOT match any tags 
                limit: integer in range [1, 5] 
        """
        (input_name_filter, input_attrs_filter, input_text_filter, input_limit, r_exp) = input
        tag = self.test_html_page_element.a # get first tag <a>
        r = tag.find_next_siblings(name=input_name_filter, attrs=input_attrs_filter, text=input_text_filter, limit=input_limit)
        self.assertTrue(len(r)==r_exp)


    @composite
    def input_and_r_4(draw):
        num_attr = 1
        input_name_filter = draw(one_of([sampled_from(["a_not_exist", "p_not_exist"]),  # string filter
                                         sampled_from([re.compile("^a_not_exist"), re.compile("^p_not_exist")]), # re filter
                                         permutations(["a_not_exist", "p_not_exist"]).map(lambda x: x[:num_attr]), # list of filter
                                         # sampled_from([True]), # boolean True
                                         ]))
        input_attrs_filter = draw(dictionaries(keys=sampled_from(["class"]), values=sampled_from(["sister_not_exist"]), min_size=1))
        input_text_filter = draw(one_of([sampled_from(["Lacie_not_exist"]),  # string filter
                                         sampled_from([re.compile("^Lacie_not_exist")]), # re filter
                                         permutations(["Lacie_not_exist"]).map(lambda x: x[:num_attr]), # list of filter
                                         # sampled_from([True]), # boolean True
                                         ]))
        input_limit = draw(integers(min_value=1, max_value=5))     # seems that behavior is not deterministic if limit<=0                              

        # set expected result based on attrs_filter
        r_exp=0
        # set expected result to input_limit if 0<input_limit<r_exp 
        if (input_limit>0 and input_limit<r_exp): r_exp=input_limit 

        return (input_name_filter, input_attrs_filter, input_text_filter, input_limit, r_exp)
    @given(input=input_and_r_4())
    def test_black_4(self, input):
        """ Testcase for following block:
                name: non-empty filter that NOT match any tags (including string, re, list, function, True)
                attrs: non-empty dict of filter that NOT match any tags
                text: non-empty filter that NOT match any tags 
                limit: integer in range [1, 5] 
        """
        (input_name_filter, input_attrs_filter, input_text_filter, input_limit, r_exp) = input
        tag = self.test_html_page_element.a # get first tag <a>
        r = tag.find_next_siblings(name=input_name_filter, attrs=input_attrs_filter, text=input_text_filter, limit=input_limit)
        self.assertTrue(len(r)==r_exp)


    @composite
    def input_and_r_5(draw):
        num_attr = 1
        input_name_filter = draw(one_of([sampled_from([""]),  # string filter
                                         sampled_from([[]]), # list of filter
                                         ]))
        input_attrs_filter = draw(dictionaries(keys=sampled_from(["class"]), values=sampled_from(["sister"]), min_size=1))
        input_text_filter = draw(one_of([sampled_from(["Lacie"]),  # string filter
                                         sampled_from([re.compile("^Lacie")]), # re filter
                                         permutations(["Lacie"]).map(lambda x: x[:num_attr]), # list of filter
                                         sampled_from([True]), # boolean True
                                         ]))
        input_limit = draw(integers(min_value=1, max_value=5))     # seems that behavior is not deterministic if limit<=0                              

        # set expected result based on attrs_filter
        if input_name_filter=="" :r_exp=0 
        elif input_text_filter==True: r_exp=2
        else: r_exp=1
        # set expected result to input_limit if 0<input_limit<r_exp 
        if (input_limit>0 and input_limit<r_exp): r_exp=input_limit 

        return (input_name_filter, input_attrs_filter, input_text_filter, input_limit, r_exp)
    @given(input=input_and_r_5())
    def test_black_5(self, input):
        """ Testcase for following block:
                name: empty filter (including string, list,)
                attrs: non-empty dict of filter that may match some tags
                text: non-empty filter that may match some tags 
        """
        (input_name_filter, input_attrs_filter, input_text_filter, input_limit, r_exp) = input
        tag = self.test_html_page_element.a # get first tag <a>
        r = tag.find_next_siblings(name=input_name_filter, attrs=input_attrs_filter, text=input_text_filter, limit=input_limit)
        self.assertTrue(len(r)==r_exp)


    @composite
    def input_and_r_6(draw):
        num_attr = 1
        input_name_filter = draw(one_of([sampled_from(["a", "p"]),  # string filter
                                         sampled_from([re.compile("^a"), re.compile("^p")]), # re filter
                                         permutations(["a", "p"]).map(lambda x: x[:num_attr]), # list of filter
                                         sampled_from([True]), # boolean True
                                         ]))
        input_attrs_filter = {} # empty dict
        input_text_filter = draw(one_of([sampled_from(["Lacie"]),  # string filter
                                         sampled_from([re.compile("^Lacie")]), # re filter
                                         permutations(["Lacie"]).map(lambda x: x[:num_attr]), # list of filter
                                         sampled_from([True]), # boolean True
                                         ]))
        input_limit = draw(integers(min_value=1, max_value=5))     # seems that behavior is not deterministic if limit<=0                              

        # set expected result based on attrs_filter
        if ( input_name_filter=="a" or 
             input_name_filter==re.compile("^a") or 
             input_name_filter==["a"] ):
            if input_text_filter==True: r_exp=2
            else: r_exp=1
        elif input_name_filter==True:
            if input_text_filter==True: r_exp=4
            else: r_exp=1
        else: 
            if input_text_filter==True: r_exp=2
            else: r_exp=0
        # set expected result to input_limit if 0<input_limit<r_exp 
        if (input_limit>0 and input_limit<r_exp): r_exp=input_limit 

        return (input_name_filter, input_attrs_filter, input_text_filter, input_limit, r_exp)
    @given(input=input_and_r_6())
    def test_black_6(self, input):
        """ Testcase for following block:
                name: non-empty filter that may match some tags (including string, re, list, function, True)
                attrs: empty dict of filter 
                text: non-empty filter that may match any tags 
        """
        (input_name_filter, input_attrs_filter, input_text_filter, input_limit, r_exp) = input
        tag = self.test_html_page_element.a # get first tag <a>
        r = tag.find_next_siblings(name=input_name_filter, attrs=input_attrs_filter, text=input_text_filter, limit=input_limit)
        self.assertTrue(len(r)==r_exp)


    @composite
    def input_and_r_7(draw):
        num_attr = 1
        input_name_filter = draw(one_of([sampled_from(["a", "p"]),  # string filter
                                         sampled_from([re.compile("^a"), re.compile("^p")]), # re filter
                                         permutations(["a", "p"]).map(lambda x: x[:num_attr]), # list of filter
                                         sampled_from([True]), # boolean True
                                         ]))
        input_attrs_filter = draw(dictionaries(keys=sampled_from(["class"]), values=sampled_from(["sister"]), min_size=1))
        input_text_filter = draw(one_of([sampled_from([""]),  # string filter (empty string "" works as True)
                                         sampled_from([[]]), # list of filter
                                         ]))
        input_limit = draw(integers(min_value=1, max_value=5))     # seems that behavior is not deterministic if limit<=0                              

        # set expected result based on attrs_filter
        if input_name_filter==True: r_exp=2
        elif ( input_name_filter=="a" or 
             input_name_filter==re.compile("^a") or 
             input_name_filter==["a"] ): r_exp=2
        else: r_exp=0
        # set expected result to input_limit if 0<input_limit<r_exp 
        if (input_limit>0 and input_limit<r_exp): r_exp=input_limit 

        return (input_name_filter, input_attrs_filter, input_text_filter, input_limit, r_exp)
    @given(input=input_and_r_7())
    def test_black_7(self, input):
        """ Testcase for following block:
                name: non-empty filter that may match some tags (including string, re, list, function, True)
                attrs: non-empty dict of filter that may match some tags
                text: empty filter (including string, list,)
        """
        (input_name_filter, input_attrs_filter, input_text_filter, input_limit, r_exp) = input
        tag = self.test_html_page_element.a # get first tag <a>
        r = tag.find_next_siblings(name=input_name_filter, attrs=input_attrs_filter, string=input_text_filter, limit=input_limit)
        self.assertTrue(len(r)==r_exp)


    """ Whitebox Testing's args:
            name: 
                - String(with prefix)
                - String(without prefix)
                - True/None
                - instance of SoupStrainer
            text: 
                - String
                - None
            limit: Integer
            kwargs: contains "string"
    """ 

    def test_white_1(self):
        """ text: None
            kwargs: contains "string"
            name: instance of SoupStrainer
        """
        tag = self.test_html_page_element.a # get first tag <a>
        n = SoupStrainer("p")
        r = tag.find_next_siblings(name=n, text=None, string=["Tom", "Bob"])
        r = [i.text for i in r]
        r_exp = ["Tom", "Bob"]
        self.assertEqual(r, r_exp)

    def test_white_2(self):
        """ text: None
            name: True / None
        """
        tag = self.test_html_page_element.a # get first tag <a>
        r = tag.find_next_siblings(name=True, text=None)
        r = [i.text for i in r]
        r_exp = ["Lacie", "Tillie", "Tom", "Bob"]
        self.assertEqual(r, r_exp)

    def test_white_3(self):
        """ text: not None
            name: String with prefix
        """
        tag = self.test_html_page_element.a # get first tag <a>
        r = tag.find_next_siblings(name="prefix:p", text=None)
        r = [i.text for i in r]
        r_exp = []
        self.assertEqual(r, r_exp)

    def test_white_4(self):
        """ text: not None
            name: String without prefix
        """
        tag = self.test_html_page_element.a # get first tag <a>
        r = tag.find_next_siblings(name="p", text=None)
        r = [i.text for i in r]
        r_exp = ["Tom", "Bob"]
        self.assertEqual(r, r_exp)

if __name__ == '__main__':
    unittest.main()