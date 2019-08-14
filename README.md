# Analyzing Individual Fairness Based on System Models

In this file, we present the artifact used in our paper. The submission includes:
* the *UMLfair profile*.
* the pseudocode of *generating temporal logic claims* from a UML model annotated with the UML profile.
* the pseudocode of *checking individual-fairness* based on the results of verifying the generated claims against the UML model from where they are generated. 
* The inputs and the outputs of applying our proposed framework on three case studies namely, the School Management System based on an artificail case study, the Delivery Management System based on the incedent describtion of [Amazon's delivery-free service](https://www.bloomberg.com/graphics/2016-amazon-same-day/), and the Loan Management System based on [business process model](https://link.springer.com/chapter/10.1007/978-3-319-92901-9_19) from an [event log](https://www.win.tue.nl/bpi/doku.php?id=2012:challenge) recording the loan management process of a Dutch financial institute. 

# Recources

* **Profile: The UMLfair Profile:**
* **Pseudocode: the pseudocode of generating temporal logic claims:**
* **Pseudocode: the pseudocode of checking individual-fairness:**
* **Artifacts: The artifacts of the school management system case study:** https://figshare.com/s/c9812d35226244625436
* **Artifacts: The artifacts of the delivery management system case study:**
* **Artifacts: The artifacts of the loan management system case study:**

The artifacts of each each case study contains: 
* A (*.uml*) file: the UML model of the system annotated with the UMLfair profile.
* A (*.xlsx*) file: the dataset of the system which used to uncover proxies for protected data. 
* a (.pml) file: the result of transforming the UML into PROMELA by using the [Hugo/RT](https://www.informatik.uni-augsburg.de/en/chairs/swt/sse/hugort/) tool. 
* a (*.pdf*) file: provides the generated batches of claims together with their verifications results. The verifiaction results are the output of  the [SPIN](http://spinroot.com/spin/whatispin.html) model checker. 
* a (*.trail*) file: a counterexample generated by the [SPIN](http://spinroot.com/spin/whatispin.html) model checker that explain one of the violated claims in the (*.pdf*) file.
