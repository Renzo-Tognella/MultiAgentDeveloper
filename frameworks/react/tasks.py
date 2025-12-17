"""
React framework tasks with detailed expert-level instructions.
Based on React official documentation and industry best practices.
"""
from typing import Dict, List
from crewai import Agent, Task
from frameworks.base import BaseTasks


class ReactTasks(BaseTasks):
    """Factory for React-specific tasks with comprehensive instructions."""
    
    @property
    def framework_name(self) -> str:
        return "React"
    
    def react_architecture_task(self, agent: Agent, analysis: Dict) -> Task:
        return self.create_architecture_task(
            agent=agent,
            analysis=analysis,
            description="""\
                Design a comprehensive React architecture for:
                
                **REQUIREMENTS:**
                {requirements}
                
                **FILES TO MODIFY:** {files_to_modify}
                **FILES TO CREATE:** {files_to_create}
                
                ---
                
                **DELIVERABLES:**
                
                1. **Component Hierarchy Diagram**
                   - Parent-child relationships
                   - Data flow direction (props down, events up)
                   - State ownership locations
                
                2. **Component Specifications**
                   For each component, define:
                   ```
                   ComponentName:
                     Purpose: [single responsibility]
                     Props: [interface definition]
                     State: [local state if any]
                     Hooks: [custom hooks to use]
                     Children: [child components]
                   ```
                
                3. **State Management Strategy**
                   - Local state vs lifted state vs global state
                   - Context providers needed
                   - Server state management (React Query/SWR)
                
                4. **Custom Hooks Design**
                   ```
                   useHookName:
                     Purpose: [what logic it encapsulates]
                     Parameters: [inputs]
                     Returns: [outputs]
                     Side Effects: [API calls, subscriptions]
                   ```
                
                5. **Directory Structure**
                   ```
                   src/
                   ├── components/
                   ├── features/
                   ├── hooks/
                   ├── utils/
                   └── types/
                   ```
                
                6. **Performance Considerations**
                   - Components that need memoization
                   - Code splitting boundaries
                   - Lazy loading strategy
                
                7. **Accessibility Plan**
                   - Semantic HTML elements to use
                   - ARIA requirements
                   - Keyboard navigation flow
                
                {incentive}""",
            expected_output="""\
                Complete architecture document with:
                - Visual component hierarchy
                - Detailed component specifications with TypeScript interfaces
                - State management approach with justification
                - Custom hooks API design
                - File/folder structure
                - Performance optimization strategy
                - Accessibility compliance plan""",
        )
    
    def react_implementation_task(self, agent: Agent, context: List[Task]) -> Task:
        return self.create_implementation_task(
            agent=agent,
            context=context,
            description="""\
                Implement React components following the architecture design.
                
                **IMPLEMENTATION STANDARDS:**
                
                1. **Component Structure**
                   ```jsx
                   // imports (external → internal → styles)
                   import React, { useState, useEffect } from 'react';
                   import { useQuery } from '@tanstack/react-query';
                   import { Button } from '@/components/ui';
                   import { useAuth } from '@/hooks';
                   import styles from './Component.module.css';
                   
                   // types
                   interface Props {
                     title: string;
                     onAction: () => void;
                   }
                   
                   // component
                   export const Component: React.FC<Props> = ({ title, onAction }) => {
                     // hooks first
                     const [state, setState] = useState(initialState);
                     const { data } = useQuery(['key'], fetchData);
                     
                     // derived state
                     const derivedValue = useMemo(() => compute(data), [data]);
                     
                     // effects
                     useEffect(() => {
                       // effect logic
                       return () => { /* cleanup */ };
                     }, [dependency]);
                     
                     // handlers
                     const handleClick = useCallback(() => {
                       onAction();
                     }, [onAction]);
                     
                     // early returns for loading/error states
                     if (isLoading) return <Skeleton />;
                     if (error) return <ErrorMessage error={error} />;
                     
                     // render
                     return (
                       <div className={styles.container}>
                         {/* JSX */}
                       </div>
                     );
                   };
                   ```
                
                2. **Custom Hooks Pattern**
                   ```jsx
                   export const useCustomHook = (param: string) => {
                     const [state, setState] = useState(null);
                     const [error, setError] = useState(null);
                     const [loading, setLoading] = useState(false);
                     
                     useEffect(() => {
                       let cancelled = false;
                       
                       const fetchData = async () => {
                         setLoading(true);
                         try {
                           const result = await api.fetch(param);
                           if (!cancelled) setState(result);
                         } catch (e) {
                           if (!cancelled) setError(e);
                         } finally {
                           if (!cancelled) setLoading(false);
                         }
                       };
                       
                       fetchData();
                       return () => { cancelled = true; };
                     }, [param]);
                     
                     return { state, error, loading };
                   };
                   ```
                
                3. **Accessibility Requirements**
                   - Use semantic HTML: <button>, <nav>, <main>, <article>
                   - Add aria-label for icon-only buttons
                   - Implement keyboard navigation (Tab, Enter, Escape)
                   - Manage focus for modals and dynamic content
                   - Ensure 4.5:1 color contrast ratio
                
                4. **Error Boundaries**
                   ```jsx
                   class ErrorBoundary extends React.Component {
                     state = { hasError: false };
                     
                     static getDerivedStateFromError(error) {
                       return { hasError: true };
                     }
                     
                     componentDidCatch(error, info) {
                       logErrorToService(error, info);
                     }
                     
                     render() {
                       if (this.state.hasError) {
                         return <FallbackUI />;
                       }
                       return this.props.children;
                     }
                   }
                   ```
                
                5. **File Naming Conventions**
                   - Components: PascalCase (UserProfile.tsx)
                   - Hooks: camelCase with use prefix (useAuth.ts)
                   - Utils: camelCase (formatDate.ts)
                   - Types: PascalCase (User.types.ts)
                   - Styles: Component.module.css""",
            expected_output="""\
                Complete React implementation including:
                - All components with TypeScript interfaces
                - Custom hooks with proper cleanup
                - Error boundaries at appropriate levels
                - Loading and error states handled
                - Accessible markup with ARIA where needed
                - Proper file organization""",
        )
    
    def react_testing_task(self, agent: Agent, context: List[Task]) -> Task:
        return self.create_testing_task(
            agent=agent,
            context=context,
            description="""\
                Write comprehensive tests following React Testing Library best practices.
                
                **TESTING REQUIREMENTS:**
                
                1. **Test File Structure**
                   ```
                   src/
                   ├── components/
                   │   └── Button/
                   │       ├── Button.tsx
                   │       ├── Button.test.tsx    # Component tests
                   │       └── Button.stories.tsx # Storybook (optional)
                   └── hooks/
                       └── useAuth/
                           ├── useAuth.ts
                           └── useAuth.test.ts   # Hook tests
                   ```
                
                2. **Component Test Template**
                   ```javascript
                   import { render, screen } from '@testing-library/react';
                   import userEvent from '@testing-library/user-event';
                   import { ComponentName } from './ComponentName';
                   
                   describe('ComponentName', () => {
                     // Setup
                     const defaultProps = {
                       title: 'Test Title',
                       onClick: jest.fn(),
                     };
                     
                     const renderComponent = (props = {}) => {
                       return render(<ComponentName {...defaultProps} {...props} />);
                     };
                     
                     beforeEach(() => {
                       jest.clearAllMocks();
                     });
                     
                     // Rendering tests
                     describe('rendering', () => {
                       it('renders with required props', () => {
                         renderComponent();
                         expect(screen.getByRole('button')).toBeInTheDocument();
                       });
                       
                       it('displays the title', () => {
                         renderComponent({ title: 'Custom Title' });
                         expect(screen.getByText('Custom Title')).toBeInTheDocument();
                       });
                     });
                     
                     // Interaction tests
                     describe('interactions', () => {
                       it('calls onClick when clicked', async () => {
                         const user = userEvent.setup();
                         const onClick = jest.fn();
                         renderComponent({ onClick });
                         
                         await user.click(screen.getByRole('button'));
                         
                         expect(onClick).toHaveBeenCalledTimes(1);
                       });
                     });
                     
                     // Accessibility tests
                     describe('accessibility', () => {
                       it('is keyboard accessible', async () => {
                         const user = userEvent.setup();
                         const onClick = jest.fn();
                         renderComponent({ onClick });
                         
                         await user.tab();
                         await user.keyboard('{Enter}');
                         
                         expect(onClick).toHaveBeenCalled();
                       });
                     });
                   });
                   ```
                
                3. **Custom Hook Test Template**
                   ```javascript
                   import { renderHook, act, waitFor } from '@testing-library/react';
                   import { useCustomHook } from './useCustomHook';
                   
                   describe('useCustomHook', () => {
                     it('returns initial state', () => {
                       const { result } = renderHook(() => useCustomHook());
                       
                       expect(result.current.data).toBeNull();
                       expect(result.current.loading).toBe(false);
                     });
                     
                     it('fetches data on mount', async () => {
                       const { result } = renderHook(() => useCustomHook());
                       
                       await waitFor(() => {
                         expect(result.current.data).not.toBeNull();
                       });
                     });
                     
                     it('handles errors', async () => {
                       server.use(
                         rest.get('/api/data', (req, res, ctx) => {
                           return res(ctx.status(500));
                         })
                       );
                       
                       const { result } = renderHook(() => useCustomHook());
                       
                       await waitFor(() => {
                         expect(result.current.error).toBeTruthy();
                       });
                     });
                   });
                   ```
                
                4. **Query Priority (ALWAYS follow this order)**
                   1. getByRole - most accessible
                   2. getByLabelText - form fields
                   3. getByPlaceholderText
                   4. getByText - content
                   5. getByTestId - LAST RESORT only
                
                5. **What to Test**
                   ✅ User interactions (clicks, typing, form submissions)
                   ✅ Conditional rendering
                   ✅ Props affecting output
                   ✅ Error states
                   ✅ Loading states
                   ✅ Accessibility (keyboard navigation)
                   
                   ❌ Implementation details
                   ❌ Internal state values
                   ❌ Private methods""",
            expected_output="""\
                Complete test suite including:
                - Component tests with user interactions
                - Custom hook tests with async handling
                - Integration tests for complex flows
                - Accessibility tests for keyboard navigation
                - MSW handlers for API mocking
                - 80%+ code coverage""",
        )
    
    def react_reviewing_task(self, agent: Agent, context: List[Task]) -> Task:
        return self.create_review_task(
            agent=agent,
            context=context,
            description="""\
                Review the React implementation for production readiness.
                
                **REVIEW CHECKLIST:**
                
                1. **Code Quality**
                   □ Components follow single responsibility principle
                   □ No prop drilling beyond 2 levels
                   □ Custom hooks extract reusable logic
                   □ TypeScript types are specific (no 'any')
                   □ Consistent naming conventions
                   □ No commented-out code
                   □ No console.log statements
                
                2. **Performance**
                   □ React.memo used for expensive pure components
                   □ useMemo/useCallback used appropriately
                   □ No unnecessary re-renders
                   □ Large lists virtualized
                   □ Images optimized and lazy-loaded
                   □ Code splitting implemented
                   □ Bundle size acceptable
                
                3. **Accessibility (WCAG 2.1 AA)**
                   □ Semantic HTML used correctly
                   □ All images have alt text
                   □ Form inputs have labels
                   □ Color contrast meets 4.5:1 ratio
                   □ Focus indicators visible
                   □ Keyboard navigation works
                   □ Screen reader tested
                
                4. **Security**
                   □ No dangerouslySetInnerHTML with user input
                   □ URLs validated before use
                   □ No sensitive data in client state
                   □ API keys not exposed
                   □ XSS prevention measures
                
                5. **Error Handling**
                   □ Error boundaries at appropriate levels
                   □ API errors handled gracefully
                   □ Loading states shown
                   □ Empty states handled
                   □ Network failures handled
                
                6. **Testing**
                   □ Tests cover happy path
                   □ Tests cover error cases
                   □ Tests use accessible queries
                   □ Tests are maintainable
                   □ No snapshot tests for large components
                
                **PROVIDE:**
                - Issues found with severity (Critical/Major/Minor)
                - Specific code suggestions for each issue
                - Overall quality score (1-10)
                - Approval status (Approved/Changes Requested)""",
            expected_output="""\
                Comprehensive review report including:
                - Categorized issues with severity levels
                - Specific fix recommendations with code examples
                - Performance improvement suggestions
                - Accessibility compliance status
                - Security assessment
                - Overall quality score and approval status
                - Instructions to run the application""",
        )
