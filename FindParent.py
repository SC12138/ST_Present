import unittest
import bs4
from hypothesis import given, example, settings, Verbosity
from hypothesis.internal.conjecture.utils import boolean
from hypothesis.strategies import *
import re


class TestFindParent(unittest.TestCase):       
    """
    This class contains all blackbox testcases for function find_parent() of class BeautifulSoup(inherited from class PageElement)

    Signature of function find_parent:
    find_parent(self, name=None, attrs={}, **kwargs):
        '''Find the closest parent of this PageElement that matches the given criteria.'''

        :param name: A filter on tag name.
        :param attrs: A dictionary of filters on attribute values.
        :kwargs: A dictionary of filters on attribute values.

        :return: A PageElement.
        :rtype: bs4.element.Tag | bs4.element.NavigableString
    
    Attributes
    ----------
    
    """

    
    @classmethod
    def setUpClass(cls) -> None:
        cls.test_html_page_element = bs4.BeautifulSoup(
        """
        <html><head><title>The Dormouse's story</title></head>
        <body>
        
        <p class="title"><b>The Dormouse's story</b></p>

        <div class="wrapper_div_1">
            <div class="wrapper_div_2">
                <p class="wrapper">
                    <p class="story">
                        Once upon a time there were three little sisters; and their names were
                        <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
                        <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
                        <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
                        and they lived at the bottom of a well.
                    </p>
                </p>
            </div>
        </div>

        <p class="story">...</p>
        """
        , "html.parser")
    
    @classmethod
    def tearDownClass(cls) -> None:
        cls.test_html_element = None
    

    @composite
    def input_and_r_1(draw):
        start_tag_name = draw(sampled_from(["Elsie", "Lacie", "Tillie"]))
        num_attr = 1
        input_name_filter = draw(one_of([sampled_from(["p", "div"]),  # string filter
                                         sampled_from([re.compile("^p"), re.compile("^div")]), # re filter
                                         permutations(["p", "div"]).map(lambda x: x[:num_attr]), # list of filter
                                         sampled_from([True]), # boolean True
                                         ]))
        input_attrs_filter = draw(dictionaries(keys=sampled_from(["class"]), values=sampled_from(["wrapper_div_2"]), min_size=1))

        # set expected result based on attrs_filter
        if ( input_name_filter=="div" or 
             input_name_filter==re.compile("^div") or 
             (isinstance(input_name_filter,list) and "div" in input_name_filter) or
             input_name_filter==True):
            r_exp="wrapper_div_2"
        else:
            r_exp=None
        return (start_tag_name, input_name_filter, input_attrs_filter, r_exp)

    @given(input=input_and_r_1())
    def test_black_1(self, input):
        """ Testcase for following block:
                name: filter that match some parent tags (including string, re, list, True)
                attrs: dict of filter that match some parent tags
        """
        (start_tag_name, input_name_filter, input_attrs_filter, r_exp) = input
        tag = self.test_html_page_element.find(string=start_tag_name)
        r = tag.find_parent(name=input_name_filter, attrs=input_attrs_filter)
        r_c = r['class'][0] if not r==None else None
        self.assertEqual(r_c, r_exp)


    @composite
    def input_and_r_2(draw):
        start_tag_name = draw(sampled_from(["Elsie", "Lacie", "Tillie"]))
        num_attr = 1
        input_name_filter = draw(one_of([sampled_from(["p", "div"]),  # string filter
                                         sampled_from([re.compile("^p"), re.compile("^div")]), # re filter
                                         permutations(["p", "div"]).map(lambda x: x[:num_attr]), # list of filter
                                         sampled_from([True]), # boolean True
                                         ]))
        input_attrs_filter = draw(dictionaries(keys=sampled_from(["class"]), values=sampled_from(["class_not_exits"]), min_size=1))
        # set expected result based on attrs_filter
        r_exp = None

        return (start_tag_name, input_name_filter, input_attrs_filter, r_exp)
    @given(input=input_and_r_2())
    def test_black_2(self, input):
        """ Testcase for following block:
                name: filter that match some parent tags (including string, re, list, True)
                attrs: dict of multiple filters that does NOT match any parent
        """
        (start_tag_name, input_name_filter, input_attrs_filter, r_exp) = input
        tag = self.test_html_page_element.find(string=start_tag_name)
        r = tag.find_parent(name=input_name_filter, attrs=input_attrs_filter)
        r_c = r['class'][0] if not r==None else None
        self.assertEqual(r_c, r_exp)


    @composite
    def input_and_r_3(draw):
        start_tag_name = draw(sampled_from(["Elsie", "Lacie", "Tillie"]))
        num_attr = 1
        input_name_filter = draw(one_of([sampled_from(["p", "div"]),  # string filter
                                         sampled_from([re.compile("^p"), re.compile("^div")]), # re filter
                                         permutations(["p", "div"]).map(lambda x: x[:num_attr]), # list of filter
                                         sampled_from([True]), # boolean True
                                         ]))
        input_attrs_filter = {} # empty dict
        # set expected result based on attrs_filter
        if ( input_name_filter=="div" or 
             input_name_filter==re.compile("^div") or 
             (isinstance(input_name_filter,list) and "div" in input_name_filter) ):
            r_exp = "wrapper_div_2"
        elif input_name_filter==True:
            r_exp = "sister"
        else:
            r_exp = "story"

        return (start_tag_name, input_name_filter, input_attrs_filter, r_exp)
    @given(input=input_and_r_3())
    def test_black_3(self, input):
        """ Testcase for following block:
                name: filter that match some parent tags (including string, re, list, True)
                attrs: emtpy dict of filters
        """
        (start_tag_name, input_name_filter, input_attrs_filter, r_exp) = input
        tag = self.test_html_page_element.find(string=start_tag_name)
        r = tag.find_parent(name=input_name_filter, attrs=input_attrs_filter)
        r_c = r['class'][0] if not r==None else None
        self.assertEqual(r_c, r_exp)


    @composite
    def input_and_r_4(draw):
        start_tag_name = draw(sampled_from(["Elsie", "Lacie", "Tillie"]))
        num_attr = draw(sampled_from([1, 2]))        
        input_name_filter = draw(one_of([sampled_from(["p_not_exist", "div_not_exist"]),  # string filter
                                         sampled_from([re.compile("^p_not_exist"), re.compile("^div_not_exist")]), # re filter
                                         permutations(["p_not_exist", "div_not_exist"]).map(lambda x: x[:num_attr]), # list of filter
                                         ]))
        input_attrs_filter = draw(dictionaries(keys=sampled_from(["class"]), values=sampled_from(["class_not_exits"]), min_size=1))                   
        # set expected result based on attrs_filter
        r_exp = None

        return (start_tag_name, input_name_filter, input_attrs_filter, r_exp)
    @given(input=input_and_r_4())
    def test_black_4(self, input):
        """ Testcase for following block:
                name: filter that doesn't match any parent tags (including string, re, list)
                attrs: dict of multiple filters that does NOT match any parent
        """
        (start_tag_name, input_name_filter, input_attrs_filter, r_exp) = input
        tag = self.test_html_page_element.find(string=start_tag_name)
        r = tag.find_parent(name=input_name_filter, attrs=input_attrs_filter)
        r_c = r['class'][0] if not r==None else None
        self.assertEqual(r_c, r_exp)
        
        
    @composite
    def input_and_r_5(draw):
        start_tag_name = draw(sampled_from(["Elsie", "Lacie", "Tillie"]))
        num_attr = draw(sampled_from([1, 2]))        
        input_name_filter = draw(one_of([sampled_from(["p_not_exist", "div_not_exist"]),  # string filter
                                         sampled_from([re.compile("^p_not_exist"), re.compile("^div_not_exist")]), # re filter
                                         permutations(["p_not_exist", "div_not_exist"]).map(lambda x: x[:num_attr]), # list of filter
                                         # sampled_from([True]), # boolean True
                                         ]))
        input_attrs_filter = {} # empty dict
        # set expected result based on attrs_filter
        r_exp = None

        return (start_tag_name, input_name_filter, input_attrs_filter, r_exp)    
    @given(input=input_and_r_5())
    def test_black_5(self, input):
        """ Testcase for following block:
                name: filter that doesn't match any parent tags (including string, re, list)
                attrs: emtpy dict of filters
        """
        (start_tag_name, input_name_filter, input_attrs_filter, r_exp) = input
        tag = self.test_html_page_element.find(string=start_tag_name)
        r = tag.find_parent(name=input_name_filter, attrs=input_attrs_filter)
        r_c = r['class'][0] if not r==None else None
        self.assertEqual(r_c, r_exp)

    @composite
    def input_and_r_6(draw):
        start_tag_name = draw(sampled_from(["Elsie", "Lacie", "Tillie"]))       
        input_name_filter = draw(sampled_from(["", []]))
        input_attrs_filter = draw(dictionaries(keys=sampled_from(["class"]), values=sampled_from(["class_not_exits"]), min_size=1))
        # set expected result based on attrs_filter
        r_exp = None
        return (start_tag_name, input_name_filter, input_attrs_filter, r_exp)    
    @given(input=input_and_r_6())
    def test_black_6(self, input):
        """ Testcase for following block:
                name: empty filter (string, re, list)
                attrs: dict of multiple filters that does NOT match any parent
        """
        (start_tag_name, input_name_filter, input_attrs_filter, r_exp) = input
        tag = self.test_html_page_element.find(string=start_tag_name)
        r = tag.find_parent(name=input_name_filter, attrs=input_attrs_filter)
        r_c = r['class'][0] if not r==None else None
        self.assertEqual(r_c, r_exp)


    @composite
    def input_and_r_7(draw):
        start_tag_name = draw(sampled_from(["Elsie", "Lacie", "Tillie"]))       
        input_name_filter = draw(sampled_from(["", []]))
        input_attrs_filter = {} # empty dict
        # set expected result based on attrs_filter
        if input_name_filter=="": r_exp = None
        else: r_exp="sister"

        return (start_tag_name, input_name_filter, input_attrs_filter, r_exp)    
    @given(input=input_and_r_7())
    def test_black_7(self, input):
        """ Testcase for following block:
                name: empty filter (string, re, list)
                attrs: emtpy dict of filters
        """
        (start_tag_name, input_name_filter, input_attrs_filter, r_exp) = input
        tag = self.test_html_page_element.find(string=start_tag_name)
        r = tag.find_parent(name=input_name_filter, attrs=input_attrs_filter)
        r_c = r['class'][0] if not r==None else None
        self.assertEqual(r_c, r_exp)
    

if __name__ == '__main__':
    unittest.main()

