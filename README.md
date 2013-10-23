Qt Model Generator
==================

This is a tool designed for helping people to create Qt Models. All the Q_PROPERTY code is generated based on a json description file.

Why use it?
-----------
For avoiding the repeatable fact of coding the Qt Models and its properties all the time we need it.

How to use?
-----------
The user needs to execute two steps:
- Create a json file that describes all the model's properties;
- Run the tool using the json description files.

Bellow you can see an example of a model. We are modelling a hipotetical person.

```json
{
	"name": "Person",
	"properties" : [
		{"name": "name", "type": "QString", "operations": "rwn"},
		{"name": "Age", "type": "int", "operations": "nwr"},
		{"name": "id", "type": "double", "operations": "r"},
		{"name": "children", "type": "QList<Person*> *", "operations": "rwnf"}
    ]
}
````
The json file contais the Model and Property entities. They have following fields:

#####Model
- **name** - name of the model;
- **properties** - a list of properties ([Property...])

#####Property
- **name** - name of the property;
- **type** - type of the property; 
- **operations** - the related property's operations. It should be a composition of the following characters: r - READ, w - WRITE, n - NOTIFY, and f - FINAL.
For example: ..."operations": "rn"... it rely on the fact that the generated property will have the READ and NOTIFY operations. The ordering is not important.

Available commands
------------------
You can see usage tips just typing the following command on terminal: 
```sh
> python qtmodelgen.py -h
usage: qtmodelgen.py [-h] [-o OUTPUT_FOLDER]
                     json_description_file [json_description_file ...]

This is a tool designed for helping you to gen models based on json
description files.

positional arguments:
  json_description_file
                        These are the files used as base for generating the
                        desired models.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_FOLDER, --output-folder OUTPUT_FOLDER
                        The destiny FOLDER (NOT FILE) for all generated
                        models.
```

For generating the code for the PersonModel.json already described, you have to type:
```sh
> python qtmodelgen.py PersonModel.json 
Generating code for: Person.hpp...[OK]
```
Done! Your brand new model was generated successfully! Bellow, you the result:

```c++

/*
 * Person.hpp
 *
 *  Created on:
 *      Author:
 */

#ifndef PERSON_H
#define PERSON_H

#include <QObject>

class Person: public QObject {
    Q_OBJECT
    Q_PROPERTY(QString name READ name WRITE setName NOTIFY nameChanged)
    Q_PROPERTY(int Age READ Age WRITE setAge NOTIFY AgeChanged)
    Q_PROPERTY(double id READ id)
    Q_PROPERTY(QList<Person*> * children READ children WRITE setChildren NOTIFY childrenChanged FINAL)

public:
    Person(QObject * parent) : QObject(parent) {}
    QString name() {
        return m_name;
    }
    void setName(QString newName){
        if(m_name != newName) {
            m_name = newName;
            emit nameChanged();
        }
    }
    int Age() {
        return m_Age;
    }
    void setAge(int newAge){
        if(m_Age != newAge) {
            m_Age = newAge;
            emit AgeChanged();
        }
    }
    double id() {
        return m_id;
    }
    void setId(double newId){
        if(m_id != newId) {
            m_id = newId;
        }
    }
    QList<Person*> * children() {
        return m_children;
    }
    void setChildren(QList<Person*> * newChildren){
        if(m_children != newChildren) {
            m_children = newChildren;
            emit childrenChanged();
        }
    }

signals:
    void nameChanged();
    void AgeChanged();
    void childrenChanged();

private:
    QString m_name;
    int m_Age;
    double m_id;
    QList<Person*> * m_children;

};

#endif /* PERSON_H */
```


You also can run the tools for several models at the same time. The command should be like:

```sh
> python qtmodelgen.py PersonModel.json AnimalModel.json CarModel.json
Generating code for: Person.hpp...[OK]
Generating code for: Animal.hpp...[OK]
Generating code for: Car.h.hpp..[OK]
```
Known limitation
----------------
* The includes are not performed automatically. You still need to do all includes for each model file;
* All the generated methods are inline. There are no cpp files, just the hpp;
* There are no garantees for running this using Python 3.x. I've tested with Python2.7.4 and GCC version 4.2.1.

Contact
-------
Rodrigo Peixoto - rpeixoto@blackberry.com

**BlackBerry** Application Development Consultant 

Importante note
================
This is **NOT** an official BlackBerry tool and there is no plan to provide support or updates. Use it at your own risk.



License
-------

LGPL v3

Copyright © 2007 Free Software Foundation, Inc. <http://fsf.org/>
