# Analyzing Individual Fairness Based on System Models

In this file, we present the artifact used in our paper. The submission includes our proposed UMLfair profile and three UML models annotated with the UMLfair profile. The UML models represent three systems namely, the School Management System based on an artificail case study, the Delivery Management System based on the incedent describtion of [Amazon's delivery-free service](https://www.bloomberg.com/graphics/2016-amazon-same-day/), and the Loan Management System based on [business process model](https://link.springer.com/chapter/10.1007/978-3-319-92901-9_19) from an [event log](https://www.win.tue.nl/bpi/doku.php?id=2012:challenge) recording the loan management process of a Dutch financial institute. 

In addition to the UML models, we provide a data table that represents the source of the data in each system model. The data tables of the school and the delivery systems are contains artificial data while the data table of the loan management system is derived from the [Statlog German Credit](https://archive.ics.uci.edu/ml/datasets/statlog+(german+credit+data)) dataset. As a result of appying our individual-fairness analysis framework in each case study, the followings files are generated: 
* a file contains PROMELA specifications that represents the result of transforming a UML model into formal specifications, using [Hugo/RT](https://www.informatik.uni-augsburg.de/en/chairs/swt/sse/hugort/).
* a file incudles the generated baches of temporal logic claims, based on a system model and its data table. 
* a file contains the results of verifying the generated claims against the PROMELA specifications of a system model by using the [SPIN](http://spinroot.com/spin/whatispin.html) model checker.


# The artifacts of the school management system: 

* [The UML model of the school system] 
* [The dataset of the school system] 
* [The school system model in PROMELA]
* [The generated batches of claims together with their verifications results]
