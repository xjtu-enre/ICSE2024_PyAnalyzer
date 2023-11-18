## Relation: Define
A entity `A` define another entity `B` when `B` is created in `A`'s namespace.


### Supported Patterns
```yaml
name: Define
```

#### Semantic: 

##### Examples
###### Module Level Definition
```python
//// test_module_level_define.py

class Base:


    ...
class Inherit(Base):



    ...
def func1():


    return 0
x = 1


y: int = 1


t1, t2 = 1, 2




(t3 := 1)
```

```yaml
name: ModuleLevelDefine
relation:
  type: Define
  extra: false
  items:
  - to: Class:'test_module_level_define.Base'
    loc: '2:6'
    from: Module:'test_module_level_define'
  - to: Class:'test_module_level_define.Inherit'
    loc: '6:6'
    from: Module:'test_module_level_define'
  - to: Function:'test_module_level_define.func1'
    loc: '11:4'
    from: Module:'test_module_level_define'
  - to: Variable:'test_module_level_define.x'
    loc: '15:0'
    from: Module:'test_module_level_define'
  - to: Variable:'test_module_level_define.y'
    loc: '18:0'
    from: Module:'test_module_level_define'
  - to: Variable:'test_module_level_define.t1'
    loc: '21:0'
    from: Module:'test_module_level_define'
  - to: Variable:'test_module_level_define.t2'
    loc: '21:4'
    from: Module:'test_module_level_define'
  - to: Variable:'test_module_level_define.t3'
    loc: '26:1'
    from: Module:'test_module_level_define'
```


###### Local Definition

```python
//// test_nested_define.py

def func():


    def inner():


        def inner_inner():


            func()

        func()


        inner_inner()

    inner()

def func2():

    x = 1


    y: int = 1


    t1, t2 = 1, 2




    (t3 := 1)


```

```yaml
name: LocalDefinition
relation:
  type: Define
  extra: false
  items:
  - to: Function:'test_nested_define.func.inner'
    loc: '5:8'
    from: Function:'test_nested_define.func'
  - to: Function:'test_nested_define.func.inner.inner_inner'
    loc: '8:12'
    from: Function:'test_nested_define.func.inner'
  - to: Function:'test_nested_define.func2'
    loc: '20:4'
    from: Module:'test_nested_define'
  - to: Variable:'test_nested_define.func2.x'
    loc: '22:4'
    from: Function:'test_nested_define.func2'
  - to: Variable:'test_nested_define.func2.y'
    loc: '25:4'
    from: Function:'test_nested_define.func2'
  - to: Variable:'test_nested_define.func2.t1'
    loc: '28:4'
    from: Function:'test_nested_define.func2'
  - to: Variable:'test_nested_define.func2.t2'
    loc: '28:8'
    from: Function:'test_nested_define.func2'
  - to: Variable:'test_nested_define.func2.t3'
    loc: '33:5'
    from: Function:'test_nested_define.func2'
    
    # define but not LocalDefinition
  - to: Function:'test_nested_define.func'
    loc: '2:4'
    from: Module:'test_nested_define'
```


###### Parameter Definition

```python
//// test_parameter_define.py

def func(x0, y0, z0):


    def inner(x0, y0, z0):


        def inner_inner(x0, y0, z0):
            ...
        ...
    ...

```

```yaml
name: ParameterDefinition
relation:
  type: Define
  extra: false
  items:
  - type: Define
    to: Parameter:'test_parameter_define.func.x0'
    from: Function:'test_parameter_define.func'
    loc: '2:9'
  - type: Define
    to: Parameter:'test_parameter_define.func.y0'
    from: Function:'test_parameter_define.func'
    loc: '2:13'
  - type: Define
    to: Parameter:'test_parameter_define.func.z0'
    from: Function:'test_parameter_define.func'
    loc: '2:17'
  - type: Define
    to: Parameter:'test_parameter_define.func.inner.x0'
    from: Function:'test_parameter_define.func.inner'
    loc: '5:14'
  - type: Define
    to: Parameter:'test_parameter_define.func.inner.y0'
    from: Function:'test_parameter_define.func.inner'
    loc: '5:18'
  - type: Define
    to: Parameter:'test_parameter_define.func.inner.z0'
    from: Function:'test_parameter_define.func.inner'
    loc: '5:22'
  - type: Define
    to: Parameter:'test_parameter_define.func.inner.inner_inner.x0'
    from: Function:'test_parameter_define.func.inner.inner_inner'
    loc: '8:24'
  - type: Define
    to: Parameter:'test_parameter_define.func.inner.inner_inner.y0'
    from: Function:'test_parameter_define.func.inner.inner_inner'
    loc: '8:28'
  - type: Define
    to: Parameter:'test_parameter_define.func.inner.inner_inner.z0'
    from: Function:'test_parameter_define.func.inner.inner_inner'
    loc: '8:32'
    
    # define but not ParameterDefinition
  - type: Define
    to: Function:'test_parameter_define.func'
    from: Module:'test_parameter_define'
    loc: '2:4'
  - type: Define
    to: Function:'test_parameter_define.func.inner'
    from: Function:'test_parameter_define.func'
    loc: '5:8'
  - type: Define
    to: Function:'test_parameter_define.func.inner.inner_inner'
    from: Function:'test_parameter_define.func.inner'
    loc: '8:12'
```

