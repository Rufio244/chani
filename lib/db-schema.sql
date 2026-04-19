-- USERS
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email TEXT,
  role TEXT
);

-- REQUEST LOGS
CREATE TABLE logs (
  id UUID PRIMARY KEY,
  user_id UUID,
  route TEXT,
  payload JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

-- AI MEMORY
CREATE TABLE memory (
  id UUID PRIMARY KEY,
  type TEXT,
  data JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

-- EVENTS
CREATE TABLE events (
  id UUID PRIMARY KEY,
  event_name TEXT,
  data JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);
