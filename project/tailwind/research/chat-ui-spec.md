## ChatGPT Clone UI Styling Specification

### Overview
This specification outlines the Tailwind CSS utility classes and structural recommendations for building a ChatGPT-like user interface. The design prioritizes a mobile-first approach, ensuring responsiveness, accessibility, and a clean, modern aesthetic. The UI consists of a main container split into a sidebar (for chat history) and a main chat area (for messages and input).

### `tailwind.config.js` Additions
For this basic layout, no custom additions to `tailwind.config.js` are strictly necessary. The default Tailwind color palette and spacing scale are sufficient. If custom branding colors or specific font families were required, they would be added here.

### Overall Layout Strategy

**Recommended Structure:**
Use a flexbox layout for the main application wrapper to manage the sidebar and main content area.

**Utility Classes:**
*   **Root Container (e.g., `<body>` or `<div>` wrapping the entire app):**
    *   `min-h-screen`: Ensures the container takes at least the full viewport height.
    *   `bg-gray-900`: Dark background for the entire application.
    *   `text-gray-100`: Default text color.
    *   `flex`: Establishes a flex container.
    *   `flex-col`: Stacks children vertically by default (mobile-first).
    *   `lg:flex-row`: Arranges children horizontally on large screens and above.
    *   `overflow-hidden`: Prevents unwanted scrollbars on the main layout.

### Sidebar (Chat History)

**Recommended Structure:**
A `div` element acting as the sidebar, containing a list of chat history items.

**Utility Classes:**
*   **Sidebar Container:**
    *   `w-full`: Full width on mobile.
    *   `lg:w-64`: Fixed width of 16rem on large screens.
    *   `flex-shrink-0`: Prevents the sidebar from shrinking.
    *   `bg-gray-900`: Dark background, consistent with the root.
    *   `border-r`: Right border to separate from main content.
    *   `border-gray-700`: Border color.
    *   `p-4`: Padding inside the sidebar.
    *   `overflow-y-auto`: Allows vertical scrolling for chat history.
    *   `hidden`: Hidden by default on mobile (can be toggled visible).
    *   `lg:block`: Visible on large screens.
    *   `h-screen`: Ensures sidebar takes full height.

*   **Chat History Item (e.g., `<a>` or `<div>`):**
    *   `block`: Ensures the item takes full width.
    *   `p-2`: Padding.
    *   `rounded-md`: Slightly rounded corners.
    *   `text-sm`: Smaller text size.
    *   `text-gray-300`: Default text color.
    *   `hover:bg-gray-800`: Background on hover.
    *   `transition-colors`: Smooth transition for hover effects.
    *   `cursor-pointer`: Indicates interactivity.
    *   **For Active Item:** `bg-gray-700 text-white`

### Main Chat Area

**Recommended Structure:**
A `div` element that fills the remaining space, containing the message display area and the input box.

**Utility Classes:**
*   **Main Chat Container:**
    *   `flex-1`: Takes up all available space.
    *   `flex`: Establishes a flex container.
    *   `flex-col`: Stacks children vertically (messages + input).
    *   `bg-gray-800`: Slightly lighter dark background than the sidebar.
    *   `h-screen`: Ensures main area takes full height.

*   **Message Display Area:**
    *   `flex-1`: Takes up available vertical space within the main chat container.
    *   `overflow-y-auto`: Allows vertical scrolling for messages.
    *   `p-4`: Padding.
    *   `space-y-4`: Adds vertical spacing between message elements.

### Message Input Box

**Recommended Structure:**
A `div` at the bottom of the main chat area, containing an `input` (or `textarea`) and a `button`.

**Utility Classes:**
*   **Input Box Container:**
    *   `w-full`: Full width.
    *   `bg-gray-700`: Background color.
    *   `p-4`: Padding.
    *   `border-t`: Top border to separate from messages.
    *   `border-gray-600`: Border color.
    *   `flex`: Establishes a flex container for input and button.
    *   `items-center`: Vertically aligns items.
    *   `gap-2`: Space between input and button.

