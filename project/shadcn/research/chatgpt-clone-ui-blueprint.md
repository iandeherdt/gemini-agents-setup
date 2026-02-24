# Shadcn/UI Component Blueprint: ChatGPT Clone UI

This blueprint outlines the necessary shadcn/ui components, their structure, installation commands, dependencies, and accessibility considerations for building a ChatGPT-like user interface.

## 1. Overall Layout: Resizable Panels

**Description**: The main layout will consist of a resizable sidebar for chat history and a main content area for the chat interface.

**Shadcn/ui Component**: `resizable`

**CLI Command**:
```bash
npx shadcn-ui@latest add resizable
```

**Dependencies**: None specific (relies on common shadcn/ui dependencies like `clsx`, `tailwind-merge`).

**Anatomy/Structure**:
```html
<ResizablePanelGroup direction="horizontal">
  <ResizablePanel defaultSize={30} minSize={20}>
    <!-- Sidebar Content (Chat History, New Chat Button) -->
  </ResizablePanel>
  <ResizableHandle withHandle />
  <ResizablePanel defaultSize={70}>
    <!-- Main Chat Area (Messages, Input Box) -->
  </ResizablePanel>
</ResizablePanelGroup>
```

**Props & Accessibility**:
*   `ResizablePanelGroup`: `direction` (e.g., `"horizontal"`) is crucial. Handles `aria-orientation` automatically.
*   `ResizablePanel`: `defaultSize`, `minSize`, `maxSize` for layout control.
*   `ResizableHandle`: `withHandle` provides a visual grabber. Automatically includes `aria-label` for resizing and keyboard navigation.

## 2. Sidebar: Chat History & New Chat Button

**Description**: Contains a list of previous chats and a button to start a new conversation.

**Shadcn/ui Components**: `scroll-area`, `button`

**CLI Commands**:
```bash
npx shadcn-ui@latest add scroll-area
npx shadcn-ui@latest add button
```

**Dependencies**: `lucide-react` (for optional icons on buttons).

**Anatomy/Structure**:
```html
<ScrollArea className="h-full p-4">
  <div className="flex flex-col gap-2">
    <Button variant="ghost" className="justify-start">
      <Plus className="mr-2 h-4 w-4" /> New Chat
    </Button>
    <div className="mt-4 space-y-2">
      <!-- Mock Chat History Items -->
      <Button variant="ghost" className="justify-start w-full" aria-current="page">
        Chat about AI models
      </Button>
      <Button variant="ghost" className="justify-start w-full">
        Project planning discussion
      </Button>
      <!-- More chat history items -->
    </div>
  </div>
</ScrollArea>
```

**Props & Accessibility**:
*   `ScrollArea`: Provides native scrolling behavior for long chat histories. Ensure content within is semantically structured.
*   `Button`: `variant` (e.g., `"ghost"`, `"default"`), `className` for styling. Each chat history button should clearly indicate its purpose. For the active chat, `aria-current="page"` is recommended.
*   Icons (e.g., `Plus` from `lucide-react`) should be accompanied by descriptive text or an `aria-label` if standalone.

## 3. Main Chat Area: Message Display

**Description**: Displays the conversation messages, typically with user and AI responses.

**Shadcn/ui Components**: `scroll-area`, `avatar` (optional, for user/AI profiles)

**CLI Commands**:
```bash
npx shadcn-ui@latest add scroll-area  // Already added
npx shadcn-ui@latest add avatar       // Optional
```

**Dependencies**: `lucide-react` (for optional `AvatarFallback` icons).

**Anatomy/Structure**:
```html
<ScrollArea className="flex-1 p-4">
  <div className="space-y-4">
    <!-- Mock Chat Messages -->
    <div className="flex items-start gap-3">
      <Avatar>
        <AvatarImage src="/avatars/user.png" alt="@user" />
        <AvatarFallback>U</AvatarFallback>
      </Avatar>
      <div className="bg-muted p-3 rounded-lg max-w-[80%]">
        <p>Hello, how can you help me today?</p>
      </div>
    </div>
    <div className="flex items-start gap-3 justify-end">
      <div className="bg-primary text-primary-foreground p-3 rounded-lg max-w-[80%]">
        <p>I am an AI assistant, ready to assist you with a wide range of tasks.</p>
      </div>
      <Avatar>
        <AvatarImage src="/avatars/ai.png" alt="@ai" />
        <AvatarFallback>AI</AvatarFallback>
      </Avatar>
    </div>
    <!-- More messages -->
  </div>
</ScrollArea>
```

