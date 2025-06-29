- Research Computing Certificate info session announcement - the 6th, RSVP for
  Lunch

Revisit classes from last time

- Examples of classes using undataclass website
- Mention match_args being added in 3.10, getting it for free just using
  dataclasses (forgot to do this)
- Show rich pretty printing
- Show cattrs usage - modular, separation of concerns (API structure vs. data
  conversion)
  - We could write a different converter for a different source or target!

Design patterns in OOP

- See class notes for some definitions, read on your own - didn't really cover
  in class except inline as we went.
- Why design classes?
  - Modular - not going to give this one up!
  - Can make an API easy to use correctly - hard to use incorrectly
  - Keep values & data together & organized (there's a ~256 or so parameter
    limit in C! I met someone who discovered that first hand.)
  - DRY code
- Two patterns for making classes
  - Inheritance - "is a" & code reuse - spaghetti code warning!
  - Composition - "has a" & restrict interface (you can't delete attributes with
    ) - verbose!
- UML diagrams
  - Can show classes, interface, relationships
  - Several links to read more if interested

- OOP Pattern 1: code injection
  - You can replace steps in a calculation via inheritance and overriding

- OOP Pattern 2: Required interface (ABCs)
  - You can require an implementation to implement certain methods - called
    "abstract" (italics on a UML diagram)
  - Example: `content/week03/geom_example`
  - We did the dataclasses version in class (voted)
  - Example: `content/week03/integrator_example` (also in rendered notes)

- SOLID:
  - S: modular
  - O: Open/closed API
  - Liskov substitution principle (like adding `power=` to `Geometry.area` but
    not the subclasses overrides)
  - I: Interfaces
  - D: Dependency inversion (low level depend on high level)

- OOP Pattern 3: Functors
  - Not very native in Python, but common in some languages like C++
  - Can implement with function capture instead of classes

- Separation of concerns
  - Some languages have techniques like multifile classes
  - Other ways to achieve, like mixins, dispatch (later), etc

- OOP Pattern 4: eDSLs
  - Example with Path using division for joining

- OOP Pattern 5: Mixins
  - Example using Path mixin to build separately
  - Follow rules when using Mixins to avoid multiple inheritance pitfalls!
    - No constructor
    - No overloading
    - No members, just methods
    - Later (static typing) we'll see Protocols which help too
