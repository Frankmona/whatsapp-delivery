-- =======================================================
-- FM XPRESS: Admin Users & Role-Based Access Control (RBAC)
-- Run this script in the Supabase SQL Editor:
-- https://supabase.com/dashboard/project/_/sql
-- =======================================================

CREATE TABLE IF NOT EXISTS public.admin_users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'dispatcher', -- 'super_admin', 'admin', 'dispatcher'
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index on email for fast lookups
CREATE INDEX IF NOT EXISTS idx_admin_users_email ON public.admin_users (email);

-- Enable Row Level Security (RLS)
ALTER TABLE public.admin_users ENABLE ROW LEVEL SECURITY;

-- Allow full access to backend service role
DROP POLICY IF EXISTS "Allow service role full access to admin_users" ON public.admin_users;
CREATE POLICY "Allow service role full access to admin_users"
    ON public.admin_users
    FOR ALL
    USING (true)
    WITH CHECK (true);
