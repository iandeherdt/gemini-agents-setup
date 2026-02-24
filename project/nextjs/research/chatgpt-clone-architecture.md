# Next.js App Router Architecture Blueprint: ChatGPT Clone UI

## 1. Feature Overview
This blueprint outlines the architecture for a ChatGPT-like user interface, featuring a persistent sidebar for chat history, a main area for displaying messages of the selected chat, and an interactive input box for sending new messages.

## 2. Proposed File Structure
```
app/
├── (chat)/                  # Route group for chat-related pages
│   ├── layout.tsx           # Shared layout for chat pages (sidebar + main content)
│   ├── page.tsx             # Default chat page (e.g., redirect to latest chat or 'new chat' state)
│   ├── [chatId]/            # Dynamic route for individual chat pages
│   │   ├── page.tsx         # Displays messages for a specific chat
│   │   ├── loading.tsx      # Loading state for individual chat messages
│   │   └── error.tsx        # Error boundary for individual chat messages
│   ├── components/          # Reusable components for the chat UI
│   │   ├── Sidebar.tsx
│   │   ├── ChatHistoryList.tsx
│   │   ├── ChatHistoryItem.tsx
│   │   ├── ChatMessageList.tsx
│   │   ├── ChatMessage.tsx
│   │   └── MessageInput.tsx
│   ├── lib/                 # Server-side data fetching utilities and mock data
│   │   └── data.ts
│   └── actions.ts           # Server Actions for data mutations
└── globals.css
```

## 3. Rendering Strategy (Server vs. Client Components)

**Default to Server Components (RSC) for optimal performance, SEO, and reduced client-side JavaScript bundle size. Client Components are used only when interactivity or browser APIs are strictly required.**

### Server Components (Default)

*   **`app/(chat)/layout.tsx`**: Renders the overall structure, including the `Sidebar` and the main content area. Fetches global chat data if needed (e.g., user info). No client-side interactivity. 
*   **`app/(chat)/page.tsx`**: Renders the initial state of the chat application (e.g., a welcome message or a prompt to start a new chat). 
*   **`app/(chat)/[chatId]/page.tsx`**: Fetches and renders the messages for a specific `chatId`. This component will receive `params.chatId` and pass it down to `ChatMessageList`. 
*   **`app/(chat)/components/Sidebar.tsx`**: Fetches the list of chat history items from `lib/data.ts` and renders `ChatHistoryList`. It's a Server Component because its primary role is data fetching and rendering static links. 
*   **`app/(chat)/components/ChatHistoryList.tsx`**: Receives chat history data as props and maps over it to render `ChatHistoryItem` components. 
*   **`app/(chat)/components/ChatHistoryItem.tsx`**: Displays a single chat history item (e.g., chat title, link). 
*   **`app/(chat)/components/ChatMessageList.tsx`**: Fetches and displays the list of `ChatMessage` components for the current `chatId`. 
*   **`app/(chat)/components/ChatMessage.tsx`**: Renders an individual chat message (user or AI). 

### Client Components (`