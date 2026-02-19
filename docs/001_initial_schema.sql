-- Evolution Content Factory - Database Schema
-- Run this in Supabase SQL Editor (https://supabase.com)
-- After creating your free project

-- 1. Enable Vector extension for AI semantic search
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. State Machine - Tracks project through production pipeline
CREATE TYPE project_status AS ENUM (
  'idea',                 -- Initial creation
  'researching',          -- Scraping race data
  'scripting',            -- AI writing script
  'approval_script',      -- HUMAN: Review script via Telegram
  'gathering_clips',      -- Downloading YouTube segments
  'approval_clips',       -- HUMAN: Verify clips
  'rendering',            -- FFmpeg stitching video
  'approval_final',       -- HUMAN: Review final video
  'done',                 -- Posted to TikTok
  'failed'                -- Error state
);

-- 3. Projects - Master ledger for each video
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  race_url TEXT,
  status project_status DEFAULT 'idea',
  
  -- Creative brief (your "knobs and dials")
  creative_brief JSONB DEFAULT '{}'::JSONB,
  -- Example: {
  --   "template": "pre-race-hype",
  --   "pacing": "fast",
  --   "voice": "gritty",
  --   "length_seconds": 60,
  --   "focus_horses": ["Midnight Run", "Thunder Bolt"],
  --   "youtube_clips": [
  --     {"url": "https://youtube.com/...", "start": 45, "end": 90}
  --   ]
  -- }
  
  script_content JSONB,           -- Timed script segments
  video_url TEXT,                 -- Final render path
  telegram_chat_id TEXT,          -- For approval notifications
  
  -- Tracking
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  error_count INTEGER DEFAULT 0,
  last_error TEXT
);

-- Index for quick status lookups
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_created ON projects(created_at DESC);

-- 4. YouTube Clips - Specific segments to extract
CREATE TABLE clips (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  youtube_url TEXT NOT NULL,
  start_seconds INTEGER NOT NULL,
  end_seconds INTEGER NOT NULL,
  label TEXT,                     -- e.g., "finish_line", "close_up"
  local_path TEXT,                -- Downloaded file path
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'downloading', 'downloaded', 'extracted', 'failed')),
  error_message TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_clips_project ON clips(project_id);
CREATE INDEX idx_clips_status ON clips(status);

-- 5. Research Data - Raw scraped racing data
CREATE TABLE research_data (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  source_url TEXT,
  source_name TEXT,               -- "racing.com", "tab", "nztr"
  raw_data JSONB,                 -- Full scrape dump
  summary TEXT,                   -- AI-generated angle/summary
  runners JSONB,                  -- Structured runner data
  form_guides JSONB,              -- Form analysis
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. B-Roll Assets - Vector-searchable library
CREATE TABLE assets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  filename TEXT NOT NULL,
  local_path TEXT NOT NULL,
  description TEXT,               -- "Horse galloping in heavy mud"
  embedding VECTOR(768),          -- AI vector for semantic search
  tags TEXT[],                    -- ["mud", "gallop", "finish_line"]
  asset_type TEXT DEFAULT 'broll' CHECK (asset_type IN ('broll', 'graphic', 'audio', 'music')),
  usage_count INTEGER DEFAULT 0,
  last_used_at TIMESTAMPTZ,
  source TEXT,                    -- "flow", "veo3", "canva", "youtube", "manual"
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Vector search index
CREATE INDEX idx_assets_embedding ON assets USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX idx_assets_tags ON assets USING GIN(tags);
CREATE INDEX idx_assets_type ON assets(asset_type);

-- 7. Templates - Preset configurations
CREATE TABLE templates (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  default_brief JSONB NOT NULL,
  system_prompt TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Seed with Evolution Stables presets
INSERT INTO templates (id, name, description, default_brief, system_prompt) VALUES
(
  'pre-race-preview', 
  'Pre-Race Preview', 
  'Build hype for upcoming races with fast cuts and high energy',
  '{"pacing": "fast", "voice": "high_energy", "music": "phonk", "length_seconds": 45, "style": "hype"}',
  'You are a racing hype-man. Focus on upcoming rivalries, favor fast cuts (0.5-1s), avoid safe bets. Use phrases like "The horse the bookies are terrified of" and "This Saturday, everything changes." Maximum energy.'
),
(
  'results-recap', 
  'Results Recap', 
  'Monday morning style summary of race results',
  '{"pacing": "medium", "voice": "news_anchor", "music": "lofi", "length_seconds": 60, "style": "news"}',
  'You are a racing news anchor. Summarize facts, payouts, and upsets clearly. Who won, who lost money, any surprises. Authoritative tone, clear facts.'
),
(
  'form-guide-deep-dive', 
  'Form Guide Deep Dive', 
  'Professional punter analysis of form, barriers, and jockeys',
  '{"pacing": "slow", "voice": "analytical", "music": "study", "length_seconds": 90, "style": "analytical", "show_odds": true}',
  'You are a professional punter with 20 years experience. Analyze weight, barrier draw, jockey history, track conditions. Be cold, calculated, and data-driven. Mention specific form patterns.'
);

-- 8. Jobs - Work queue for stateless workers
CREATE TABLE jobs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  job_type TEXT NOT NULL CHECK (job_type IN ('research', 'write', 'download_clip', 'extract_segment', 'render', 'voiceover')),
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'claimed', 'running', 'complete', 'failed')),
  worker_id TEXT,
  input_payload JSONB DEFAULT '{}',
  output_payload JSONB,
  error_message TEXT,
  retry_count INTEGER DEFAULT 0,
  claimed_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_jobs_status ON jobs(status) WHERE status IN ('pending', 'failed');
CREATE INDEX idx_jobs_project ON jobs(project_id);

-- 9. Function to auto-update updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON projects
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 10. View: Active projects (for dashboard)
CREATE VIEW active_projects AS
SELECT p.*, t.name as template_name
FROM projects p
LEFT JOIN templates t ON (p.creative_brief->>'template') = t.id
WHERE p.status NOT IN ('done', 'failed')
ORDER BY p.created_at DESC;
