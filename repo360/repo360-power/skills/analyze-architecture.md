# Analyze Architecture Skill

## Purpose
Evaluate software architecture, identify design patterns, analyze dependencies, and assess structural quality.

## Analysis Areas

### 1. Architecture Pattern Detection
- Layered (Presentation, Business, Data)
- Microservices
- Clean Architecture / Hexagonal
- MVC / MVVM
- Event-Driven
- CQRS

### 2. Dependency Analysis
- Build dependency graph
- Detect circular dependencies
- Calculate coupling metrics
- Identify dependency violations

### 3. Design Patterns
- Creational (Singleton, Factory, Builder)
- Structural (Adapter, Facade, Proxy)
- Behavioral (Strategy, Observer, Command)
- Anti-patterns (God Object, Spaghetti Code)

### 4. SOLID Principles
- Single Responsibility
- Open/Closed
- Liskov Substitution
- Interface Segregation
- Dependency Inversion

### 5. Metrics
- Instability: I = Ce / (Ca + Ce)
- Abstractness: A = Abstract / Total
- Distance from Main Sequence: |A + I - 1|
- Coupling Between Objects
- Lack of Cohesion

## Process

1. Map directory structure and identify layers
2. Parse imports/dependencies
3. Build component graph
4. Detect patterns and anti-patterns
5. Calculate metrics
6. Generate recommendations

## Output
```json
{
  "architecture_score": 75,
  "pattern": "layered_architecture",
  "layers": ["presentation", "business", "data"],
  "circular_dependencies": 3,
  "solid_compliance": 68,
  "metrics": {
    "instability": 0.45,
    "abstractness": 0.32,
    "distance": 0.23
  },
  "recommendations": []
}
```
