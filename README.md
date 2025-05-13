# -ITNE352-Project-Group-SA13
sequenceDiagram
    Client->>Server: Connect with username
    Server->>API: Fetch flight data
    API-->>Server: Return JSON data
    Server->>Client: Send formatted response