**Props & Accessibility**:
*   `ScrollArea`: Ensures messages are scrollable. The `flex-1` class is important for it to take available vertical space.
*   `Avatar`: `AvatarImage` should have a descriptive `alt` attribute. `AvatarFallback` provides a textual fallback if the image fails to load.
*   Messages should be structured in a way that clearly distinguishes sender and content. Using `aria-live` regions might be considered for new messages arriving, but often simple DOM updates are sufficient.

## 4. Message Input Box

**Description**: An input field for typing messages and a send button.

**Shadcn/ui Components**: `textarea`, `button`

**CLI Commands**:
```bash
npx shadcn-ui@latest add textarea
npx shadcn-ui@latest add button   // Already added
```

**Dependencies**: `lucide-react` (for send button icon).

**Anatomy/Structure**:
```html
<div className="p-4 border-t flex items-center gap-2">
  <Textarea
    placeholder="Type your message here..."
    className="min-h-[40px] resize-none"
    aria-label="Message input"
  />
  <Button type="submit" size="icon">
    <Send className="h-4 w-4" />
    <span className="sr-only">Send message</span>
  </Button>
</div>
```

**Props & Accessibility**:
*   `Textarea`: `placeholder` provides a hint. Crucially, `aria-label="Message input"` is used for accessibility as there's no visible `<label>` element. `resize-none` prevents manual resizing by the user.
*   `Button`: `type="submit"` is important if part of a form. `size="icon"` for a compact button. For an icon-only button, `sr-only` span or `aria-label` is essential for screen reader users to understand its purpose (e.g., `aria-label="Send message"`).

## 5. Mock Test Data

**Description**: Example data structure for chat history and individual messages to facilitate initial UI development.

**Data Structure (Example)**:

```typescript
interface ChatMessage {
  id: string;
  sender: 'user' | 'ai';
  content: string;
  timestamp: Date;
}

interface ChatHistoryItem {
  id: string;
  title: string;
  messages: ChatMessage[];
  lastUpdated: Date;
}

const mockChatHistory: ChatHistoryItem[] = [
  {
    id: 'chat-1',
    title: 'Chat about AI models',
    lastUpdated: new Date('2023-10-26T10:00:00Z'),
    messages: [
      { id: 'msg-1', sender: 'user', content: 'What are the latest advancements in large language models?', timestamp: new Date('2023-10-26T09:55:00Z') },
      { id: 'msg-2', sender: 'ai', content: 'Recent advancements include improved context windows, multimodal capabilities, and enhanced reasoning. Models like GPT-4 and Claude 2 are leading the way.', timestamp: new Date('2023-10-26T09:56:00Z') }
    ]
  },
  {
    id: 'chat-2',
    title: 'Project planning discussion',
    lastUpdated: new Date('2023-10-25T15:30:00Z'),
    messages: [
      { id: 'msg-3', sender: 'user', content: 'Can you help me outline a project plan for a new web application?', timestamp: new Date('2023-10-25T15:20:00Z') },
      { id: 'msg-4', sender: 'ai', content: 'Certainly! We can start by defining the scope, target audience, key features, and technology stack.', timestamp: new Date('2023-10-25T15:21:00Z') }
    ]
  }
];

const currentChatMessages: ChatMessage[] = mockChatHistory[0].messages; // Example for current chat
```

**Notes for Main Developer Agent**:
*   Integrate `lucide-react` for icons (e.g., `Plus`, `Send`).
*   Ensure proper state management for `currentChatMessages` and `mockChatHistory` selection.
*   Implement dynamic rendering for chat history items and messages based on the mock data.
*   Focus on responsive design for different screen sizes, especially for the `ResizablePanelGroup`.