###### Static Class Attribute Definition
```python
//// test_static_class_attribute.py
class Base:
    attribute_a = 1
    attribute_b: int
    attribute_c, attribute_d = 1, 2 
    def __init__(self):
        self.attribute_x = 1
class Inherit(Base):
    attribute_e = 1
    def __init__(self):
        super().__init__()        
        self.attribute_f = 1
```

```yaml
name: StaticClassAttributeDefinition
relation:
  type: Define
  extra: false
  items:
  - to: Attribute:'test_static_class_attribute.Base.attribute_a'
    from: Class:'test_static_class_attribute.Base'
    type: Define
    loc: '2:4'
  - type: Define
    from: Class:'test_static_class_attribute.Base'
    to: Attribute:'test_static_class_attribute.Base.attribute_b'
    loc: '3:4'
  - type: Define
    to: Attribute:'test_static_class_attribute.Base.attribute_c'
    from: Class:'test_static_class_attribute.Base'
    loc: '4:4'
  - type: Define
    to: Attribute:'test_static_class_attribute.Base.attribute_d'
    from: Class:'test_static_class_attribute.Base'
    loc: '4:17'
  - type: Define
    to: Attribute:'test_static_class_attribute.Base.attribute_x'
    from: Function:'test_static_class_attribute.Base.__init__'
    loc: '6:13'
  - type: Define
    to: Attribute:'test_static_class_attribute.Inherit.attribute_e'
    from: Class:'test_static_class_attribute.Inherit'
    loc: '8:4'
  - type: Define
    to: Attribute:'test_static_class_attribute.Inherit.attribute_f'
    from: Function:'test_static_class_attribute.Inherit.__init__'
    loc: '11:13'
    
    # define but not StaticClassAttributeDefinition
  - type: Define
    to: Class:'test_static_class_attribute.Base'
    from: Module:'test_static_class_attribute'
    loc: '1:6'
  - type: Define
    to: Function:'test_static_class_attribute.Base.__init__'
    from: Class:'test_static_class_attribute.Base'
    loc: '5:8'
  - type: Define
    to: Class:'test_static_class_attribute.Inherit'
    from: Module:'test_static_class_attribute'
    loc: '7:6'
  - type: Define
    to: Function:'test_static_class_attribute.Inherit.__init__'
    from: Class:'test_static_class_attribute.Inherit'
    loc: '9:8'
  - type: Define
    to: Parameter:'test_static_class_attribute.Base.__init__.self'
    from: Function:'test_static_class_attribute.Base.__init__'
    loc: '5:17'
  - type: Define
    to: Parameter:'test_static_class_attribute.Inherit.__init__.self'
    from: Function:'test_static_class_attribute.Inherit.__init__'
    loc: '9:17'
```


###### Anonymous Function Definition
```python
//// test_define_anonymous.py
lambda :None

def foo():
    lambda :None

class ClassA:
    lambda : None
```

```yaml
name: AnonymousFunctionDefinition
relation:
  type: Define
  extra: false
  items:
  - type: Define
    to: AnonymousFunction:'<Anonymous as="Function">'[@loc=1]
    from: Module:'test_define_anonymous'
    loc: '1:0'
  - type: Define
    to: AnonymousFunction:'<Anonymous as="Function">'[@loc=4]
    from: Function:'test_define_anonymous.foo'
    loc: '4:4'
  - type: Define
    to: AnonymousFunction:'<Anonymous as="Function">'[@loc=7]
    from: Class:'test_define_anonymous.ClassA'
    loc: '7:4'
    
    # define but not AnonymousFunctionDefinition
  - type: Define
    to: Function:'test_define_anonymous.foo'
    from: Module:'test_define_anonymous'
    loc: '3:4'
  - type: Define
    to: Class:'test_define_anonymous.ClassA'
    from: Module:'test_define_anonymous'
    loc: '6:6'
```

### Properties

| Name | Description | Type | Default |
|---|---|:---:|:---:|