*   **Message Input Field (e.g., `<textarea>`):**
    *   `flex-1`: Takes up available horizontal space.
    *   `p-2`: Padding.
    *   `rounded-md`: Rounded corners.
    *   `bg-gray-600`: Input background.
    *   `text-white`: Input text color.
    *   `border-none`: Removes default border.
    *   `focus:outline-none`: Removes default focus outline.
    *   `focus:ring-2`: Adds a ring on focus.
    *   `focus:ring-blue-500`: Blue ring color.
    *   `resize-none`: Prevents manual resizing of textarea.
    *   `h-10`: Fixed height for input.

*   **Send Button:**
    *   `bg-blue-600`: Primary button background.
    *   `hover:bg-blue-700`: Darker blue on hover.
    *   `text-white`: White text.
    *   `px-4`: Horizontal padding.
    *   `py-2`: Vertical padding.
    *   `rounded-md`: Rounded corners.
    *   `transition-colors`: Smooth transition for hover effects.
    *   `flex-shrink-0`: Prevents button from shrinking.

### Mock Chat Message Styling

**Recommended Structure:**
Individual message `div`s within the message display area.

**Utility Classes:**
*   **Base Message Container:**
    *   `flex`: Establishes a flex container.
    *   `items-start`: Aligns items to the start (top).
    *   `gap-3`: Space between avatar and message bubble.
    *   `max-w-[80%]`: Limits message width to 80% of container.

*   **User Message (e.g., `div` with user content):**
    *   `ml-auto`: Pushes message to the right (for user).
    *   `bg-blue-600`: Distinct background color.
    *   `text-white`: White text.
    *   `p-3`: Padding.
    *   `rounded-lg`: Rounded corners.
    *   `rounded-br-none`: Sharper corner on bottom-right for bubble effect.

*   **AI Message (e.g., `div` with AI content):**
    *   `mr-auto`: Pushes message to the left (for AI).
    *   `bg-gray-700`: Distinct background color.
    *   `text-gray-100`: Text color.
    *   `p-3`: Padding.
    *   `rounded-lg`: Rounded corners.
    *   `rounded-bl-none`: Sharper corner on bottom-left for bubble effect.

*   **Avatar (Optional, for both user/AI):**
    *   `w-8 h-8`: Fixed width and height.
    *   `rounded-full`: Circular shape.
    *   `bg-gray-500`: Placeholder background.
    *   `flex-shrink-0`: Prevents avatar from shrinking.

*   **Message Content (inside bubble):**
    *   `text-base`: Default text size.
    *   `leading-relaxed`: Relaxed line height.

*   **Timestamp/Metadata (Optional, inside or near bubble):**
    *   `text-xs`: Extra small text.
    *   `text-gray-400`: Lighter gray text.
    *   `mt-1`: Margin top.
    *   `block`: Ensures it takes its own line if needed.

### Accessibility Considerations
*   **Semantic HTML**: Ensure appropriate HTML elements are used (e.g., `nav` for sidebar, `main` for chat area, `button` for interactive elements).
*   **Keyboard Navigation**: Ensure all interactive elements (chat history items, input, send button) are focusable and operable via keyboard.
*   **Color Contrast**: The chosen dark theme colors (`gray-900`, `gray-800`, `gray-700`, `blue-600` with `text-gray-100`, `text-white`) generally provide good contrast, but always verify with a contrast checker.
*   **`sr-only`**: Use `sr-only` for visually hidden labels on buttons or inputs that provide context for screen reader users (e.g., a "Send message" label for the send button).
*   **`aria-*` Attributes**: Consider `aria-live` regions for new messages, `aria-label` for navigation items, and `aria-current` for the active chat in the sidebar to enhance screen reader experience.

This blueprint provides a comprehensive set of Tailwind utility classes and structural recommendations to build the ChatGPT clone UI, adhering to performance, accessibility, and UX directives.