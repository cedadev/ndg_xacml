ndg_xacml
=========
XACML 2.0 implementation for CEDA (the Centre for Environmental Data Analysis) 
STFC, Rutherford Appleton Laboratory.  This is follow on work from the NERC 
(Natural Environment Research Council) DataGrid 3 Project.

XACML (eXtensible Access Control Mark-up Language), is an XML based language for
expressing access control policies.

See: http://www.oasis-open.org/committees/xacml/

Release 0.5.2
-------------
 * Fix for test_pdp with SubjectMatch semantics - ALL values must match
   within a `<SubjectMatch/>` element for a rule match
   
Release 0.5.1
-------------
 * Added MANIFEST.in to fix missing policy files in test area
 * fixed epydoc mark-up

Release 0.5.0
-------------
Major enhancements including additional language features and support for `lxml`:

 * Optional support for `lxml` as alternative to `ElementTree` - gives better Xpath support
 * Added concatenate functions and custom functions for URL encoding and MD5 hash custom functions.
 * Added support for language features:
   - for SAML 2.0 profile of XACML v2.0 (http://docs.oasis-open.org/xacml/2.0/access_control-xacml-2.0-saml-profile-spec-os.pdf)
   - AttributeSelectors
   - PolicySets. 
   - first-applicable rule combining algorithm
   - Incorporated NOT and modified AND functions (from Prashant Kediyal). 
 * Support for adding custom functions with `ndg.xacml.core.functions.FunctionMap.load_custom_function`
 * Fix for ticket:1130 and related bug
  - In `ndg.xacml.core.target.Target._matchChild`, all SubjectMatches within a 
  Subject must evaluate to true for an overall match for the Subject (and 
  similarly for Resource, Action and Environment).
  - In `ndg.xacml.core.match.MatchBase`, matching of the attribute value for a 
  `SubjectMatch` with any of the values for the selected attribute of the Subject 
  should result in an overall match (and similarly for Resource, Action and 
  Environment).

Release 0.4.0
-------------
Added support for custom DataTypes and functions. e.g.
```
        # Add attribute value type
        AttributeValueClassFactory.addClass('<my new type uri', 
                                            MyAttributeValueClass)
        
        # ...and new parser for this type
        DataTypeReaderClassFactory.addReader('<my new type uri', 
                                             ETreeMyDataTypeReaderClass)
        
        # Add new function
        functionMap['<my function type uri'] = MyNewFunctionClass
```

Release 0.3
-----------
Includes important fixes for equals functions, and improvement to at least one
member functions.  Unit tests improved with wider coverage of different rule
definitions and example request contexts.

Improved and added to support for context handler and Policy Information Point
interfaces including the ability for the PDP to call back to a PIP via a 
Context handler to retrieve additional subject attributes.

Release 0.2
-----------
Only the parts of the specification immediately required for CEDA have been 
implemented in this initial release:
 Policy Decision Point;
 Deny overrides and Permit overrides rule combining algorithms;
 AttributeDesignators;
 various function types: see `ndg.xacml.core.functions`;
 and attribute types: see `ndg.xacml.core.attribute`;
 incomplete support for `<AttributeSelector/>`s, `<VariableReference/>`, 
 `<VariableDefinition/>`. `<Obligations/>`;
 includes an ElementTree based parser for Policies. No support for writing
 out policies or read/write of XML representation of `<Request/>` and `<Response/>`;
   
See `ndg.xacml.test` for unit tests and examples.

The software follows a modular structure to allow it to be extended easily to 
include new parsers, functions and attribute types 
