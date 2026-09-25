# Analyze React Code Skill

## Purpose
Analyze React/TypeScript applications for code quality, component design, performance patterns, and best practices.

## Capabilities

- Component structure analysis (functional vs class components)
- Hooks usage patterns (useState, useEffect, custom hooks)
- State management (Context, Redux, MobX, Zustand)
- Type safety coverage (TypeScript strict mode)
- Performance optimization (memo, useMemo, useCallback)
- Accessibility compliance (ARIA, semantic HTML)
- Testing coverage (Jest, React Testing Library)

## Key Checks

### Component Quality
- Component size and complexity
- Props interface definitions
- Proper hook usage and dependencies
- Key props in lists
- Conditional rendering patterns

### Performance
- Unnecessary re-renders
- Missing memoization
- Large bundle sizes
- Code splitting usage
- Lazy loading patterns

### Accessibility
- ARIA attributes
- Keyboard navigation
- Focus management
- Alt text for images
- Semantic HTML elements

### Type Safety
- Any type usage
- Missing prop types
- Incomplete interfaces
- Type assertion overuse

## Output
```json
{
  "framework": "react",
  "version": "18.2.0",
  "typescript": true,
  "total_components": 45,
  "quality_score": 82,
  "accessibility_score": 75,
  "performance_score": 78,
  "type_coverage": 92,
  "issues": []
}
```
