import csv
import xml.etree.ElementTree as ET
from pprint import pprint
from boolean_parser import parse
import itertools
import random
from tabulate import tabulate


class Parserr:
    __author__ = "SFAT"
    '''
    
    This class defines a parser that parses XML documents generated by papyrus to generate initializations for the data attributes

    ...
    Attributes
    ----------
    xml : str
        The path to the xml file that contains the UML Model
    tree : xml.etree.ElementTree
        The ElementTree object obtained from the XML file
    '''

    def __init__(self, xml):
        '''
        Class constructor

        Parameters
        ----------
        xml : str
            The file path to the XML document

        '''

        self.number_of_inis = None
        self.xml = xml
        self.tree = ET.parse(self.xml)

    def get_root_element(self):
        '''
        Finds and returns root element of ElementTree

        Returns
        -------

        xml.etree.ElementTree.ElementTree:
            root element of ElementTree
        '''
        return self.tree.getroot()

    def find_all(self, query, namespaces=None, element=None):
        '''
        Queries the root element for a query string

        :param query: Query string
        :type query: str
        :param namespaces: dictionary of namespaces in the XML document
        :type namespaces: dict
        :param element The element that should be searched
        :type  xml.etree.ElementTree.Element
        :return: A list of all elements matching the search query
        :rtype: list[xml.etree.ElementTree.Element]
        '''

        if element!=None:
            return element.findall(query, namespaces)
        return self.get_root_element().findall(query, namespaces)

    def find(self, query, namespaces=None, element=None):
        '''

        :param query: Query string
        :type query: str
        :param namespaces: dictionary of namespaces in the XML document
        :type namespaces: dict
        :param element The element that should be searched
        :type element: xml.etree.ElementTree.Element
        :return: The element matching the search query
        :rtype: xml.etree.ElementTree.Element
        '''

        if element!=None:
            return element.find(query, namespaces)
        return self.get_root_element().find(query, namespaces)

    def get_uml_fairnes_criticals(self):
        '''
        Finds the UML critical element

        :return: UML critical element
        :rtype: [xml.etree.ElementTree.Element]
        '''

        return self.find_all(".//UMLFairness:critical", self.namespace())

    def get_all_attibutes(self, element=None):
        '''
        Gets all attributes
        :param element The element that should be searched
        :type element: xml.etree.ElementTree.Element
        :return: A list of all attributes
        :rtype: list[xml.etree.ElementTree.Element]
        '''

        if element != None:
            return element.findall(".//ownedAttribute")

        return self.find_all(".//ownedAttribute")

    def get_attributes(self, element=None):
        '''
        Finds all the attributes in the Element Tree that are part of a critical annotation
        :return: A list of attributes
        :rtype:list[xml.etree.ElementTree]
        '''

        if element != None:
            all_attributes = self.find_all(".//ownedAttribute", element=element)
        else:
            all_attributes = self.find_all(".//ownedAttribute")
        normal_attributes = []
        for attribute in all_attributes:
            if attribute.get("isDerived") != 'true':
               normal_attributes.append(attribute)
        return normal_attributes

    def get_derived_attributes(self, element=None):
        '''
        Finds all derived attributes

        :return: A list of all derived attributes
        :rtype:list[xml.etree.ElementTree]
        '''

        if element != None:
            return self.find_all(query=".//ownedAttribute[@isDerived='true']", element=element)
        return self.find_all(".//ownedAttribute[@isDerived='true']")

    def get_guards(self, element=None):
        '''
        Finds all the guards in an the root element

        :return: A list of all Guards
        :rtype:list[xml.etree.ElementTree]
        '''

        if element!=None:
            # Hypothesis - guard IDs are present in transitions as attributes
            transitions_with_guards = self.find_all(query=".//transition[@guard]", element=element)
            return [x.find(f".//ownedRule[@xmi:id='{x.get('guard')}']", self.namespace()) for x in
                    transitions_with_guards]
        # Hypothesis - guard IDs are present in transitions as attributes
        transitions_with_guards = self.find_all(".//transition[@guard]")
        return [x.find(f".//ownedRule[@xmi:id='{x.get('guard')}']", self.namespace()) for x in transitions_with_guards]

    def get_type(self, type_id):
        '''
        Finds the datatype of an attribute given the ID of the datatype

        :param type_id: ID of type
        :type type_id: str
        :return: The id element
        :rtype:list[xml.etree.ElementTree]
        '''
        return self.find(f".//packagedElement[@xmi:id='{type_id}']", self.namespace())


    def get_attrib_default_vals(self, derived_attribute):
        '''
        Finds the default value of an attribute

        Parameters
        ----------
        derived_attribute : xml.etree.ElementTree.Element
            A derived attribute

        Returns
        -------
        str:
            default value an attribute
        '''

        if (derived_attribute.get("isDerived") != "true"):
            return None
        default = derived_attribute.find(".//defaultValue")
        try:
            return default.get("name")
        except:
            return None

    def namespace(self):
        '''
        Finds all namespaces contained in the XML document

        :return: A dictionary with all the namespaces contained in the XML document
        :rtype: dict
        '''
        my_namespaces = dict([
            node for _, node in ET.iterparse(
            self.xml, events = ['start-ns']
            )
        ])
        return my_namespaces

    def isDerived(self, attribute):
        '''
        Checks whether and attribute is derived or not

        :param attribute: An attribute
        :type attribute: xml.etree.ElementTree
        :return: Returns True if the an attribute is a derived attribute. Returns False otherwise
        :rtype: bool
        '''

        if attribute.get("isDerived") != 'true':
            return True
        return False

    def get_guard_names(self, packagedElement=None):
        '''
        Gets the name of all guards (ownedRule elements)

        :return: A list containing the name attribute of all guards (ownedRule elements)
        :rtype: list[str]
        '''
        try:
            return [name.replace('&&', 'AND') for name in [guard.get("name") for guard in self.get_guards(element=packagedElement)]]
        except:
            return []

    def get_parsed_guard_conditions(self, packagedElement=None):
        '''
        Parses the names or condition strings of all gaurds (ownedRule elements)

        :return: A list of conditions
        :rtype: [boolean_parser.parsers.sqla.SQLACondition]
        '''
        parsed_guard_conditions = []
        for x in self.get_guard_names(packagedElement=packagedElement):
            try:
                x_parsed = parse(x)
                parsed_guard_conditions.append(x_parsed)
            except:
                continue
        return parsed_guard_conditions

    def get_guard_conditions_that_have_attributes(self, attributes=None, packagedElement=None):
        '''
        Gets all guard conditions that have an attribute or a derived attribute

        :param attributes: A list of attributes
        :type attributes: list[xml.etree.ElementTree]
        :return: A list of conditions
        :rtype: [boolean_parser.parsers.sqla.SQLACondition]
        '''
        list_of_attribute_names = [x.get("name") for x in attributes]
        condition_data = []
        for x in self.get_parsed_guard_conditions(packagedElement=packagedElement):
            try:
                if x.data['parameter'] in list_of_attribute_names:
                    condition_data.append(x.data)
            except:
                try:
                    for i in x.conditions:
                        if i.data['parameter'] in list_of_attribute_names:
                            condition_data.append(i.data)
                except:
                    # Check for a better idea
                    continue
        return condition_data

    def protected_characteristics(self):
        '''
        Gets protected data
        :return: Protected characteristics
        :rtype: xml.etree.ElementTree
        '''
        results = []

        criticals = self.find_all(query=".//UMLFairness:critical", namespaces=self.namespace())
        for critical in criticals:
            base_StructuredClassifier = critical.get("base_StructuredClassifier")
            parent_class_name = self.find(query=f".//packagedElement[@xmi:id='{base_StructuredClassifier}']", namespaces=self.namespace()).get('name')
            protected_chars = critical.find(".//protectedData").text

            disallowed_characters = "()"

            for character in disallowed_characters:
                try:
                    protected_chars = protected_chars.replace(character, "")
                except:
                    continue
            try:

                protected_chars = list(protected_chars.split(","))
            except:
                protected_chars = None

            protected_chars = [parent_class_name + "_" + x for x in protected_chars]

            results = results + protected_chars

        return results
        # protected_chars =  self.find_all(".//protectedData")

    def generate_initializations(self):
        '''
        Generates innitializations

        :return: void
        '''

        # Getting a list of packagedElement

        packagedElements = self.find_all(".//packagedElement")
        guard_conditions_with_attributes_and_class = []
        guard_conditions_with_derived_attributes_and_class = []

        # Looping through packagedElements to get conditions
        for i in packagedElements:

            # Getting guard conditions for class attributes (non-derived attributes)
            guard_conditions_with_attributes = self.get_guard_conditions_that_have_attributes(self.get_attributes(element=i))
            guard_conditions_with_attributes = list(map(dict, set(tuple(sorted(d.items())) for d in guard_conditions_with_attributes)))

            # Adding class name to list of guard conditions for non-derived attributes
            for j in guard_conditions_with_attributes:
                if type(j) == dict:
                    # Adding class name to conditions
                    j["class_name"] = i.get("name")
                    # j["type"] = type(json.load(j["value"]))
                    j['default'] = self.get_attrib_default_vals(self.find(query=f".//ownedAttribute[@name='{j['parameter']}']", element=i))

                    j['type'] = self.get_type(self.find(query=f".//ownedAttribute[@name='{j['parameter']}']",element=i).get("type")).get("name")
                    guard_conditions_with_attributes_and_class.append(j)

            # Getting guard conditions for derived class attributes
            guard_conditions_with_derived_attributes = self.get_guard_conditions_that_have_attributes(
                self.get_derived_attributes(element=i))
            guard_conditions_with_derived_attributes = list(map(dict, set(tuple(sorted(d.items())) for d in guard_conditions_with_derived_attributes)))
            for j in guard_conditions_with_derived_attributes:
                if type(j) == dict:
                    # Adding class name to conditions
                    j["class_name"] = i.get("name")
                    j['default'] = self.get_attrib_default_vals(self.find(query=f".//ownedAttribute[@name='{j['parameter']}']", element=i))
                    j['type'] = self.get_type(
                        self.find(query=f".//ownedAttribute[@name='{j['parameter']}']", element=i).get("type")).get(
                        "name")
                    guard_conditions_with_derived_attributes_and_class.append(j)

        guard_conditions_with_attributes_and_class = list(map(dict, set(tuple(sorted(d.items())) for d in guard_conditions_with_attributes_and_class)))


        guard_conditions_with_attributes_and_class = self.filterListOfDictionaries(guard_conditions_with_attributes_and_class)

        guard_conditions_with_derived_attributes_and_class = list(map(dict, set(tuple(sorted(d.items())) for d in guard_conditions_with_derived_attributes_and_class)))
        guard_conditions_with_derived_attributes_and_class = self.filterListOfDictionaries(guard_conditions_with_derived_attributes_and_class)



        # Default values for attributes attributes
        default_vals_for_derived_attributes = {
            "boolean": [False],
            'int': [0]
        }
        # Default values for attributes
        default_vals_for_attributes = {
            "int": lambda x: [
            random.randint(int(x) - int(x), int(x) - 1),
            random.randint(int(x), int(x) + int(x))
        ],
            "boolean": lambda x=None: [True, False]
         }
        itertool_params = []
        column_names = []
        # getting list of possible values for derived attributes
        for x in guard_conditions_with_derived_attributes_and_class:
            if x["default"] is None:
                itertool_params.append(default_vals_for_derived_attributes[x['type']])
                column_names.append(x['class_name'] + '_' + x['parameter'])
            else:
                itertool_params.append([x["default"]])
                column_names.append(x['class_name'] + '_' + x['parameter'])

        # getting list of possible values for attributes
        for x in guard_conditions_with_attributes_and_class:
            if x["default"] is None:
                if x['class_name'] + '_' + x['parameter'] in column_names:
                    index = column_names.index(x['class_name'] + '_' + x['parameter'])
                    old = itertool_params[index]
                    new = default_vals_for_attributes[x['type']](x['value'])
                    final = old + new
                    itertool_params[index] = final
                else:
                    itertool_params.append(default_vals_for_attributes[x['type']](x['value']))

                column_names.append(x['class_name'] + '_' + x['parameter'])
            else:
                itertool_params.append([x["default"]])
                column_names.append(x['class_name'] + '_' + x['parameter'])

        # Generating a truth table from the conditions
        table = list(itertools.product(*itertool_params))

        # Generating Innitialization IDs
        innitialization_ids = [x for x in range(0, len(table))]
        self.number_of_inis = len(table)

        # Adding Innitialization IDs column
        column_names.insert(0, "__Ini_ID")
        table = [tuple([str(y)] + list(x)) for x, y in zip(table, innitialization_ids)]

        # Adding column names to data
        table.insert(0, (*column_names,))

        # printing the table
        print(tabulate(table))

        with open('initializations_table.csv', 'w',newline='') as f:
            # using csv.writer method from CSV package
            write = csv.writer(f)
            write.writerows(table)

        prepended_protected_characteristics = self.protected_characteristics()

        with open('protected_characteristics.csv', 'w',newline='') as f:
            # using csv.writer method from CSV package
            write = csv.writer(f)
            write.writerow(prepended_protected_characteristics)

        print("------Protected characteristics------")
        pprint(prepended_protected_characteristics)

        # ---------- Saving Datatypes to CSV ------------- #
        guard_conditions = guard_conditions_with_attributes_and_class+guard_conditions_with_derived_attributes_and_class
        data_types = [[x['class_name'] + '_' + x['parameter'], x['type']] for x in guard_conditions]
        pprint(data_types)
        with open('attributes_data_types.csv', 'w',newline='') as f:
            # using csv.writer method from CSV package
            write = csv.writer(f)
            write.writerows(data_types)

        # __________ Saving Class Names to CSV ------------- #
        class_names = [x['class_name'] for x in guard_conditions]
        class_names = list(set(class_names))
        pprint(class_names)

        with open('class_names.csv', 'w',newline='') as f:
            # using csv.writer method from CSV package
            write = csv.writer(f)
            write.writerow(class_names)

        # saving decision data attributes
        try:
            self.get_decision_data_attributes()
        except Exception:
            print("")

    def filterListOfDictionaries(self, dictionary):
        existing_dicts = set()
        filtered_list = []
        for d in dictionary:
            if (d['class_name'], d['parameter']) not in existing_dicts:
                existing_dicts.add((d['class_name'], d['parameter']))
                filtered_list.append(d)
        return filtered_list

    def get_decision_data_attributes(self):
        # get the xml element sensitiveDecisions
        # loop through the list of obtained attributes and try to find the class to which it belongs.
        # if a class is found, append the class_name. If no class is found return the attribute as it is
        try:

            decision_data_attribs = self.find(query=".//sensitiveDecisions", namespaces=self.namespace()).text
            disallowed_characters = "() "

            for character in disallowed_characters:
                decision_data_attribs = decision_data_attribs.replace(character, "")

            decision_data_attribs = list(decision_data_attribs.split(","))

            packagedElement = self.find_all(".//packagedElement")
            # get the class of the decision_data_attributes

            prepended_decision_data_attribs = []
            decision_attribs_data_types = []
            for i in packagedElement:
                attributes = self.get_all_attibutes(i)
                for j in attributes:
                    if j.get("name") in decision_data_attribs:
                        prepended_decision_data_attribs.append(i.get("name") + '_' + j.get("name"))
                        decision_attribs_data_types.append([i.get("name") + '_' + j.get("name"), self.get_type(j.get("type")).get("name")])

            with open('decision_data_attribs.csv', 'w',newline='') as f:
                # using csv.writer method from CSV package
                write = csv.writer(f)
                write.writerow(prepended_decision_data_attribs)

            with open('decision_data_attribs_types.csv', 'w', newline='') as f:
                # using csv.writer method from CSV package
                write = csv.writer(f)
                write.writerows(decision_attribs_data_types)
            print("Decision Data Attributes:")
            pprint(decision_attribs_data_types)
            return prepended_decision_data_attribs
        except Exception:
            return None
            # return self.namespace()
    def number_of_xml_tags(self):
        return len(list(self.get_root_element().findall(".//*", self.namespace())))
    def number_of_annotated_elements(self):
        return len(self.get_uml_fairnes_criticals())
